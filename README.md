# Starlink Ubuntu Desktop App

A native Ubuntu/Linux desktop app (GTK4 + Python) that mirrors key workflows from the Starlink mobile app experience, using realistic mock Starlink API simulation.

## Features

- **Setup Assistant**: AR-like setup guidance with obstruction scoring simulation and directional placement hints
- **Connection Diagnostics**:
  - WiFi connectivity verification
  - Service obstruction status
  - Satellite-to-router and router-to-device speed tests
  - Service alert simulation
- **Device Management**: View connected local network devices
- **Performance Monitoring**: Real-time dashboard (auto-refresh) with:
  - Uptime
  - Latency
  - Power draw
  - Signal strength
  - Download/Upload throughput
- **Troubleshooting Tools**:
  - In-app support guide
  - Debug logs viewer
  - Direct support contact info
- **Account & Settings Management**:
  - Subscription profile (Residential, Roam, Standby Mode)
  - Billing email storage
  - WiFi SSID/password configuration
  - Bypass Mode toggle
- **Firmware & Updates**:
  - Current/pending firmware display
  - Firmware update action simulation
- **Security & Privacy**:
  - Mock API payload encryption/decryption using Fernet (symmetric encryption)
- **Debug Logs & Statistics**: Advanced technical metrics panel
- **Modern UI**: Multi-tab, responsive GTK4 desktop interface with periodic metric refresh

## Project Structure

- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/main.py` — app entry point
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/starlink_app/app.py` — GTK application window + screen composition
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/starlink_app/ui/screens.py` — all UI screens/components
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/starlink_app/services/mock_api.py` — mock Starlink API and simulation logic
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/starlink_app/services/encryption.py` — encrypted payload transport helper
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/starlink_app/config.py` — persistence/configuration storage
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/starlink_app/logging_config.py` — application logging setup
- `/home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app/tests/test_services.py` — focused service/config tests

## Ubuntu Setup

### 1) Install system packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-gi gir1.2-gtk-4.0
```

### 2) Install Python dependencies

```bash
cd /home/runner/work/starlink-ubuntu-app/starlink-ubuntu-app
./install.sh
```

### 3) Run

```bash
source .venv/bin/activate
python main.py
```

## Configuration & Data Persistence

- Config file: `~/.config/starlink-ubuntu-app/config.json`
- Logs: `~/.local/state/starlink-ubuntu-app/app.log`

Settings are persisted automatically from the **Account/Settings** tab.

## Testing

Run focused tests:

```bash
pytest tests/test_services.py
```

## Notes

- This desktop app uses **mock endpoints** with realistic behavior for development/testing.
- API calls are simulated and encrypted internally to model secure data transmission behavior.
