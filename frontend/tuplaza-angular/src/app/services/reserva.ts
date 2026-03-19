import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ReservaService {
  // Ajusta esta URL a la de tu servidor Django
  private apiUrl = 'http://127.0.0.1:8000/api/reservas/';

  constructor(private http: HttpClient) { }

  // 1. Obtener reservas que le han hecho al dueño (dueño logueado)
  getReservasRecibidas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}recibidas/`);
  }

  // 2. Aceptar una reserva específica
  aceptarReserva(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/aceptar/`, {});
  }

  // 3. Rechazar una reserva específica
  rechazarReserva(id: number): Observable<any> {
    return this.http.post(`${this.apiUrl}${id}/rechazar/`, {});
  }
} 