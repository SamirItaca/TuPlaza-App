import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { 
  IonHeader, IonToolbar, IonTitle, IonContent, IonList, 
  IonItem, IonLabel, IonBadge, IonButton, IonIcon, IonText 
} from '@ionic/angular/standalone';
import { ReservaService } from '../../services/reserva';
import { addIcons } from 'ionicons';
import { checkmarkOutline, closeOutline } from 'ionicons/icons';

@Component({
  selector: 'app-mis-reservas',
  templateUrl: './mis-reservas.component.html',
  standalone: true,
  imports: [
    CommonModule, IonHeader, IonToolbar, IonTitle, IonContent, 
    IonList, IonItem, IonLabel, IonBadge, IonButton, IonIcon, IonText
  ]
})
export class MisReservasComponent implements OnInit {
  reservas: any[] = [];

  constructor(private reservaService: ReservaService) {
    // Registramos los iconos de Ionicons que vamos a usar
    addIcons({ checkmarkOutline, closeOutline });
  }

  ngOnInit() {
    this.cargarReservas();
  }

  cargarReservas() {
    this.reservaService.getReservasRecibidas().subscribe({
      next: (data) => {
        this.reservas = data;
      },
      error: (err) => console.error('Error cargando reservas', err)
    });
  }

  gestionarReserva(id: number, accion: 'aceptar' | 'rechazar') {
    const solicitud = accion === 'aceptar' 
      ? this.reservaService.aceptarReserva(id) 
      : this.reservaService.rechazarReserva(id);

    solicitud.subscribe({
      next: () => {
        console.log(`Reserva ${id} ${accion}ada`);
        this.cargarReservas(); // Refrescamos la lista
      },
      error: (err) => alert('No se pudo procesar la acción')
    });
  }
}