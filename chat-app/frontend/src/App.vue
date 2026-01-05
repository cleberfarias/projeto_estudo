<template>
  <v-app class="app-container">
    <!-- Navbar CRM -->
    <DSNavBar v-if="showNavBar" :items="navItems" :show-header="true" header-title="Chat CRM" />
    
    <!-- Main Content -->
    <v-main :class="{ 'with-navbar': showNavBar }">
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { computed, ref, onMounted, watch, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import { DSNavBar } from './design-system/components/DSNavBar'
import type { NavItem } from './design-system/components/DSNavBar'
import { useCustomBots } from './composables/useCustomBots'
import { useContactsStore } from '@/stores/contacts'

const route = useRoute()

// Define quando mostrar a navbar (não mostrar no login)
const showNavBar = computed(() => route.path !== '/login')

// Items do menu de navegação - versão estática primeiro para garantir que funcione
const navItems = ref<NavItem[]>([
  {
    id: 'crm',
    title: 'Dashboard',
    icon: 'view-dashboard',
    to: '/crm',
  },
  {
    id: 'chat',
    title: 'Conversas',
    icon: 'message-text',
    to: '/chat',
    // badge agora será atualizado dinamicamente a partir do store de contatos
  },
  {
    id: 'contatos',
    title: 'Contatos',
    icon: 'account-multiple',
    to: '/contatos',
  },
  {
    id: 'grupos',
    title: 'Grupos',
    icon: 'account-group',
    to: '/grupos',
  },
  {
    id: 'bots',
    title: 'Agentes',
    icon: 'robot',
    to: '/bots',
  },
  {
    id: 'analytics',
    title: 'Analytics',
    icon: 'chart-bar',
    to: '/analytics',
  },
  {
    id: 'relatorios',
    title: 'Relatórios',
    icon: 'file-document',
    to: '/relatorios',
  },
])

// Mantém o badge de Conversas sincronizado com o total de conversas não-lidas
const contactsStore = useContactsStore()
// Prefer server-provided unread conversations quando disponível
const unreadCount = computed(() => contactsStore.unreadConversationsDisplay)
watch(unreadCount, (val) => {
  const idx = navItems.value.findIndex(i => i.id === 'chat')
  if (idx !== -1) {
    const item = navItems.value[idx]!
    // Cap no badge em 99+
    const displayBadge = (val ?? 0) > 99 ? '99+' : ((val ?? 0) > 0 ? val : undefined)

    navItems.value[idx] = {
      ...item,
      // mostra número (ou '99+') no desktop; no mobile mostramos apenas um dot via 'badgeDotMobile'
      badge: displayBadge,
      badgeColor: (val ?? 0) > 0 ? 'error' : 'success',
      badgeDotMobile: (val ?? 0) > 0,
    }
  }
}, { immediate: true })

// Carrega agentes de forma assíncrona sem bloquear o menu
onMounted(async () => {
  try {
    const { bots, refreshBots } = useCustomBots()
    await refreshBots()

    // Inicia polling de unread counts ao montar a app (chama imediatamente)
    try {
      contactsStore.startUnreadPolling()
    } catch (e) {
      // Silencioso — se falhar, fallback local permanece
    }

    // Ao desmontar a app, para o polling
    onBeforeUnmount(() => {
      contactsStore.stopUnreadPolling()
    })
    
    if (Array.isArray(bots.value) && bots.value.length > 0) {
      // Atualiza o item Bots/Agentes com os agentes carregados
      const botsIndex = navItems.value.findIndex(item => item.id === 'bots')
      if (botsIndex !== -1) {
        const agentChildren: NavItem[] = bots.value.map((bot: any) => ({
          id: `agent-${bot.key}`,
          title: bot.name,
          icon: bot.emoji || '🤖',
          to: `/bots?edit=${bot.key}`,
        }))
        
        const item = navItems.value[botsIndex]!
        navItems.value[botsIndex] = {
          ...item,
          badge: agentChildren.length,
          badgeColor: 'primary',
          children: agentChildren,
        }
      }
    }
  } catch (error) {
    console.error('Erro ao carregar agentes:', error)
    // Menu continua funcionando mesmo se falhar
  }
})
</script>

<style scoped lang="scss">
.app-container {
  height: 100vh;
  overflow: hidden;
}

.v-main.with-navbar {
  height: 100%;
  overflow: hidden;
  
  // Ajusta padding para navbar em rail mode (retrátil) no desktop
  @media (min-width: 960px) {
    padding-left: 72px !important;
  }
  
  // Em mobile, adiciona padding inferior para bottom navigation
  @media (max-width: 959px) {
    padding-bottom: 56px !important;
  }
}

</style>