from pydantic import BaseModel


class CostInfo(BaseModel):
    model: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float
    total_cost: float


class InvoiceData(BaseModel):
    invoice_id: str | None = None
    name: str | None = None
    from_entity: str | None = None
    to_entity: str | None = None
    amount: str | None = None
    cgst: str | None = None
    sgst: str | None = None
    invoice_generated_date: str | None = None
    cost: CostInfo | None = None
