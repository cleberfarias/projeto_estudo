import { ref, onMounted, onBeforeUnmount } from 'vue';
import { io, Socket } from 'socket.io-client';
import type { Message } from '../types';
import { validateAndNormalizeMessage } from '../types/validation';

export function useChat(socketUrl: string) {
  const messages = ref<Message[]>([]);
  const isConnected = ref(false);
  const isTyping = ref(false);
  let socket: Socket | null = null;

  onMounted(() => {
    socket = io(socketUrl, {
      transports: ['websocket'],
    });

    socket.on('connect', () => {
      isConnected.value = true;
      console.log('✅ Conectado ao servidor');
    });

    socket.on('disconnect', () => {
      isConnected.value = false;
      console.log('❌ Desconectado do servidor');
    });

    socket.on('chat:new-message', (data: unknown) => {
      try {
        // Valida e normaliza a mensagem recebida
        const message = validateAndNormalizeMessage(data);
        
        console.log('📨 Mensagem válida recebida:', message);
        
        // Evita duplicação: só adiciona se a mensagem não existir
        const exists = messages.value.some(m => m.id === message.id);
        if (!exists) {
          messages.value.push(message);
        } else {
          console.log('⚠️  Mensagem duplicada ignorada:', message.id);
        }
      } catch (error) {
        console.error('❌ Erro ao processar mensagem:', error);
        // Não adiciona mensagem inválida ao array
        // Pode emitir evento de erro para UI se necessário
      }
    });

    socket.on('user:typing', (data: { userId: string; isTyping: boolean }) => {
      isTyping.value = data.isTyping;
    });
  });

  onBeforeUnmount(() => {
    socket?.disconnect();
  });

  function sendMessage(message: Omit<Message, 'id' | 'timestamp'>) {
    const msg: Message = {
      ...message,
      id: crypto.randomUUID(),
      timestamp: Date.now(),
    };
    
    console.log('📤 Enviando mensagem:', msg);
    socket?.emit('chat:new-message', msg);
    
    // Não adiciona localmente - vai receber de volta pelo socket
    // Isso evita duplicação e garante que a mensagem foi processada pelo servidor
  }

  function sendTypingStatus(typing: boolean) {
    socket?.emit('user:typing', typing);
  }

  return {
    messages,
    isConnected,
    isTyping,
    sendMessage,
    sendTypingStatus,
  };
}