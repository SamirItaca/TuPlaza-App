import { ComponentFixture, TestBed, waitForAsync } from '@angular/core/testing';
import { IonicModule } from '@ionic/angular';

import { TabComponent } from './tab.component';

describe('TabComponent', () => {
  let component: TabComponent;
  let fixture: ComponentFixture<TabComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [ TabComponent ],
      imports: [IonicModule.forRoot()]
    }).compileComponents();

    fixture = TestBed.createComponent(TabComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  }));

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should initialize tabButtons with correct pages on ngOnInit', () => {
    component.ngOnInit();
    expect(component.tabButtons.length).toBe(5);

    expect(component.tabButtons).toEqual([
      { tab: 'home', iconName: 'home', text: 'Home' },
      { tab: 'garajes', iconName: 'car', text: 'Garajes' },
      { tab: 'favoritos', iconName: 'heart', text: 'Favoritos' },
      { tab: 'publicar', iconName: 'add-circle', text: 'Publicar' },
      { tab: 'mis-garajes', iconName: 'folder-open', text: 'Mis garajes' }
    ]);
  });

  it('initPagesInTabButton should populate tabButtons correctly', () => {
    component.ngOnInit();  // inicializa tabButtons
    expect(component.tabButtons.length).toBe(5);
    expect(component.tabButtons[0].tab).toBe('home');
  });

});
