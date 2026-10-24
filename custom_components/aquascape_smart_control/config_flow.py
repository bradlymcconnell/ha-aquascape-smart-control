"""Config flow for Aquascape Smart Control integration."""

from __future__ import annotations

import asyncio
import hashlib
import logging
from typing import Any

import aiohttp
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import (
    BASE_API_URL,
    CONF_AUTH_TOKEN,
    CONF_DEVICE_NAME,
    DEFAULT_NAME,
    DOMAIN,
    PIN_TEMPERATURE,
)

_LOGGER = logging.getLogger(__name__)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect to the Aquascape API."""
    token = data[CONF_AUTH_TOKEN].strip()
    session = async_get_clientsession(hass)

    test_url = f"{BASE_API_URL}/get?token={token}&{PIN_TEMPERATURE}"
    meta_url = f"{BASE_API_URL}/device/meta?token={token}&metaFieldId=1"

    try:
        async with asyncio.timeout(15):
            resp = await session.get(test_url)
            body = await resp.text()
            if "Invalid token" in body:
                raise InvalidAuth

            resp.raise_for_status()

            remote_name = DEFAULT_NAME
            try:
                meta_resp = await session.get(meta_url)
                if meta_resp.status == 200:
                    meta_json = await meta_resp.json(content_type=None)
                    if isinstance(meta_json, dict) and meta_json.get("value"):
                        remote_name = str(meta_json["value"])
            except (aiohttp.ClientError, ValueError):
                pass

    except InvalidAuth:
        raise
    except (aiohttp.ClientError, TimeoutError) as err:
        raise CannotConnect from err

    user_name = data.get(CONF_DEVICE_NAME, "").strip()
    final_name = user_name or remote_name

    # Derive a deterministic unique ID without storing the raw token in the registry ID
    token_hash = hashlib.sha256(token.encode("utf-8")).hexdigest()[:16]

    return {
        "title": final_name,
        "device_name": final_name,
        "auth_token": token,
        "unique_id": f"aquascape_{token_hash}",
    }


class AquascapeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Aquascape Smart Control."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:  # pylint: disable=broad-except
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                await self.async_set_unique_id(info["unique_id"])
                self._abort_if_unique_id_configured()
                return self.async_create_entry(
                    title=info["title"],
                    data={
                        CONF_AUTH_TOKEN: info["auth_token"],
                        CONF_DEVICE_NAME: info["device_name"],
                    },
                )

        schema = vol.Schema(
            {
                vol.Required(CONF_AUTH_TOKEN): str,
                vol.Optional(CONF_DEVICE_NAME, default=DEFAULT_NAME): str,
            }
        )

        return self.async_show_form(
            step_id="user", data_schema=schema, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
