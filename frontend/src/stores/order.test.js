import { describe, it, expect, vi, beforeEach } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useOrderStore } from '@/stores/order'

// Mock axios
vi.mock('axios', () => {
  return {
    default: {
      post: vi.fn()
    }
  }
})

describe('Order Store', () => {
  beforeEach(() => {
    // 创建新的 Pinia 实例并设置为活动实例
    setActivePinia(createPinia())
    
    // 清除所有模拟
    vi.clearAllMocks()
  })

  it('initializes with empty groups', () => {
    const store = useOrderStore()
    expect(store.groups).toEqual([])
  })

  it('adds files to groups', () => {
    const store = useOrderStore()
    const mockFile = new File([''], 'test.pdf', { type: 'application/pdf' })
    
    store.addFiles([mockFile])
    
    expect(store.groups).toHaveLength(1)
    expect(store.groups[0].documents).toHaveLength(1)
    expect(store.groups[0].documents[0].fileName).toBe('test.pdf')
  })

  it('removes document', () => {
    const store = useOrderStore()
    const mockFile = new File([''], 'test.pdf', { type: 'application/pdf' })
    
    store.addFiles([mockFile])
    const docId = store.groups[0].documents[0].id
    
    store.removeDocument(docId)
    
    expect(store.groups).toHaveLength(0)
  })

  it('updates document settings', () => {
    const store = useOrderStore()
    const mockFile = new File([''], 'test.pdf', { type: 'application/pdf' })
    
    store.addFiles([mockFile])
    const docId = store.groups[0].documents[0].id
    
    store.updateDocumentSettings(docId, { colorMode: 'color' })
    
    expect(store.groups[0].documents[0].settings.colorMode).toBe('color')
  })

  it('updates group binding', () => {
    const store = useOrderStore()
    const mockFile = new File([''], 'test.pdf', { type: 'application/pdf' })
    
    store.addFiles([mockFile])
    const groupId = store.groups[0].id
    
    store.updateGroupBinding(groupId, 'staple')
    
    expect(store.groups[0].bindingType).toBe('staple')
  })

  it('calculates total cost', () => {
    const store = useOrderStore()
    expect(store.totalCost).toBe('0.50') // Base service fee
  })

  it('resets store', () => {
    const store = useOrderStore()
    const mockFile = new File([''], 'test.pdf', { type: 'application/pdf' })
    
    store.addFiles([mockFile])
    store.phoneNumber = '123456789'
    store.resetStore()
    
    expect(store.groups).toEqual([])
    expect(store.phoneNumber).toBe('')
  })
})