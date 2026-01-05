import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { setActivePinia, createPinia } from 'pinia'
import { createVuetify } from 'vuetify'
import ContactsView from '@/views/crm/ContactsView.vue'
import { useContactsStore } from '@/stores/contacts'

const vuetify = createVuetify()

describe('ContactsView', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  it('abre dialog e cria contato chamando a store', async () => {
    const store = useContactsStore()
    const createSpy = vi.spyOn(store, 'createContact').mockResolvedValueOnce(undefined)

    const wrapper = mount(ContactsView, {
      global: {
        plugins: [vuetify],
        stubs: {
          'router-link': true
        }
      }
    })

    // Abre o diálogo: procura botão com texto "Novo Contato"
    // Procura por qualquer nó que contenha o texto 'Novo Contato'
    const newBtn = wrapper.findAll('*').find(n => n.text().trim() === 'Novo Contato')
    if (!newBtn) {
      throw new Error('Botão Novo Contato não encontrado no componente')
    }
    await newBtn.trigger('click')

    // Define o nome do novo contato no estado do componente
    // Usa vm para acessar newContact reativo definido no <script setup>
    ;(wrapper.vm as any).newContact.name = 'Teste'

    // Chama o handler diretamente
    await (wrapper.vm as any).onCreateContact()

    expect(createSpy).toHaveBeenCalledWith({ name: 'Teste', email: undefined, phone: undefined })
    // Após criar, o diálogo deve ser fechado
    expect((wrapper.vm as any).showCreateDialog).toBe(false)
    // Exibe snackbar de sucesso
    expect((wrapper.vm as any).showSnackbar).toBe(true)
    expect((wrapper.vm as any).snackbarText).toContain('Teste')
  })

  it('mostra snackbar de erro quando a store lança exceção', async () => {
    const store = useContactsStore()
    vi.spyOn(store, 'createContact').mockRejectedValueOnce(new Error('fail'))

    const wrapper = mount(ContactsView, {
      global: {
        plugins: [vuetify],
        stubs: { 'router-link': true }
      }
    })

    // Abre o diálogo e seta nome
    const newBtn = wrapper.findAll('*').find(n => n.text().trim() === 'Novo Contato')
    if (!newBtn) throw new Error('Botão Novo Contato não encontrado no componente')
    await newBtn.trigger('click')
    ;(wrapper.vm as any).newContact.name = 'ErroTest'

    await expect((wrapper.vm as any).onCreateContact()).rejects.toThrow()
    expect((wrapper.vm as any).showSnackbar).toBe(true)
    expect((wrapper.vm as any).snackbarText).toBe('Erro ao criar contato')
  })
})