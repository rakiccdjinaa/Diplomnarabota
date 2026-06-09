import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DoctorHistory } from './doctor-history';

describe('DoctorHistory', () => {
  let component: DoctorHistory;
  let fixture: ComponentFixture<DoctorHistory>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DoctorHistory],
    }).compileComponents();

    fixture = TestBed.createComponent(DoctorHistory);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
