export interface CostInfo {
  model: string;
  input_tokens: number;
  output_tokens: number;
  input_cost: number;
  output_cost: number;
  total_cost: number;
}

export interface InvoiceData {
  invoice_id: string | null;
  name: string | null;
  from_entity: string | null;
  to_entity: string | null;
  amount: string | null;
  cgst: string | null;
  sgst: string | null;
  invoice_generated_date: string | null;
  cost: CostInfo | null;
}
