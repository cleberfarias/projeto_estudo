export const colors = {
  // WhatsApp Brand Colors
  primary: 'rgb(var(--v-theme-primary))',
  primaryLight: 'rgb(var(--v-theme-primary-lighten-1))',
  secondary: 'rgb(var(--v-theme-secondary))',
  
  // Message Colors
  sentMessage: 'rgb(var(--v-theme-surface-light))',
  receivedMessage: 'rgb(var(--v-theme-surface))',
  
  // Background
  chatBackground: 'rgb(var(--v-theme-background))',
  inputBackground: 'rgb(var(--v-theme-surface-variant))',
  
  // Text
  textPrimary: 'rgb(var(--v-theme-on-surface))',
  textSecondary: 'rgba(var(--v-theme-on-surface-rgb), 0.6)',
  textHint: 'rgba(var(--v-theme-on-surface-rgb), 0.45)',
  textWhite: 'rgb(var(--v-theme-on-primary))',
  
  // Status
  online: 'rgb(var(--v-theme-success))',
  offline: 'rgb(var(--v-theme-grey))',
  typing: 'rgb(var(--v-theme-primary-darken-1))',
  
  // UI Elements
  border: 'rgb(var(--v-theme-border))',
  divider: 'rgba(var(--v-theme-on-surface-rgb), 0.12)',
  shadow: 'rgba(0, 0, 0, 0.1)',
  
  // Status Message
  success: 'rgb(var(--v-theme-success))',
  error: 'rgb(var(--v-theme-error))',
  warning: 'rgb(var(--v-theme-warning))',
  info: 'rgb(var(--v-theme-info))',
} as const;

export type ColorToken = keyof typeof colors;