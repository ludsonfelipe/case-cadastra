import asyncio
import os
from datetime import datetime
from typing import List

from dotenv import load_dotenv

from src.client.coincap_client import CoinCapClient
from src.model.sql_models import Base
from src.service.crypto_service import CryptoService
from src.util.db import engine, get_db
from src.util.logger import logger

load_dotenv()


async def main(
    asset_ids: List[str] = None,
    start_date: datetime = None,
    ingest_history: bool = True,
    ingest_market: bool = True,
    market_limit: int = 100,
    market_offset: int = 0,
):
    """
    Main function to ingest cryptocurrency data.

    Args:
        asset_ids: List of asset IDs to fetch data for. If None, defaults to ['bitcoin']
        start_date: Optional start date for historical data
        ingest_history: Whether to ingest price history data
        ingest_market: Whether to ingest market data
        market_limit: Number of market results to return (default is 100)
        market_offset: Number of market results to skip (default is 0)
    """
    if asset_ids is None:
        asset_ids = ["bitcoin"]

    # Initialize database
    Base.metadata.create_all(engine)

    # Get database session
    db = next(get_db())

    try:
        # Initialize service and client
        crypto_service = CryptoService(db)
        async with CoinCapClient(
            os.getenv(
                "COINCAP_API_KEY",
            )
        ) as client:
            # Ingest data for all specified assets
            await crypto_service.ingest_multiple_assets(
                client,
                asset_ids,
                start_date,
                ingest_history=ingest_history,
                ingest_market=ingest_market,
                market_limit=market_limit,
                market_offset=market_offset,
            )

    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Example usage with different options:

    # 1. Ingest both history and market data
    assets = ["bitcoin", "ethereum", "cardano"]
    start_date = datetime(2024, 1, 1)
    asyncio.run(main(assets, start_date))

    # 2. Ingest only history data
    # assets = ["bitcoin"]
    # start_date = datetime(2024, 1, 1)
    # asyncio.run(main(assets, start_date, ingest_market=False))

    # 3. Ingest only market data with pagination
    # assets = ["bitcoin"]
    # asyncio.run(main(assets, ingest_history=False, market_limit=50, market_offset=0))
