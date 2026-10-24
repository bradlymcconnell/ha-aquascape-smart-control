"""Constants for the Aquascape Smart Control integration."""

from datetime import timedelta

DOMAIN = "aquascape_smart_control"

CONF_AUTH_TOKEN = "auth_token"
CONF_DEVICE_NAME = "device_name"

DEFAULT_NAME = "Aquascape Smart Pond Thermometer"
DEFAULT_SCAN_INTERVAL = timedelta(seconds=60)

BASE_API_URL = "https://smartcontrol.aquascapeinc.com/external/api"

PIN_TEMPERATURE = "v11"
PIN_WIFI_RSSI = "v30"
PIN_WIFI_BARS = "v31"
