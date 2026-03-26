import base64
import json
import re

import anthropic

from app.config import ANTHROPIC_API_KEY, MODEL_NAME
from app.models.invoice import CostInfo, InvoiceData, LineItem

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

EXTRACTION_PROMPT = """Extract the following fields from this invoice and return ONLY valid JSON (no markdown, no explanation, no code fences).

Return this exact structure:
{
  "invoiceNumber": "string or null",
  "invoiceDate": "string or null",
  "placeOfSupply": "string or null",
  "sellerName": "string or null",
  "sellerGstin": "string or null",
  "sellerAddress": "string or null",
  "buyerName": "string or null",
  "buyerGstin": "string or null",
  "buyerAddress": "string or null",
  "lineItems": [
    {
      "description": "string",
      "hsnSac": "string or null",
      "quantity": "string or null",
      "unitPrice": "string or null",
      "taxableAmount": "string or null",
      "taxRate": "string or null",
      "lineTotal": "string or null"
    }
  ],
  "subTotal": "string or null",
  "cgstAmount": "string or null (only for intra-state)",
  "sgstAmount": "string or null (only for intra-state)",
  "igstAmount": "string or null (only for inter-state)",
  "totalTax": "string or null",
  "totalAmount": "string or null",
  "poNumber": "string or null",
  "dueDate": "string or null",
  "irn": "string or null"
}

Rules:
- Keep monetary values as strings with original formatting (e.g. "35,918.73")
- For tax fields: use cgstAmount/sgstAmount for intra-state, igstAmount for inter-state. Set unused ones to null.
- lineItems should contain ALL items listed in the invoice
- If a field cannot be found, set it to null
- Return ONLY the JSON object, nothing else"""


def _parse_json(text: str) -> dict:
    """Extract JSON from LLM response, stripping markdown fences if present."""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1).strip())

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return json.loads(match.group(0))

    raise ValueError(f"Could not parse JSON from response: {text[:200]}")


def extract_invoice(pdf_bytes: bytes) -> InvoiceData:
    base64_pdf = base64.standard_b64encode(pdf_bytes).decode("utf-8")

    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=4096,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "document",
                        "source": {
                            "type": "base64",
                            "media_type": "application/pdf",
                            "data": base64_pdf,
                        },
                    },
                    {
                        "type": "text",
                        "text": EXTRACTION_PROMPT,
                    },
                ],
            }
        ],
    )

    input_tokens = message.usage.input_tokens
    output_tokens = message.usage.output_tokens
    input_cost = input_tokens * 3.00 / 1_000_000
    output_cost = output_tokens * 15.00 / 1_000_000
    total_cost = input_cost + output_cost

    cost = CostInfo(
        model=MODEL_NAME,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        input_cost=round(input_cost, 6),
        output_cost=round(output_cost, 6),
        total_cost=round(total_cost, 6),
    )

    response_text = message.content[0].text
    data = _parse_json(response_text)

    def to_str(val):
        return str(val) if val is not None else None

    raw_items = data.get("lineItems") or []
    line_items = [
        LineItem(
            description=to_str(item.get("description")),
            hsn_sac=to_str(item.get("hsnSac")),
            quantity=to_str(item.get("quantity")),
            unit_price=to_str(item.get("unitPrice")),
            taxable_amount=to_str(item.get("taxableAmount")),
            tax_rate=to_str(item.get("taxRate")),
            line_total=to_str(item.get("lineTotal")),
        )
        for item in raw_items
    ]

    return InvoiceData(
        invoice_number=to_str(data.get("invoiceNumber")),
        invoice_date=to_str(data.get("invoiceDate")),
        place_of_supply=to_str(data.get("placeOfSupply")),
        seller_name=to_str(data.get("sellerName")),
        seller_gstin=to_str(data.get("sellerGstin")),
        seller_address=to_str(data.get("sellerAddress")),
        buyer_name=to_str(data.get("buyerName")),
        buyer_gstin=to_str(data.get("buyerGstin")),
        buyer_address=to_str(data.get("buyerAddress")),
        line_items=line_items,
        sub_total=to_str(data.get("subTotal")),
        cgst_amount=to_str(data.get("cgstAmount")),
        sgst_amount=to_str(data.get("sgstAmount")),
        igst_amount=to_str(data.get("igstAmount")),
        total_tax=to_str(data.get("totalTax")),
        total_amount=to_str(data.get("totalAmount")),
        po_number=to_str(data.get("poNumber")),
        due_date=to_str(data.get("dueDate")),
        irn=to_str(data.get("irn")),
        cost=cost,
    )
