import { describe, it, expect, vi, beforeEach } from 'vitest'
import { mount } from '@vue/test-utils'
import DSChatInput from '@/design-system/components/DSChatInput/DSChatInput.vue'

describe('DSChatInput - Gravação de Áudio', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Modo de Gravação', () => {
    it('renderiza UI de gravação quando recording=true', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true,
          recordingTime: '0:05'
        }
      })

      expect(wrapper.find('.ds-chat-input__form--recording').exists()).toBe(true)
      expect(wrapper.find('.recording-content-inline').exists()).toBe(true)
    })

    it('não renderiza campo de input quando gravando', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(false)
    })

    it('renderiza botão de deletar durante gravação', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      expect(wrapper.find('.recording-delete-btn').exists()).toBe(true)
    })

    it('renderiza indicador vermelho pulsante', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      expect(wrapper.find('.recording-dot-pulse').exists()).toBe(true)
    })

    it('exibe timer de gravação formatado', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true,
          recordingTime: '1:23'
        }
      })

      expect(wrapper.find('.recording-time-inline').text()).toBe('1:23')
    })

    it('renderiza waveform animada', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      const waveBars = wrapper.findAll('.wave-bar-inline')
      expect(waveBars.length).toBe(30)
    })

    it('renderiza botão verde de enviar durante gravação', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      const sendBtn = wrapper.find('.recording-send-btn')
      expect(sendBtn.exists()).toBe(true)
    })
  })

  describe('Eventos de Gravação', () => {
    it('emite cancel-recording ao clicar em deletar', async () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      await wrapper.find('.recording-delete-btn').trigger('click')
      expect(wrapper.emitted('cancel-recording')).toBeTruthy()
    })

    it('emite send-recording ao clicar em enviar', async () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      const sendBtn = wrapper.find('.recording-send-btn')
      await sendBtn.trigger('click')
      expect(wrapper.emitted('send-recording')).toBeTruthy()
    })
  })

  describe('Modo Normal', () => {
    it('renderiza campo de input quando não está gravando', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: false
        }
      })

      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(true)
      expect(wrapper.find('.recording-content-inline').exists()).toBe(false)
    })

    it('renderiza ícones da esquerda no modo normal', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: false
        }
      })

      expect(wrapper.find('.ds-chat-input__left-icons').exists()).toBe(true)
    })

    it('alterna para modo de gravação quando prop recording muda', async () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: false
        }
      })

      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(true)

      await wrapper.setProps({ recording: true })

      expect(wrapper.find('.recording-content-inline').exists()).toBe(true)
      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(false)
    })
  })

  describe('Props de Gravação', () => {
    it('aceita prop recording', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      expect(wrapper.props('recording')).toBe(true)
    })

    it('aceita prop recordingTime', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true,
          recordingTime: '2:45'
        }
      })

      expect(wrapper.props('recordingTime')).toBe('2:45')
    })

    it('usa valor padrão para recordingTime', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      expect(wrapper.props('recordingTime')).toBe('0:00')
    })
  })

  describe('Estilos e Classes', () => {
    it('aplica classe de gravação ao form', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true
        }
      })

      const form = wrapper.find('.ds-chat-input__form')
      expect(form.classes()).toContain('ds-chat-input__form--recording')
    })

    it('não aplica classe de gravação quando não está gravando', () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: false
        }
      })

      const form = wrapper.find('.ds-chat-input__form')
      expect(form.classes()).not.toContain('ds-chat-input__form--recording')
    })
  })

  describe('Integração', () => {
    it('permite cancelar e depois gravar novamente', async () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: '',
          recording: true,
          recordingTime: '0:10'
        }
      })

      // Cancela
      await wrapper.find('.recording-delete-btn').trigger('click')
      expect(wrapper.emitted('cancel-recording')).toBeTruthy()

      // Simula retorno ao modo normal
      await wrapper.setProps({ recording: false, recordingTime: '0:00' })
      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(true)

      // Inicia gravação novamente
      await wrapper.setProps({ recording: true })
      expect(wrapper.find('.recording-content-inline').exists()).toBe(true)
    })

    it('mantém estado consistente durante ciclo completo', async () => {
      const wrapper = mount(DSChatInput, {
        props: {
          modelValue: 'Texto digitado',
          recording: false
        }
      })

      // Estado inicial
      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(true)
      expect(wrapper.props('modelValue')).toBe('Texto digitado')

      // Inicia gravação
      await wrapper.setProps({ recording: true, recordingTime: '0:00' })
      expect(wrapper.find('.recording-content-inline').exists()).toBe(true)

      // Envia gravação
      const sendBtn = wrapper.find('.recording-send-btn')
      await sendBtn.trigger('click')
      expect(wrapper.emitted('send-recording')).toBeTruthy()

      // Retorna ao normal
      await wrapper.setProps({ recording: false, recordingTime: '0:00' })
      expect(wrapper.find('.ds-chat-input__field').exists()).toBe(true)
    })
  })
})
