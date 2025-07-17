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
import draggable from 'vuedraggable';
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
/*
  BindingGroup.vue 的样式已更新，使用 CSS 变量以支持主题切换。
*/
.binding-group {
  border: 1px solid var(--color-border); /* 已修改 */
  border-radius: 12px;
  background-color: var(--color-background-soft); /* 已修改 */
  padding: 1rem;
  margin-bottom: 1.5rem;
  transition: background-color 0.2s, border-color 0.2s;
}

.binding-group[draggable="true"] {
  cursor: grab;
}

/* 拖拽悬停时的目标高亮样式 */
.is-drop-target {
  background-color: rgba(var(--color-primary-rgb, 37, 99, 235), 0.1); /* 已修改 */
  border-color: var(--color-primary); /* 已修改 */
  border-style: dashed;
}

.group-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid var(--color-border); /* 已修改 */
}

.group-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-heading); /* 已修改 */
  display: flex;
  align-items: center;
}

.drag-handle {
  color: var(--color-text-mute); /* 已修改 */
  margin-right: 0.75rem;
  font-size: 1.25rem;
}

.file-count {
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text-mute); /* 已修改 */
  margin-left: 0.5rem;
}

.binding-selector label {
  margin-right: 0.5rem;
  font-size: 0.9rem;
  font-weight: 500;
  color: var(--color-text); /* 已修改 */
}

.binding-selector select {
  padding: 0.5rem;
  border-radius: 8px;
  border: 1px solid var(--color-border); /* 已修改 */
  background-color: var(--color-background); /* 已修改 */
  color: var(--color-text); /* 已修改 */
}

.documents-container {
  padding-top: 0.5rem;
}

/* vuedraggable 的占位符样式 */
.ghost-document {
  opacity: 0.5;
  background: var(--color-background-mute); /* 已修改 */
  border: 1px dashed var(--color-primary); /* 已修改 */
}

@media (max-width: 767px) {
  .group-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.75rem;
  }
  .group-title {
    font-size: 1rem;
  }
  .binding-selector select {
    padding: 0.4rem;
    font-size: 0.9rem;
  }
}
</style>
