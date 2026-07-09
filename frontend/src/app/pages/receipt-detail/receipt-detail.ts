import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { DatePipe, JsonPipe } from '@angular/common';
import { finalize } from 'rxjs';
import { ActivatedRoute, RouterLink } from '@angular/router';

import { ReceiptService } from '../../core/services/receipt.service';
import { ReceiptDetail as ReceiptDetailModel } from '../../core/models/receipt.model';
import { PageState } from '../../shared/components/page-state/page-state';

@Component({
  selector: 'app-receipt-detail',
  imports: [DatePipe, JsonPipe, RouterLink, PageState],
  templateUrl: './receipt-detail.html',
  styleUrl: './receipt-detail.css',
})
export class ReceiptDetailComponent implements OnInit {
  receipt: ReceiptDetailModel | null = null;
  loading = false;
  errorMessage = '';

  constructor(
    private route: ActivatedRoute,
    private receiptService: ReceiptService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    const idParam = this.route.snapshot.paramMap.get('id');

    if (!idParam) {
      this.errorMessage = 'Receipt id is missing.';
      return;
    }

    const id = Number(idParam);

    if (Number.isNaN(id)) {
      this.errorMessage = 'Receipt id is invalid.';
      return;
    }

    this.loadReceipt(id);
  }

  loadReceipt(id: number): void {
    this.loading = true;
    this.errorMessage = '';

    this.receiptService
      .getReceiptById(id)
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.detectChanges();
        })
      )
      .subscribe({
        next: (data) => {
          this.receipt = data;
        },
        error: () => {
          this.errorMessage = 'Unable to load receipt.';
        },
      });
  }
}