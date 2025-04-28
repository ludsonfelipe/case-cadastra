from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from src.client.coincap_client import CoinCapClient
from src.model.sql_models import AssetHistory, Market
from src.repository.crypto_repository import CryptoRepository
from src.util.logger import logger


class CryptoService:
    def __init__(self, session: Session):
        self.crypto_repo = CryptoRepository(session)

    async def ingest_asset_history(
        self, client: CoinCapClient, asset_id: str, start_date: datetime = None
    ) -> None:
        """
        Ingest historical data for a specific asset.

        Args:
            client: CoinCapClient instance
            asset_id: The asset ID to fetch data for
            start_date: Optional start date. If not provided, will use the latest date in DB or default to 2018
        """
        try:
            # Get the latest date in our database if no start_date provided
            if not start_date:
                latest_date = self.crypto_repo.get_latest_date(asset_id)
                if latest_date:
                    start_date = latest_date + timedelta(days=1)
                    logger.info(
                        f"Found existing data until {latest_date}, fetching from {start_date}"
                    )
                else:
                    start_date = datetime(2018, 1, 1)
                    logger.info(f"No existing data found, starting from {start_date}")

            # End date is yesterday (to ensure we have complete data)
            end_date = datetime.now() - timedelta(days=1)

            # Convert dates to milliseconds for API
            start_ms = int(start_date.timestamp() * 1000)
            end_ms = int(end_date.timestamp() * 1000)

            logger.info(
                f"Fetching history for {asset_id} from {start_date} to {end_date}"
            )
            history_data = await client.get_history(
                asset_id=asset_id, interval="d1", start=start_ms, end=end_ms
            )

            if not history_data:
                logger.warning(f"No new data found for {asset_id}")
                return

            # Get existing records for the date range
            existing_records = self.crypto_repo.get_asset_history_by_date_range(
                asset_id, start_date, end_date
            )
            existing_dates = {record.date for record in existing_records}

            # Convert API data to database models, filtering out existing records
            db_models = []
            for item in history_data:
                record_date = datetime.fromtimestamp(item.time / 1000)
                if record_date not in existing_dates:
                    db_model = AssetHistory(
                        asset_id=asset_id,
                        price_usd=float(item.price_usd),
                        date=record_date,
                        time=item.time,
                    )
                    db_models.append(db_model)

            if not db_models:
                logger.info(f"No new records to insert for {asset_id}")
                return

            # Insert into database
            logger.info(
                f"Inserting {len(db_models)} new records for {asset_id} into database"
            )
            self.crypto_repo.insert_asset_histories(db_models)
            logger.info(f"Data ingestion completed successfully for {asset_id}")

        except Exception as e:
            logger.error(f"Error during data ingestion for {asset_id}: {str(e)}")
            raise

    async def ingest_market_data(
        self, client: CoinCapClient, asset_id: str, limit: int = 100, offset: int = 0
    ) -> None:
        """
        Ingest market data for a specific asset.

        Args:
            client: CoinCapClient instance
            asset_id: The asset ID to fetch market data for
            limit: Number of results to return (default is 100)
            offset: Number of results to skip (default is 0)
        """
        try:
            logger.info(
                f"Fetching market data for {asset_id} with limit={limit}, offset={offset}"
            )
            market_data = await client.get_markets(asset_id, limit=limit, offset=offset)

            if not market_data:
                logger.warning(f"No market data found for {asset_id}")
                return

            # Convert API data to database models
            db_models = []
            for market in market_data:
                db_model = Market(
                    exchange_id=market.exchange_id,
                    base_id=market.base_id,
                    quote_id=market.quote_id,
                    base_symbol=market.base_symbol,
                    quote_symbol=market.quote_symbol,
                    volume_usd_24h=market.volume_usd_24h,
                    price_usd=market.price_usd,
                    volume_percent=market.volume_percent,
                )
                db_models.append(db_model)

            if not db_models:
                logger.info(f"No market records to insert for {asset_id}")
                return

            # Insert into database
            logger.info(
                f"Inserting {len(db_models)} market records for {asset_id} into database"
            )
            self.crypto_repo.insert_markets(db_models)
            logger.info(f"Market data ingestion completed successfully for {asset_id}")

        except Exception as e:
            logger.error(f"Error during market data ingestion for {asset_id}: {str(e)}")
            raise

    async def ingest_multiple_assets(
        self,
        client: CoinCapClient,
        asset_ids: List[str],
        start_date: datetime = None,
        ingest_history: bool = True,
        ingest_market: bool = True,
        market_limit: int = 100,
        market_offset: int = 0,
    ) -> None:
        """
        Ingest historical data for multiple assets.

        Args:
            client: CoinCapClient instance
            asset_ids: List of asset IDs to fetch data for
            start_date: Optional start date for all assets
            ingest_history: Whether to ingest price history data
            ingest_market: Whether to ingest market data
            market_limit: Number of market results to return (default is 100)
            market_offset: Number of market results to skip (default is 0)
        """
        for asset_id in asset_ids:
            try:
                if ingest_history:
                    await self.ingest_asset_history(client, asset_id, start_date)
                if ingest_market:
                    await self.ingest_market_data(
                        client, asset_id, limit=market_limit, offset=market_offset
                    )
            except Exception as e:
                logger.error(f"Failed to ingest data for {asset_id}: {str(e)}")
                # Continue with next asset even if one fails
                continue
