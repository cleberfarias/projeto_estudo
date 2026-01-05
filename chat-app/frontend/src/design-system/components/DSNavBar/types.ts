/**
 * Tipos para o componente DSNavBar
 */

export interface NavItem {
  /**
   * Identificador único do item
   */
  id: string;
  
  /**
   * Título exibido no menu
   */
  title: string;
  
  /**
   * Ícone do Material Design Icons (sem o prefixo 'mdi-')
   */
  icon: string;
  
  /**
   * Rota para navegação
   */
  to?: string;
  
  /**
   * Badge opcional (ex: contador de notificações). Pode ser número ou texto (ex: '99+').
   */
  badge?: number | string;
  
  /**
   * Cor do badge
   */
  badgeColor?: string;

  /**
   * Quando true e em mobile, mostra um dot em vez do número (útil para bottom navigation)
   */
  badgeDotMobile?: boolean;
  
  /**
   * Subitems (para menus expansíveis)
   */
  children?: NavItem[];
}

export interface DSNavBarProps {
  /**
   * Lista de itens do menu
   */
  items: NavItem[];
  
  /**
   * Se true, mostra o logo/header no topo (apenas desktop)
   */
  showHeader?: boolean;
  
  /**
   * Título do header
   */
  headerTitle?: string;
}
