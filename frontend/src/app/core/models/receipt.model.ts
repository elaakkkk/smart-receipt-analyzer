export interface ExtractedReceiptData {
  merchant_name: string;
  purchase_date: string | null;
  total_amount: number | null;
  currency: string | null;
  items: unknown[];
}

export interface ValidationResult {
  is_valid: boolean;
  errors: string[];
  warnings: string[];
}

export interface ReceiptListItem {
  id: number;
  original_filename: string;
  content_type: string;
  saved_path: string;
  document_type: string | null;
  created_at: string;
}

export interface ReceiptDetail extends ReceiptListItem {
  extracted_text: string | null;
  structured_data: ExtractedReceiptData | null;
  validation_result: ValidationResult | null;
}

export interface UploadReceiptResponse {
  receipt_id: number;
  filename: string;
  content_type: string;
  saved_path: string;
  extracted_text: string;
  document_type: string | null;
  structured_data: ExtractedReceiptData
  validation_result: ValidationResult
  message: string;
}

export interface DeleteReceiptResponse {
  receipt_id: number;
  message: string;
}