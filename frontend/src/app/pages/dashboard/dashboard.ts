import { Component, OnInit } from '@angular/core';
import { AnalyticsService } from '../../core/services/analytics.service';
import { AnalyticsCharts, AnalyticsSummary, DocumentTypesStats, ValidationStats } from '../../core/models/analytics.model';

@Component({
  selector: 'app-dashboard',
  imports: [],
  templateUrl: './dashboard.html',
  styleUrl: './dashboard.css',
})
export class Dashboard implements OnInit{
  summary: AnalyticsSummary | null = null;
  documentTypes: DocumentTypesStats | null = null;
  validationStats: ValidationStats | null = null;
  chartsData: AnalyticsCharts | null = null;

  loading = false;
  errorMessage = '';

  constructor(
    private analyticsService: AnalyticsService,
  ){}
  ngOnInit(): void {
    this.loadDashboardData();
  }

  loadDashboardData(): void {
    this.loading = true;
    this.errorMessage = '';

    this.analyticsService.getAnalyticsSummary().subscribe({
      next: (data) => {
        this.summary = data;
        this.loading = false;
      },
      error: () => {
        this.errorMessage = 'Unable to load dashboard summary.';
        this.loading = false;
      },
    });

    this.analyticsService.getDocumentTypes().subscribe({
      next: (data) => {
        this.documentTypes = data;
      },
      error : () => {
        this.errorMessage = 'Unable to load document type statistics.';
      },
    });

    this.analyticsService.getValidationStats().subscribe({
      next: (data) => {
        this.validationStats= data ;
      },
      error: () => {
        this.errorMessage = 'Unable to load validation stats.'
      },
    });
  }
}
