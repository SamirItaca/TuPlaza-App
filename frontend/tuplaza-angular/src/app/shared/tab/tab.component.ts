import { Component, OnInit } from '@angular/core';
import {
  IonContent,
  IonHeader,
  IonIcon,
  IonTab,
  IonTabBar,
  IonTabButton,
  IonTabs,
  IonTitle,
  IonToolbar,
} from '@ionic/angular/standalone';

import { addIcons } from 'ionicons';
import { library, playCircle, radio, search } from 'ionicons/icons';

@Component({
  selector: 'tuplaza-tab',
  templateUrl: './tab.component.html',
  styleUrls: ['./tab.component.scss'],
  imports: [IonContent, IonHeader, IonIcon, IonTab, IonTabBar, IonTabButton, IonTabs, IonTitle, IonToolbar],
})
export class TabComponent  implements OnInit {

  constructor() { 
    addIcons({ library, playCircle, radio, search });
  }

  ngOnInit() {}

}
