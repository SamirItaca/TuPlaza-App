import { Component, OnInit } from '@angular/core';

import {
  IonMenu,
  IonHeader,
  IonToolbar,
  IonTitle,
  IonContent,
  IonList,
  IonItem,
  IonIcon,
  IonLabel
} from '@ionic/angular/standalone';

import { addIcons } from 'ionicons';
import { personOutline, settingsOutline, alertCircleOutline } from 'ionicons/icons';

@Component({
  selector: 'tuplaza-menu',
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.scss'],
  imports: [IonMenu, IonHeader, IonToolbar, IonTitle, IonContent, IonList, IonItem, IonIcon, IonLabel]
})
export class MenuComponent implements OnInit {

  constructor() { 
    addIcons({ personOutline, settingsOutline, alertCircleOutline });
  }

  ngOnInit() {}

}
