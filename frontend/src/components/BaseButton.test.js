import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import BaseButton from '@/components/BaseButton.vue'

describe('BaseButton', () => {
  it('renders properly', () => {
    const wrapper = mount(BaseButton, {
      slots: {
        default: 'Click me'
      }
    })
    expect(wrapper.text()).toContain('Click me')
  })

  it('displays spinner when loading', () => {
    const wrapper = mount(BaseButton, {
      props: {
        loading: true
      },
      slots: {
        default: 'Loading...'
      }
    })
    expect(wrapper.find('.spinner').exists()).toBe(true)
  })

  it('is disabled when loading', async () => {
    const wrapper = mount(BaseButton, {
      props: {
        loading: true
      },
      slots: {
        default: 'Loading...'
      }
    })
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('is disabled when disabled prop is true', async () => {
    const wrapper = mount(BaseButton, {
      props: {
        disabled: true
      },
      slots: {
        default: 'Disabled'
      }
    })
    expect(wrapper.attributes('disabled')).toBeDefined()
  })

  it('emits click event when clicked', async () => {
    const wrapper = mount(BaseButton, {
      slots: {
        default: 'Click me'
      }
    })
    await wrapper.trigger('click')
    expect(wrapper.emitted()).toHaveProperty('click')
  })
})