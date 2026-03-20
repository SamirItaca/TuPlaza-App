import { Component, OnInit, inject } from '@angular/core';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { IonicModule, AlertController } from '@ionic/angular'; // Añadido AlertController
import { addIcons } from 'ionicons';
import { 
  personOutline, 
  calendarOutline, 
  cashOutline, 
  timeOutline, 
  checkmarkCircleOutline, 
  closeCircleOutline 
} from 'ionicons/icons';

@Component({
  selector: 'app-gestion-reserva',
  standalone: true,
  imports: [CommonModule, RouterModule, IonicModule], 
  templateUrl: './gestion-reserva.component.html',
  styleUrls: ['./gestion-reserva.component.css']
})
export class GestionReservaComponent implements OnInit {
  
  private route = inject(ActivatedRoute);
  private router = inject(Router);
  private http = inject(HttpClient);
  private alertCtrl = inject(AlertController); // Para las confirmaciones

  reservaId: string | null = null;
  reserva: any = null;

  constructor() {
    // Registramos los iconos para que se vean en el HTML
    addIcons({ 
      personOutline, 
      calendarOutline, 
      cashOutline, 
      timeOutline,
      checkmarkCircleOutline,
      closeCircleOutline 
    });
  }

  ngOnInit() {
    this.reservaId = this.route.snapshot.paramMap.get('id');
    if (this.reservaId) {
      this.cargarDetallesReserva();
    }
    window.scrollTo(0, 0);
  }

  cargarDetallesReserva() {
    this.http.get(`http://localhost:8000/api/reservas/${this.reservaId}/`).subscribe({
      next: (data) => {
        this.reserva = data;
      },
      error: (err) => console.error('Error al cargar la reserva:', err)
    });
  }

  // Nueva función para confirmar antes de ejecutar
  async confirmarAccion(accion: 'aceptar' | 'rechazar') {
    const titulo = accion === 'aceptar' ? 'Confirmar Reserva' : 'Rechazar Reserva';
    const mensaje = accion === 'aceptar' 
      ? '¿Estás seguro de que quieres aceptar esta solicitud? Se notificará al cliente.' 
      : '¿Realmente deseas rechazar esta solicitud?';

    const alert = await this.alertCtrl.create({
      header: titulo,
      message: mensaje,
      buttons: [
        { text: 'Cancelar', role: 'cancel' },
        {
          text: 'Confirmar',
          handler: () => this.actualizarEstado(accion)
        }
      ]
    });

    await alert.present();
  }

  actualizarEstado(accion: 'aceptar' | 'rechazar') {
    this.http.post(`http://localhost:8000/api/reservas/${this.reservaId}/${accion}/`, {})
      .subscribe({
        next: () => {
          // Navegamos de vuelta a notificaciones tras el éxito
          this.router.navigate(['/notificaciones']);
        },
        error: (err) => {
          const errorMsg = err.error?.error || 'Error al procesar la reserva';
          console.error(errorMsg);
        }
      });
  }
}