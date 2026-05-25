import json
import re
from groq import Groq
from datetime import datetime
from app.config import settings
from app.excel_loader import get_orders, get_expenses

client = Groq(api_key=settings.groq_api_key)


def run() -> dict:
    orders   = get_orders()
    expenses = get_expenses()

    import pandas as pd
    # Revenue per drop
    drop_data = orders.groupby("Drop Name").agg(
        units=("Qty", lambda x: pd.to_numeric(x, errors="coerce").sum()),
        revenue=("Selling Price (₹)", lambda x: pd.to_numeric(x, errors="coerce").sum()),
    ).to_dict(orient="index")

    # Satisfaction scores from existing data
    satisfaction = {"Drop 1 - Aug'24": "50%", "Drop 2 - Oct'24": "80%"}

    prompt = f"""You are the Seasonal & Business Cycle Agent for RIFT WEAR.

DROP PERFORMANCE:
{json.dumps(drop_data, indent=2, default=str)}

CUSTOMER SATISFACTION PER DROP:
{json.dumps(satisfaction)}

BUSINESS CONTEXT:
- Drop 1 (Aug-Sep): ₹9,783 revenue, 50% satisfaction (delivery issues)
- Drop 2 (Oct): ₹2,935 revenue, 80% satisfaction (delivery improved)
- Drop 2 was shorter window + exam season = fewer orders
- Brand is now expanding from college to Mumbai city-wide
- No more in-person college delivery — need proper delivery logistics now

TODAY: {datetime.now().strftime("%B %Y")}

Analyze seasonal patterns for Indian college + Mumbai market and advise.

Respond ONLY in this JSON format:
{{
  "current_season": "season name",
  "season_score": 7,
  "best_drop_window": "month range",
  "worst_drop_window": "month range",
  "next_recommended_drop": "Month YYYY",
  "weeks_to_ideal_launch": 3,
  "drop_timing_calendar": [
    {{"month": "January", "score": 9, "reason": "College fest season"}},
    {{"month": "February", "score": 8, "reason": "Valentine + fests"}},
    {{"month": "March", "score": 5, "reason": "Exams starting"}},
    {{"month": "April", "score": 4, "reason": "Summer, low college activity"}},
    {{"month": "May", "score": 3, "reason": "Exams + summer"}},
    {{"month": "June", "score": 4, "reason": "New admissions"}},
    {{"month": "July", "score": 6, "reason": "New semester energy"}},
    {{"month": "August", "score": 8, "reason": "Fresh year, brand drops"}},
    {{"month": "September", "score": 6, "reason": "Mid-sem fests"}},
    {{"month": "October", "score": 8, "reason": "Diwali + fests"}},
    {{"month": "November", "score": 7, "reason": "Post-Diwali"}},
    {{"month": "December", "score": 5, "reason": "End sem exams"}}
  ],
  "mumbai_specific_advice": ["advice1", "advice2"],
  "delivery_recommendations": ["rec1", "rec2"],
  "pricing_strategy": "maintain/increase/discount",
  "marketing_suggestion": "one line for RIFT WEAR next drop"
}}"""

    response = client.chat.completions.create(
        model=settings.groq_model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1500,
    )

    raw = response.choices[0].message.content
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        return json.loads(match.group()) if match else {"error": raw}
