"""DataUpdateCoordinator for Aquascape Smart Control."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

import aiohttp

from homeassistant.core import HomeAssistant
from homeassistant.exceptions import ConfigEntryAuthFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import (
    BASE_API_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    PIN_TEMPERATURE,
    PIN_WIFI_BARS,
    PIN_WIFI_RSSI,
)

_LOGGER = logging.getLogger(__name__)


class AquascapeDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Class to manage fetching Aquascape Smart Control data from the cloud API."""

    def __init__(
        self,
        hass: HomeAssistant,
        auth_token: str,
        device_name: str,
        entry_id: str,
    ) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry_id}",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.auth_token = auth_token
        self.device_name = device_name
        self.entry_id = entry_id
        self._session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch data from Aquascape Smart Control REST API."""
        pins_url = (
            f"{BASE_API_URL}/get?token={self.auth_token}"
            f"&{PIN_TEMPERATURE}&{PIN_WIFI_RSSI}&{PIN_WIFI_BARS}"
        )
        online_url = f"{BASE_API_URL}/isHardwareConnected?token={self.auth_token}"

        try:
            async with asyncio.timeout(15):
                pins_resp, online_resp = await asyncio.gather(
                    self._session.get(pins_url),
                    self._session.get(online_url),
                )

                if pins_resp.status in (400, 401, 403):
                    body = await pins_resp.text()
                    if "Invalid token" in body:
                        raise ConfigEntryAuthFailed("Invalid Aquascape Auth Token")

                pins_resp.raise_for_status()
                online_resp.raise_for_status()

                pins_data = await pins_resp.json(content_type=None)
                online_text = (await online_resp.text()).strip().lower()

        except ConfigEntryAuthFailed:
            raise
        except (aiohttp.ClientError, TimeoutError, ValueError) as err:
            raise UpdateFailed(f"Error communicating with Aquascape API: {err}") from err

        if isinstance(pins_data, dict) and "error" in pins_data:
            msg = pins_data["error"].get("message", "Unknown API error")
            if "Invalid token" in msg:
                raise ConfigEntryAuthFailed(msg)
            raise UpdateFailed(f"Aquascape API error: {msg}")

        temp_raw = pins_data.get(PIN_TEMPERATURE)
        rssi_raw = pins_data.get(PIN_WIFI_RSSI)
        bars_raw = pins_data.get(PIN_WIFI_BARS)

        return {
            "temperature": round(float(temp_raw), 1) if temp_raw is not None else None,
            "wifi_rssi": round(float(rssi_raw), 0) if rssi_raw is not None else None,
            "wifi_bars": int(bars_raw) if bars_raw is not None else None,
            "online": online_text == "true",
        }
