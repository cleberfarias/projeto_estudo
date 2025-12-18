<template>
  <div class="ds-chat-input">
    <!-- Modo de gravação ativo -->
    <div v-if="recording" class="ds-chat-input__form ds-chat-input__form--recording">
      <!-- Botão deletar/cancelar -->
      <v-btn
        icon="mdi-delete-outline"
        variant="text"
        size="small"
        class="recording-delete-btn"
        @click="$emit('cancel-recording')"
      />

      <!-- Conteúdo de gravação -->
      <div class="recording-content-inline">
        <!-- Indicador vermelho pulsante -->
        <div class="recording-dot-pulse"></div>
        
        <!-- Timer vermelho -->
        <span class="recording-time-inline">{{ recordingTime }}</span>
        
        <!-- Waveform animada -->
        <div class="recording-wave-inline">
          <div class="wave-bar-inline" v-for="i in 30" :key="i" :style="{ animationDelay: `${i * 0.02}s` }"></div>
        </div>
      </div>

      <!-- Botão enviar verde -->
      <v-btn
        icon="mdi-send"
        color="#25d366"
        size="40"
        elevation="0"
        class="recording-send-btn"
        @click="$emit('send-recording')"
      />
    </div>

    <!-- Modo normal -->
    <v-form v-else @submit.prevent="handleSubmit" class="ds-chat-input__form">
      <!-- Container dos ícones da esquerda -->
      <div class="ds-chat-input__left-icons">
        <slot name="attach-btn">
          <v-btn 
            icon="mdi-plus"
            variant="text" 
            color="grey-darken-1"
            size="small"
            class="ds-chat-input__icon-btn"
            :disabled="uploading"
          />
        </slot>

        <v-btn 
          icon="mdi-emoticon-outline" 
          variant="text" 
          color="grey-darken-1" 
          size="small"
          class="ds-chat-input__icon-btn"
          @click="$emit('emoji')"
        />
      </div>

      <!-- Campo de input com estilo WhatsApp -->
      <div class="ds-chat-input__input-wrapper">
        <v-text-field
          :model-value="modelValue"
          @update:model-value="$emit('update:modelValue', $event)"
          placeholder="Digite uma mensagem"
          variant="plain"
          density="compact"
          hide-details
          class="ds-chat-input__field"
          @keyup.enter.exact.prevent="handleEnterKey"
          :disabled="uploading"
        />
      </div>

      <!-- Botão microfone/enviar à direita -->
      <v-btn
        icon
        variant="text"
        :color="hasText ? colors.secondary : 'grey-darken-1'"
        size="small"
        class="ds-chat-input__action-btn"
        @click="handleSubmit"
        :disabled="uploading"
        :loading="uploading"
      >
        <v-icon>{{ hasText ? 'mdi-send' : 'mdi-microphone' }}</v-icon>

        <v-progress-circular
          v-if="uploading && uploadProgress > 0"
          :model-value="uploadProgress"
          :size="40"
          :width="3"
          color="white"
          class="ds-chat-input__progress"
        />
      </v-btn>
    </v-form>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';
import { colors } from '../../tokens';

interface Props {
  modelValue: string;
  uploading?: boolean;
  uploadProgress?: number;
  recording?: boolean;
  recordingTime?: string;
}

const props = withDefaults(defineProps<Props>(), {
  uploading: false,
  uploadProgress: 0,
  recording: false,
  recordingTime: '0:00'
});

const emit = defineEmits<{
  'update:modelValue': [value: string];
  'submit': [text: string];
  'typing': [isTyping: boolean];
  'emoji': [];
  'voice': [];
  'cancel-recording': [];
  'send-recording': [];
}>();

const hasText = computed(() => props.modelValue.trim().length > 0);
const typingTimeout = ref<number | null>(null);
const isTyping = ref(false);

watch(() => props.modelValue, (newValue) => {
  if (newValue && !isTyping.value) {
    isTyping.value = true;
    emit('typing', true);
  }

  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value);
  }

  typingTimeout.value = window.setTimeout(() => {
    if (isTyping.value) {
      isTyping.value = false;
      emit('typing', false);
    }
  }, 1000);

  if (!newValue && isTyping.value) {
    isTyping.value = false;
    emit('typing', false);
    if (typingTimeout.value) {
      clearTimeout(typingTimeout.value);
    }
  }
});

function handleEnterKey() {
  if (hasText.value && !props.uploading) {
    sendMessage();
  }
}

function handleSubmit() {
  if (hasText.value && !props.uploading) {
    sendMessage();
  } else if (!hasText.value && !props.uploading) {
    emit('voice');
  }
}

function sendMessage() {
  if (isTyping.value) {
    isTyping.value = false;
    emit('typing', false);
  }
  if (typingTimeout.value) {
    clearTimeout(typingTimeout.value);
  }

  emit('submit', props.modelValue);
  emit('update:modelValue', '');
}
</script>

<style scoped lang="scss" src="./DSChatInput.scss"></style>
