<script setup>
import { ref } from 'vue';
const emit = defineEmits(['file-selected']);
const fileName = ref('');

function handleFileChange(event) {
  const file = event.target.files[0];
  if (file) {
    fileName.value = file.name;
    emit('file-selected', file); // 通过emit事件将文件对象传递出去
  }
}
</script>

<template>
  <div class="uploader-wrapper">
    <label for="file-input" class="file-label">
      {{ fileName ? `已选择: ${fileName}` : '点击选择打印文件' }}
    </label>
    <input id="file-input" type="file" @change="handleFileChange" hidden />
  </div>
</template>

<style scoped>
.file-label {
  display: block;
  padding: 2rem;
  border: 2px dashed #ccc;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: background-color 0.2s, border-color 0.2s;
}
.file-label:hover {
  border-color: #007bff;
  background-color: #f8f9fa;
}
</style>
