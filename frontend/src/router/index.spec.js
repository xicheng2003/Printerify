
/**
 * @vitest-environment jsdom
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { createRouter, createWebHistory } from 'vue-router'
import { setActivePinia, createPinia } from 'pinia'

// Use vi.hoisted to define mocks that need to be accessed in tests AND used in vi.mock factory
const mockAxios = vi.hoisted(() => {
    const axiosInstance = {
        get: vi.fn(),
        post: vi.fn(),
        create: vi.fn(),
        interceptors: {
            request: { use: vi.fn(), eject: vi.fn() },
            response: { use: vi.fn(), eject: vi.fn() }
        },
        defaults: { headers: { common: {} } }
    }

    // Make create return the instance itself
    axiosInstance.create.mockReturnValue(axiosInstance)

    return axiosInstance
})

vi.mock('axios', () => ({ default: mockAxios }))

// Mock components to avoid loading actual views
vi.mock('../views/HomeView.vue', () => ({ default: { template: '<div>Home</div>' } }))
vi.mock('../views/ProductIntroView.vue', () => ({ default: { template: '<div>Intro</div>' } }))
vi.mock('../views/AuthView.vue', () => ({ default: { template: '<div>Auth</div>' } }))
vi.mock('../views/ProfileView.vue', () => ({ default: { template: '<div>Profile</div>' } }))
vi.mock('@/views/OAuthCallbackView.vue', () => ({ default: { template: '<div>OAuth</div>' } }))
vi.mock('@/views/ClosureNoticeView.vue', () => ({ default: { template: '<div>Closure</div>' } }))
vi.mock('../views/AboutView.vue', () => ({ default: { template: '<div>About</div>' } }))
vi.mock('../views/TermsView.vue', () => ({ default: { template: '<div>Terms</div>' } }))
vi.mock('../views/PrivacyView.vue', () => ({ default: { template: '<div>Privacy</div>' } }))
vi.mock('../views/QueryView.vue', () => ({ default: { template: '<div>Query</div>' } }))
vi.mock('../views/NotFoundView.vue', () => ({ default: { template: '<div>NotFound</div>' } }))


// Now import the router
import router from '../router/index.js'

describe('Router Guard - Business Pause Logic', () => {
    let originalDateNow

    beforeEach(async () => {
        setActivePinia(createPinia())
        vi.clearAllMocks()
        // vi.useFakeTimers() // REMOVED

        // Mock Date.now
        originalDateNow = Date.now
        // Default start time
        Date.now = vi.fn(() => new Date(2023, 1, 1, 10, 0, 0).getTime())

        await router.push('/') // Reset route

        // Reset defaults
        mockAxios.create.mockReturnValue(mockAxios)
    })

    afterEach(() => {
        // Restore Date.now
        if (originalDateNow) {
            Date.now = originalDateNow
        }
    })

    it('allows access to order page when business is OPEN', async () => {
        // Mock API response: Open
        mockAxios.get.mockResolvedValue({ data: { is_open: true } })

        await router.push('/order')

        // Should be on /order
        expect(router.currentRoute.value.path).toBe('/order')
        // The router calls /api/system-config/
        expect(mockAxios.get).toHaveBeenCalledWith('/api/system-config/')
    })

    it('redirects to closure notice when accessing order page and business is CLOSED', async () => {
        // Advance time to expire cache (1 hour later)
        Date.now = vi.fn(() => new Date(2023, 1, 1, 11, 0, 0).getTime())

        // Mock API response: Closed
        mockAxios.get.mockResolvedValue({ data: { is_open: false, closure_reason: 'Closed' } })

        await router.push('/order')

        // Wait for potential redirect. 
        // With real timers (microtasks), simply awaiting flushPromises should be enough
        // But await router.push should settle.
        // Let's add a small tick just in case.
        await new Promise(r => setTimeout(r, 0))

        // Should be redirected to /closure-notice
        expect(router.currentRoute.value.name).toBe('closure-notice')
    })

    it('allows access to other pages (e.g. About) when business is CLOSED', async () => {
        // Ensure cache is fresh or expired
        Date.now = vi.fn(() => new Date(2023, 1, 1, 12, 0, 0).getTime())

        // Mock API response: Closed
        mockAxios.get.mockResolvedValue({ data: { is_open: false, closure_reason: 'Closed' } })

        await router.push('/about')

        expect(router.currentRoute.value.path).toBe('/about')
    })

    it('allows access to Intro page when business is CLOSED', async () => {
        // Ensure cache is fresh or expired
        Date.now = vi.fn(() => new Date(2023, 1, 1, 13, 0, 0).getTime())

        // Mock API response: Closed
        mockAxios.get.mockResolvedValue({ data: { is_open: false, closure_reason: 'Closed' } })

        await router.push('/')

        // Should be on / (intro)
        expect(router.currentRoute.value.path).toBe('/')
    })
})
