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
   * Badge opcional (ex: contador de notificações)
   */
  badge?: number;
  
  /**
   * Cor do badge
   */
  badgeColor?: string;
  
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
