from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Numeric, PrimaryKeyConstraint, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AssetHistory(Base):
    """SQLAlchemy model for asset price history."""

    __tablename__ = "asset_history"
    __table_args__ = (
        PrimaryKeyConstraint("asset_id", "date", name="asset_history_pkey"),
    )

    asset_id = Column(String, nullable=False)
    price_usd = Column(Numeric(20, 8), nullable=False)
    date = Column(DateTime, nullable=False)
    time = Column(Integer, nullable=False)
    created_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )


class Market(Base):
    """SQLAlchemy model for cryptocurrency markets."""

    __tablename__ = "markets"
    __table_args__ = (
        PrimaryKeyConstraint(
            "base_id", "quote_id", "exchange_id", "created_at", name="markets_pkey"
        ),
    )

    exchange_id = Column(String, nullable=False)
    base_id = Column(String, nullable=False)
    quote_id = Column(String, nullable=False)
    base_symbol = Column(String, nullable=False)
    quote_symbol = Column(String, nullable=False)
    volume_usd_24h = Column(Numeric, nullable=False)
    price_usd = Column(Numeric, nullable=False)
    volume_percent = Column(Numeric, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
