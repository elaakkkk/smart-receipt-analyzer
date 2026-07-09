import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ReceiptDetail } from './receipt-detail';

describe('ReceiptDetail', () => {
  let component: ReceiptDetail;
  let fixture: ComponentFixture<ReceiptDetail>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReceiptDetail],
    }).compileComponents();

    fixture = TestBed.createComponent(ReceiptDetail);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
