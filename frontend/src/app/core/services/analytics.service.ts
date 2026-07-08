import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { API_BASE_URL } from '../constants/api.constants';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private readonly baseUrl = API_BASE_URL;

  constructor(private http: HttpClient) {}

  getAnalyticsSummary(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/api/analytics/summary`);
  }

  getDocumentTypes(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/api/analytics/document-types`);
  }

  getValidationStats(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/api/analytics/validation`);
  }

  getChartsData(): Observable<unknown> {
    return this.http.get(`${this.baseUrl}/api/analytics/charts`);
  }
}