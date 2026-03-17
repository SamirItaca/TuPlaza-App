import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // <--- 1. Importa esto
import { GarajeService } from '../services/garaje.service';

@Component({
  selector: 'app-garajes',
  standalone: true,           
  imports: [CommonModule],    
  templateUrl: './garajes.component.html',
  styleUrls: ['./garajes.component.css']
})
export class GarajesComponent implements OnInit {
  listaGarajes: any[] = []; 

  constructor(private garajeService: GarajeService) { }

  ngOnInit(): void {
    this.garajeService.getGarajes().subscribe({
      next: (data) => {
        this.listaGarajes = data;
        console.log('Datos recibidos:', data);
      },
      error: (err) => {
        console.error('Error en la petición:', err);
      }
    });
  }
}