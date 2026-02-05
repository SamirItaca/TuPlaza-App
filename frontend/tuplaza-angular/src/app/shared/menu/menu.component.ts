import { Component, OnInit } from '@angular/core';

import {
  IonMenu,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem
} from '@ionic/angular/standalone';

@Component({
  selector: 'tuplaza-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  imports: [IonMenu, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem]
})
export class MenuComponent  implements OnInit {

  constructor() { }

  ngOnInit() {}

}
