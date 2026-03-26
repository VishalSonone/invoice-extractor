from pydantic import BaseModel


class CostInfo(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float


class LineItem(BaseModel):
    description: str | None = None
    hsn_sac: str | None = None
    quantity: str | None = None
    unit_price: str | None = None
    taxable_amount: str | None = None
    tax_rate: str | None = None
    line_total: str | None = None


class InvoiceData(BaseModel):
    # Invoice Header
    invoice_number: str | None = None
    invoice_date: str | None = None
    place_of_supply: str | None = None

    # Seller Details
    seller_name: str | None = None
    seller_gstin: str | None = None
    seller_address: str | None = None

    # Buyer Details
    buyer_name: str | None = None
    buyer_gstin: str | None = None
    buyer_address: str | None = None

    # Line Items
    line_items: list[LineItem] = []

    # Tax & Totals
    sub_total: str | None = None
    cgst_amount: str | None = None
    sgst_amount: str | None = None
    igst_amount: str | None = None
    total_tax: str | None = None
    total_amount: str | None = None

    # Reference & Payment
    po_number: str | None = None
    due_date: str | None = None
    irn: str | None = None

    # API Cost
    cost: CostInfo | None = None
