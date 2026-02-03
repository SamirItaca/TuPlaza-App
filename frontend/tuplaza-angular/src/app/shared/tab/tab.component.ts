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

import { NgFor } from '@angular/common';

import { addIcons } from 'ionicons';
import { home, car, heart, addCircle, folderOpen } from 'ionicons/icons';
import { TabButtonPages } from './interfaces/tab-button-pages.interface'

/**
 * Componente de Tab para la navegacion principal de la app
 *
 * Este componente permite moverse entre las pantallas principales (home, garajes, favoritos, publicar y mis garajes).
 *
 * @example
 * ```html
 * <tuplaza-tab>
 * </tuplaza-tab>
 * ```
 */
@Component({
  selector: 'tuplaza-tab',
  templateUrl: './tab.component.html',
  styleUrls: ['./tab.component.scss'],
  imports: [IonContent, IonHeader, IonIcon, IonTab, IonTabBar, IonTabButton, IonTabs, IonTitle, IonToolbar, NgFor],
})
export class TabComponent  implements OnInit {

  /**
   * Lista de las pantallas.
   * @default []
   */
  public tabButtons: TabButtonPages[] = []

  constructor() { 
    addIcons({ home, car, heart, addCircle, folderOpen });
  }

  ngOnInit() {
    this.initPagesInTabButton();
  }

  /**
  * Inicializa la configuración de los botones de navegación del componente de tabs.
  *
  * Este método define las pestañas principales de la aplicación, asignando
  * a cada una su ruta asociada, el icono que se mostrará y el texto visible
  * para el usuario en la barra de navegación.
  *
  * La información generada se utiliza para renderizar dinámicamente
  * los botones del componente `ion-tab-bar`.
  */
  private initPagesInTabButton(): void {
    this.tabButtons = [
      { tab: "home", iconName: "home", text: "Home"},
      { tab: "garajes", iconName: "car", text: "Garajes"},
      { tab: "favoritos", iconName: "heart", text: "Favoritos"},
      { tab: "publicar", iconName: "add-circle", text: "Publicar"},
      { tab: "mis-garajes", iconName: "folder-open", text: "Mis garajes"}
    ]
  }

}
