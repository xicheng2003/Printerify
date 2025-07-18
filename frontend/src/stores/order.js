// frontend/src/stores/order.js (最终响应式修复版)

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import { v4 as uuidv4 } from 'uuid';
import axios from 'axios';

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

    async function _fetchPriceForDocument(docId) {
        const doc = findDocumentById(docId);
        if (!doc) return;

        doc.isRecalculating = true; // 【核心修复】使用 isRecalculating
        doc.error = null;
        try {
            const response = await axios.post('/api/estimate-price/', {
                file_path: doc.serverId,
                color_mode: doc.settings.colorMode,
                print_sided: doc.settings.printSided,
                paper_size: doc.settings.paperSize, // <--- 【在此处新增】
                copies: doc.settings.copies
            }, { withCredentials: true });
            doc.pageCount = response.data.page_count;
            doc.printCost = response.data.print_cost;
        } catch (error) {
            doc.error = '计价失败';
        } finally {
            doc.isRecalculating = false; // 【核心修复】使用 isRecalculating
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
            await _fetchPriceForDocument(docId);
        } catch (error) {
            doc.error = '上传失败';
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
                    paperSize: 'a4' // <--- 【在此处新增】
                },
                pageCount: 0, printCost: 0,
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

    const totalCost = computed(() => {
        let total = 0.5;
        groups.value.forEach(group => {
            group.documents.forEach(doc => {
                total += Number(doc.printCost) || 0;
            });
            const bindingType = group.bindingType;
            if (bindingType in BINDING_PRICE_CONFIG) {
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
        isLoading,
        setLoading,
        addFiles, removeDocument, updateDocumentSettings, updateGroupBinding, resetStore, mergeGroups,
        totalCost, isReadyToSubmit
    };
});
