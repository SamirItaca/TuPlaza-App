import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api'; // ruta de la api django

  constructor(private http: HttpClient) {}

  // Caso de uso: Crear cuenta
  registrar(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/registro/`, userData);
  }

  // Caso de uso: Iniciar sesión
  login(credentials: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/token/`, credentials).pipe(
      tap((response: any) => {
        // Guardamos los tokens al recibir la respuesta
        localStorage.setItem('access_token', response.access);
        localStorage.setItem('refresh_token', response.refresh);
      })
    );
  }

  // Para cerrar sesión
  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  }

  // Comprobar si está logueado
  isLoggedIn(): boolean {
    return !!localStorage.getItem('access_token');
  }
}