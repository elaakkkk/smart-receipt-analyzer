import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReceiptReview } from './receipt-review';

describe('ReceiptReview', () => {
  let component: ReceiptReview;
  let fixture: ComponentFixture<ReceiptReview>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReceiptReview],
    }).compileComponents();

    fixture = TestBed.createComponent(ReceiptReview);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
