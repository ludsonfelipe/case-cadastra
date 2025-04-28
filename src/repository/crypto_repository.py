from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from src.model.sql_models import AssetHistory, Market
from src.repository.base_repository import BaseRepository


class CryptoRepository(BaseRepository):
    def __init__(self, session: Session):
        super().__init__(session, AssetHistory)
        self.market_model = Market

    def get_asset_history_by_date_range(
        self, asset_id: str, start_date: datetime, end_date: datetime
    ) -> List[AssetHistory]:
        """Get asset history by date range."""
        query = select(AssetHistory).where(
            and_(
                AssetHistory.asset_id == asset_id,
                AssetHistory.date >= start_date,
                AssetHistory.date <= end_date,
            )
        )
        return self.session.execute(query).scalars().all()

    def insert_asset_history(
        self, asset_id: str, price_usd: float, date: datetime, time: int
    ) -> AssetHistory:
        """Insert a new asset history into the database."""
        asset_history = AssetHistory(
            asset_id=asset_id, price_usd=price_usd, date=date, time=time
        )
        return self.create(asset_history)

    def insert_asset_histories(
        self, histories: List[AssetHistory]
    ) -> List[AssetHistory]:
        """Insert multiple asset histories into the database."""
        return self.create_many(histories)

    def get_latest_date(self, asset_id: str) -> Optional[datetime]:
        query = (
            select(AssetHistory.date)
            .where(AssetHistory.asset_id == asset_id)
            .order_by(AssetHistory.date.desc())
            .limit(1)
        )
        result = self.session.execute(query).scalar_one_or_none()
        return result

    def insert_market(self, market: Market) -> Market:
        """Insert a new market into the database."""
        asset_market = Market(
            market_id=market.market_id,
            base_id=market.base_id,
            quote_id=market.quote_id,
            base_symbol=market.base_symbol,
            quote_symbol=market.quote_symbol,
            volume_usd_24h=market.volume_usd_24h,
            price_usd=market.price_usd,
            volume_percent=market.volume_percent,
        )
        return self.create(asset_market)

    def insert_markets(self, markets: List[Market]) -> List[Market]:
        """Insert multiple markets into the database."""
        return self.create_many(markets)
