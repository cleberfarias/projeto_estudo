import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useContactsStore } from '@/stores/contacts'

describe('ContactsStore Polling', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.useFakeTimers()
  })

  afterEach(() => {
    vi.useRealTimers()
    vi.restoreAllMocks()
  })

  it('inicia polling e chama fetchUnreadCounts periodicamente', async () => {
    const store = useContactsStore()
    const spy = vi.spyOn(store, 'fetchUnreadCounts').mockResolvedValue(undefined)

    store.startUnreadPolling(1000)

    // chamada imediata
    expect(spy).toHaveBeenCalledTimes(1)

    // avança 3000ms (3 ticks de 1000ms)
    await vi.advanceTimersByTimeAsync(3000)
    await Promise.resolve()

    // chamada imediata + 3 ticks = pelo menos 4
    expect(spy.mock.calls.length).toBeGreaterThanOrEqual(4)

    store.stopUnreadPolling()
  })

  it('stop cancela polling', async () => {
    const store = useContactsStore()
    const spy = vi.spyOn(store, 'fetchUnreadCounts').mockResolvedValue(undefined)

    store.startUnreadPolling(1000)

    // após 1 tick
    await vi.advanceTimersByTimeAsync(1000)
    await Promise.resolve()

    expect(spy.mock.calls.length).toBeGreaterThanOrEqual(2)

    store.stopUnreadPolling()

    const callsBefore = spy.mock.calls.length

    // avança mais tempo — não deve haver novas chamadas
    await vi.advanceTimersByTimeAsync(3000)
    await Promise.resolve()

    expect(spy.mock.calls.length).toBe(callsBefore)
  })
})