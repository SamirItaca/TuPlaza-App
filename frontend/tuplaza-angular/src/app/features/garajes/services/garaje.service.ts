import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { environment } from '../../../environments/environments';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class GarajeService {
  private apiUrl = `${environment.apiUrl}/garajes/`;

  constructor(private http: HttpClient) { }

  getGarajes(): Observable<any[]> {
    return this.http.get<any[]>(this.apiUrl);
  }
}