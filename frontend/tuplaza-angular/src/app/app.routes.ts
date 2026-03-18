import { Routes } from '@angular/router';
import { authGuard } from './core/guards/auth.guard';

export const routes: Routes = [
  // 1. Ruta inicial: Redirige al Home (o a Garajes, según prefieras)
  { path: '', redirectTo: '/home', pathMatch: 'full' },

  // 2. Ruta de Login (Añadida siguiendo tu esquema de carpetas)
 { 
  path: 'login', 
  loadComponent: () => import('./features/auth/login/login.component').then(m => m.LoginComponent) 
  },

  // 3. Resto de módulos funcionales
  {
    path: 'favoritos',
    canActivate: [authGuard], // ruta protegida, si no estas logueado no puedes entrar
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
    canActivate: [authGuard],// ruta protegida, si no estas logueado no puedes entrar
    loadChildren: () => import('./features/mis-garajes/mis-garajes.routes').then(m => m.MIS_GARAJES_ROUTES)
  },
  {
    path: 'publicar',
    canActivate: [authGuard],// ruta protegida, si no estas logueado no puedes entrar
    loadChildren: () => import('./features/publicar/publicar.routes').then(m => m.PUBLICAR_ROUTES)
  }
];