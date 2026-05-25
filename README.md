# RIFT WEAR — AI Supply Chain Orchestrator

An AI-powered supply chain management system built for RIFT WEAR, a college clothing brand expanding to Mumbai. 5 specialized agents analyze real business data from Excel and autonomously make supply chain decisions.

## What it does

- **Demand Forecasting** — predicts next drop size based on historical sales patterns
- **Inventory & Profitability Analysis** — margin analysis, vendor cost comparison
- **Seasonal Cycle Planning** — optimal drop timing for Indian college + Mumbai market
- **Purchase Order Generation** — auto-generates POs for next drop
- **Supplier Negotiation** — drafts bulk discount emails to vendors

## Tech Stack

- **Backend** — FastAPI
- **AI** — Groq (Llama 3.3 70B)
- **Data** — Pandas + Excel (no database)
- **Frontend** — Vanilla JS + Tailwind CSS

## Setup

```bash
pip install -r requirements.txt
```

Create `.env` file:
```
GROQ_API_KEY=your_key_here
EXCEL_PATH=data.xlsx
GROQ_MODEL=llama-3.3-70b-versatile
```

Add your business data to `data.xlsx` and run:
```bash
uvicorn app.main:app --reload
```

Open `http://localhost:8000`

## Data Structure

All business data lives in `data.xlsx` with 6 sheets:
- **Orders** — every sale logged here
- **Expenses** — all costs tracked
- **Products** — catalog with COGS and margins
- **Vendors** — supplier directory
- **Drop Summary** — P&L per drop
- **Dashboard** — auto-calculated KPIs

## Results

Built on real RIFT WEAR data — 2 drops, 27 orders, ₹17,571 revenue across 3 months.

## Note

`data.xlsx` are excluded from this repo. Add your own data file following the sheet structure above.
