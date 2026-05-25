from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db, InventoryItem, PurchaseOrder

router = APIRouter(prefix="/api/inventory", tags=["inventory"])


@router.get("/")
def get_inventory(db: Session = Depends(get_db)):
    items = db.query(InventoryItem).all()
    return [
        {
            "id": i.id,
            "product": i.product_name,
            "category": i.category,
            "size": i.size,
            "stock": i.current_stock,
            "reorder_level": i.reorder_level,
            "max_stock": i.max_stock,
            "unit_cost": i.unit_cost,
            "selling_price": i.selling_price,
            "supplier": i.supplier_name,
            "status": "critical" if i.current_stock <= i.reorder_level else "healthy"
        }
        for i in items
    ]


@router.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(PurchaseOrder).order_by(PurchaseOrder.created_at.desc()).all()
    return [
        {
            "id": o.id,
            "product": o.product_name,
            "quantity": o.quantity,
            "supplier": o.supplier_name,
            "total_cost": o.total_cost,
            "status": o.status,
            "created_at": o.created_at,
            "notes": o.notes
        }
        for o in orders
    ]


@router.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str, db: Session = Depends(get_db)):
    order = db.query(PurchaseOrder).filter(PurchaseOrder.id == order_id).first()
    if not order:
        return {"error": "Order not found"}
    order.status = status
    db.commit()
    return {"message": f"Order {order_id} updated to {status}"}