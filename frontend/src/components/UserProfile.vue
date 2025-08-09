<template>
  <div class="user-profile-container">
    <div class="profile-header">
      <div class="avatar-placeholder">
        <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"></path>
          <circle cx="12" cy="7" r="4"></circle>
        </svg>
      </div>
      <div class="user-info">
        <h2 class="username">{{ user.username }}</h2>
        <p class="member-since">注册于 {{ formatDate(user.date_joined) }}</p>
      </div>
    </div>

    <div class="profile-details">
      <div class="detail-item">
        <label>用户名</label>
        <p>{{ user.username }}</p>
      </div>

      <div class="detail-item">
        <label>电子邮件</label>
        <p>{{ user.email || '未设置' }}</p>
      </div>

      <div class="detail-item">
        <label>手机号</label>
        <p>{{ user.phone_number || '未设置' }}</p>
      </div>

      <div class="detail-item">
        <label>姓名</label>
        <p>{{ fullName || '未设置' }}</p>
      </div>
    </div>

    <div class="profile-actions">
      <BaseButton @click="showEditModal = true" class="edit-button">
        编辑资料
      </BaseButton>
      <BaseButton @click="handleLogout" :loading="logoutLoading" class="logout-button">
        退出登录
      </BaseButton>
    </div>

    <!-- 编辑资料模态框 -->
    <Modal :show="showEditModal" @close="showEditModal = false">
      <template #header>
        <h3>编辑个人资料</h3>
      </template>
      <template #body>
        <form @submit.prevent="updateProfile" class="edit-form">
          <div class="form-group">
            <label for="edit-first-name">名字</label>
            <input
              id="edit-first-name"
              v-model="editForm.first_name"
              type="text"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="edit-last-name">姓氏</label>
            <input
              id="edit-last-name"
              v-model="editForm.last_name"
              type="text"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="edit-email">电子邮件</label>
            <input
              id="edit-email"
              v-model="editForm.email"
              type="email"
              class="form-input"
            />
          </div>

          <div class="form-group">
            <label for="edit-phone">手机号</label>
            <input
              id="edit-phone"
              v-model="editForm.phone_number"
              type="tel"
              class="form-input"
            />
          </div>

          <div class="form-actions">
            <BaseButton type="submit" :loading="updateLoading" :disabled="!isEditFormValid">
              保存更改
            </BaseButton>
            <BaseButton @click="showEditModal = false" :disabled="updateLoading" variant="secondary">
              取消
            </BaseButton>
          </div>

          <div v-if="updateError" class="error-message">
            {{ updateError }}
          </div>
        </form>
      </template>
    </Modal>
  </div>
</template>

<script setup>
import { ref, computed, reactive } from 'vue'
import { useUserStore } from '@/stores/user'
import BaseButton from '@/components/BaseButton.vue'
import Modal from '@/components/Modal.vue'

const userStore = useUserStore()
const showEditModal = ref(false)
const logoutLoading = ref(false)
const updateLoading = ref(false)
const updateError = ref('')

const user = computed(() => userStore.user)

const fullName = computed(() => {
  const first = user.value.first_name || ''
  const last = user.value.last_name || ''
  return first || last ? `${first} ${last}`.trim() : ''
})

const editForm = reactive({
  first_name: '',
  last_name: '',
  email: '',
  phone_number: ''
})

const isEditFormValid = computed(() => {
  return editForm.email && editForm.email.includes('@')
})

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function handleLogout() {
  logoutLoading.value = true
  userStore.logout()
    .finally(() => {
      logoutLoading.value = false
    })
}

function updateProfile() {
  if (!isEditFormValid.value) return

  updateLoading.value = true
  updateError.value = ''

  // 准备更新数据
  const updateData = {}
  Object.keys(editForm).forEach(key => {
    if (editForm[key] !== user.value[key]) {
      updateData[key] = editForm[key]
    }
  })

  userStore.updateProfile(updateData)
    .then(() => {
      showEditModal.value = false
    })
    .catch(err => {
      updateError.value = err.response?.data?.detail || err.message || '更新失败，请重试'
    })
    .finally(() => {
      updateLoading.value = false
    })
}

// 当打开编辑模态框时，填充当前用户数据
showEditModal.value = false // 初始化为关闭状态
</script>

<style scoped>
.user-profile-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 2rem;
  background-color: var(--color-background-soft);
  border-radius: 12px;
  box-shadow: var(--shadow-card);
  border: 1px solid var(--color-border);
}

.profile-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid var(--color-border);
}

.avatar-placeholder {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background-color: var(--color-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.username {
  margin: 0 0 0.5rem 0;
  color: var(--color-heading);
  font-size: 1.5rem;
  font-weight: 600;
}

.member-since {
  margin: 0;
  color: var(--color-text-mute);
  font-size: 0.9rem;
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.detail-item label {
  font-weight: 600;
  color: var(--color-heading);
  font-size: 0.9rem;
}

.detail-item p {
  margin: 0;
  color: var(--color-text);
  font-size: 1.1rem;
}

.profile-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
}

.edit-button, .logout-button {
  flex: 1;
  padding: 0.75rem;
}

.logout-button {
  background-color: var(--color-danger);
}

.logout-button:hover:not(:disabled) {
  background-color: var(--color-danger-hover);
}

.edit-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: var(--color-heading);
  font-size: 0.9rem;
}

.form-input {
  padding: 0.75rem 1rem;
  border: 1px solid var(--color-border);
  border-radius: 8px;
  font-size: 1rem;
  background-color: var(--color-background);
  color: var(--color-text);
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-input:focus {
  outline: none;
  border-color: var(--color-primary);
  box-shadow: 0 0 0 3px rgba(var(--color-primary-rgb, 37, 99, 235), 0.2);
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}

.form-actions button {
  flex: 1;
}

.error-message {
  padding: 0.75rem;
  background-color: var(--color-danger);
  color: var(--color-text-on-danger);
  border-radius: 8px;
  font-size: 0.9rem;
  text-align: center;
  margin-top: 1rem;
}

@media (max-width: 768px) {
  .user-profile-container {
    padding: 1.5rem;
  }
  
  .profile-header {
    flex-direction: column;
    text-align: center;
  }
  
  .profile-actions {
    flex-direction: column;
  }
  
  .form-actions {
    flex-direction: column;
  }
}
</style>