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

  cargarNotificaciones() {
    return this.http.get<Notificacion[]>(this.apiUrl).pipe(
      tap(notifs => this.notificacionesSubject.next(notifs))
    ).subscribe();
  }

  marcarLeida(id: number) {
    return this.http.post(`${this.apiUrl}${id}/marcar_leida/`, {});
  }
}