import json
import re
from groq import Groq
from app.config import settings
from app.excel_loader import get_products, get_orders

client = Groq(api_key=settings.groq_api_key)


def run() -> dict:
    products = get_products()
    orders   = get_orders()

    # Units sold per product
    import pandas as pd
    sales_count = orders.groupby("Product(s)").apply(
        lambda x: pd.to_numeric(x["Qty"], errors="coerce").sum()
    ).to_dict()

    products_text = products[["Product Name","Drop","T-shirt Cost (₹)","Print Cost (₹)",
                               "Selling Price (₹)","Margin (₹)","Margin %","Vendor Used"]].to_string(index=False)

    prompt = f"""You are the Inventory & Profitability Agent for RIFT WEAR.

PRODUCT CATALOG WITH COSTS:
{products_text}

UNITS SOLD PER PRODUCT:
{json.dumps(sales_count, indent=2)}

Analyze profitability and inventory performance.

Respond ONLY in this JSON format:
{{
  "overall_health": "good/warning/critical",
  "most_profitable_product": "product name",
  "least_profitable_product": "product name",
  "best_seller": "product name",
  "worst_seller": "product name",
  "high_margin_products": [
    {{"product": "name", "margin_pct": "49%", "recommendation": "increase stock"}}
  ],
  "low_margin_products": [
    {{"product": "name", "margin_pct": "20%", "recommendation": "renegotiate or reprice"}}
  ],
  "vendor_comparison": {{
    "whiscoop_avg_cogs": 0.0,
    "okb_avg_cogs": 0.0,
    "savings_per_unit": 0.0
  }},
  "recommendations": ["rec1", "rec2", "rec3"],
  "summary": "one line summary"
}}"""

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return json.loads(match.group()) if match else {"error": raw}
