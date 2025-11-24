<template>
  <div class="guru-commands-bar" v-if="modelValue">
    <div class="guru-commands-content">
      <div class="guru-commands-header">
        <v-icon size="small" color="teal-darken-3" class="mr-1">mdi-robot-happy</v-icon>
        <span class="guru-commands-title">Comandos do Guru</span>
      </div>

      <div class="chips-row">
        <v-chip
          size="small"
          color="teal-darken-1"
          variant="flat"
          prepend-icon="mdi-broom"
          class="mr-2 mb-2"
          @click="onCommand('/limpar')"
        >
          /limpar
        </v-chip>
        <v-chip
          size="small"
          color="purple-darken-1"
          variant="flat"
          prepend-icon="mdi-view-list"
          class="mr-2 mb-2"
          @click="onCommand('/ajuda')"
        >
          /ajuda
        </v-chip>
        <v-chip
          size="small"
          color="indigo-darken-1"
          variant="flat"
          prepend-icon="mdi-clipboard-text"
          class="mr-2 mb-2"
          @click="onCommand('/resumo')"
        >
          /resumo
        </v-chip>
        <v-chip
          size="small"
          color="blue-darken-3"
          variant="flat"
          prepend-icon="mdi-chart-box"
          class="mr-2 mb-2"
          @click="onCommand('/contexto')"
        >
          /contexto
        </v-chip>
      </div>

      <v-divider class="my-2"></v-divider>

      <div class="guru-commands-header mt-2">
        <v-icon size="small" color="purple-darken-2" class="mr-1">mdi-account-group</v-icon>
        <span class="guru-commands-title">Agentes Especializados:</span>
      </div>

      <div class="chips-row">
        <v-chip
          size="small"
          color="deep-purple-darken-1"
          variant="flat"
          prepend-icon="mdi-scale-balance"
          class="mr-2 mb-2"
          @click="onCommand('@advogado ')"
        >
          @advogado ⚖️
        </v-chip>
        <v-chip
          size="small"
          color="blue-grey-darken-1"
          variant="flat"
          prepend-icon="mdi-briefcase-account"
          class="mr-2 mb-2"
          @click="onCommand('@vendedor ')"
        >
          @vendedor 💼
        </v-chip>
        <v-chip
          size="small"
          color="red-darken-1"
          variant="flat"
          prepend-icon="mdi-hospital-box"
          class="mr-2 mb-2"
          @click="onCommand('@medico ')"
        >
          @medico 🩺
        </v-chip>
        <v-chip
          size="small"
          color="green-darken-1"
          variant="flat"
          prepend-icon="mdi-meditation"
          class="mr-2 mb-2"
          @click="onCommand('@psicologo ')"
        >
          @psicologo 🧘
        </v-chip>
        <v-chip
          size="small"
          color="amber-darken-2"
          variant="flat"
          prepend-icon="mdi-robot"
          class="mr-2 mb-2"
          @click="onCommand('/agentes')"
        >
          /agentes
        </v-chip>
      </div>

      <v-btn
        icon="mdi-close"
        size="x-small"
        variant="text"
        color="grey-darken-2"
        class="ml-auto close-btn"
        @click="$emit('update:modelValue', false)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{
  modelValue: boolean;
}>();

const emit = defineEmits<{
  (e: 'update:modelValue', val: boolean): void;
  (e: 'command', cmd: string): void;
}>();

function onCommand(cmd: string) {
  emit('command', cmd);
}
</script>

<style scoped>
.guru-commands-bar {
  background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
  border-bottom: 1px solid #4dd0e1;
  padding: 8px 10px;
  overflow-x: auto;
  overflow-y: hidden;
}

.guru-commands-content {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 6px 4px;
  width: 100%;
}

.guru-commands-header {
  display: flex;
  align-items: center;
  width: 100%;
  margin-bottom: 6px;
  font-weight: 600;
  font-size: 12px;
  color: #00695c;
  white-space: nowrap;
}

.guru-commands-title {
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.chips-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px 4px;
  width: 100%;
}

.guru-commands-bar .v-chip {
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
  font-size: 11px;
  white-space: nowrap;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.12);
  height: 30px;
  padding: 0 10px;
}

.close-btn {
  margin-left: auto;
  margin-top: 4px;
}

@media (max-width: 599px) {
  .guru-commands-bar {
    padding: 6px 8px;
  }
  
  .guru-commands-header {
    font-size: 10px;
  }
  
  .guru-commands-bar .v-chip {
    font-size: 10.5px;
    height: 26px;
    padding: 0 8px;
  }
}
</style>
