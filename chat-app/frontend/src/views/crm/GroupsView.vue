<template>
  <div class="groups-view">
    <div class="groups-view__header">
      <h1 class="text-h4">Grupos</h1>
      <v-btn color="primary" prepend-icon="mdi-plus">
        Novo Grupo
      </v-btn>
    </div>

    <div class="groups-view__content">
      <v-row>
        <v-col
          v-for="group in groups"
          :key="group.id"
          cols="12"
          sm="6"
          md="4"
        >
          <v-card elevation="2" hover class="group-card">
            <v-card-text>
              <!-- Header do card -->
              <div class="d-flex justify-space-between align-center mb-3">
                <v-avatar :color="group.color" size="48">
                  <v-icon :icon="group.icon" size="28" color="white" />
                </v-avatar>
                <v-menu>
                  <template #activator="{ props }">
                    <v-btn icon="mdi-dots-vertical" size="small" variant="text" v-bind="props" />
                  </template>
                  <v-list>
                    <v-list-item prepend-icon="mdi-pencil" title="Editar" />
                    <v-list-item prepend-icon="mdi-account-multiple-plus" title="Adicionar membros" />
                    <v-list-item prepend-icon="mdi-delete" title="Excluir" />
                  </v-list>
                </v-menu>
              </div>

              <!-- Info do grupo -->
              <h3 class="text-h6 font-weight-bold mb-1">{{ group.name }}</h3>
              <p class="text-body-2 text-grey mb-3">{{ group.description }}</p>

              <!-- Estatísticas -->
              <div class="d-flex gap-4 mb-3">
                <div>
                  <v-icon icon="mdi-account-multiple" size="16" class="mr-1" />
                  <span class="text-caption">{{ group.members }} membros</span>
                </div>
                <div>
                  <v-icon icon="mdi-message" size="16" class="mr-1" />
                  <span class="text-caption">{{ group.messages }} msgs</span>
                </div>
              </div>

              <!-- Status -->
              <v-chip :color="group.active ? 'success' : 'grey'" size="small" variant="flat">
                {{ group.active ? 'Ativo' : 'Inativo' }}
              </v-chip>
            </v-card-text>

            <v-divider />

            <v-card-actions>
              <v-btn variant="text" prepend-icon="mdi-message">
                Abrir chat
              </v-btn>
              <v-spacer />
              <v-btn variant="text" icon="mdi-cog" size="small" />
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

interface Group {
  id: number
  name: string
  description: string
  members: number
  messages: number
  active: boolean
  icon: string
  color: string
}

const groups = ref<Group[]>([
  {
    id: 1,
    name: 'Suporte Técnico',
    description: 'Grupo para atendimento de suporte aos clientes',
    members: 24,
    messages: 1543,
    active: true,
    icon: 'mdi-headset',
    color: 'primary',
  },
  {
    id: 2,
    name: 'Vendas - Equipe A',
    description: 'Time de vendas região sul',
    members: 12,
    messages: 856,
    active: true,
    icon: 'mdi-cart',
    color: 'success',
  },
  {
    id: 3,
    name: 'Marketing',
    description: 'Campanhas e estratégias de marketing',
    members: 8,
    messages: 432,
    active: true,
    icon: 'mdi-bullhorn',
    color: 'warning',
  },
  {
    id: 4,
    name: 'Desenvolvimento',
    description: 'Equipe de desenvolvimento de produto',
    members: 15,
    messages: 2134,
    active: true,
    icon: 'mdi-code-braces',
    color: 'info',
  },
  {
    id: 5,
    name: 'VIP Clientes',
    description: 'Grupo exclusivo para clientes premium',
    members: 45,
    messages: 3421,
    active: true,
    icon: 'mdi-star',
    color: 'amber',
  },
  {
    id: 6,
    name: 'Pós-venda',
    description: 'Atendimento e acompanhamento pós-venda',
    members: 18,
    messages: 967,
    active: false,
    icon: 'mdi-account-check',
    color: 'grey',
  },
])
</script>

<style scoped lang="scss">
@import '@/design-system/styles/foundations.scss';
@import '@/design-system/styles/crm-mixins.scss';

.groups-view {
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

.group-card {
  @include crm-card;
  height: 100%;
}
</style>
