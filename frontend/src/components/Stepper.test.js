import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import Stepper from '@/components/Stepper.vue'

describe('Stepper', () => {
  const steps = ['第一步', '第二步', '第三步']

  it('renders properly', () => {
    const wrapper = mount(Stepper, {
      props: {
        currentStep: 1,
        steps
      }
    })
    expect(wrapper.findAll('.step')).toHaveLength(3)
  })

  it('shows correct step labels', () => {
    const wrapper = mount(Stepper, {
      props: {
        currentStep: 1,
        steps
      }
    })
    const stepLabels = wrapper.findAll('.step-label')
    expect(stepLabels[0].text()).toBe('第一步')
    expect(stepLabels[1].text()).toBe('第二步')
    expect(stepLabels[2].text()).toBe('第三步')
  })

  it('highlights the current step', () => {
    const wrapper = mount(Stepper, {
      props: {
        currentStep: 2,
        steps
      }
    })
    const stepsElements = wrapper.findAll('.step')
    expect(stepsElements[1].classes()).toContain('active')
  })

  it('marks previous steps as completed', () => {
    const wrapper = mount(Stepper, {
      props: {
        currentStep: 3,
        steps
      }
    })
    const stepsElements = wrapper.findAll('.step')
    expect(stepsElements[0].classes()).toContain('completed')
    expect(stepsElements[1].classes()).toContain('completed')
  })

  it('calculates progress width correctly', async () => {
    const wrapper = mount(Stepper, {
      props: {
        currentStep: 1,
        steps
      }
    })
    // First step: 0% progress
    expect(wrapper.find('.stepper-progress').attributes('style')).toContain('width: 0%;')
    
    await wrapper.setProps({ currentStep: 2 })
    // Second step: 50% progress
    expect(wrapper.find('.stepper-progress').attributes('style')).toContain('width: 50%;')
    
    await wrapper.setProps({ currentStep: 3 })
    // Third step: 100% progress
    expect(wrapper.find('.stepper-progress').attributes('style')).toContain('width: 100%;')
  })
})