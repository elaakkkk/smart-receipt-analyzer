export interface AnalyticsSummary {
  total_receipts: number;
  valid_receipts: number;
  invalid_receipts: number;
  unknown_documents: number;
  receipt_documents: number;
  invoice_documents: number;
}

export interface DocumentTypesStats {
  unknown: number;
  receipt: number;
  invoice: number;
}

export interface ValidationStats {
  valid: number;
  invalid: number;
  with_warnings: number;
  without_warnings: number;
}

export interface ChartDataItem {
  label: string;
  value: number;
}

export interface AnalyticsCharts {
  document_types: ChartDataItem[];
  validation_status: ChartDataItem[];
}

export interface MerchantSpendingItem {
  merchant_name: string;
  total_spent: number;
  receipt_count: number;
}

export interface MonthlySpendingItem {
  month: string;
  total_spent: number;
  receipt_count: number;
}

export interface TopProductItem {
  product_name: string;
  total_spent: number;
  quantity: number;
}

export interface CategorySpendingItem {
  category: string;
  total_spent: number;
}