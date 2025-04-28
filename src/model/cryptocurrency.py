from datetime import datetime
from decimal import Decimal
from typing import List

from pydantic import BaseModel, Field


class TimeStampedModel(BaseModel):
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AssetHistory(TimeStampedModel):
    """
    Represents historical price data for a cryptocurrency asset.
    {
            "priceUsd": "62792.1302611715766342",
            "time": 1714348800000,
            "date": "2024-04-29T00:00:00.000Z"
        }
    """

    price_usd: Decimal = Field(
        ..., alias="priceUsd", description="Price of the asset in USD"
    )
    time: int = Field(..., description="Timestamp of the price data")
    date: datetime = Field(..., description="Date of the price data")


class Market(TimeStampedModel):
    """
    Represents a cryptocurrency market (trading pair).
    {
            "exchangeId": "Binance",
            "baseId": "bitcoin",
            "quoteId": "tether",
            "baseSymbol": "BTC",
            "quoteSymbol": "USDT",
            "volumeUsd24Hr": "1052454026.6015994220800000",
            "priceUsd": "94330.6106960000000000",
            "volumePercent": "17.1112453842931043"
        }

    """

    exchange_id: str = Field(..., alias="exchangeId", description="ID of the exchange")
    base_id: str = Field(..., alias="baseId", description="ID of the base asset")
    quote_id: str = Field(..., alias="quoteId", description="ID of the quote asset")
    base_symbol: str = Field(
        ..., alias="baseSymbol", description="Symbol of the base asset"
    )
    quote_symbol: str = Field(
        ..., alias="quoteSymbol", description="Symbol of the quote asset"
    )
    volume_usd_24h: Decimal = Field(
        ...,
        alias="volumeUsd24Hr",
        description="Volume in USD of the trading pair in the last 24 hours",
    )
    price_usd: Decimal = Field(
        ..., alias="priceUsd", description="Current price of the trading pair in USD"
    )
    volume_percent: Decimal = Field(
        ...,
        alias="volumePercent",
        description="Percent of the volume of the trading pair in the last 24 hours",
    )


class AssetHistoryResponse(BaseModel):
    """Response model for asset history endpoint"""

    data: List[AssetHistory]


class MarketResponse(BaseModel):
    """Response model for markets endpoint"""

    data: List[Market]
