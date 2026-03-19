export interface Notificacion {
  id: number;
  titulo: string;
  mensaje: string;
  tipo: 'NUEVA_RESERVA' | 'RESERVA_ACEPTADA' | 'RESERVA_RECHAZADA' | 'MENSAJE_CHAT';
  leida: boolean;
  fecha_creacion: string;
  reserva?: number;
}