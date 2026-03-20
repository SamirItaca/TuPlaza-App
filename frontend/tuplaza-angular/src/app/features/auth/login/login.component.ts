import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { IonicModule, ToastController } from '@ionic/angular';
import { AuthService } from '../auth.service'; // Ajusta la ruta
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [IonicModule, CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  credentials = {
    username: '',
    password: ''
  };

  constructor(
    private authService: AuthService,
    private router: Router,
    private toastController: ToastController
  ) {}

  async onLogin() {
    this.authService.login(this.credentials).subscribe({
      next: (res) => {
        this.presentToast('¡Bienvenido a TuPlaZa!', 'success');
        this.router.navigate(['/notificaciones']); // Te redirige a la lista de notificaciones 
      },
      error: (err) => {
        this.presentToast('Error: Usuario o contraseña incorrectos', 'danger');
        console.error(err);
      }
    });
  }

  async presentToast(message: string, color: string) {
    const toast = await this.toastController.create({
      message,
      duration: 2000,
      color,
      position: 'bottom'
    });
    await toast.present();
  }
}