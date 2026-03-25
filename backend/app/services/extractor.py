import base64
import json
import re

import anthropic

from app.config import ANTHROPIC_API_KEY, MODEL_NAME
from app.models.invoice import CostInfo, InvoiceData

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

EXTRACTION_PROMPT = (
    "Extract the following fields from this invoice and return ONLY valid JSON "
    "(no markdown, no explanation, no code fences):\n"
    "- invoiceId\n"
    "- name (the person or company the invoice is for)\n"
    "- from (the sender/seller)\n"
    "- to (the recipient/buyer)\n"
    "- amount (the total amount due)\n"
    "- cgst (CGST tax amount)\n"
    "- sgst (SGST tax amount)\n"
    "- invoiceGeneratedDate (the date the invoice was created)\n\n"
    "If a field cannot be found, set it to null."
)


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
        max_tokens=1024,
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

    return InvoiceData(
        invoice_id=to_str(data.get("invoiceId")),
        name=to_str(data.get("name")),
        from_entity=to_str(data.get("from")),
        to_entity=to_str(data.get("to")),
        amount=to_str(data.get("amount")),
        cgst=to_str(data.get("cgst")),
        sgst=to_str(data.get("sgst")),
        invoice_generated_date=to_str(data.get("invoiceGeneratedDate")),
        cost=cost,
    )
