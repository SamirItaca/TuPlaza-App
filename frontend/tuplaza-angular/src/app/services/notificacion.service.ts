import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, tap } from 'rxjs';
import { Notificacion } from '../core/models/notificacion.model';

@Injectable({ providedIn: 'root' })
export class NotificacionService {
  private http = inject(HttpClient);
  private apiUrl = 'http://localhost:8000/api/notificaciones/';

  private notificacionesSubject = new BehaviorSubject<Notificacion[]>([]);
  notificaciones$ = this.notificacionesSubject.asObservable();

  // 1. CARGAR: El Interceptor añadirá el Token automáticamente
  cargarNotificaciones() {
    return this.http.get<Notificacion[]>(this.apiUrl).pipe(
      tap(notifs => {
        // Solo mostramos las que NO están leídas en la lista principal
        const pendientes = notifs.filter(n => !n.leida);
        this.notificacionesSubject.next(pendientes);
      })
    ).subscribe();
  }

  // 2. MARCAR LEÍDA: Al hacer el POST, el Interceptor también actúa aquí
  marcarLeida(id: number) {
    return this.http.post(`${this.apiUrl}${id}/marcar_leida/`, {}).pipe(
      tap(() => {
        // Actualizamos el estado local inmediatamente para que la tarjeta desaparezca
        const listaActual = this.notificacionesSubject.value;
        const listaNueva = listaActual.filter(n => n.id !== id);
        this.notificacionesSubject.next(listaNueva);
      })
    );
  }
  actualizarEstadoReserva(reservaId: number, nuevoEstado: 'confirmada' | 'rechazada') {
  // Ajusta la URL según tu API de Django (ej: /api/reservas/1/actualizar_estado/)
  const url = `http://localhost:8000/api/reservas/${reservaId}/actualizar_estado/`;
  
  return this.http.patch(url, { estado: nuevoEstado }).pipe(
    tap(() => {
      console.log(`Reserva ${reservaId} actualizada a ${nuevoEstado} en la BBDD`);
      // Aquí Django, por detrás, debería encargarse de crear la notificación para el cliente
    })
  );
}
}