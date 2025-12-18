<template>
  <div class="analytics-view">
    <div class="analytics-view__header">
      <h1 class="text-h4">Analytics</h1>
      <v-btn-group>
        <v-btn prepend-icon="mdi-download" variant="outlined">
          Exportar
        </v-btn>
        <v-btn prepend-icon="mdi-cog" variant="outlined">
          Configurar
        </v-btn>
      </v-btn-group>
    </div>

    <!-- Period Selector -->
    <v-card class="mb-6" elevation="0" variant="outlined">
      <v-card-text>
        <v-row align="center">
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedPeriod"
              :items="['Hoje', 'Últimos 7 dias', 'Últimos 30 dias', 'Últimos 90 dias', 'Este ano']"
              label="Período"
              variant="outlined"
              density="compact"
              hide-details
            />
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedMetric"
              :items="['Todas as métricas', 'Atendimento', 'Vendas', 'Marketing', 'Suporte']"
              label="Categoria"
              variant="outlined"
              density="compact"
              hide-details
            />
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>

    <!-- KPIs principais -->
    <v-row class="mb-6">
      <v-col v-for="kpi in kpis" :key="kpi.title" cols="12" sm="6" md="3">
        <v-card elevation="2" :color="kpi.color" dark>
          <v-card-text>
            <div class="d-flex align-center justify-space-between">
              <div>
                <p class="text-caption mb-1">{{ kpi.title }}</p>
                <h2 class="text-h4 font-weight-bold">{{ kpi.value }}</h2>
              </div>
              <v-icon :icon="kpi.icon" size="48" class="opacity-50" />
            </div>
            <v-divider class="my-2 opacity-30" />
            <div class="d-flex align-center">
              <v-icon :icon="kpi.trend > 0 ? 'mdi-trending-up' : 'mdi-trending-down'" size="16" class="mr-1" />
              <span class="text-caption">{{ kpi.trend > 0 ? '+' : '' }}{{ kpi.trend }}% vs período anterior</span>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Charts -->
    <v-row class="mb-6">
      <v-col cols="12" md="8">
        <v-card elevation="2">
          <v-card-title>Atendimentos por Dia</v-card-title>
          <v-card-text>
            <div class="chart-placeholder">
              <v-icon icon="mdi-chart-line" size="64" color="grey-lighten-2" />
              <p class="text-grey mt-4">Gráfico de linha - Integrar biblioteca de charts</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="4">
        <v-card elevation="2">
          <v-card-title>Canais de Atendimento</v-card-title>
          <v-card-text>
            <div class="chart-placeholder">
              <v-icon icon="mdi-chart-donut" size="64" color="grey-lighten-2" />
              <p class="text-grey mt-4">Gráfico de pizza</p>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Tabelas de dados -->
    <v-row>
      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Top Atendentes</v-card-title>
          <v-list>
            <v-list-item
              v-for="agent in topAgents"
              :key="agent.name"
              :subtitle="`${agent.chats} atendimentos`"
            >
              <template #prepend>
                <v-avatar :color="agent.color">
                  <span>{{ getInitials(agent.name) }}</span>
                </v-avatar>
              </template>
              <v-list-item-title>{{ agent.name }}</v-list-item-title>
              <template #append>
                <v-chip color="success" size="small" variant="flat">
                  {{ agent.satisfaction }}% satisfação
                </v-chip>
              </template>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card elevation="2">
          <v-card-title>Horários de Pico</v-card-title>
          <v-card-text>
            <div v-for="hour in peakHours" :key="hour.time" class="mb-3">
              <div class="d-flex justify-space-between mb-1">
                <span class="font-weight-medium">{{ hour.time }}</span>
                <span class="text-grey">{{ hour.count }} atendimentos</span>
              </div>
              <v-progress-linear
                :model-value="hour.percentage"
                color="primary"
                height="8"
                rounded
              />
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const selectedPeriod = ref('Últimos 30 dias')
const selectedMetric = ref('Todas as métricas')

const kpis = ref([
  { title: 'Total Atendimentos', value: '3.847', trend: 23, icon: 'mdi-message-text', color: 'primary' },
  { title: 'Tempo Médio Resposta', value: '2m 34s', trend: -12, icon: 'mdi-clock-fast', color: 'success' },
  { title: 'Taxa Satisfação', value: '94%', trend: 5, icon: 'mdi-heart', color: 'error' },
  { title: 'Tickets Resolvidos', value: '98%', trend: 8, icon: 'mdi-check-circle', color: 'info' },
])

const topAgents = ref([
  { name: 'Maria Silva', chats: 234, satisfaction: 98, color: 'primary' },
  { name: 'João Santos', chats: 198, satisfaction: 96, color: 'success' },
  { name: 'Ana Costa', chats: 187, satisfaction: 95, color: 'info' },
  { name: 'Pedro Lima', chats: 156, satisfaction: 93, color: 'warning' },
])

const peakHours = ref([
  { time: '09:00 - 10:00', count: 342, percentage: 85 },
  { time: '10:00 - 11:00', count: 398, percentage: 99 },
  { time: '14:00 - 15:00', count: 378, percentage: 94 },
  { time: '15:00 - 16:00', count: 312, percentage: 78 },
])

const getInitials = (name: string) => {
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
}
</script>

<style scoped lang="scss">
@import '@/design-system/styles/foundations.scss';
@import '@/design-system/styles/crm-mixins.scss';

.analytics-view {
  @include crm-page-padding;
  max-width: 1400px;
  margin: 0 auto;
  
  &__header {
    @include crm-page-header;
  }
}

.chart-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 300px;
  background-color: var(--ds-color-input-background);
  border-radius: var(--ds-radius-md);
}
</style>
