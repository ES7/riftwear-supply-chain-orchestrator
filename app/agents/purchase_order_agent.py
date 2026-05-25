import json
import re
from groq import Groq
from datetime import datetime
from app.config import settings
from app.excel_loader import get_products, get_vendors, get_orders

client = Groq(api_key=settings.groq_api_key)


def run(drop_name: str = "Drop 3 - Mumbai", target_units: int = 25) -> dict:
    products = get_products()
    vendors  = get_vendors()
    orders   = get_orders()

    import pandas as pd
    # Best selling products from history
    sales = orders.groupby("Product(s)").apply(
        lambda x: pd.to_numeric(x["Qty"], errors="coerce").sum()
    ).sort_values(ascending=False).to_dict()

    products_text = products[["Product Name","Drop","T-shirt Cost (₹)","Print Cost (₹)",
                               "Selling Price (₹)","Vendor Used"]].to_string(index=False)

    prompt = f"""You are the Purchase Order Agent for RIFT WEAR.

PRODUCT CATALOG:
{products_text}

HISTORICAL SALES (units sold per product):
{json.dumps(sales, indent=2)}

NEW DROP DETAILS:
- Drop Name: {drop_name}
- Target Units: {target_units}
- Date: {datetime.now().strftime("%B %Y")}
- Context: Expanding to Mumbai, mix of site + custom orders expected

Generate purchase orders for the next drop. Use OKB for t-shirts and Local Print Vendor for DTF printing (cheaper than Whiscoop).

Respond ONLY in this JSON format:
{{
  "drop_name": "{drop_name}",
  "total_units_to_order": {target_units},
  "purchase_orders": [
    {{
      "po_number": "PO-RW-003-001",
      "vendor": "Own Knighted Blank",
      "vendor_type": "T-Shirts",
      "items": [
        {{"product": "GTA Tee", "qty": 5, "unit_cost": 187.8, "total": 939}},
        {{"product": "Anime Tee", "qty": 8, "unit_cost": 187.8, "total": 1502.4}}
      ],
      "subtotal": 0.0,
      "expected_delivery_days": 7,
      "notes": "Request bulk discount"
    }},
    {{
      "po_number": "PO-RW-003-002",
      "vendor": "Local Print Vendor",
      "vendor_type": "DTF Print",
      "items": [
        {{"product": "GTA Tee print", "qty": 5, "unit_cost": 157.14, "total": 785.7}}
      ],
      "subtotal": 0.0,
      "expected_delivery_days": 5,
      "notes": "Match t-shirt quantities exactly"
    }}
  ],
  "total_cogs_estimate": 0.0,
  "expected_revenue": 0.0,
  "expected_profit": 0.0,
  "recommended_launch_date": "date string"
}}"""

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=2048,
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return json.loads(match.group()) if match else {"error": raw}
