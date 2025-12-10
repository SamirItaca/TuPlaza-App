import { Component } from '@angular/core';
import { ButtonComponent } from '../../../../shared/button/button.component';
import { FormularioComponent } from '../../../../shared/formulario/formulario.component';

@Component({
  selector: 'app-home',
  imports: [ButtonComponent,FormularioComponent],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

}
