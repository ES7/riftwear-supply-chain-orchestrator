from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from app.config import settings

engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()


class InventoryItem(Base):
    __tablename__ = "inventory"
    id            = Column(Integer, primary_key=True, index=True)
    product_name  = Column(String, nullable=False)
    category      = Column(String)          # tshirts, hoodies, caps, etc
    size          = Column(String)          # S, M, L, XL, XXL
    current_stock = Column(Integer, default=0)
    reorder_level = Column(Integer, default=20)
    max_stock     = Column(Integer, default=200)
    unit_cost     = Column(Float, default=0.0)
    selling_price = Column(Float, default=0.0)
    supplier_name = Column(String)
    supplier_email= Column(String)
    last_updated  = Column(DateTime, default=datetime.utcnow)


class PurchaseOrder(Base):
    __tablename__ = "purchase_orders"
    id            = Column(Integer, primary_key=True, index=True)
    product_name  = Column(String)
    quantity      = Column(Integer)
    supplier_name = Column(String)
    supplier_email= Column(String)
    status        = Column(String, default="draft")   # draft, sent, confirmed
    total_cost    = Column(Float)
    created_at    = Column(DateTime, default=datetime.utcnow)
    notes         = Column(Text)


class AgentLog(Base):
    __tablename__ = "agent_logs"
    id         = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String)
    action     = Column(String)
    result     = Column(Text)
    timestamp  = Column(DateTime, default=datetime.utcnow)


class SalesRecord(Base):
    __tablename__ = "sales"
    id           = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    quantity_sold= Column(Integer)
    month        = Column(String)    # "2024-01", "2024-02"
    season       = Column(String)    # peak, off, normal
    revenue      = Column(Float)


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()