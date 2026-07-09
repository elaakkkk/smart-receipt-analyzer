import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';
import { finalize } from 'rxjs';

import { ReceiptListItem } from '../../core/models/receipt.model';
import { ReceiptService } from '../../core/services/receipt.service';
import { RouterLink } from '@angular/router';
import { PageState } from '../../shared/components/page-state/page-state';
import { ActionButton } from '../../shared/components/action-button/action-button';

@Component({
  selector: 'app-receipts',
  imports: [DatePipe, RouterLink, PageState, ActionButton],
  templateUrl: './receipts.html',
  styleUrl: './receipts.css',
})
export class Receipts implements OnInit {
  receipts: ReceiptListItem[] = [];

  loading = false;
  uploading = false;
  deleting = false;

  errorMessage = '';
  successMessage = '';

  selectedFile: File | null = null;

  showDeleteModal = false;
  receiptIdToDelete: number | null = null;

  constructor(
    private receiptService: ReceiptService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadReceipts();
  }

  loadReceipts(): void {
    this.loading = true;
    this.errorMessage = '';

    this.receiptService
      .getReceipts()
      .pipe(
        finalize(() => {
          this.loading = false;
          this.cdr.detectChanges();
        })
      )
      .subscribe({
        next: (data) => {
          this.receipts = data;
        },
        error: () => {
          this.errorMessage = 'Unable to load receipts.';
        },
      });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (!input.files || input.files.length === 0) {
      this.selectedFile = null;
      return;
    }

    this.selectedFile = input.files[0];
    this.successMessage = '';
    this.errorMessage = '';
  }

  uploadReceipt(): void {
    if (!this.selectedFile) {
      this.errorMessage = 'Please select a file before uploading.';
      return;
    }

    this.uploading = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.receiptService
      .uploadReceipt(this.selectedFile)
      .pipe(
        finalize(() => {
          this.uploading = false;
          this.cdr.detectChanges();
        })
      )
      .subscribe({
        next: () => {
          this.selectedFile = null;
          this.successMessage = 'Receipt uploaded successfully.';
          this.loadReceipts();
        },
        error: () => {
          this.errorMessage = 'Unable to upload receipt.';
          this.loadReceipts();
        },
      });
  }

  openDeleteModal(id: number): void {
    this.receiptIdToDelete = id;
    this.showDeleteModal = true;
    this.errorMessage = '';
    this.successMessage = '';
  }

  closeDeleteModal(): void {
    this.showDeleteModal = false;
    this.receiptIdToDelete = null;
  }

  confirmDelete(): void {
    if (this.receiptIdToDelete === null) {
      return;
    }

    const id = this.receiptIdToDelete;

    this.deleting = true;
    this.errorMessage = '';
    this.successMessage = '';

    this.receiptService
      .deleteReceipt(id)
      .pipe(
        finalize(() => {
          this.deleting = false;
          this.cdr.detectChanges();
        })
      )
      .subscribe({
        next: () => {
          this.receipts = this.receipts.filter((receipt) => receipt.id !== id);
          this.successMessage = 'Receipt deleted successfully.';
          this.closeDeleteModal();
          this.loadReceipts();
        },
        error: () => {
          this.errorMessage = 'Unable to delete the receipt.';
          this.closeDeleteModal();
          this.loadReceipts();
        },
      });
  }
}