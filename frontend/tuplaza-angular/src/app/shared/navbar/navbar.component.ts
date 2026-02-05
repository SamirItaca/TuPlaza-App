import { Component } from '@angular/core';
import { RouterModule } from '@angular/router';
import { IonHeader, IonToolbar, IonItem, IonInput, IonButtons, IonMenuButton } from '@ionic/angular/standalone';

@Component({
  selector: 'tuplaza-nav',
  imports: [RouterModule, IonHeader, IonToolbar, IonItem, IonInput, IonButtons, IonMenuButton],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css',
})
export class NavbarComponent {
  
}
