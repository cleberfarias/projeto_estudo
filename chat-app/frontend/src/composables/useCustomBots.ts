import { ref } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

export interface CustomBotPayload {
  name: string;
  emoji: string;
  prompt: string;
  specialties: string[];
  openaiApiKey: string;
  openaiAccount?: string;
}

export interface CustomBotSummary {
  name: string;
  emoji: string;
  key: string;
  specialties: string[];
  createdAt?: string;
}

// Estado compartilhado (singleton) - todos os componentes veem os mesmos dados
const loading = ref(false);
const error = ref<string | null>(null);
const bots = ref<CustomBotSummary[]>([]);

export function useCustomBots() {

  const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:3000';

  const authHeaders = () => {
    const authStore = useAuthStore();
    return {
      Authorization: `Bearer ${authStore.token || ''}`
    };
  };

  const listBots = async (): Promise<CustomBotSummary[]> => {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await axios.get(`${apiBase}/custom-bots`, {
        headers: authHeaders()
      });
      return data?.bots || [];
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Erro ao carregar bots';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const refreshBots = async () => {
    try {
      const result = await listBots();
      bots.value = result;
    } catch (err) {
      console.error('Erro ao atualizar bots:', err);
      bots.value = [];
    }
  };

  const createBot = async (payload: CustomBotPayload): Promise<CustomBotSummary> => {
    loading.value = true;
    error.value = null;
    try {
      const { data } = await axios.post(
        `${apiBase}/custom-bots`,
        {
          name: payload.name,
          emoji: payload.emoji,
          prompt: payload.prompt,
          specialties: payload.specialties,
          openaiApiKey: payload.openaiApiKey,
          openaiAccount: payload.openaiAccount
        },
        { headers: { ...authHeaders(), 'Content-Type': 'application/json' } }
      );
      
      // Adiciona o bot criado à lista automaticamente
      const newBot = data?.bot;
      if (newBot) {
        bots.value.push(newBot);
      }
      
      return newBot;
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Erro ao criar bot';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  const deleteBot = async (botKey: string): Promise<void> => {
    loading.value = true;
    error.value = null;
    try {
      await axios.delete(`${apiBase}/custom-bots/${botKey}`, {
        headers: authHeaders()
      });
      
      // Remove o bot da lista automaticamente
      bots.value = bots.value.filter(bot => bot.key !== botKey);
    } catch (err: any) {
      error.value = err?.response?.data?.detail || 'Erro ao remover bot';
      throw err;
    } finally {
      loading.value = false;
    }
  };

  return {
    bots,
    loading,
    error,
    listBots,
    refreshBots,
    createBot,
    deleteBot
  };
}
