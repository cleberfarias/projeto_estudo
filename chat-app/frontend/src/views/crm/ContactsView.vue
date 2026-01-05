<template>
  <div class="contacts-view">
    <div class="contacts-view__header">
      <h1 class="text-h4">Contatos</h1>
      <v-btn color="primary" prepend-icon="mdi-plus" @click="showCreateDialog = true">
        Novo Contato
      </v-btn>

      <v-dialog v-model="showCreateDialog" max-width="480">
        <v-card>
          <v-card-title>Novo Contato</v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="newContact.name" label="Nome" required />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="newContact.email" label="Email" />
              </v-col>
              <v-col cols="12" md="6">
                <v-text-field v-model="newContact.phone" label="Telefone" />
              </v-col>
            </v-row>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn variant="text" @click="showCreateDialog = false">Cancelar</v-btn>
            <v-btn color="primary" @click="onCreateContact" :loading="creating">Criar</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>

      <!-- Snackbar para feedback de criação -->
      <v-snackbar v-model="showSnackbar" :color="snackbarColor" timeout="3000" location="top">
        {{ snackbarText }}
      </v-snackbar>
    </div>

    <div class="contacts-view__content">
      <!-- Barra de busca e filtros -->
      <v-card class="mb-4" elevation="0" variant="outlined">
        <v-card-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="searchQuery"
                prepend-inner-icon="mdi-magnify"
                label="Buscar contatos"
                variant="outlined"
                density="compact"
                hide-details
                clearable
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="filterStatus"
                :items="statusOptions"
                label="Status"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
            <v-col cols="12" md="3">
              <v-select
                v-model="filterSegment"
                :items="segmentOptions"
                label="Segmento"
                variant="outlined"
                density="compact"
                hide-details
              />
            </v-col>
          </v-row>
        </v-card-text>
      </v-card>

      <!-- Lista de contatos -->
      <v-card elevation="0" variant="outlined">
        <v-data-table
          :headers="headers"
          :items="contacts"
          :search="searchQuery"
          :loading="loading"
          class="contacts-table"
        >
          <template #item.name="{ item }">
            <div class="d-flex align-center gap-2">
              <v-avatar :color="item.avatarColor" size="32">
                <span class="text-white">{{ getInitials(item.name) }}</span>
              </v-avatar>
              <div>
                <div class="font-weight-medium">{{ item.name }}</div>
                <div class="text-caption text-grey">{{ item.email }}</div>
              </div>
            </div>
          </template>

          <template #item.status="{ item }">
            <v-chip :color="getStatusColor(item.status)" size="small" variant="flat">
              {{ item.status }}
            </v-chip>
          </template>

          <template #item.actions="{ item: _item }">
            <v-btn icon="mdi-pencil" size="small" variant="text" />
            <v-btn icon="mdi-eye" size="small" variant="text" />
            <v-btn icon="mdi-delete" size="small" variant="text" color="error" />
          </template>
        </v-data-table>
      </v-card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useContactsStore } from '@/stores/contacts'

// Estado
const searchQuery = ref('')
const filterStatus = ref('Todos')
const filterSegment = ref('Todos')

// Usa store de contatos
const contactsStore = useContactsStore()

const loading = computed(() => contactsStore.loading)

onMounted(() => {
  contactsStore.loadContacts()
})

// Opções de filtro
const statusOptions = ['Todos', 'Ativo', 'Inativo', 'Lead', 'Cliente']
const segmentOptions = ['Todos', 'Varejo', 'Atacado', 'Serviços', 'Indústria']

// Headers da tabela
const headers = [
  { title: 'Nome', key: 'name', sortable: true },
  { title: 'Telefone', key: 'phone', sortable: true },
  { title: 'Empresa', key: 'company', sortable: true },
  { title: 'Status', key: 'status', sortable: true },
  { title: 'Última interação', key: 'lastInteraction', sortable: true },
  { title: 'Ações', key: 'actions', sortable: false, align: 'end' as const },
]

// Dados obtidos da API (mapeia formato do backend para a tabela)
const contacts = computed(() => 
  contactsStore.sortedContacts.map(c => ({
    id: c.id,
    name: c.name,
    email: c.email,
    phone: (c as any).phone || '',
    company: '',
    status: '',
    lastInteraction: c.lastMessage || '',
    avatarColor: null,
  }))
)

// Helpers
const getInitials = (name: string) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
}

const getStatusColor = (status: string) => {
  const colors: Record<string, string> = {
    'Cliente': 'success',
    'Lead': 'warning',
    'Ativo': 'info',
    'Inativo': 'grey',
  }
  return colors[status] || 'grey'
}

// UI: criação de contato
const showCreateDialog = ref(false)
const creating = ref(false)
const newContact = ref({ name: '', email: '', phone: '' })

// Snackbar
const showSnackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const onCreateContact = async () => {
  if (!newContact.value.name) return
  try {
    creating.value = true
    await contactsStore.createContact({
      name: newContact.value.name,
      email: newContact.value.email || undefined,
      phone: newContact.value.phone || undefined
    })

    // feedback ao usuário
    snackbarText.value = `Contato ${newContact.value.name} criado com sucesso!`
    snackbarColor.value = 'success'
    showSnackbar.value = true

    showCreateDialog.value = false
    newContact.value = { name: '', email: '', phone: '' }
  } catch (err) {
    // notifica erro
    snackbarText.value = 'Erro ao criar contato'
    snackbarColor.value = 'error'
    showSnackbar.value = true

    console.error('Erro ao criar contato:', err)
    throw err
  } finally {
    creating.value = false
  }
}
</script>

<style scoped lang="scss">
@import '@/design-system/styles/foundations.scss';
@import '@/design-system/styles/crm-mixins.scss';

.contacts-view {
  @include crm-page-padding;
  max-width: 1400px;
  margin: 0 auto;
  
  &__header {
    @include crm-page-header;
  }

  &__content {
    width: 100%;
  }
}

.contacts-table {
  :deep(.v-data-table__td) {
    padding: var(--ds-spacing-md) var(--ds-spacing-lg);
  }
}
</style>
