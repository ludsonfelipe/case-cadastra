from datetime import datetime, timezone
from decimal import Decimal

import pytest

from src.model.cryptocurrency import (
    AssetHistory,
    AssetHistoryResponse,
    Market,
    MarketResponse,
)


@pytest.fixture
def sample_history_dict():
    return {
        "priceUsd": "62792.13",
        "time": 1714348800000,
        "date": "2024-04-29T00:00:00.000Z",
    }


def test_asset_history_model(sample_history_dict):
    ah = AssetHistory.model_validate(sample_history_dict)
    assert ah.price_usd == Decimal("62792.13")
    assert isinstance(ah.date, datetime)
    # timestamp int mantido
    assert ah.time == 1714348800000


@pytest.fixture
def sample_market_dict():
    return {
        "exchangeId": "binance",
        "baseId": "bitcoin",
        "quoteId": "tether",
        "baseSymbol": "BTC",
        "quoteSymbol": "USDT",
        "volumeUsd24Hr": "1052454026.6015994220800000",
        "priceUsd": "94330.6106960000000000",
        "volumePercent": "17.1112453842931043",
    }


def test_market_model_happy_path(sample_market_dict):
    m = Market.model_validate(sample_market_dict)
    assert m.exchange_id == "binance"
    assert m.base_id == "bitcoin"
    assert m.quote_id == "tether"
    assert m.base_symbol == "BTC"
    assert m.quote_symbol == "USDT"
    assert m.volume_usd_24h == Decimal("1052454026.6015994220800000")
    assert m.price_usd == Decimal("94330.6106960000000000")
    assert m.volume_percent == Decimal("17.1112453842931043")


def test_market_missing_required_field(sample_market_dict):
    bad = sample_market_dict.copy()
    del bad["exchangeId"]
    with pytest.raises(ValueError):
        Market.model_validate(bad)


def test_market_invalid_type(sample_market_dict):
    bad = sample_market_dict.copy()
    bad["exchangeId"] = 123
    with pytest.raises(ValueError):
        Market.model_validate(bad)


def test_history_model_happy_path(sample_history_dict):
    h = AssetHistory.model_validate(sample_history_dict)
    assert h.price_usd == Decimal("62792.13")
    assert h.time == 1714348800000
    assert h.date == datetime(2024, 4, 29, 0, 0, 0, tzinfo=timezone.utc)


def test_history_missing_required_field(sample_history_dict):
    bad = sample_history_dict.copy()
    del bad["priceUsd"]
    with pytest.raises(ValueError):
        AssetHistory.model_validate(bad)


def test_history_invalid_type(sample_history_dict):
    bad = sample_history_dict.copy()
    bad["priceUsd"] = "not a number"
    with pytest.raises(ValueError):
        AssetHistory.model_validate(bad)
