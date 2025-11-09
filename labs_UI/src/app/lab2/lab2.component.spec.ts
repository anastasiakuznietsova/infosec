import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Lab2Component } from './lab2.component';

describe('Lab2Component', () => {
  let component: Lab2Component;
  let fixture: ComponentFixture<Lab2Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Lab2Component]
    });
    fixture = TestBed.createComponent(Lab2Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
