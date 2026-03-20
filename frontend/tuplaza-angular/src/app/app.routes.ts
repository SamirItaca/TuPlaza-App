import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';
import { NotificacionesComponent } from './features/notificaciones/notificaciones.component';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },

  { 
    path: 'login', 
    loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent) 
  },

  {
    path: 'favoritos',
    canActivate: [authGuard],
    loadChildren: () => import('./features/favoritos/favoritos.routes').then(m => m.FAVORITOS_ROUTES)
  },
  {
    path: 'garajes',
    loadChildren: () => import('./features/garajes/garajes.routes').then(m => m.GARAJES_ROUTES)
  },
  {
    path: 'home',
    loadChildren: () => import('./features/home/home.routes').then(m => m.HOME_ROUTES)
  },
  {
    path: 'mis-garajes',
    canActivate: [authGuard],
    loadChildren: () => import('./features/mis-garajes/mis-garajes.routes').then(m => m.MIS_GARAJES_ROUTES)
  },
  {
    path: 'publicar',
    canActivate: [authGuard],
    loadChildren: () => import('./features/publicar/publicar.routes').then(m => m.PUBLICAR_ROUTES)
  },
  {
    path: 'mis-reservas',
    loadComponent: () => import('./pages/mis-reservas/mis-reservas.component').then(m => m.MisReservasComponent)
  },
  { 
    path: 'notificaciones', 
    component: NotificacionesComponent 
  },
  { 
    path: 'gestion-reserva/:id', 
    loadComponent: () => import('./features/reservas/gestion-reserva.component').then(m => m.GestionReservaComponent) 
  }, // <--- AQUÍ FALTABA ESTA COMA
  { 
    path: 'crear-reserva/:id', 
    // He ajustado la ruta al archivo .ts según tu captura anterior
    loadComponent: () => import('./features/reservas/pages/crear-reserva.component').then(m => m.CrearReservaComponent) 
  }
];