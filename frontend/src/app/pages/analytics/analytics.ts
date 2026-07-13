import { ChangeDetectorRef, Component, OnInit } from '@angular/core';
import { DecimalPipe } from '@angular/common';
import { forkJoin } from 'rxjs';

import { AnalyticsService } from '../../core/services/analytics.service';
import {
  CategorySpendingItem,
  MerchantSpendingItem,
  MonthlySpendingItem,
  TopProductItem,
} from '../../core/models/analytics.model';
import { PageState } from '../../shared/components/page-state/page-state';

@Component({
  selector: 'app-analytics',
  imports: [DecimalPipe, PageState],
  templateUrl: './analytics.html',
  styleUrl: './analytics.css',
})
export class Analytics implements OnInit {
  merchantSpending: MerchantSpendingItem[] = [];
  monthlySpending: MonthlySpendingItem[] = [];
  topProducts: TopProductItem[] = [];
  categorySpending: CategorySpendingItem[] = [];

  loading = false;
  errorMessage = '';

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

    forkJoin({
      merchantSpending: this.analyticsService.getMerchantSpending(),
      monthlySpending: this.analyticsService.getMonthlySpending(),
      topProducts: this.analyticsService.getTopProducts(12),
      categorySpending: this.analyticsService.getCategorySpending(),
    }).subscribe({
      next: (data) => {
        this.merchantSpending = data.merchantSpending;
        this.monthlySpending = data.monthlySpending;
        this.topProducts = data.topProducts;
        this.categorySpending = data.categorySpending;

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

  get totalSpent(): number {
    return this.merchantSpending.reduce(
      (total, merchant) => total + merchant.total_spent,
      0
    );
  }

  get receiptsCount(): number {
    return this.merchantSpending.reduce(
      (total, merchant) => total + merchant.receipt_count,
      0
    );
  }

  get averageBasket(): number {
    if (this.receiptsCount === 0) return 0;
    return this.totalSpent / this.receiptsCount;
  }

  get topMerchant(): string {
    if (this.merchantSpending.length === 0) return 'No data';
    return this.merchantSpending[0].merchant_name;
  }

  get topCategory(): string {
    if (this.categorySpending.length === 0) return 'No data';
    return this.formatLabel(this.categorySpending[0].category);
  }

  get maxMonthlySpending(): number {
    if (this.monthlySpending.length === 0) return 0;

    return Math.max(
      ...this.monthlySpending.map((month) => month.total_spent)
    );
  }

  get maxCategorySpending(): number {
    if (this.categorySpending.length === 0) return 0;

    return Math.max(
      ...this.categorySpending.map((category) => category.total_spent)
    );
  }

  get maxMerchantSpending(): number {
    if (this.merchantSpending.length === 0) return 0;

    return Math.max(
      ...this.merchantSpending.map((merchant) => merchant.total_spent)
    );
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
}