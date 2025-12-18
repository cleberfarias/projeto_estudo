<template>
  <div class="crm-view">
    <div class="crm-view__header">
      <h1 class="text-h4">CRM Dashboard</h1>
      <v-btn-group>
        <v-btn prepend-icon="mdi-calendar-today" variant="outlined">
          Hoje
        </v-btn>
        <v-btn prepend-icon="mdi-calendar-week" variant="outlined">
          Esta semana
        </v-btn>
        <v-btn prepend-icon="mdi-calendar-month" variant="outlined">
          Este mês
        </v-btn>
      </v-btn-group>
    </div>

    <!-- Cards de métricas -->
    <v-row class="mb-6">
      <v-col v-for="metric in metrics" :key="metric.title" cols="12" sm="6" md="3">
        <v-card elevation="2">
          <v-card-text>
            <div class="d-flex justify-space-between align-center">
              <div>
                <p class="text-caption text-grey mb-1">{{ metric.title }}</p>
                <h2 class="text-h4 font-weight-bold">{{ metric.value }}</h2>
                <v-chip
                  :color="metric.trend > 0 ? 'success' : 'error'"
                  size="x-small"
                  class="mt-2"
                  variant="flat"
                >
                  <v-icon :icon="metric.trend > 0 ? 'mdi-arrow-up' : 'mdi-arrow-down'" size="14" start />
                  {{ Math.abs(metric.trend) }}%
                </v-chip>
              </div>
              <v-avatar :color="metric.color" size="56">
                <v-icon :icon="metric.icon" size="28" color="white" />
              </v-avatar>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Funil de vendas -->
    <v-row class="mb-6">
      <v-col cols="12" md="8">
        <v-card elevation="2">
          <v-card-title>Funil de Vendas</v-card-title>
          <v-card-text>
            <div v-for="(stage, index) in salesFunnel" :key="stage.name" class="funnel-stage mb-4">
              <div class="d-flex justify-space-between align-center mb-2">
                <span class="font-weight-medium">{{ stage.name }}</span>
                <span class="text-grey">{{ stage.count }} leads - R$ {{ formatCurrency(stage.value) }}</span>
              </div>
              <v-progress-linear
                :model-value="stage.percentage"
                :color="getFunnelColor(index)"
                height="24"
                rounded
              >
                <strong>{{ stage.percentage }}%</strong>
              </v-progress-linear>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="2" class="mb-4">
          <v-card-title>Taxa de Conversão</v-card-title>
          <v-card-text class="text-center">
            <div class="conversion-rate">
              <v-progress-circular
                :model-value="conversionRate"
                :size="120"
                :width="12"
                color="success"
              >
                <span class="text-h4 font-weight-bold">{{ conversionRate }}%</span>
              </v-progress-circular>
            </div>
            <p class="text-body-2 text-grey mt-4">
              Meta: 25%
            </p>
          </v-card-text>
        </v-card>

        <v-card elevation="2">
          <v-card-title>Ticket Médio</v-card-title>
          <v-card-text class="text-center">
            <h2 class="text-h3 font-weight-bold text-success">
              R$ {{ formatCurrency(averageTicket) }}
            </h2>
            <p class="text-body-2 text-grey mt-2">
              +12% vs mês anterior
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Últimas atividades -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Oportunidades Recentes</v-card-title>
          <v-list>
            <v-list-item
              v-for="opportunity in recentOpportunities"
              :key="opportunity.id"
              :subtitle="opportunity.company"
            >
              <template #prepend>
                <v-avatar :color="opportunity.color">
                  <v-icon icon="mdi-currency-usd" />
                </v-avatar>
              </template>
              <v-list-item-title>{{ opportunity.title }}</v-list-item-title>
              <template #append>
                <v-chip :color="opportunity.stageColor" size="small" variant="flat">
                  {{ opportunity.stage }}
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Tarefas Pendentes</v-card-title>
          <v-list>
            <v-list-item
              v-for="task in pendingTasks"
              :key="task.id"
              :subtitle="task.dueDate"
            >
              <template #prepend>
                <v-checkbox-btn />
              </template>
              <v-list-item-title>{{ task.title }}</v-list-item-title>
              <template #append>
                <v-chip :color="task.priority === 'Alta' ? 'error' : 'warning'" size="small" variant="flat">
                  {{ task.priority }}
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Métricas principais
const metrics = ref([
  { title: 'Leads Ativos', value: '248', trend: 12, icon: 'mdi-account-multiple', color: 'primary' },
  { title: 'Negócios Abertos', value: '42', trend: 8, icon: 'mdi-handshake', color: 'success' },
  { title: 'Receita (mês)', value: 'R$ 128k', trend: -5, icon: 'mdi-currency-usd', color: 'info' },
  { title: 'Taxa Conversão', value: '18%', trend: 3, icon: 'mdi-chart-line', color: 'warning' },
])

// Funil de vendas
const salesFunnel = ref([
  { name: 'Prospecção', count: 248, value: 620000, percentage: 100 },
  { name: 'Qualificação', count: 124, value: 372000, percentage: 50 },
  { name: 'Proposta', count: 62, value: 217000, percentage: 25 },
  { name: 'Negociação', count: 31, value: 124000, percentage: 12.5 },
  { name: 'Fechamento', count: 18, value: 90000, percentage: 7.3 },
])

const conversionRate = ref(18)
const averageTicket = ref(5000)

// Oportunidades recentes
const recentOpportunities = ref([
  { id: 1, title: 'Implementação Sistema ERP', company: 'Tech Corp', stage: 'Proposta', stageColor: 'warning', color: 'primary' },
  { id: 2, title: 'Consultoria Digital', company: 'StartupXYZ', stage: 'Negociação', stageColor: 'info', color: 'success' },
  { id: 3, title: 'Licenças Software', company: 'Indústria ABC', stage: 'Qualificação', stageColor: 'grey', color: 'warning' },
])

// Tarefas pendentes
const pendingTasks = ref([
  { id: 1, title: 'Follow-up com João Silva', dueDate: 'Hoje, 15:00', priority: 'Alta' },
  { id: 2, title: 'Enviar proposta para Maria Santos', dueDate: 'Amanhã, 10:00', priority: 'Alta' },
  { id: 3, title: 'Reunião de alinhamento - Tech Corp', dueDate: 'Sex, 14:00', priority: 'Média' },
])

// Helpers
const formatCurrency = (value: number) => {
  return (value / 1000).toFixed(0) + 'k'
}

const getFunnelColor = (index: number) => {
  const colors = ['primary', 'info', 'success', 'warning', 'error']
  return colors[index] || 'grey'
}
</script>

<style scoped lang="scss">
@import '@/design-system/styles/foundations.scss';
@import '@/design-system/styles/crm-mixins.scss';

.crm-view {
  @include crm-page-padding;
  max-width: 1400px;
  margin: 0 auto;
  
  &__header {
    @include crm-page-header;
  }
}

.funnel-stage {
  &:last-child {
    margin-bottom: 0 !important;
  }
}

.conversion-rate {
  padding: var(--ds-spacing-xxl) 0;
}
</style>
