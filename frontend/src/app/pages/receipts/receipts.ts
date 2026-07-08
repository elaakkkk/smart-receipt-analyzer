import { Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';

import { ReceiptListItem } from '../../core/models/receipt.model';
import { ReceiptService } from '../../core/services/receipt.service';

@Component({
  selector: 'app-receipts',
  imports: [DatePipe],
  templateUrl: './receipts.html',
  styleUrl: './receipts.css',
})
export class Receipts implements OnInit {
  receipts: ReceiptListItem[] = [];
  loading = false;
  errorMessage = '';

  constructor(private receiptService: ReceiptService) {}

  ngOnInit(): void {
    this.loadReceipts();
  }

  loadReceipts(): void {
    this.loading = true;
    this.errorMessage = '';

    this.receiptService.getReceipts().subscribe({
      next: (data) => {
        this.receipts = data;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Unable to load receipts.';
        this.loading = false;
      },
    });
  }

  deleteReceipt(id: number): void {
    this.receiptService.deleteReceipt(id).subscribe({
      next: () => {
        this.receipts = this.receipts.filter((receipt) => receipt.id !== id);
      },
      error: () => {
        this.errorMessage = 'Unable to delete the receipt.';
      },
    });
  }
}