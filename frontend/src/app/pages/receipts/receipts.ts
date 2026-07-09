import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { DatePipe } from '@angular/common';

import { ReceiptListItem } from '../../core/models/receipt.model';
import { ReceiptService } from '../../core/services/receipt.service';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-receipts',
  imports: [DatePipe, RouterLink],
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

    this.receiptService.getReceipts().subscribe({
      next: (data) => {
        this.receipts = data;
        this.loading = false;
        this.cdr.detectChanges();
      },
      error: () => {
        this.errorMessage = 'Unable to load receipts.';
        this.loading = false;
        this.cdr.detectChanges();
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

    this.receiptService.uploadReceipt(this.selectedFile).subscribe({
      next: () => {
        this.uploading = false;
        this.selectedFile = null;
        this.successMessage = 'Receipt uploaded successfully.';

        this.loadReceipts();
        this.cdr.detectChanges();
      },
      error: () => {
        this.uploading = false;
        this.errorMessage = 'Unable to upload receipt.';

        this.loadReceipts();
        this.cdr.detectChanges();
      },
      complete: () => {
        this.uploading = false;
        this.cdr.detectChanges();
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

    this.receiptService.deleteReceipt(id).subscribe({
      next: () => {
        this.deleting = false;
        this.receipts = this.receipts.filter((receipt) => receipt.id !== id);
        this.successMessage = 'Receipt deleted successfully.';
        this.closeDeleteModal();

        this.loadReceipts();
        this.cdr.detectChanges();
      },
      error: () => {
        this.deleting = false;
        this.errorMessage = 'Unable to delete the receipt.';
        this.closeDeleteModal();

        this.loadReceipts();
        this.cdr.detectChanges();
      },
      complete: () => {
        this.deleting = false;
        this.cdr.detectChanges();
      },
    });
  }
}