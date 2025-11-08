import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Garajes } from './garajes';

describe('Garajes', () => {
  let component: Garajes;
  let fixture: ComponentFixture<Garajes>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [Garajes]
    })
    .compileComponents();

    fixture = TestBed.createComponent(Garajes);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
