import { ref, nextTick } from 'vue';

export function useScrollToBottom() {
  const containerRef = ref<HTMLElement | null>(null);

  /**
   * Rola o container até o final
   * @param smooth - Se true, rola suavemente. Default: false para melhor performance
   * 
   * Performance note: smooth=false é recomendado para scroll automático em 
   * alta frequência (ex: mensagens chegando rapidamente), enquanto smooth=true 
   * é melhor para interações do usuário (ex: botão "ir para o final")
   */
  async function scrollToBottom(smooth = false) {
    await nextTick();
    if (containerRef.value) {
      containerRef.value.scrollTo({
        top: containerRef.value.scrollHeight,
        behavior: smooth ? 'smooth' : 'auto',
      });
    }
  }

  return {
    containerRef,
    scrollToBottom,
  };
}