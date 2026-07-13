import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { FormsModule } from '@angular/forms';

import { AnalyticsService } from '../../core/services/analytics.service';
import {
  AnalyticsInsightsResponse,
  CategorySpendingItem,
  MerchantSpendingItem,
  MonthlySpendingItem,
  TopProductInsightItem,
} from '../../core/models/analytics.model';
import { PageState } from '../../shared/components/page-state/page-state';

@Component({
  selector: 'app-analytics',
  imports: [DecimalPipe, FormsModule, PageState],
  templateUrl: './analytics.html',
  styleUrl: './analytics.css',
})
export class Analytics implements OnInit {
  insights: AnalyticsInsightsResponse | null = null;

  merchantSpending: MerchantSpendingItem[] = [];
  monthlySpending: MonthlySpendingItem[] = [];
  topProducts: TopProductInsightItem[] = [];
  categorySpending: CategorySpendingItem[] = [];

  selectedPeriod = 'all';
  dateFrom = '';
  dateTo = '';
  selectedMerchant = '';
  selectedCategory = '';

  loading = false;
  errorMessage = '';

  showFilters = false;

  constructor(
    private analyticsService: AnalyticsService,
    private cdr: ChangeDetectorRef
  ) {}

  ngOnInit(): void {
    this.loadAnalytics();
  }

  loadAnalytics(): void {
    this.loading = true;
    this.errorMessage = '';

    this.analyticsService
      .getInsights({
        period: this.selectedPeriod,
        date_from: this.selectedPeriod === 'custom' ? this.dateFrom : '',
        date_to: this.selectedPeriod === 'custom' ? this.dateTo : '',
        merchant: this.selectedMerchant,
        category: this.selectedCategory,
      })
      .subscribe({
        next: (data) => {
          this.insights = data;
          this.merchantSpending = data.merchant_spending;
          this.monthlySpending = data.monthly_spending;
          this.topProducts = data.top_products;
          this.categorySpending = data.category_spending;

          this.loading = false;
          this.cdr.detectChanges();
        },
        error: () => {
          this.errorMessage = 'Unable to load analytics data.';
          this.loading = false;
          this.cdr.detectChanges();
        },
      });
  }

  resetFilters(): void {
    this.selectedPeriod = 'all';
    this.dateFrom = '';
    this.dateTo = '';
    this.selectedMerchant = '';
    this.selectedCategory = '';
    this.loadAnalytics();
  }

  get totalSpent(): number {
    return this.insights?.kpis.total_spent ?? 0;
  }

  get receiptsCount(): number {
    return this.insights?.kpis.receipt_count ?? 0;
  }

  get averageBasket(): number {
    return this.insights?.kpis.average_basket ?? 0;
  }

  get topMerchant(): string {
    return this.insights?.kpis.top_merchant ?? 'No data';
  }

  get topCategory(): string {
    const category = this.insights?.kpis.top_category;
    return category ? this.formatLabel(category) : 'No data';
  }

  get merchantOptions(): string[] {
    return this.merchantSpending.map((merchant) => merchant.merchant_name);
  }

  get categoryOptions(): string[] {
    return this.categorySpending.map((category) => category.category);
  }

  get maxMonthlySpending(): number {
    if (this.monthlySpending.length === 0) return 0;
    return Math.max(...this.monthlySpending.map((month) => month.total_spent));
  }

  get maxMerchantSpending(): number {
    if (this.merchantSpending.length === 0) return 0;
    return Math.max(...this.merchantSpending.map((merchant) => merchant.total_spent));
  }

  get maxProductSpending(): number {
    if (this.topProducts.length === 0) return 0;
    return Math.max(...this.topProducts.map((product) => product.total_spent));
  }

  getBarWidth(value: number, max: number): string {
    if (!max || max <= 0) return '0%';
    const percentage = Math.round((value / max) * 100);
    return `${Math.max(percentage, 4)}%`;
  }

  formatLabel(value: string): string {
    return value
      .split('_')
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(' ');
  }

  toggleFilters(): void {
    this.showFilters = !this.showFilters;
  }

  get activeFiltersCount(): number {
    let count = 0;

    if (this.selectedPeriod !== 'all') count++;
    if (this.selectedMerchant) count++;
    if (this.selectedCategory) count++;
    if (this.selectedPeriod === 'custom' && this.dateFrom) count++;
    if (this.selectedPeriod === 'custom' && this.dateTo) count++;

    return count;
  }

  get selectedPeriodLabel(): string {
    const labels: Record<string, string> = {
      all: 'All time',
      today: 'Today',
      this_month: 'This month',
      custom: 'Custom period',
    };

    return labels[this.selectedPeriod] ?? 'All time';
  }
}