"""Binary sensor platform for Aquascape Smart Control."""

from __future__ import annotations

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AquascapeDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Aquascape Smart Control binary sensor based on a config entry."""
    coordinator: AquascapeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([AquascapeOnlineBinarySensor(coordinator, entry)])


class AquascapeOnlineBinarySensor(
    CoordinatorEntity[AquascapeDataUpdateCoordinator], BinarySensorEntity
):
    """Representation of the Aquascape hardware connectivity status."""

    _attr_has_entity_name = True
    _attr_name = "Online"
    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(
        self,
        coordinator: AquascapeDataUpdateCoordinator,
        entry: ConfigEntry,
    ) -> None:
        """Initialize the binary sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_online"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id or entry.entry_id)},
            name=coordinator.device_name,
            manufacturer="Aquascape",
            model="Smart Pond Thermometer (#74012 / #74013)",
            configuration_url="https://smartcontrol.aquascapeinc.com/dashboard/login",
        )

    @property
    def is_on(self) -> bool | None:
        """Return true if the hardware is connected to Aquascape cloud."""
        if not self.coordinator.data:
            return None
        return bool(self.coordinator.data.get("online"))
