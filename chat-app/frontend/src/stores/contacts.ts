import { defineStore } from 'pinia';
import { useAuthStore } from './auth';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000';

export interface Contact {
  id: string;
  name: string;
  email: string;
  avatar?: string;
  lastMessage?: string;
  lastMessageTime?: number;
  unreadCount: number;
  online: boolean;
}

export const useContactsStore = defineStore('contacts', {
  state: () => ({
    contacts: [] as Contact[],
    selectedContactId: null as string | null,
    loading: false,
    error: null as string | null,
    // Métricas de não-lidas fornecidas pelo backend (pode ser null se não carregado)
    unreadConversations: null as number | null,
    unreadMessages: null as number | null,
    // ID do setInterval para polling de não-lidas (número no browser)
    unreadPollingId: null as number | null,
  }),

  getters: {
    selectedContact: (state) => {
      if (!state.selectedContactId) return null;
      return state.contacts.find(c => c.id === state.selectedContactId) || null;
    },

    sortedContacts: (state) => {
      return [...state.contacts].sort((a, b) => {
        // Online primeiro
        if (a.online !== b.online) return a.online ? -1 : 1;
        // Depois por última mensagem
        return (b.lastMessageTime || 0) - (a.lastMessageTime || 0);
      });
    },

    totalUnread: (state) => {
      return state.contacts.reduce((sum, c) => sum + c.unreadCount, 0);
    },

    // Prefer server-provided unread conversations count when disponível; fallback para soma local
    unreadConversationsDisplay: (state) => {
      return state.unreadConversations !== null ? state.unreadConversations : state.contacts.reduce((sum, c) => sum + (c.unreadCount > 0 ? 1 : 0), 0);
    },
  },

  actions: {
    async loadContacts() {
      this.loading = true;
      this.error = null;

      try {
        const authStore = useAuthStore();
        const headers: Record<string, string> = {};
        if (authStore.token) headers.Authorization = `Bearer ${authStore.token}`;

        console.log('🔄 Carregando contatos de:', `${API_URL}/contacts/`);
        const res = await fetch(`${API_URL}/contacts/`, {
          redirect: 'follow',
          headers
        });
        console.log('📡 Resposta:', res.status, res.ok);
        if (!res.ok) throw new Error('Falha ao carregar contatos');

        this.contacts = await res.json();
        console.log(`✅ ${this.contacts.length} contatos carregados:`, this.contacts);
      } catch (error: any) {
        this.error = error.message;
        console.error('❌ Erro ao carregar contatos:', error);
      } finally {
        this.loading = false;
      }
    },

    // Cria um contato externo
    async createContact(payload: { name?: string; email?: string; phone?: string }) {
      try {
        const authStore = useAuthStore();
        const headers: Record<string, string> = { 'Content-Type': 'application/json' };
        if (authStore.token) headers.Authorization = `Bearer ${authStore.token}`;

        const res = await fetch(`${API_URL}/contacts/`, {
          method: 'POST',
          headers,
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Falha ao criar contato');
        const data = await res.json();
        // Recarrega lista após criar
        await this.loadContacts();
        return data
      } catch (error: any) {
        console.error('❌ Erro ao criar contato:', error);
        throw error;
      }
    },

    // Busca no backend o total de conversas e mensagens não-lidas
    async fetchUnreadCounts() {
      try {
        const authStore = useAuthStore();
        const headers: Record<string, string> = {};
        if (authStore.token) headers.Authorization = `Bearer ${authStore.token}`;

        const res = await fetch(`${API_URL}/contacts/unread-count`, { headers });
        if (!res.ok) throw new Error('Falha ao buscar contadores de não-lidas');

        const data = await res.json();
        // API retorna: { unreadConversations: number, unreadMessages: number }
        this.unreadConversations = Number(data.unreadConversations ?? null);
        this.unreadMessages = Number(data.unreadMessages ?? null);
      } catch (error) {
        console.warn('❌ Não foi possível buscar unread counts:', error);
        // Não falha na UI — apenas mantemos as métricas locais
      }
    },

    // Inicia polling periódico para atualizar as métricas de não-lidas.
    startUnreadPolling(intervalMs = 30000) {
      // Evita múltiplos timers
      if (this.unreadPollingId) return;
      // Chama imediatamente (não bloquear a UI se falhar)
      this.fetchUnreadCounts().catch(() => {});

      const id = window.setInterval(() => {
        this.fetchUnreadCounts().catch(() => {});
      }, intervalMs);

      this.unreadPollingId = Number(id);
    },

    // Para o polling
    stopUnreadPolling() {
      if (this.unreadPollingId) {
        clearInterval(this.unreadPollingId);
        this.unreadPollingId = null;
      }
    },

    selectContact(contactId: string) {
      this.selectedContactId = contactId;
      console.log('📞 Contato selecionado:', contactId);
    },

    unselectContact() {
      this.selectedContactId = null;
    },

    updateContactLastMessage(contactId: string, message: string, timestamp: number) {
      const contact = this.contacts.find(c => c.id === contactId);
      if (contact) {
        contact.lastMessage = message;
        contact.lastMessageTime = timestamp;
      }
    },

    incrementUnread(contactId: string) {
      console.log('🔔 incrementUnread chamado para:', contactId);
      console.log('📋 Contatos disponíveis:', this.contacts.map(c => ({ id: c.id, name: c.name })));
      let contact = this.contacts.find(c => c.id === contactId);
      // Fallback: algumas mensagens chegam com contactId invertido; tenta pelo userId do contato
      if (!contact) {
        contact = this.contacts.find(c => c.id === contactId);
      }
      if (contact) {
        contact.unreadCount++;
        console.log('✅ Unread incrementado:', contact.name, '→', contact.unreadCount);
      } else {
        console.warn('⚠️ Contato não encontrado na lista:', contactId);
      }
    },

    async markContactRead(contactId: string) {
      const contact = this.contacts.find(c => c.id === contactId);
      if (contact) {
        contact.unreadCount = 0;

        try {
          const authStore = useAuthStore();
          const headers: Record<string, string> = {};
          if (authStore.token) headers.Authorization = `Bearer ${authStore.token}`;

          await fetch(`${API_URL}/contacts/${contactId}/mark-read`, {
            method: 'POST',
            headers
          });
        } catch (error) {
          console.error('❌ Erro ao marcar como lido:', error);
        }
      }
    },

    setOnlineStatus(contactId: string, online: boolean) {
      const contact = this.contacts.find(c => c.id === contactId);
      if (contact) {
        contact.online = online;
      }
    },
  },
});
