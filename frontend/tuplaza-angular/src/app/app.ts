import { Component, signal } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { Navbar } from './shared/navbar/navbar';
import { TabComponent } from './shared/tab/tab.component';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, Navbar, TabComponent],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App {
  protected readonly title = signal('tuplaza-angular');
}
