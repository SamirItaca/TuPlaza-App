import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  {
    path: 'favoritos',
    loadChildren: () =>
      import('./features/favoritos/favoritos.routes').then(m => m.FAVORITOS_ROUTES)
  },
  {
    path: 'garajes',
    loadChildren: () =>
      import('./features/garajes/garajes.routes').then(m => m.GARAJES_ROUTES)
  },
  {
    path: 'home',
    loadChildren: () =>
      import('./features/home/home.routes').then(m => m.HOME_ROUTES)
  },
  {
    path: 'mis-garajes',
    loadChildren: () =>
      import('./features/mis-garajes/mis-garajes.routes').then(m => m.MIS_GARAJES_ROUTES)
  },
  {
    path: 'publicar',
    loadChildren: () =>
      import('./features/publicar/publicar.routes').then(m => m.PUBLICAR_ROUTES)
  }
];

