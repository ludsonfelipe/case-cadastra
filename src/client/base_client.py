from abc import ABC, abstractmethod
from typing import List

from src.model.cryptocurrency import AssetHistory, Market


class BaseCryptoClient(ABC):
    """Abstract base class for cryptocurrency API clients."""

    @abstractmethod
    async def get_history(self, asset_id: str) -> List[AssetHistory]:
        """
        Get historical price data for a specific asset.

        Args:
            asset_id (str): The ID of the cryptocurrency asset

        Returns:
            List[AssetHistory]: List of historical price data
        """
        pass

    @abstractmethod
    async def get_markets(self, asset_id: str) -> List[Market]:
        """
        Get market data for a specific asset.

        Args:
            asset_id (str): The ID of the cryptocurrency asset

        Returns:
            List[Market]: List of market data
        """
        pass
