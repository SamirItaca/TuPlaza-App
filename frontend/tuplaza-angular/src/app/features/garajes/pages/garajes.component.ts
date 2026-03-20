import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common'; // <--- 1. Importa esto
import { GarajeService } from '../services/garaje.service';
import { RouterModule } from '@angular/router';
import { IonicModule } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { personOutline, arrowForwardOutline,locationOutline , resizeOutline } from 'ionicons/icons';
@Component({
  selector: 'app-garajes',
  standalone: true,           
  imports: [CommonModule, RouterModule, IonicModule],    
  templateUrl: './garajes.component.html',
  styleUrls: ['./garajes.component.css']
})
export class GarajesComponent implements OnInit {
  listaGarajes: any[] = []; 

  constructor(private garajeService: GarajeService) {
    addIcons({ personOutline, arrowForwardOutline, resizeOutline, locationOutline  });
   }

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