<template>
  <div class="agent-pane">
    <div class="agent-pane-header">
      <div class="agent-title">
        <span class="agent-emoji" v-if="emoji">{{ emoji }}</span>
        <strong>{{ title }}</strong>
      </div>
      <div class="agent-actions">
        <v-btn icon size="small" variant="text" @click="close">
          <v-icon>mdi-close</v-icon>
        </v-btn>
      </div>
    </div>

    <div class="agent-messages" ref="messagesEl">
      <div v-for="(m, i) in messages" :key="i" class="agent-message">
        <div class="agent-msg-author">{{ m.author }}</div>
        <div class="agent-msg-text">{{ m.text }}</div>
      </div>
    </div>

    <div class="agent-input">
      <v-text-field
        v-model="input"
        :placeholder="`Enviar mensagem para ${title}`"
        @keyup.enter="send"
        dense
        hide-details
      />
      <v-btn :disabled="!input.trim()" @click="send">Enviar</v-btn>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useChatStore } from '@/stores/chat';

interface Props {
  agentKey: string;
  title: string;
  emoji?: string;
}
const props = defineProps<Props>();
const emit = defineEmits(['close']);

const chatStore = useChatStore();
const input = ref('');
const messages = ref<Array<{ author: string; text: string }>>([]);
const messagesEl = ref<HTMLElement | null>(null);

function close() {
  emit('close', props.agentKey);
}

function send() {
  const text = input.value.trim();
  if (!text || !chatStore.socket) return;

  // Envia para o backend usando menção ao agente (servidor reconhece e responde)
  const payload = {
    author: chatStore.currentUser,
    text: `@${props.agentKey} ${text}`.trim(),
    type: 'text',
    tempId: `agent_${Date.now()}_${Math.random()}`
  };

  try {
    chatStore.socket.emit('chat:send', payload);
    // Adiciona mensagem local (do usuário) na lista do painel
    messages.value.push({ author: chatStore.currentUser, text });
    input.value = '';
    nextTick(() => {
      if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
    });
  } catch (e) {
    console.error('Erro ao enviar mensagem ao agente:', e);
  }
}

function onNewMessage(msg: any) {
  // Filtra mensagens do agente pelo author contendo o nome do agente
  if (!msg || !msg.author) return;
  const agentName = props.title;
  if (String(msg.author).includes(agentName) || String(msg.author).toLowerCase().includes(props.agentKey.toLowerCase())) {
    messages.value.push({ author: msg.author, text: msg.text });
    nextTick(() => {
      if (messagesEl.value) messagesEl.value.scrollTop = messagesEl.value.scrollHeight;
    });
  }
}

onMounted(() => {
  if (chatStore.socket) {
    chatStore.socket.on('chat:new-message', onNewMessage);
  }
});

onBeforeUnmount(() => {
  if (chatStore.socket) {
    chatStore.socket.off('chat:new-message', onNewMessage);
  }
});
</script>

<style scoped>
.agent-pane {
  width: 360px;
  height: 72vh;
  background: white;
  border-left: 1px solid rgba(0,0,0,0.06);
  display: flex;
  flex-direction: column;
  box-shadow: -4px 0 12px rgba(0,0,0,0.06);
}
.agent-pane-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
}
.agent-title { display:flex; align-items:center; gap:8px }
.agent-emoji { font-size:18px }
.agent-messages { flex:1; overflow-y:auto; padding:12px }
.agent-message { margin-bottom:12px }
.agent-msg-author { font-weight:600; font-size:12px; color:#444 }
.agent-msg-text { margin-top:4px; font-size:14px }
.agent-input { display:flex; gap:8px; padding:8px; border-top:1px solid #f3f3f3 }
</style>