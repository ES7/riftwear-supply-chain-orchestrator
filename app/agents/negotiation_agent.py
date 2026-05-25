import json
import re
import pandas as pd
from groq import Groq
from app.config import settings
from app.excel_loader import get_vendors, get_expenses, get_orders

client = Groq(api_key=settings.groq_api_key)


def run() -> dict:
    vendors  = get_vendors()
    expenses = get_expenses()
    orders   = get_orders()

    total_units = pd.to_numeric(orders["Qty"], errors="coerce").sum()
    total_spend = pd.to_numeric(expenses["Amount (₹)"], errors="coerce").sum()

    vendors_text  = vendors.to_string(index=False)
    expenses_text = expenses[["Category","Drop / Event","Description","Amount (₹)","Vendor"]].to_string(index=False)

    prompt = f"""You are the Supplier Negotiation Agent for RIFT WEAR — a growing Indian clothing brand.

VENDOR DIRECTORY:
{vendors_text}

EXPENSE HISTORY:
{expenses_text}

BUSINESS CONTEXT:
- Total units sold so far: {int(total_units)}
- Total spend with vendors: Rs {round(float(total_spend), 2)}
- Brand is expanding from college to Mumbai city-wide
- Next drop target: 25-30 units
- Currently using OKB + Local Print Vendor (cheaper than Whiscoop)

Draft professional negotiation emails to:
1. Own Knighted Blank (OKB) - negotiate bulk discount for next drop
2. Local Print Vendor - negotiate better rate for 25+ units

Respond ONLY in valid JSON. No special characters, no newlines inside strings. Use \\n for line breaks in email body.

{{
  "emails": [
    {{
      "vendor_name": "Own Knighted Blank",
      "vendor_type": "T-shirt Wholesale",
      "subject": "Bulk Order Request - RIFT WEAR Drop 3",
      "body": "Dear OKB Team,\\n\\nWe are RIFT WEAR...",
      "current_rate": "Rs 187.8/unit",
      "target_rate": "Rs 170/unit",
      "order_quantity": 30,
      "negotiation_angle": "growing brand, consistent orders"
    }},
    {{
      "vendor_name": "Local Print Vendor",
      "vendor_type": "DTF Print",
      "subject": "Bulk Print Order - RIFT WEAR Drop 3",
      "body": "Dear Team,\\n\\nWe are placing a bulk order...",
      "current_rate": "Rs 157.14/unit",
      "target_rate": "Rs 140/unit",
      "order_quantity": 30,
      "negotiation_angle": "bulk order, repeat business"
    }}
  ],
  "potential_savings_per_drop": 850,
  "recommendation": "Switch fully to OKB and Local Print for all future drops"
}}"""

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content.strip()

    # Clean control characters
    raw = re.sub(r'[\x00-\x1f\x7f](?<![\n\t])', '', raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            cleaned = re.sub(r'[\x00-\x1f\x7f](?<![\n\t])', '', match.group())
            try:
                return json.loads(cleaned)
            except:
                pass
        return {
            "emails": [],
            "potential_savings_per_drop": 850,
            "recommendation": "Draft emails manually — AI response had formatting issues"
        }