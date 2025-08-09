import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount, flushPromises } from '@vue/test-utils'
import { createRouter, createWebHistory } from 'vue-router'
import { createPinia, setActivePinia } from 'pinia'
import AuthForm from '@/components/AuthForm.vue'
import BaseButton from '@/components/BaseButton.vue'

// Mock the user store
vi.mock('@/stores/user', () => {
  return {
    useUserStore: vi.fn().mockImplementation(() => {
      return {
        login: vi.fn().mockResolvedValue({}),
        register: vi.fn().mockResolvedValue({}),
        isAuthenticated: false,
        user: null
      }
    })
  }
})

// Mock the BaseButton component
vi.mock('@/components/BaseButton.vue', () => ({
  default: {
    name: 'BaseButton',
    template: '<button><slot></slot></button>',
    props: ['loading', 'disabled']
  }
}))

// Create a simple router for testing
const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/auth',
      component: { template: '<div>Auth</div>' }
    }
  ]
})

describe('AuthForm', () => {
  beforeEach(() => {
    // Create a new Pinia instance and make it active
    setActivePinia(createPinia())
  })

  it('renders login form by default', () => {
    const wrapper = mount(AuthForm, {
      global: {
        plugins: [router]
      }
    })
    
    expect(wrapper.find('.form-title').text()).toBe('用户登录')
    expect(wrapper.find('#username').exists()).toBe(true)
    expect(wrapper.find('#password').exists()).toBe(true)
    expect(wrapper.find('#email').exists()).toBe(false)
  })

  it('renders registration form when isLogin is false', async () => {
    const wrapper = mount(AuthForm, {
      props: {
        isLogin: false
      },
      global: {
        plugins: [router]
      }
    })
    
    await flushPromises()
    
    expect(wrapper.find('.form-title').text()).toBe('用户注册')
    expect(wrapper.find('#username').exists()).toBe(true)
    expect(wrapper.find('#email').exists()).toBe(true)
    expect(wrapper.find('#password').exists()).toBe(true)
    expect(wrapper.find('#password_confirm').exists()).toBe(true)
  })

  it('emits update:isLogin event when toggle link is clicked', async () => {
    const wrapper = mount(AuthForm, {
      global: {
        plugins: [router]
      }
    })
    
    await wrapper.find('.auth-toggle a').trigger('click')
    
    expect(wrapper.emitted('update:isLogin')).toBeTruthy()
    expect(wrapper.emitted('update:isLogin')[0]).toEqual([false])
  })

  it('validates login form correctly', async () => {
    const wrapper = mount(AuthForm, {
      global: {
        plugins: [router]
      }
    })
    
    // Initially form should be invalid
    expect(wrapper.findComponent(BaseButton).props('disabled')).toBe(true)
    
    // Fill in username and password
    await wrapper.find('#username').setValue('testuser')
    await wrapper.find('#password').setValue('testpassword')
    
    // Form should now be valid
    expect(wrapper.findComponent(BaseButton).props('disabled')).toBe(false)
  })

  it('validates registration form correctly', async () => {
    const wrapper = mount(AuthForm, {
      props: {
        isLogin: false
      },
      global: {
        plugins: [router]
      }
    })
    
    // Initially form should be invalid
    expect(wrapper.findComponent(BaseButton).props('disabled')).toBe(true)
    
    // Fill in required fields
    await wrapper.find('#username').setValue('testuser')
    await wrapper.find('#email').setValue('test@example.com')
    await wrapper.find('#password').setValue('testpassword')
    await wrapper.find('#password_confirm').setValue('testpassword')
    
    // Form should now be valid
    expect(wrapper.findComponent(BaseButton).props('disabled')).toBe(false)
  })
})