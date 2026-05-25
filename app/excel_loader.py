import pandas as pd
from app.config import EXCEL_PATH


def get_products() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="👕 Products", header=2)
    df = df.dropna(subset=["Product Name"])
    df.columns = df.columns.str.strip()
    return df


def get_orders() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="🛒 Orders", header=2)
    df = df.dropna(subset=["Order ID"])
    df.columns = df.columns.str.strip()

    # Build COGS lookup from Products sheet
    products = get_products()
    cogs_map = {}
    for _, row in products.iterrows():
        name = str(row["Product Name"]).strip()
        tshirt = pd.to_numeric(row.get("T-shirt Cost (₹)", 0), errors="coerce") or 0
        print_cost = pd.to_numeric(row.get("Print Cost (₹)", 0), errors="coerce") or 0
        cogs_map[name] = {"tshirt": tshirt, "print": print_cost}

    # Fill T-shirt Cost and Print Cost from Products lookup
    def get_tshirt_cost(row):
        product = str(row.get("Product(s)", "")).strip()
        qty = pd.to_numeric(row.get("Qty", 1), errors="coerce") or 1
        cost = cogs_map.get(product, {}).get("tshirt", 0)
        return cost * qty

    def get_print_cost(row):
        product = str(row.get("Product(s)", "")).strip()
        qty = pd.to_numeric(row.get("Qty", 1), errors="coerce") or 1
        cost = cogs_map.get(product, {}).get("print", 0)
        return cost * qty

    df["T-shirt Cost (₹)"] = df.apply(get_tshirt_cost, axis=1)
    df["Print Cost (₹)"]   = df.apply(get_print_cost, axis=1)
    df["Total COGS (₹)"]   = df["T-shirt Cost (₹)"] + df["Print Cost (₹)"]

    # Razorpay fee
    sell = pd.to_numeric(df["Selling Price (₹)"], errors="coerce").fillna(0)
    df["Razorpay Fee (₹)"] = df.apply(
        lambda r: round(sell[r.name] * 0.0256, 2) if r.get("Order Type") == "Site" else 0, axis=1
    )

    df["Amount Received (₹)"] = sell - df["Razorpay Fee (₹)"]
    df["Profit (₹)"]          = df["Amount Received (₹)"] - df["Total COGS (₹)"]

    return df


def get_expenses() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="💸 Expenses", header=2)
    df = df[df["Category"].notna() & (df["Category"] != "TOTAL EXPENSES")]
    df = df[df["Amount (₹)"].notna() & (df["Amount (₹)"] != "")]
    df.columns = df.columns.str.strip()
    return df


def get_vendors() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="🏭 Vendors", header=2)
    df = df.dropna(subset=["Vendor Name"])
    df.columns = df.columns.str.strip()
    return df


def get_drop_summary() -> pd.DataFrame:
    df = pd.read_excel(EXCEL_PATH, sheet_name="📊 Drop Summary", header=2)
    df.columns = df.columns.str.strip()
    return df


def get_business_summary() -> dict:
    orders   = get_orders()
    expenses = get_expenses()

    total_revenue  = pd.to_numeric(orders["Selling Price (₹)"], errors="coerce").sum()
    razorpay_fees  = pd.to_numeric(orders["Razorpay Fee (₹)"],  errors="coerce").sum()
    net_received   = pd.to_numeric(orders["Amount Received (₹)"],errors="coerce").sum()
    total_units    = pd.to_numeric(orders["Qty"],                errors="coerce").sum()
    total_cogs     = pd.to_numeric(orders["Total COGS (₹)"],     errors="coerce").sum()
    total_expenses = pd.to_numeric(expenses["Amount (₹)"],       errors="coerce").sum()

    # Net profit = revenue - razorpay - COGS - non-COGS expenses
    non_cogs_expenses = total_expenses - (
        expenses[expenses["Category"].isin(["T-Shirts","DTF Print"])]["Amount (₹)"]
        .pipe(pd.to_numeric, errors="coerce").sum()
    )
    net_profit = net_received - total_cogs - non_cogs_expenses

    drops = orders["Drop Name"].dropna().unique().tolist()

    return {
        "total_revenue":    round(float(total_revenue), 2),
        "razorpay_fees":    round(float(razorpay_fees), 2),
        "net_received":     round(float(net_received), 2),
        "total_units_sold": int(total_units),
        "total_expenses":   round(float(total_expenses), 2),
        "total_cogs":       round(float(total_cogs), 2),
        "net_profit":       round(float(net_profit), 2),
        "total_orders":     len(orders),
        "drops":            drops,
        "site_orders":      int((orders["Order Type"] == "Site").sum()),
        "custom_orders":    int((orders["Order Type"] == "Custom").sum()),
        "dept_orders":      int((orders["Order Type"] == "Dept").sum()),
    }
