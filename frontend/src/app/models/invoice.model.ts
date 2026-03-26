export interface CostInfo {
  model: string;
  input_tokens: number;
  output_tokens: number;
  input_cost: number;
  output_cost: number;
  total_cost: number;
}

export interface LineItem {
  description: string | null;
  hsn_sac: string | null;
  quantity: string | null;
  unit_price: string | null;
  taxable_amount: string | null;
  tax_rate: string | null;
  line_total: string | null;
}

export interface InvoiceData {
  // Invoice Header
  invoice_number: string | null;
  invoice_date: string | null;
  place_of_supply: string | null;

  // Seller Details
  seller_name: string | null;
  seller_gstin: string | null;
  seller_address: string | null;

  // Buyer Details
  buyer_name: string | null;
  buyer_gstin: string | null;
  buyer_address: string | null;

  // Line Items
  line_items: LineItem[];

  // Tax & Totals
  sub_total: string | null;
  cgst_amount: string | null;
  sgst_amount: string | null;
  igst_amount: string | null;
  total_tax: string | null;
  total_amount: string | null;

  // Reference & Payment
  po_number: string | null;
  due_date: string | null;
  irn: string | null;

  // API Cost
  cost: CostInfo | null;
}
