// Exporta validação e tipos de mensagem
export * from './validation';

export interface User {
  id: string;
  name: string;
  avatar?: string;
  online: boolean;
  lastSeen?: number;
}

export interface ChatRoom {
  id: string;
  name: string;
  participants: User[];
  lastMessage?: import('./validation').Message;
  unreadCount: number;
}