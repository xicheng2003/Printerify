// frontend/src/stores/order.js (最终响应式修复版)

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import apiService from '@/services/apiService';

const BINDING_PRICE_CONFIG = {
    'none': 0.00,
    'staple_top_left': 0.10,
    'staple_left_side': 0.10,
    'staple': 2.00,
    'ring_bound': 5.00,
};

export const useOrderStore = defineStore('order', () => {
    const groups = ref([]);
    const phoneNumber = ref('');
    const paymentMethod = ref('ALIPAY');
    const paymentScreenshotFile = ref(null);
    const isLoading = ref(false);
    const pricingConfig = ref(null); // 新增：存储从后端获取的计费规则

    // 新增：用户订单相关状态
    const userOrders = ref([]);
    const userOrdersLoading = ref(false);
    const userOrdersError = ref(null);

    // 新增：获取计费规则
    async function fetchPricingConfig() {
        try {
            const response = await apiService.getPricingConfig();
            pricingConfig.value = response.data;
        } catch (error) {
            console.error('Failed to fetch pricing config:', error);
            // 如果获取失败，可以使用默认的兜底配置，或者提示用户刷新
        }
    }

    async function _fetchPriceForDocument(docId) {
        const doc = findDocumentById(docId);
        if (!doc) return;

        doc.isRecalculating = true; // 【核心修复】使用 isRecalculating
        doc.error = null;
        try {
            // 使用 apiService 的价格估算方法
            const specifications = {
                file_path: doc.serverId,
                color_mode: doc.settings.colorMode,
                print_sided: doc.settings.printSided,
                paper_size: doc.settings.paperSize,
                copies: doc.settings.copies,
                // 在第一步希望尽量拿到精确页数（会稍慢，但能“状态翻转”并同步价格）
                prefer_exact: true,
                // 如果已经有页数（例如PDF快速读取），可以传递以减少一次解析
                override_page_count: doc.pageCount || undefined,
            };
            const response = await apiService.getPriceQuote(null, specifications);
            doc.pageCount = response.data.page_count;
            doc.printCost = response.data.print_cost;
            // 新增：记录预估/精确状态，便于前端提示
            doc.isEstimated = Boolean(response.data.is_estimated);
            doc.pageCountSource = response.data.page_count_source || (doc.isEstimated ? 'estimated' : 'exact');
            doc.priceNote = response.data.note || (doc.isEstimated ? '价格为预估，后台将自动校正' : '价格已精确计算');
        } catch (error) {
            console.error('Price estimation error:', error);
            doc.error = '计价失败';
        } finally {
            doc.isRecalculating = false; // 【核心修复】使用 isRecalculating
        }
    }

    async function _uploadFile(docId) {
        const doc = findDocumentById(docId);
        if (!doc) return;

        try {
            const response = await apiService.uploadPrintFile(doc.fileObject, (progressEvent) => {
                if (progressEvent.total) {
                    doc.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                }
            });
            doc.uploadProgress = 100;
            doc.serverId = response.data.file_id;
            await _fetchPriceForDocument(docId);
        } catch (error) {
            console.error('File upload error:', error);
            // 使用友好的错误提示
            if (error.friendlyMessage) {
                doc.error = error.friendlyMessage;
            } else if (error.code === 'ECONNABORTED' || error.message?.includes('timeout')) {
                doc.error = '上传超时，文件可能过大';
            } else {
                doc.error = '上传失败，请重试';
            }
        } finally {
            doc.isUploading = false;
        }
    }

    function findDocumentById(docId) {
        for (const group of groups.value) {
            const doc = group.documents.find(d => d.id === docId);
            if (doc) return doc;
        }
        return null;
    }

    function addFiles(fileList) {
        for (const file of fileList) {
            const newDocument = {
                id: `doc_${uuidv4()}`,
                fileObject: file, fileName: file.name, serverId: null,
                isUploading: true, uploadProgress: 0, isRecalculating: false, error: null,
                settings: {
                    colorMode: 'black_white',
                    printSided: 'single',
                    copies: 1,
                    paperSize: 'a4_70g' // <--- 【在此处新增】
                },
                pageCount: 0, printCost: 0,
                // 新增：默认先视为预估，收到后端响应后再更新
                isEstimated: true,
                pageCountSource: 'estimated',
                priceNote: '价格为预估，后台将自动校正',
            };
            const newGroup = { id: `group_${uuidv4()}`, bindingType: 'none', documents: [newDocument] };
            groups.value.push(newGroup);
            _uploadFile(newDocument.id);
        }
    }

    function removeDocument(docId) { for (let i = 0; i < groups.value.length; i++) { const group = groups.value[i]; const docIndex = group.documents.findIndex(doc => doc.id === docId); if (docIndex !== -1) { group.documents.splice(docIndex, 1); if (group.documents.length === 0) { groups.value.splice(i, 1); } return; } } }

    async function updateDocumentSettings(docId, newSettings) {
        const document = findDocumentById(docId);
        if (document) {
            document.settings = { ...document.settings, ...newSettings };
            if (document.serverId && !document.isUploading) {
                await _fetchPriceForDocument(docId);
            }
        }
    }

    function updateGroupBinding(groupId, bindingType) {
        const group = groups.value.find(g => g.id === groupId);
        if (group) {
            group.bindingType = bindingType;
        }
    }

    function mergeGroups(sourceGroupId, targetGroupId) {
        if (sourceGroupId === targetGroupId) return;
        const sourceGroupIndex = groups.value.findIndex(g => g.id === sourceGroupId);
        const targetGroup = groups.value.find(g => g.id === targetGroupId);
        if (sourceGroupIndex !== -1 && targetGroup) {
            const sourceGroup = groups.value[sourceGroupIndex];
            targetGroup.documents.push(...sourceGroup.documents);
            groups.value.splice(sourceGroupIndex, 1);
        }
    }

    function setLoading(status) {
        isLoading.value = status;
    }

    function resetStore() {
        groups.value = [];
        phoneNumber.value = '';
        paymentMethod.value = 'WECHAT';
        paymentScreenshotFile.value = null;
    }

    // 新增：获取用户订单列表
    async function fetchUserOrders() {
        userOrdersLoading.value = true;
        userOrdersError.value = null;

        try {
            const response = await apiService.getUserOrders();
            userOrders.value = response.data;
        } catch (error) {
            userOrdersError.value = '获取订单列表失败';
            console.error('Failed to fetch user orders:', error);
        } finally {
            userOrdersLoading.value = false;
        }
    }

    // 新增：创建订单（集成用户认证）
    async function createOrder(orderData) {
        setLoading(true);

        try {
            // 构建完整的订单数据
            const completeOrderData = {
                phone_number: orderData.phone_number || phoneNumber.value,
                payment_method: orderData.payment_method || paymentMethod.value,
                groups: groups.value.map((group, groupIndex) => ({
                    binding_type: group.bindingType,
                    sequence_in_order: groupIndex,
                    documents: group.documents.map((doc, docIndex) => ({
                        file_id: doc.serverId,
                        original_filename: doc.fileName,
                        color_mode: doc.settings.colorMode,
                        print_sided: doc.settings.printSided,
                        paper_size: doc.settings.paperSize,
                        copies: doc.settings.copies,
                        sequence_in_group: docIndex
                    }))
                }))
            };

            // 如果有付款截图，先上传
            if (paymentScreenshotFile.value) {
                const screenshotResponse = await apiService.uploadPaymentScreenshot(paymentScreenshotFile.value);
                completeOrderData.payment_screenshot_id = screenshotResponse.data.screenshot_id;
            }

            const response = await apiService.createOrder(completeOrderData);

            // 订单创建成功后，刷新用户订单列表
            await fetchUserOrders();

            // 重置当前订单状态
            resetStore();

            return response.data;
        } catch (error) {
            console.error('Order creation failed:', error);
            throw error;
        } finally {
            setLoading(false);
        }
    }

    // 新增：根据取件码查询订单
    async function queryOrderByCode(pickupCode, phoneNumber) {
        setLoading(true);

        try {
            const response = await apiService.queryOrder(phoneNumber, pickupCode);
            return response.data;
        } catch (error) {
            console.error('Order query failed:', error);
            throw error;
        } finally {
            setLoading(false);
        }
    }

    const totalCost = computed(() => {
        // 优先使用后端配置，否则使用默认值
        const config = pricingConfig.value;
        let total = 0.5; // 默认基础服务费

        if (config && config.base_service_fee !== undefined) {
            const fee = Number(config.base_service_fee);
            if (!isNaN(fee)) {
                total = fee;
            }
        }

        groups.value.forEach(group => {
            group.documents.forEach(doc => {
                const cost = Number(doc.printCost);
                if (!isNaN(cost)) {
                    total += cost;
                }
            });
            const bindingType = group.bindingType;

            // 计算装订费
            if (config && config.binding && bindingType in config.binding) {
                const bindingFee = Number(config.binding[bindingType]);
                if (!isNaN(bindingFee)) {
                    total += bindingFee;
                }
            } else if (bindingType in BINDING_PRICE_CONFIG) {
                // 兜底：如果配置未加载，使用本地常量
                total += BINDING_PRICE_CONFIG[bindingType];
            }
        });
        return total.toFixed(2);
    });

    const isReadyToSubmit = computed(() => {
        if (groups.value.length === 0) return false;
        // 【核心修复】使用 isRecalculating
        return groups.value.every(g => g.documents.every(d => !d.isUploading && !d.isRecalculating && d.serverId && !d.error));
    });

    return {
        groups, phoneNumber, paymentMethod, paymentScreenshotFile,
        isLoading, userOrders, userOrdersLoading, userOrdersError, pricingConfig, // Export pricingConfig
        setLoading, addFiles, removeDocument, updateDocumentSettings,
        updateGroupBinding, resetStore, mergeGroups,
        fetchUserOrders, createOrder, queryOrderByCode, fetchPricingConfig, // Export fetchPricingConfig
        totalCost, isReadyToSubmit
    };
});
