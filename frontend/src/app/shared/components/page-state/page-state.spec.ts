import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PageState } from './page-state';

describe('PageState', () => {
  let component: PageState;
  let fixture: ComponentFixture<PageState>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [PageState],
    }).compileComponents();

    fixture = TestBed.createComponent(PageState);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
