// frontend/src/stores/order.js (最终响应式修复版)

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

// 【新增】在前端也创建一个装订价格配置表，与后端保持同步
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
    const paymentMethod = ref('ALIPAY'); // 默认支付方式
    const paymentScreenshotFile = ref(null);
    const isLoading = ref(false); // <--- 【新增】全局加载状态

    // 【关键修复】内部函数现在接收 docId，而不是整个 doc 对象
    async function _fetchPriceForDocument(docId) {
        const doc = findDocumentById(docId);
        if (!doc) return;

        doc.isCalculatingPrice = true;
        doc.error = null;
        try {
            const response = await axios.post('/api/estimate-price/', {
                file_path: doc.serverId,
                color_mode: doc.settings.colorMode,
                print_sided: doc.settings.printSided,
                copies: doc.settings.copies
            }, { withCredentials: true });
            doc.pageCount = response.data.page_count;
            doc.printCost = response.data.print_cost;
        } catch (error) {
            doc.error = '计价失败';
        } finally {
            doc.isCalculatingPrice = false;
        }
    }

    async function _uploadFile(docId) {
        const doc = findDocumentById(docId);
        if (!doc) return;

        try {
            const formData = new FormData();
            formData.append('file', doc.fileObject);
            const response = await axios.post('/api/upload/', formData, {
                onUploadProgress: progressEvent => {
                    if (progressEvent.total) {
                        doc.uploadProgress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    }
                },
                withCredentials: true
            });
            doc.uploadProgress = 100;
            doc.serverId = response.data.file_id;
            await _fetchPriceForDocument(docId); // 【关键修复】传递id
        } catch (error) {
            doc.error = '上传失败';
        } finally {
            doc.isUploading = false;
        }
    }

    // 辅助函数，用于根据ID在 state 中找到对应的 document 对象
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
                isUploading: true, uploadProgress: 0, isCalculatingPrice: false, error: null,
                settings: { colorMode: 'black_white', printSided: 'single', copies: 1 },
                pageCount: 0, printCost: 0,
            };
            const newGroup = { id: `group_${uuidv4()}`, bindingType: 'none', documents: [newDocument] };
            groups.value.push(newGroup);
            _uploadFile(newDocument.id); // 【关键修复】只传递新文件的ID
        }
    }

    // ... 其他所有 Actions 和 Getters 保持不变 ...
    function removeDocument(docId) { for (let i = 0; i < groups.value.length; i++) { const group = groups.value[i]; const docIndex = group.documents.findIndex(doc => doc.id === docId); if (docIndex !== -1) { group.documents.splice(docIndex, 1); if (group.documents.length === 0) { groups.value.splice(i, 1); } return; } } }
    async function updateDocumentSettings(docId, newSettings) { const document = findDocumentById(docId); if (document) { document.settings = { ...document.settings, ...newSettings }; if (document.serverId && !document.isUploading) { await _fetchPriceForDocument(docId); } } }
    function updateGroupBinding(groupId, bindingType) { const group = groups.value.find(g => g.id === groupId); if (group) { group.bindingType = bindingType; } }

    // 【新增】合并装订组的动作
    function mergeGroups(sourceGroupId, targetGroupId) {
        // 防止一个组被拖拽到自己身上
        if (sourceGroupId === targetGroupId) return;

        const sourceGroupIndex = groups.value.findIndex(g => g.id === sourceGroupId);
        const targetGroup = groups.value.find(g => g.id === targetGroupId);

        // 确保源组和目标组都存在
        if (sourceGroupIndex !== -1 && targetGroup) {
            const sourceGroup = groups.value[sourceGroupIndex];

            // 1. 将源组的所有文件，追加到目标组的文件列表末尾
            targetGroup.documents.push(...sourceGroup.documents);

            // 2. 从groups数组中，根据索引移除现已变空的源组
            groups.value.splice(sourceGroupIndex, 1);
        }
    }

    // 我们只需要在 Store 中暴露一个方法来切换加载状态
    function setLoading(status) {
        isLoading.value = status;
    }

    function resetStore() { groups.value = []; phoneNumber.value = ''; paymentMethod.value = 'WECHAT'; paymentScreenshotFile.value = null; }

    const totalCost = computed(() => {
    let total = 0.5; // 基础服务费
    groups.value.forEach(group => {
        // 1. 累加组内所有文件的打印费 (这部分不变)
        group.documents.forEach(doc => {
            total += Number(doc.printCost) || 0;
        });

        // 2. 【核心修改】累加该组的装订费
        // 我们现在从上面的配置表中查找价格，而不是用 if-else
        const bindingType = group.bindingType;
        if (bindingType in BINDING_PRICE_CONFIG) {
            total += BINDING_PRICE_CONFIG[bindingType];
        }
    });
    return total.toFixed(2);
});

    const isReadyToSubmit = computed(() => { if (groups.value.length === 0) return false; return groups.value.every(g => g.documents.every(d => !d.isUploading && !d.isCalculatingPrice && d.serverId && !d.error)); });

    return {
        groups, phoneNumber, paymentMethod, paymentScreenshotFile,
        isLoading, // <--- 暴露状态
        setLoading, // <--- 暴露方法
        addFiles, removeDocument, updateDocumentSettings, updateGroupBinding, resetStore, mergeGroups, // <--- 在这里导出新函数
        totalCost, isReadyToSubmit
    };
});
