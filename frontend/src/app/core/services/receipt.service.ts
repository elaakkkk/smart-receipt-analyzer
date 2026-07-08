import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../constants/api.constants';

@Injectable({
  providedIn: 'root'
})
export class ReceiptService {
  private readonly baseUrl = API_BASE_URL;

  constructor(private http: HttpClient) {}

  getReceipts(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/api/receipts`);
  }

  getReceiptById(id: number): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/api/receipts/${id}`);
  }

  uploadReceipt(file: File): Observable<unknown> {
    const formData = new FormData();
    formData.append('file', file);

    return this.http.post(`${this.baseUrl}/api/receipts/upload`, formData);
  }

  deleteReceipt(id: number): Observable<unknown> {
    return this.http.delete(`${this.baseUrl}/api/receipts/${id}`);
  }
}