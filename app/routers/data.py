from fastapi import APIRouter
from app.excel_loader import (
    get_orders, get_expenses, get_products,
    get_vendors, get_business_summary
)

router = APIRouter(prefix="/api/data", tags=["data"])


@router.get("/summary")
def summary():
    return get_business_summary()


@router.get("/orders")
def orders():
    df = get_orders()
    return df.fillna("").to_dict(orient="records")


@router.get("/expenses")
def expenses():
    df = get_expenses()
    return df.fillna("").to_dict(orient="records")


@router.get("/products")
def products():
    df = get_products()
    return df.fillna("").to_dict(orient="records")


@router.get("/vendors")
def vendors():
    df = get_vendors()
    return df.fillna("").to_dict(orient="records")
