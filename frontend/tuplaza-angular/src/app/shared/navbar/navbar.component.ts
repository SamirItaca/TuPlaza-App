import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { IonHeader, IonToolbar, IonItem, IonIcon, IonInput, IonButtons, IonMenuButton } from '@ionic/angular/standalone';

import { addIcons } from 'ionicons';
import { searchOutline } from 'ionicons/icons';

@Component({
  selector: 'tuplaza-nav',
  imports: [RouterModule, IonHeader, IonToolbar, IonItem, IonIcon, IonInput, IonButtons, IonMenuButton],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  
  constructor() { 
    addIcons({ searchOutline });
  }

}
