<template>
  <div class="conversations-view">
    <div class="conversations-view__header">
      <h1 class="text-h4">Conversas</h1>
      <v-chip prepend-icon="mdi-message" color="primary" variant="flat">
        {{ totalUnread }} não lidas
      </v-chip>
    </div>

    <div class="conversations-view__content">
      <!-- Filtros -->
      <v-card class="mb-4" elevation="0" variant="outlined">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="4">
              <v-text-field
                v-model="searchQuery"
                prepend-inner-icon="mdi-magnify"
                label="Buscar conversas"
                variant="outlined"
                density="compact"
                hide-details
                clearable
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="filterType"
                :items="['Todas', 'WhatsApp', 'Telegram', 'Email', 'Chat']"
                label="Canal"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="4">
              <v-select
                v-model="filterStatus"
                :items="['Todas', 'Abertas', 'Aguardando resposta', 'Resolvidas', 'Arquivadas']"
                label="Status"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Lista de conversas -->
      <v-row>
        <v-col
          v-for="conversation in filteredConversations"
          :key="conversation.id"
          cols="12"
        >
          <v-card
            :class="['conversation-card', { 'conversation-card--unread': conversation.unread }]"
            elevation="0"
            variant="outlined"
            hover
          >
            <v-card-text class="d-flex align-center gap-4">
              <!-- Avatar -->
              <v-badge
                :model-value="conversation.unread > 0"
                :content="conversation.unread"
                color="success"
                overlap
              >
                <v-avatar :color="conversation.avatarColor" size="48">
                  <v-icon v-if="conversation.type === 'WhatsApp'" icon="mdi-whatsapp" />
                  <v-icon v-else-if="conversation.type === 'Telegram'" icon="mdi-telegram" />
                  <v-icon v-else-if="conversation.type === 'Email'" icon="mdi-email" />
                  <v-icon v-else icon="mdi-message" />
                </v-avatar>
              </v-badge>

              <!-- Conteúdo -->
              <div class="flex-grow-1">
                <div class="d-flex justify-space-between align-center mb-1">
                  <h3 class="text-subtitle-1 font-weight-bold">
                    {{ conversation.contact }}
                  </h3>
                  <span class="text-caption text-grey">{{ conversation.timestamp }}</span>
                </div>
                
                <p class="text-body-2 text-grey mb-2">
                  {{ conversation.lastMessage }}
                </p>

                <div class="d-flex gap-2">
                  <v-chip size="x-small" :color="getStatusColor(conversation.status)" variant="flat">
                    {{ conversation.status }}
                  </v-chip>
                  <v-chip size="x-small" variant="outlined">
                    {{ conversation.type }}
                  </v-chip>
                  <v-chip v-if="conversation.assignedTo" size="x-small" variant="outlined">
                    <v-icon icon="mdi-account" size="14" start />
                    {{ conversation.assignedTo }}
                  </v-chip>
                </div>
              </div>

              <!-- Ações -->
              <div class="conversation-card__actions">
                <v-btn icon="mdi-reply" size="small" variant="text" />
                <v-btn icon="mdi-archive-arrow-down" size="small" variant="text" />
                <v-btn icon="mdi-dots-vertical" size="small" variant="text" />
              </div>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

interface Conversation {
  id: number
  contact: string
  lastMessage: string
  timestamp: string
  type: string
  status: string
  assignedTo?: string
  unread: number
  avatarColor: string
}

// Estado
const searchQuery = ref('')
const filterType = ref('Todas')
const filterStatus = ref('Todas')

// Dados mockados
const conversations = ref<Conversation[]>([
  {
    id: 1,
    contact: 'João Silva',
    lastMessage: 'Obrigado pelo atendimento! Tudo resolvido.',
    timestamp: '10:30',
    type: 'WhatsApp',
    status: 'Resolvida',
    assignedTo: 'Maria',
    unread: 0,
    avatarColor: 'success',
  },
  {
    id: 2,
    contact: 'Maria Santos',
    lastMessage: 'Gostaria de saber mais sobre os planos disponíveis',
    timestamp: 'Ontem',
    type: 'Telegram',
    status: 'Aguardando resposta',
    assignedTo: 'Pedro',
    unread: 3,
    avatarColor: 'info',
  },
  {
    id: 3,
    contact: 'Pedro Costa',
    lastMessage: 'Quando vocês podem fazer a instalação?',
    timestamp: '2 dias atrás',
    type: 'WhatsApp',
    status: 'Aberta',
    unread: 1,
    avatarColor: 'warning',
  },
  {
    id: 4,
    contact: 'Ana Oliveira',
    lastMessage: 'Recebi o boleto, obrigada!',
    timestamp: '3 dias atrás',
    type: 'Email',
    status: 'Arquivada',
    assignedTo: 'Carlos',
    unread: 0,
    avatarColor: 'grey',
  },
])

// Computed
const filteredConversations = computed(() => {
  return conversations.value.filter(conv => {
    const matchesSearch = !searchQuery.value || 
      conv.contact.toLowerCase().includes(searchQuery.value.toLowerCase()) ||
      conv.lastMessage.toLowerCase().includes(searchQuery.value.toLowerCase())
    
    const matchesType = filterType.value === 'Todas' || conv.type === filterType.value
    const matchesStatus = filterStatus.value === 'Todas' || conv.status === filterStatus.value
    
    return matchesSearch && matchesType && matchesStatus
  })
})

const totalUnread = computed(() => {
  return conversations.value.reduce((sum, conv) => sum + conv.unread, 0)
})

// Helpers
const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'Aberta': 'error',
    'Aguardando resposta': 'warning',
    'Resolvida': 'success',
    'Arquivada': 'grey',
  }
  return colors[status] || 'grey'
}
</script>

<style scoped lang="scss">
@import '@/design-system/styles/foundations.scss';
@import '@/design-system/styles/crm-mixins.scss';

.conversations-view {
  @include crm-page-padding;
  max-width: 1200px;
  margin: 0 auto;
  
  &__header {
    @include crm-page-header;
  }

  &__content {
    width: 100%;
  }
}

.conversation-card {
  transition: all 0.2s;
  
  &--unread {
    border-left: var(--ds-spacing-xs) solid var(--ds-color-primary);
  }

  &:hover {
    transform: translateX(var(--ds-spacing-xs));
  }

  &__actions {
    display: flex;
    gap: var(--ds-spacing-xs);
    opacity: 0.7;
    
    &:hover {
      opacity: 1;
    }
  }
}
</style>
