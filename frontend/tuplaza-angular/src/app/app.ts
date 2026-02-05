import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';

import {
  IonApp
} from '@ionic/angular/standalone';

import { MenuComponent } from './shared/menu/menu.component';
import { NavbarComponent } from './shared/navbar/navbar.component';
import { TabComponent } from './shared/tab/tab.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet,
      MenuComponent, NavbarComponent, TabComponent, 
      IonApp
    ],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('tuplaza-angular');
}
