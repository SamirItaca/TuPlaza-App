// src/app/pages/home/components/near-sites/near-sites.component.ts
import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

@Component({
  selector: 'app-near-sites',
  standalone: true,
  imports: [CommonModule, IonicModule],
  template: `
    <div class="near-sites-container">
      <h3 class="section-title">Sitios cercanos a ti</h3>

      <ion-grid>
        <ion-row>
          <ion-col size="12" size-md="6" size-lg="3" *ngFor="let garaje of garajes">
            <ion-card class="site-card">
              <div class="site-image">
                <img [src]="garaje.imagen || 'assets/img/mock-garaje.jpg'" [alt]="garaje.nombre">
              </div>
              <ion-card-header>
                <div class="card-footer">
                  <div class="text-info">
                    <ion-card-title>{{ garaje.direccion }}</ion-card-title>
                    <ion-card-subtitle>{{ garaje.dimensiones }}</ion-card-subtitle>
                  </div>
                  <ion-button class="btn-ver-ahora">Ver ahora</ion-button>
                </div>
              </ion-card-header>
            </ion-card>
          </ion-col>
        </ion-row>
      </ion-grid>
    </div>
  `,
  styleUrls: ['near-sites.component.css']
})
export class NearSitesComponent {
  @Input() garajes: any[] = [];
  @Input() loading: boolean = false;
}