// src/app/pages/home/components/map-section/map-section.component.ts
import { Component } from '@angular/core';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-map-section',
  standalone: true,
  imports: [IonicModule],
  template: `
    <div class="map-card">
      <div class="map-placeholder">
        <img src="assets/img/mock-map.png" alt="Mapa de Zaragoza">
        <h2>Zaragoza</h2>
      </div>
    </div>
  `,
  styles: [`
    .map-card {
      background: white;
      border-radius: 20px;
      padding: 10px; /* Borde interior blanco */
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); /* Sombra suave de tu mockup */
      margin: 20px 0;
      overflow: hidden;
    }

    .map-placeholder {
      width: 100%;
      height: 250px;
      border-radius: 15px; /* Bordes redondeados de la imagen */
      overflow: hidden;
      position: relative;
    }

    .map-placeholder img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .map-placeholder h2 {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      margin: 0;
      color: #333;
      font-size: 2.5rem;
      font-weight: 800;
      letter-spacing: -1px;
    }
  `]
})
export class MapSectionComponent {}