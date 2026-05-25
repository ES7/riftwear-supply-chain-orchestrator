import json
import re
import pandas as pd
from groq import Groq
from datetime import datetime
from app.config import settings
from app.excel_loader import get_orders, get_products, get_expenses

client = Groq(api_key=settings.groq_api_key)


def run() -> dict:
    orders   = get_orders()
    products = get_products()
    expenses = get_expenses()

    orders_text   = orders[["Drop Name","Order Type","Product(s)","Qty","Selling Price (₹)"]].to_string(index=False)
    products_text = products[["Product Name","Drop","T-shirt Cost (₹)","Print Cost (₹)","Selling Price (₹)"]].to_string(index=False)

    drop_revenue = orders.groupby("Drop Name").apply(
        lambda x: round(pd.to_numeric(x["Selling Price (₹)"], errors="coerce").sum(), 2)
    ).to_dict()

    prompt = f"""You are the Demand Forecasting Agent for RIFT WEAR — a college clothing brand in India now expanding to Mumbai.

ORDER HISTORY:
{orders_text}

PRODUCT CATALOG:
{products_text}

REVENUE PER DROP:
{json.dumps(drop_revenue, indent=2)}

TODAY: {datetime.now().strftime("%B %Y")}

CONTEXT:
- Brand started in a college (IIT/NIT level), now expanding to Mumbai city-wide
- Drop model: limited time sales (10-14 days)
- Products: graphic tees, hoodies, caps, joggers, varsity jackets
- Custom orders are growing (friends, family, college departments)

Analyze patterns and forecast demand for the next drop.

Respond ONLY in this JSON format:
{{
  "forecast_period": "next drop (30 days)",
  "season_type": "peak/normal/off",
  "top_selling_products": ["product1", "product2"],
  "slow_moving_products": ["product1"],
  "recommended_drop_size": 25,
  "recommended_products": ["product1", "product2", "product3"],
  "price_recommendations": {{
    "GTA Tee": 649,
    "Hoodie": 1299
  }},
  "key_insights": ["insight1", "insight2", "insight3"],
  "mumbai_expansion_tips": ["tip1", "tip2"],
  "urgent_actions": ["action1", "action2"]
}}"""

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024,
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return json.loads(match.group()) if match else {"error": raw}
