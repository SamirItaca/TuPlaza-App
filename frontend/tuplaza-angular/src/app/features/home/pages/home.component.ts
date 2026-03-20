import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { IonicModule } from '@ionic/angular';

// Importamos los componentes hijos (asegúrate de que estas rutas sean correctas)
import { MapSectionComponent } from '../components/map-section/map-section.component';
import { NearSitesComponent } from '../components/near-sites/near-sites.component';

// Si aún no tienes el servicio creado, lo comentamos correctamente 
// o usamos uno genérico para que no de error de compilación.
// import { GarajeService } from '../../services/garaje.service'; 

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CommonModule, 
    IonicModule, 
    MapSectionComponent, // Ya no dará error en el HTML
    NearSitesComponent
  ],
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  // Comentamos la inyección si el servicio no existe aún para que no rompa
  // private garajeService = inject(GarajeService);
  
  garajesCercanos: any[] = [];
  loading: boolean = true;

  ngOnInit() {
    this.cargarGarajes();
  }

  cargarGarajes() {
    // Simulamos una carga de datos para que veas algo en el Home mientras conectas con Django
    setTimeout(() => {
      this.garajesCercanos = [
        { id: 1, direccion: 'Calle Falsa 123', dimensiones: '2.5m x 4.5m' },
        { id: 2, direccion: 'Av. Independencia 10', dimensiones: '3.0m x 5.0m' },
        { id: 3, direccion: 'Plaza España 5', dimensiones: '2.2m x 4.0m' },
        { id: 4, direccion: 'Calle Mayor 1', dimensiones: '2.8m x 4.8m' }
      ];
      this.loading = false;
    }, 1000);
  }
}