import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import HomeView from '@/views/HomeView.vue'
import BaseButton from '@/components/BaseButton.vue'
import Stepper from '@/components/Stepper.vue'

// Mock components that are complex to test
vi.mock('@/components/FileUploader.vue', () => ({
  default: {
    name: 'FileUploader',
    template: '<div data-testid="file-uploader-mock"></div>',
    props: ['disabled'],
    emits: ['filesSelected']
  }
}))

vi.mock('@/components/OrderConfiguration.vue', () => ({
  default: {
    name: 'OrderConfiguration',
    template: '<div data-testid="order-configuration-mock"></div>'
  }
}))

vi.mock('@/components/PaymentUploader.vue', () => ({
  default: {
    name: 'PaymentUploader',
    template: '<div data-testid="payment-uploader-mock"></div>',
    emits: ['uploadSuccess']
  }
}))

vi.mock('@/components/Modal.vue', () => ({
  default: {
    name: 'Modal',
    template: '<div data-testid="modal-mock"><slot name="header"></slot><slot name="body"></slot></div>',
    props: ['show'],
    emits: ['close']
  }
}))

// Create a simple router for testing
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      component: HomeView
    }
  ]
})

describe('HomeView', () => {
  beforeEach(() => {
    // 创建新的 Pinia 实例并设置为活动实例
    setActivePinia(createPinia())
    
    // Mock localStorage
    Object.defineProperty(window, 'localStorage', {
      value: {
        getItem: vi.fn(),
        setItem: vi.fn(),
        removeItem: vi.fn(),
        clear: vi.fn(),
      },
      writable: true,
    })
  })

  it('renders the home view', () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    expect(wrapper.find('.home-view').exists()).toBe(true)
    expect(wrapper.find('.hero-section').exists()).toBe(true)
    expect(wrapper.findComponent(Stepper).exists()).toBe(true)
  })

  it('shows step 1 content initially', () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    expect(wrapper.find('h3.step-title').text()).toBe('第一步：上传文档并设置规格')
  })

  it('shows file uploader', () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    expect(wrapper.find('[data-testid="file-uploader-mock"]').exists()).toBe(true)
  })

  it('shows order configuration when files are added', async () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    // Mock the order store to have files
    const { useOrderStore } = await import('@/stores/order')
    const store = useOrderStore()
    store.groups = [{ id: '1', documents: [{ id: '1' }] }]
    
    await flushPromises()
    
    expect(wrapper.find('[data-testid="order-configuration-mock"]').exists()).toBe(true)
  })

  it('shows payment step when currentStep is 2', async () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    // Set current step to 2
    wrapper.vm.currentStep = 2
    
    await flushPromises()
    
    expect(wrapper.find('h3.step-title').text()).toBe('第二步：确认信息并支付')
  })

  it('shows completion step when currentStep is 3 and finalOrder exists', async () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    // Set current step to 3 and finalOrder
    wrapper.vm.currentStep = 3
    wrapper.vm.finalOrder = { pickup_code: 'P-123', order_number: 'ORDER123' }
    
    await flushPromises()
    
    expect(wrapper.find('h3.step-title').text()).toBe('订单提交成功！')
  })

  it('has terms and privacy checkboxes', () => {
    const wrapper = mount(HomeView, {
      global: {
        plugins: [createPinia(), router]
      }
    })
    
    expect(wrapper.find('#terms').exists()).toBe(true)
    expect(wrapper.find('#privacy').exists()).toBe(true)
  })
})