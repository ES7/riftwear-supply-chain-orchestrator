from app.database import SessionLocal, InventoryItem, SalesRecord, init_db

def seed():
    init_db()
    db = SessionLocal()

    if db.query(InventoryItem).first():
        db.close()
        return

    # RIFT WEAR product catalog
    products = [
        {"product_name": "RIFT Classic Tee",      "category": "tshirts",  "size": "S",   "current_stock": 15,  "reorder_level": 20, "max_stock": 150, "unit_cost": 280,  "selling_price": 599,  "supplier_name": "Mumbai Threads Co.",    "supplier_email": "supplier@mumbai-threads.com"},
        {"product_name": "RIFT Classic Tee",      "category": "tshirts",  "size": "M",   "current_stock": 8,   "reorder_level": 20, "max_stock": 150, "unit_cost": 280,  "selling_price": 599,  "supplier_name": "Mumbai Threads Co.",    "supplier_email": "supplier@mumbai-threads.com"},
        {"product_name": "RIFT Classic Tee",      "category": "tshirts",  "size": "L",   "current_stock": 22,  "reorder_level": 20, "max_stock": 150, "unit_cost": 280,  "selling_price": 599,  "supplier_name": "Mumbai Threads Co.",    "supplier_email": "supplier@mumbai-threads.com"},
        {"product_name": "RIFT Classic Tee",      "category": "tshirts",  "size": "XL",  "current_stock": 30,  "reorder_level": 20, "max_stock": 150, "unit_cost": 280,  "selling_price": 599,  "supplier_name": "Mumbai Threads Co.",    "supplier_email": "supplier@mumbai-threads.com"},
        {"product_name": "RIFT Oversized Hoodie", "category": "hoodies",  "size": "M",   "current_stock": 5,   "reorder_level": 15, "max_stock": 100, "unit_cost": 520,  "selling_price": 1199, "supplier_name": "Delhi Fabric House",    "supplier_email": "orders@delhifabric.com"},
        {"product_name": "RIFT Oversized Hoodie", "category": "hoodies",  "size": "L",   "current_stock": 3,   "reorder_level": 15, "max_stock": 100, "unit_cost": 520,  "selling_price": 1199, "supplier_name": "Delhi Fabric House",    "supplier_email": "orders@delhifabric.com"},
        {"product_name": "RIFT Oversized Hoodie", "category": "hoodies",  "size": "XL",  "current_stock": 18,  "reorder_level": 15, "max_stock": 100, "unit_cost": 520,  "selling_price": 1199, "supplier_name": "Delhi Fabric House",    "supplier_email": "orders@delhifabric.com"},
        {"product_name": "RIFT Cargo Joggers",    "category": "bottoms",  "size": "M",   "current_stock": 25,  "reorder_level": 10, "max_stock": 80,  "unit_cost": 450,  "selling_price": 999,  "supplier_name": "Surat Stitch Works",    "supplier_email": "info@suratstitch.com"},
        {"product_name": "RIFT Cargo Joggers",    "category": "bottoms",  "size": "L",   "current_stock": 12,  "reorder_level": 10, "max_stock": 80,  "unit_cost": 450,  "selling_price": 999,  "supplier_name": "Surat Stitch Works",    "supplier_email": "info@suratstitch.com"},
        {"product_name": "RIFT Snapback Cap",     "category": "caps",     "size": "ONE", "current_stock": 4,   "reorder_level": 10, "max_stock": 60,  "unit_cost": 180,  "selling_price": 449,  "supplier_name": "Mumbai Threads Co.",    "supplier_email": "supplier@mumbai-threads.com"},
        {"product_name": "RIFT Varsity Jacket",   "category": "jackets",  "size": "L",   "current_stock": 6,   "reorder_level": 8,  "max_stock": 50,  "unit_cost": 980,  "selling_price": 2199, "supplier_name": "Delhi Fabric House",    "supplier_email": "orders@delhifabric.com"},
        {"product_name": "RIFT Varsity Jacket",   "category": "jackets",  "size": "XL",  "current_stock": 9,   "reorder_level": 8,  "max_stock": 50,  "unit_cost": 980,  "selling_price": 2199, "supplier_name": "Delhi Fabric House",    "supplier_email": "orders@delhifabric.com"},
    ]

    for p in products:
        db.add(InventoryItem(**p))

    # Historical sales data — seasonal patterns
    sales = [
        # Festive season (Oct-Nov) — peak
        {"product_name": "RIFT Classic Tee",      "quantity_sold": 85,  "month": "2024-10", "season": "peak",   "revenue": 50915.0},
        {"product_name": "RIFT Oversized Hoodie", "quantity_sold": 60,  "month": "2024-10", "season": "peak",   "revenue": 71940.0},
        {"product_name": "RIFT Varsity Jacket",   "quantity_sold": 35,  "month": "2024-10", "season": "peak",   "revenue": 76965.0},
        {"product_name": "RIFT Classic Tee",      "quantity_sold": 90,  "month": "2024-11", "season": "peak",   "revenue": 53910.0},
        {"product_name": "RIFT Oversized Hoodie", "quantity_sold": 72,  "month": "2024-11", "season": "peak",   "revenue": 86328.0},
        # Winter (Dec-Jan) — high for hoodies/jackets
        {"product_name": "RIFT Oversized Hoodie", "quantity_sold": 95,  "month": "2024-12", "season": "peak",   "revenue": 113905.0},
        {"product_name": "RIFT Varsity Jacket",   "quantity_sold": 48,  "month": "2024-12", "season": "peak",   "revenue": 105552.0},
        {"product_name": "RIFT Classic Tee",      "quantity_sold": 40,  "month": "2024-12", "season": "normal", "revenue": 23960.0},
        # Summer (Mar-Jun) — slow for hoodies
        {"product_name": "RIFT Classic Tee",      "quantity_sold": 110, "month": "2024-04", "season": "peak",   "revenue": 65890.0},
        {"product_name": "RIFT Snapback Cap",     "quantity_sold": 45,  "month": "2024-04", "season": "peak",   "revenue": 20205.0},
        {"product_name": "RIFT Oversized Hoodie", "quantity_sold": 18,  "month": "2024-04", "season": "off",    "revenue": 21582.0},
        {"product_name": "RIFT Cargo Joggers",    "quantity_sold": 55,  "month": "2024-04", "season": "normal", "revenue": 54945.0},
        # College fest season (Jan-Feb)
        {"product_name": "RIFT Classic Tee",      "quantity_sold": 130, "month": "2024-02", "season": "peak",   "revenue": 77870.0},
        {"product_name": "RIFT Snapback Cap",     "quantity_sold": 70,  "month": "2024-02", "season": "peak",   "revenue": 31430.0},
        {"product_name": "RIFT Cargo Joggers",    "quantity_sold": 65,  "month": "2024-02", "season": "peak",   "revenue": 64935.0},
    ]

    for s in sales:
        db.add(SalesRecord(**s))

    db.commit()
    db.close()
    print("✓ RIFT WEAR database seeded successfully")