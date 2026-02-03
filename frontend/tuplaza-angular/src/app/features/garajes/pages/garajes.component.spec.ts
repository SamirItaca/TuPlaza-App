import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GarajesComponent } from './garajes.component';

describe('Garajes', () => {
  let component: GarajesComponent;
  let fixture: ComponentFixture<GarajesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [GarajesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(GarajesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
