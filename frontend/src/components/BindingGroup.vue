<template>
  <div
    class="binding-group"
    draggable="true"
    @dragstart.stop="onDragStart"
    @dragover.prevent="onDragOver"
    @dragleave.prevent="onDragLeave"
    @drop.prevent.stop="onDrop"
    :class="{ 'is-drop-target': isDropTarget }"
  >
    <div class="group-header">
      <div class="group-title">
        <span class="drag-handle" title="拖拽此组可与其他组合并">⠿</span>
        <strong>装订组 #{{ index + 1 }}</strong>
        <span class="file-count"> ({{ group.documents.length }} 个文件)</span>
      </div>
      <div class="binding-selector">
        <label :for="'binding-' + group.id">装订方式:</label>
        <select
          :id="'binding-' + group.id"
          v-model="group.bindingType"
          @change="updateBindingType($event.target.value)"
        >
          <option value="none">不装订</option>
          <option value="staple_top_left">订书钉 (左上角) (¥0.10)</option>
          <option value="staple_left_side">订书钉 (左侧) (¥0.10)</option>
          <!-- 您可以继续添加其他装订方式
          <option value="staple">骑马钉 (¥2.00)</option>
          <option value="staple_top_left">订书钉 (左上角) (¥0.10)</option>
          <option value="staple_left_side">订书钉 (左侧) (¥0.10)</option>
          <option value="ring_bound">胶圈装 (¥5.00)</option>
          -->
        </select>
      </div>
    </div>

    <div class="documents-container">
      <draggable
        v-model="group.documents"
        item-key="id"
        handle=".doc-drag-handle"
        ghost-class="ghost-document"
      >
        <template #item="{ element: doc }">
          <DocumentItem :document="doc" />
        </template>
      </draggable>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useOrderStore } from '@/stores/order';
import draggable from 'vuedraggable'; // 【新增】导入draggable库
import DocumentItem from './DocumentItem.vue';

const props = defineProps({
  group: { type: Object, required: true },
  index: { type: Number, required: true }
});

const orderStore = useOrderStore();
const isDropTarget = ref(false);

function updateBindingType(newType) {
  orderStore.updateGroupBinding(props.group.id, newType);
}

// --- 用于“合并组”的原生拖放事件处理 (保持不变) ---
function onDragStart(event) {
  event.dataTransfer.setData('text/plain', props.group.id);
  event.dataTransfer.effectAllowed = 'move';
}
function onDragOver() { isDropTarget.value = true; }
function onDragLeave() { isDropTarget.value = false; }
function onDrop(event) {
  isDropTarget.value = false;
  const sourceGroupId = event.dataTransfer.getData('text/plain');
  if (sourceGroupId && sourceGroupId !== props.group.id) {
    orderStore.mergeGroups(sourceGroupId, props.group.id);
  }
}
</script>

<style scoped>
/* 【新增】为拖拽文件时的占位符添加样式 */
.ghost-document {
  opacity: 0.5;
  background: #f0f4ff;
  border: 1px dashed #a5b4fc;
}
/* 使整个组可被抓取 */
.binding-group[draggable="true"] {
  cursor: grab;
}
/* 当一个组成为可放置目标时的高亮样式 */
.is-drop-target {
  background-color: #e0e7ff; /* 淡蓝色背景 */
  border-color: #a5b4fc; /* 边框颜色加深 */
  border-style: dashed;
}
/* ... 其他您已有的样式保持不变 ... */
.binding-group {
  border: 1px solid #cbd5e1;
  border-radius: 12px;
  background-color: #f8fafc;
  padding: 1rem;
  margin-bottom: 1.5rem;
  transition: background-color 0.2s, border-color 0.2s;
}
.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #e2e8f0;
}
.group-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--text-dark);
  display: flex;
  align-items: center;
}
.drag-handle {
  color: #94a3b8;
  margin-right: 0.75rem;
  font-size: 1.25rem;
}
.file-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: #64748b;
  margin-left: 0.5rem;
}
.binding-selector label {
  margin-right: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
}
.binding-selector select {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid #cbd5e1;
  background-color: #fff;
}
.documents-container {
  padding-top: 0.5rem;
}
/* 【新增】响应式布局调整 */
@media (max-width: 767px) {
  .group-header {
    flex-direction: column; /* 垂直堆叠 */
    align-items: flex-start; /* 左对齐 */
    gap: 0.75rem; /* 增加堆叠后的间距 */
  }
  .group-title {
    font-size: 1rem; /* 减小标题字号 */
  }
  .binding-selector select {
    padding: 0.4rem; /* 减小选择框内边距 */
    font-size: 0.9rem;
  }
}
</style>
