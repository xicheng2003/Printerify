import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { createPinia, setActivePinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import HomeView from './HomeView.vue'

// 模拟路由
const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: HomeView },
    { path: '/auth', component: { template: '<div>Auth</div>' } }
  ]
})

// 模拟用户store
const mockUserStore = {
  isAuthenticated: false,
  user: null
}

// 模拟订单store
const mockOrderStore = {
  groups: [],
  isReadyToSubmit: false,
  totalCost: 0,
  paymentMethod: 'WECHAT',
  phoneNumber: ''
}

describe('HomeView.vue', () => {
  let wrapper
  let pinia

  beforeEach(() => {
    pinia = createPinia()
    setActivePinia(pinia)

    // 模拟store
    vi.mock('@/stores/user', () => ({
      useUserStore: () => mockUserStore
    }))

    vi.mock('@/stores/order', () => ({
      useOrderStore: () => mockOrderStore
    }))

    wrapper = mount(HomeView, {
      global: {
        plugins: [pinia, router],
        stubs: {
          'Teleport': true,
          'Stepper': true,
          'FileUploader': true,
          'PaymentUploader': true,
          'BaseButton': true,
          'Modal': true,
          'OrderConfiguration': true
        }
      }
    })
  })

  it('应该显示登录引导横幅当用户未登录时', () => {
    mockUserStore.isAuthenticated = false
    wrapper.vm.showLoginGuideBanner = true
    
    expect(wrapper.find('.login-guide-banner').exists()).toBe(true)
  })

  it('应该隐藏登录引导横幅当用户已登录时', async () => {
    mockUserStore.isAuthenticated = true
    await wrapper.vm.$nextTick()
    
    expect(wrapper.find('.login-guide-banner').exists()).toBe(false)
  })

  it('应该包含正确的横幅内容', () => {
    mockUserStore.isAuthenticated = false
    wrapper.vm.showLoginGuideBanner = true
    
    expect(wrapper.find('.banner-title').text()).toBe('登录享受更多优惠')
    expect(wrapper.find('.banner-subtitle').text()).toBe('保存订单历史 • 专属优惠券 • 快速下单')
  })

  it('应该包含登录和注册按钮', () => {
    mockUserStore.isAuthenticated = false
    wrapper.vm.showLoginGuideBanner = true
    
    expect(wrapper.find('.banner-login-btn').exists()).toBe(true)
    expect(wrapper.find('.banner-register-btn').exists()).toBe(true)
    expect(wrapper.find('.banner-remind-btn').exists()).toBe(true)
  })

  it('点击关闭按钮应该隐藏横幅', async () => {
    mockUserStore.isAuthenticated = false
    wrapper.vm.showLoginGuideBanner = true
    
    await wrapper.find('.banner-close-btn').trigger('click')
    
    expect(wrapper.vm.showLoginGuideBanner).toBe(false)
  })

  it('关闭横幅后，用户登出时应该重新显示横幅', async () => {
    // 先关闭横幅
    wrapper.vm.showLoginGuideBanner = false
    
    // 模拟用户登出
    mockUserStore.isAuthenticated = false
    await wrapper.vm.$nextTick()
    
    // 横幅应该重新显示
    expect(wrapper.vm.showLoginGuideBanner).toBe(true)
  })

  it('稍后提醒功能应该5分钟后重新显示横幅', async () => {
    mockUserStore.isAuthenticated = false
    wrapper.vm.showLoginGuideBanner = true
    
    // 模拟点击稍后提醒
    await wrapper.find('.banner-remind-btn').trigger('click')
    
    // 横幅应该立即隐藏
    expect(wrapper.vm.showLoginGuideBanner).toBe(false)
  })

  it('应该正确响应式设计', () => {
    mockUserStore.isAuthenticated = false
    wrapper.vm.showLoginGuideBanner = true
    
    // 检查横幅是否包含响应式样式类
    const banner = wrapper.find('.login-guide-banner')
    expect(banner.exists()).toBe(true)
  })
})