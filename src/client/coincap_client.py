from typing import List, Optional

from dotenv import load_dotenv
import httpx
import os
from src.client.base_client import BaseCryptoClient
from src.model.cryptocurrency import (
    AssetHistory,
    AssetHistoryResponse,
    Market,
    MarketResponse,
)
from src.util.logger import logger

load_dotenv()


class CoinCapClient(BaseCryptoClient):
    """Client for interacting with the CoinCap API."""

    BASE_URL = os.getenv("BASE_URL_API")
    TIMEOUT = 30.0  # seconds
    MAX_RETRIES = 3

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the CoinCap client.

        Args:
            api_key (Optional[str]): API key for authentication
        """
        self.api_key = api_key
        self._client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            timeout=self.TIMEOUT,
            headers=self._get_headers(),
        )

    def _get_headers(self) -> dict:
        """Get headers for API requests."""
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def __aenter__(self):
        """Context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        await self.close()

    async def close(self):
        """Close the HTTP client."""
        await self._client.aclose()

    async def _make_request(self, method: str, endpoint: str, **kwargs) -> dict:
        """
        Make an HTTP request with retry logic and error handling.

        Args:
            method (str): HTTP method
            endpoint (str): API endpoint
            **kwargs: Additional arguments for the request

        Returns:
            dict: Response data

        Raises:
            httpx.HTTPError: If the request fails after retries
        """
        for attempt in range(self.MAX_RETRIES):
            try:
                response = await self._client.request(method, endpoint, **kwargs)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 429:  # Rate limit
                    if attempt < self.MAX_RETRIES - 1:
                        logger.warning(
                            "Rate limit exceeded, retrying...",
                            attempt=attempt + 1,
                            max_retries=self.MAX_RETRIES,
                        )
                        continue
                logger.error(
                    "HTTP error occurred",
                    status_code=e.response.status_code,
                    error=str(e),
                )
                raise
            except httpx.TimeoutException:
                if attempt < self.MAX_RETRIES - 1:
                    logger.warning(
                        "Request timed out, retrying...",
                        attempt=attempt + 1,
                        max_retries=self.MAX_RETRIES,
                    )
                    continue
                logger.error("Request timed out after all retries")
                raise
            except httpx.RequestError as e:
                logger.error("Request failed", error=str(e))
                raise

    async def get_history(
        self,
        asset_id: str,
        interval: str = "d1",
        start: Optional[int] = None,
        end: Optional[int] = None,
    ) -> List[AssetHistory]:
        """
        Get historical price data for a specific asset.

        Args:
            asset_id (str): The ID of the asset
            interval (str): Time interval (m1, m5, m15, m30, h1, h2, h6, h12, d1, m30)
            start (Optional[int]): UNIX time in milliseconds
            end (Optional[int]): UNIX time in milliseconds

        Returns:
            List[AssetHistory]: List of historical price data
        """
        try:
            params = {"interval": interval}
            if start is not None:
                params["start"] = start
            if end is not None:
                params["end"] = end

            response = await self._make_request(
                "GET", f"/assets/{asset_id}/history", params=params
            )
            history_response = AssetHistoryResponse.model_validate(response)
            return history_response.data
        except Exception as e:
            logger.error(
                "Failed to get asset history",
                asset_id=asset_id,
                error=str(e),
            )
            raise

    async def get_markets(
        self, asset_id: str, limit: Optional[int] = 100, offset: Optional[int] = 0
    ) -> List[Market]:
        """
        Get market data for a specific asset.

        Args:
            asset_id (str): The ID of the asset
            limit (Optional[int]): Number of results to return (default is 100)
            offset (Optional[int]): Number of results to skip (default is 0)

        Returns:
            List[Market]: List of market data
        """
        try:
            params = {"limit": limit, "offset": offset}
            response = await self._make_request(
                "GET", f"/assets/{asset_id}/markets", params=params
            )
            market_response = MarketResponse.model_validate(response)
            return market_response.data
        except Exception as e:
            logger.error(
                "Failed to get asset markets",
                asset_id=asset_id,
                error=str(e),
            )
            raise
