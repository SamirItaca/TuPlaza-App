import { Component, OnInit, OnDestroy, inject } from '@angular/core'; // Añadido OnDestroy
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router'; // <--- 1. ¡IMPORTANTE! Añadir Router aquí
import { NotificacionService } from '../../services/notificacion.service';
import { IonicModule } from '@ionic/angular';
import { addIcons } from 'ionicons';
import { 
  personCircleOutline, 
  locationOutline, 
  calendarOutline, 
  timeOutline, 
  checkmarkCircleOutline, 
  closeCircleOutline,
  personOutline,
  lockClosedOutline,
  notificationsOffOutline,
  eyeOutline,           // <--- 2. Icono para el botón Ver Detalles
  notificationsOutline  // <--- 2. Icono para la cabecera
} from 'ionicons/icons';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-notificaciones',
  standalone: true,
  imports: [CommonModule, IonicModule, RouterModule],
  templateUrl: './notificaciones.component.html',
  styleUrls: ['./notificaciones.component.css']
})
export class NotificacionesComponent implements OnInit, OnDestroy {
  private notifService = inject(NotificacionService);
  public router = inject(Router); // <--- Ahora funcionará porque está importado arriba
  
  reservas: any[] = [];
  private notifSub!: Subscription;

  constructor() {
    addIcons({ 
      personCircleOutline, 
      locationOutline, 
      calendarOutline, 
      timeOutline, 
      checkmarkCircleOutline, 
      closeCircleOutline,
      personOutline,
      lockClosedOutline,
      notificationsOffOutline,
      eyeOutline,
      notificationsOutline
    });
  }

  ngOnInit() {
    this.notifSub = this.notifService.notificaciones$.subscribe(data => {
      console.log('Datos recibidos del servicio:', data);
      this.reservas = data;
    });

    this.notifService.cargarNotificaciones();
  }

  ngOnDestroy() {
    if (this.notifSub) {
      this.notifSub.unsubscribe();
    }
  }

verDetalles(notificacion: any) {
  const reservaId = notificacion.reserva;
  const notificacionId = notificacion.id;

  if (notificacionId) {
    // Marcamos como leída. El 'tap' del servicio se encargará de hacerla desaparecer de la lista
    this.notifService.marcarLeida(notificacionId).subscribe({
      next: () => {
        if (reservaId) {
          this.router.navigate(['/gestion-reserva', reservaId]);
        }
      },
      error: (err) => {
        console.error('Error al marcar como leída:', err);
        // Si falla la red, navegamos igual para no bloquear al usuario
        if (reservaId) this.router.navigate(['/gestion-reserva', reservaId]);
      }
    });
  }
}
  // Mantengo estas por si las usas en la otra pantalla
  aceptarReserva(id: number) { console.log('Aceptando...', id); }
  rechazarReserva(id: number) { console.log('Rechazando...', id); }
  marcarLeida(id: number) {
    this.notifService.marcarLeida(id).subscribe(() => console.log('Leída'));
  }
}