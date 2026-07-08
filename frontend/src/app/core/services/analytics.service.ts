import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { API_BASE_URL } from '../constants/api.constants';
import { AnalyticsCharts, AnalyticsSummary, DocumentTypesStats, ValidationStats } from '../models/analytics.model';

@Injectable({
  providedIn: 'root'
})
export class AnalyticsService {
  private readonly baseUrl = API_BASE_URL;

  constructor(private http: HttpClient) {}

  getAnalyticsSummary(): Observable<AnalyticsSummary> {
    return this.http.get<AnalyticsSummary>(`${this.baseUrl}/api/analytics/summary`);
  }

  getDocumentTypes(): Observable<DocumentTypesStats> {
    return this.http.get<DocumentTypesStats>(`${this.baseUrl}/api/analytics/document-types`);
  }

  getValidationStats(): Observable<ValidationStats> {
    return this.http.get<ValidationStats>(`${this.baseUrl}/api/analytics/validation`);
  }

  getChartsData(): Observable<AnalyticsCharts> {
    return this.http.get<AnalyticsCharts>(`${this.baseUrl}/api/analytics/charts`);
  }
}