import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/home', pathMatch: 'full' },
  {
    path: 'home',
    loadChildren: () =>
      import('./features/home/home.routes').then(m => m.HOME_ROUTES)
  },
  {
    path: 'garajes',
    loadChildren: () =>
      import('./features/garajes/garajes.routes').then(m => m.GARAJES_ROUTES)
  }
];

