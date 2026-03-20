import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule, NavController, ToastController } from '@ionic/angular';
import { FormsModule } from '@angular/forms';
import { HttpClient } from '@angular/common/http';
import { ActivatedRoute } from '@angular/router';
import { addIcons } from 'ionicons';
import { calendarOutline, timeOutline, cashOutline } from 'ionicons/icons';

@Component({
  selector: 'app-crear-reserva',
  standalone: true,
  imports: [CommonModule, IonicModule, FormsModule],
  templateUrl: './crear-reserva.component.html',
  styleUrls: ['./crear-reserva.component.css']
})
export class CrearReservaComponent implements OnInit {
  private http = inject(HttpClient);
  private route = inject(ActivatedRoute);
  private navCtrl = inject(NavController);
  private toastCtrl = inject(ToastController);

  garajeId: string | null = null;
  
  // Modelo que espera tu Backend
  reserva = {
    garaje: '',
    fecha_inicio: new Date().toISOString(),
    fecha_fin: ''
  };

  constructor() {
    addIcons({ calendarOutline, timeOutline, cashOutline });
  }

  ngOnInit() {
  this.garajeId = this.route.snapshot.paramMap.get('id');
  if (this.garajeId) {
    this.reserva.garaje = this.garajeId;
  }

  // Inicializamos las fechas para que los botones tengan contenido
  const ahora = new Date();
  const trasDosHoras = new Date();
  trasDosHoras.setHours(ahora.getHours() + 2);

  this.reserva.fecha_inicio = ahora.toISOString();
  this.reserva.fecha_fin = trasDosHoras.toISOString(); // <--- Esto hará que ya sea visible
}

  enviarReserva() {
    // Validación básica antes de enviar
    if (!this.reserva.fecha_fin) {
      this.mostrarToast('Selecciona una fecha de salida', 'warning');
      return;
    }

    this.http.post('http://localhost:8000/api/reservas/', this.reserva).subscribe({
      next: () => {
        this.mostrarToast('¡Solicitud enviada con éxito!', 'success');
        this.navCtrl.navigateRoot('/inicio'); 
      },
      error: (err) => {
        const msg = err.error?.error || 'Error al conectar con el servidor';
        this.mostrarToast(msg, 'danger');
      }
    });
  }

  async mostrarToast(message: string, color: string) {
    const toast = await this.toastCtrl.create({ message, duration: 2000, color, position: 'bottom' });
    await toast.present();
  }
}