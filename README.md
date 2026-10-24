# Aquascape Smart Control for Home Assistant

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fbradlymcconnell%2Fha-aquascape-smart-control%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Faquascape%2Fpond_temperature_winter_care.yaml)
[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=bradlymcconnell&repository=ha-aquascape-smart-control&category=integration)

Integrate the **Aquascape Smart Pond Thermometer** (`#74012` / `#74013`) and **Aquascape Smart Control** cloud ecosystem into **Home Assistant**, complete with a reusable **Pond Winter Care & Temperature Threshold Automation Blueprint**.

---

## What's Included

1. **HACS Custom Integration (`custom_components/aquascape_smart_control/`)**
   - Full UI setup flow (**Settings → Devices & Services → Add Integration → Aquascape Smart Control**).
   - Creates a device with 4 entities:
     - **Water Temperature** (`°F`, virtual pin `v11`)
     - **Wi-Fi Signal Strength** (`dBm`, virtual pin `v30`)
     - **Wi-Fi Signal Bars** (`bars`, virtual pin `v31`)
     - **Online** (`connectivity` binary sensor via `isHardwareConnected`)
2. **Home Assistant Automation Blueprint (`blueprints/automation/aquascape/pond_temperature_winter_care.yaml`)**
   - One-click importable blueprint for **Pond Winter Care & Seasonal Fish Feeding Alerts**:
     - **Below 60°F (Reduce Feeding)**: Alerts you to switch koi/goldfish to an easily digestible cold-water wheat-germ diet and reduce feeding frequency.
     - **Below 55°F (Stop Feeding / Cold Watch)**: Alerts you to stop feeding completely as fish enter winter torpor and watch for cold snaps.
     - Supports built-in Home Assistant persistent notifications plus custom action hooks (e.g., mobile push notifications, turning off smart fish feeders).
3. **Standalone YAML Configuration (`examples/configuration.yaml` & `examples/automations.yaml`)**
   - Pure YAML `rest:` sensor configuration if you prefer not to install a custom component.

---

## Step 1: Retrieve Your 32-Character Aquascape Auth Token

Aquascape Smart Control runs on a white-labeled **Blynk IoT** cloud server at `https://smartcontrol.aquascapeinc.com`.

> [!IMPORTANT]
> The Aquascape Smart Control mobile app displays a hyphenated hardware UID (e.g., `24229232-7380e56b-74fddf06`) on the Device Info screen. **That UID is not the API Auth Token.** To query the API, you need the 32-character `BLYNK_AUTH_TOKEN` from the Aquascape Web Console.

1. Open **[https://smartcontrol.aquascapeinc.com/dashboard/login](https://smartcontrol.aquascapeinc.com/dashboard/login)** in a desktop browser.
2. Sign in with the **same email and password** you use in the Aquascape Smart Control mobile app.
3. Click **Devices** (or the magnifying glass **Search** icon in the left sidebar) and select your **Thermometer**.
4. Open the **Device Info** tab.
5. Copy the **32-character alphanumeric Auth Token** (shown under `BLYNK_AUTH_TOKEN` or Firmware Configuration).

---

## Step 2: Install into Home Assistant

### Option A: HACS Custom Integration (Recommended)

1. Click the **Open in HACS** badge at the top of this README (or open **HACS → Integrations → ⋮ → Custom repositories**, add `https://github.com/bradlymcconnell/ha-aquascape-smart-control` with category **Integration**).
2. Install **Aquascape Smart Control** and restart Home Assistant.
3. Go to **Settings → Devices & Services → Add Integration** and search for **Aquascape Smart Control**.
4. Paste your 32-character Auth Token and give your pond thermometer a name.

### Option B: Pure YAML (`rest:` integration)

If you prefer not to use a custom component, copy the snippet from [`examples/configuration.yaml`](examples/configuration.yaml) into your `/homeassistant/configuration.yaml` (replacing `YOUR_32_CHAR_AQUASCAPE_TOKEN` with your token) and reload REST entities.

---

## Step 3: Import the Pond Winter Care Automation Blueprint

Click the button below to import the **Aquascape Pond Winter Care & Temperature Threshold Alerts** blueprint directly into your Home Assistant instance:

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fgithub.com%2Fbradlymcconnell%2Fha-aquascape-smart-control%2Fblob%2Fmain%2Fblueprints%2Fautomation%2Faquascape%2Fpond_temperature_winter_care.yaml)

Or import manually in Home Assistant via **Settings → Automations & Scenes → Blueprints → Import Blueprint** using this URL:

```text
https://github.com/bradlymcconnell/ha-aquascape-smart-control/blob/main/blueprints/automation/aquascape/pond_temperature_winter_care.yaml
```

---

## Aquascape Smart Control API Reference

Base URL: `https://smartcontrol.aquascapeinc.com/external/api`

| Endpoint / Pin | Method | Description | Example Response |
| :--- | :--- | :--- | :--- |
| `/get?token=TOKEN&v11&v30&v31` | `GET` | Fetch thermometer virtual pins in one call | `{"v11":68.666,"v30":-44.486,"v31":3}` |
| `v11` | `GET` | Pond Water Temperature (`°F`) | `68.7` |
| `v30` | `GET` | Wi-Fi RSSI (`dBm`) | `-45` |
| `v31` | `GET` | Wi-Fi Signal Level (`0`–`4` bars) | `3` |
| `/isHardwareConnected?token=TOKEN` | `GET` | Device cloud connectivity status | `true` / `false` |
| `/device/meta?token=TOKEN&metaFieldId=1` | `GET` | Device Name metadata | `{"type":"DeviceName","value":"Thermometer"}` |

---

## Submitting to the Home Assistant Community

- **Home Assistant Blueprints Exchange**: Create a new post in the [Home Assistant Community Blueprints Exchange](https://community.home-assistant.io/c/blueprints-exchange/53) and include the Blueprint URL and the `blueprint_import` badge above.
- **HACS Default Repository**: Once pushed to GitHub with a release tag (e.g., `v1.0.0`), submit the repository to [hacs/default](https://github.com/hacs/default). The included `.github/workflows/validate.yml` runs both `hacs/action` and `hassfest` checks automatically.

## License

MIT License — see [LICENSE](LICENSE).
