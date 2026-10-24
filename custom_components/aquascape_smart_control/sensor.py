"""Sensor platform for Aquascape Smart Control."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
    EntityCategory,
    UnitOfTemperature,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AquascapeDataUpdateCoordinator


@dataclass(frozen=True, kw_only=True)
class AquascapeSensorEntityDescription(SensorEntityDescription):
    """Describes an Aquascape sensor entity."""

    value_key: str


SENSOR_DESCRIPTIONS: tuple[AquascapeSensorEntityDescription, ...] = (
    AquascapeSensorEntityDescription(
        key="water_temperature",
        translation_key="water_temperature",
        name="Water Temperature",
        value_key="temperature",
        native_unit_of_measurement=UnitOfTemperature.FAHRENHEIT,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:thermometer-water",
    ),
    AquascapeSensorEntityDescription(
        key="wifi_rssi",
        translation_key="wifi_rssi",
        name="Wi-Fi Signal Strength",
        value_key="wifi_rssi",
        native_unit_of_measurement=SIGNAL_STRENGTH_DECIBELS_MILLIWATT,
        device_class=SensorDeviceClass.SIGNAL_STRENGTH,
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
    ),
    AquascapeSensorEntityDescription(
        key="wifi_bars",
        translation_key="wifi_bars",
        name="Wi-Fi Signal Bars",
        value_key="wifi_bars",
        native_unit_of_measurement="bars",
        state_class=SensorStateClass.MEASUREMENT,
        entity_category=EntityCategory.DIAGNOSTIC,
        icon="mdi:wifi",
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Aquascape Smart Control sensors based on a config entry."""
    coordinator: AquascapeDataUpdateCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        AquascapeSensorEntity(coordinator, entry, description)
        for description in SENSOR_DESCRIPTIONS
    )


class AquascapeSensorEntity(
    CoordinatorEntity[AquascapeDataUpdateCoordinator], SensorEntity
):
    """Representation of an Aquascape Smart Control Sensor."""

    _attr_has_entity_name = True
    entity_description: AquascapeSensorEntityDescription

    def __init__(
        self,
        coordinator: AquascapeDataUpdateCoordinator,
        entry: ConfigEntry,
        description: AquascapeSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.unique_id or entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.unique_id or entry.entry_id)},
            name=coordinator.device_name,
            manufacturer="Aquascape",
            model="Smart Pond Thermometer (#74012 / #74013)",
            configuration_url="https://smartcontrol.aquascapeinc.com/dashboard/login",
        )

    @property
    def native_value(self) -> Any:
        """Return the state of the sensor."""
        if not self.coordinator.data:
            return None
        return self.coordinator.data.get(self.entity_description.value_key)
