import { ComponentFixture, TestBed } from '@angular/core/testing';

import { Lab3Component } from './lab3.component';

describe('Lab3Component', () => {
  let component: Lab3Component;
  let fixture: ComponentFixture<Lab3Component>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [Lab3Component]
    });
    fixture = TestBed.createComponent(Lab3Component);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
