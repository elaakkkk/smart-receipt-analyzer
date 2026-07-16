import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../constants/api.constants';
import {
  DeleteReceiptResponse,
  ExtractedReceiptData,
  ReceiptDetail,
  ReceiptListItem,
  UploadReceiptResponse
} from '../models/receipt.model';

@Injectable({
  providedIn: 'root'
})
export class ReceiptService {
  private readonly baseUrl = API_BASE_URL;

  constructor(private http: HttpClient) {}

  getReceipts(): Observable<ReceiptListItem[]> {
    return this.http.get<ReceiptListItem[]>(`${this.baseUrl}/api/receipts/`);
  }

  getReceiptById(id: number): Observable<ReceiptDetail> {
    return this.http.get<ReceiptDetail>(`${this.baseUrl}/api/receipts/${id}`);
  }

  uploadReceipt(file: File): Observable<UploadReceiptResponse> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post<UploadReceiptResponse>(
      `${this.baseUrl}/api/receipts/upload`,
      formData
    );
  }

  deleteReceipt(id: number): Observable<DeleteReceiptResponse> {
    return this.http.delete<DeleteReceiptResponse>(
      `${this.baseUrl}/api/receipts/${id}`
    );
  }

  updateStructuredData(
    id: number,
    structuredData: ExtractedReceiptData
  ): Observable<ReceiptDetail> {
    return this.http.patch<ReceiptDetail>(
      `${this.baseUrl}/api/receipts/${id}/structured-data`,
      {
        structured_data: structuredData,
      }
    );
  }
}