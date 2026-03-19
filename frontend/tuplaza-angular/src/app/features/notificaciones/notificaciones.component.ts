import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { NotificacionService } from '../../services/notificacion.service';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-notificaciones',
  standalone: true,
  imports: [CommonModule, IonicModule],
  templateUrl: './notificaciones.component.html',
  styleUrls: ['notificaciones.component.css']
})
export class NotificacionesComponent implements OnInit {
  public notifService = inject(NotificacionService);

  ngOnInit() {
    // Cargamos las notificaciones al entrar
    this.notifService.cargarNotificaciones();
  }

  marcarLeida(id: number) {
    this.notifService.marcarLeida(id).subscribe(() => {
      // Opcional: recargar o dejar que el BehaviorSubject maneje la UI
      console.log('Notificación leída');
    });
  }
}