from __future__ import annotations

import logging
from pathlib import Path

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from ..config import load_config, save_config
from ..services.mock_api import MockStarlinkAPI

LOGGER = logging.getLogger(__name__)


class SetupAssistantView(Gtk.Box):
    def __init__(self, api: MockStarlinkAPI) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.api = api
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.result = Gtk.Label(label="Run AR-like guide scan for dish placement.")
        self.result.set_wrap(True)

        button = Gtk.Button(label="Run Setup Scan")
        button.connect("clicked", self._run_scan)

        self.append(Gtk.Label(label="Setup Assistant"))
        self.append(button)
        self.append(self.result)

    def _run_scan(self, _button: Gtk.Button) -> None:
        data = self.api.setup_scan()
        self.result.set_label(
            f"Direction: {data['recommended_direction']} | "
            f"Obstruction: {data['obstruction_percent']}% | "
            f"Quality: {data['quality']}\n{data['message']}"
        )


class DiagnosticsView(Gtk.Box):
    def __init__(self, api: MockStarlinkAPI) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.api = api
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.diagnostics_label = Gtk.Label(label="No diagnostics run yet.")
        self.diagnostics_label.set_wrap(True)
        self.speed_label = Gtk.Label(label="No speed test run yet.")

        diagnostics_button = Gtk.Button(label="Run Connection Diagnostics")
        diagnostics_button.connect("clicked", self._run_diagnostics)

        speed_button = Gtk.Button(label="Run Speed Test")
        speed_button.connect("clicked", self._run_speed_test)

        self.append(Gtk.Label(label="Connection Diagnostics"))
        self.append(diagnostics_button)
        self.append(speed_button)
        self.append(self.diagnostics_label)
        self.append(self.speed_label)

    def _run_diagnostics(self, _button: Gtk.Button) -> None:
        data = self.api.connection_diagnostics()
        self.diagnostics_label.set_label(
            f"WiFi Connected: {data['wifi_connected']} | "
            f"Obstructed: {data['service_obstructed']} | "
            f"Alerts: {data['service_alerts']}"
        )

    def _run_speed_test(self, _button: Gtk.Button) -> None:
        result = self.api.speed_test()
        self.speed_label.set_label(
            f"Satellite→Router: {result.satellite_to_router_mbps} Mbps | "
            f"Router→Device: {result.router_to_device_mbps} Mbps | "
            f"Ping: {result.ping_ms} ms"
        )


class DevicesView(Gtk.Box):
    def __init__(self, api: MockStarlinkAPI) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.api = api
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.list_box = Gtk.ListBox()
        self.append(Gtk.Label(label="Connected Devices"))
        self.append(self.list_box)

        refresh = Gtk.Button(label="Refresh Devices")
        refresh.connect("clicked", self._refresh)
        self.append(refresh)
        self._refresh(refresh)

    def _refresh(self, _button: Gtk.Button) -> None:
        child = self.list_box.get_first_child()
        while child is not None:
            next_child = child.get_next_sibling()
            self.list_box.remove(child)
            child = next_child

        for device in self.api.devices():
            row = Gtk.Label(label=f"{device['name']} ({device['type']}) - {device['ip']}")
            row.set_xalign(0)
            self.list_box.append(row)


class PerformanceView(Gtk.Box):
    def __init__(self, api: MockStarlinkAPI) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.api = api
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.labels = {
            "uptime": Gtk.Label(),
            "latency": Gtk.Label(),
            "power": Gtk.Label(),
            "signal": Gtk.Label(),
            "download": Gtk.Label(),
            "upload": Gtk.Label(),
        }
        self.append(Gtk.Label(label="Real-Time Performance Dashboard"))
        for label in self.labels.values():
            label.set_xalign(0)
            self.append(label)

        self.refresh_button = Gtk.Button(label="Refresh Performance")
        self.refresh_button.connect("clicked", self._refresh)
        self.append(self.refresh_button)
        self._refresh(self.refresh_button)

    def _refresh(self, _button: Gtk.Button) -> None:
        perf = self.api.performance()
        self.labels["uptime"].set_label(f"Uptime: {perf['uptime_seconds']} sec")
        self.labels["latency"].set_label(f"Latency: {perf['latency_ms']} ms")
        self.labels["power"].set_label(f"Power Draw: {perf['power_draw_w']} W")
        self.labels["signal"].set_label(f"Signal Strength: {perf['signal_strength_db']} dB")
        self.labels["download"].set_label(f"Download: {perf['download_mbps']} Mbps")
        self.labels["upload"].set_label(f"Upload: {perf['upload_mbps']} Mbps")


class TroubleshootingView(Gtk.Box):
    def __init__(self, log_file: Path) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.log_file = log_file
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.append(Gtk.Label(label="Troubleshooting & Support"))
        guide = Gtk.Label(
            label=(
                "Support Guide:\n"
                "1) Reboot router\n"
                "2) Re-run setup scan\n"
                "3) Verify cables and power\n"
                "4) Run diagnostics"
            )
        )
        guide.set_xalign(0)
        guide.set_wrap(True)

        self.logs_view = Gtk.TextView()
        self.logs_view.set_editable(False)
        self.logs_view.set_monospace(True)

        refresh = Gtk.Button(label="Refresh Debug Logs")
        refresh.connect("clicked", self._refresh_logs)

        contact = Gtk.Label(label="Contact support: support@starlink.example")
        contact.set_xalign(0)

        self.append(guide)
        self.append(refresh)
        self.append(self.logs_view)
        self.append(contact)
        self._refresh_logs(refresh)

    def _refresh_logs(self, _button: Gtk.Button) -> None:
        buffer = self.logs_view.get_buffer()
        if self.log_file.exists():
            text = self.log_file.read_text(encoding="utf-8")[-8000:]
        else:
            text = "No logs yet."
        buffer.set_text(text)


class AccountSettingsView(Gtk.Box):
    def __init__(self) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)
        self.config = load_config()

        self.append(Gtk.Label(label="Account & Settings"))

        subscriptions = ["Residential", "Roam", "Standby Mode"]
        self.subscription = Gtk.DropDown.new_from_strings(subscriptions)
        current_subscription = self.config.get("subscription", subscriptions[0])
        selected = subscriptions.index(current_subscription) if current_subscription in subscriptions else 0
        self.subscription.set_selected(selected)

        self.billing = Gtk.Entry()
        self.billing.set_text(self.config.get("billing_email", ""))
        self.billing.set_placeholder_text("Billing email")

        self.ssid = Gtk.Entry()
        self.ssid.set_text(self.config.get("wifi_ssid", ""))

        self.password = Gtk.Entry()
        self.password.set_visibility(False)
        self.password.set_text(self.config.get("wifi_password", ""))

        self.bypass = Gtk.Switch()
        self.bypass.set_active(bool(self.config.get("bypass_mode", False)))

        save = Gtk.Button(label="Save Settings")
        save.connect("clicked", self._save)

        self.status = Gtk.Label()
        self.status.set_xalign(0)

        self.append(Gtk.Label(label="Subscription"))
        self.append(self.subscription)
        self.append(Gtk.Label(label="Billing"))
        self.append(self.billing)
        self.append(Gtk.Label(label="WiFi SSID"))
        self.append(self.ssid)
        self.append(Gtk.Label(label="WiFi Password"))
        self.append(self.password)
        self.append(Gtk.Label(label="Bypass Mode"))
        self.append(self.bypass)
        self.append(save)
        self.append(self.status)

    def _save(self, _button: Gtk.Button) -> None:
        subscriptions = ["Residential", "Roam", "Standby Mode"]
        self.config["subscription"] = subscriptions[self.subscription.get_selected()]
        self.config["billing_email"] = self.billing.get_text().strip()
        self.config["wifi_ssid"] = self.ssid.get_text().strip()
        self.config["wifi_password"] = self.password.get_text()
        self.config["bypass_mode"] = self.bypass.get_active()
        save_config(self.config)
        LOGGER.info("Settings saved")
        self.status.set_label("Settings saved.")


class FirmwareView(Gtk.Box):
    def __init__(self, api: MockStarlinkAPI) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.api = api
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.status = Gtk.Label(label="Checking firmware...")
        self.update_button = Gtk.Button(label="Apply Firmware Update")
        self.update_button.connect("clicked", self._apply)

        refresh = Gtk.Button(label="Refresh Firmware Status")
        refresh.connect("clicked", self._refresh)

        self.append(Gtk.Label(label="Firmware & Updates"))
        self.append(refresh)
        self.append(self.update_button)
        self.append(self.status)
        self._refresh(refresh)

    def _refresh(self, _button: Gtk.Button) -> None:
        fw = self.api.firmware()
        self.status.set_label(
            f"Current: {fw['current_version']} | Pending: {fw['pending_version']} | "
            f"Update available: {fw['update_available']}"
        )

    def _apply(self, _button: Gtk.Button) -> None:
        result = self.api.apply_firmware_update()
        self.status.set_label(f"Updated firmware to {result['updated_to']}")


class DebugStatsView(Gtk.Box):
    def __init__(self, api: MockStarlinkAPI) -> None:
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        self.api = api
        self.set_margin_top(16)
        self.set_margin_bottom(16)
        self.set_margin_start(16)
        self.set_margin_end(16)

        self.label = Gtk.Label(label="Advanced technical data")
        self.label.set_xalign(0)
        self.label.set_selectable(True)

        self.refresh_button = Gtk.Button(label="Refresh Debug Statistics")
        self.refresh_button.connect("clicked", self._refresh)

        self.append(Gtk.Label(label="Debug Logs & Statistics"))
        self.append(self.refresh_button)
        self.append(self.label)
        self._refresh(self.refresh_button)

    def _refresh(self, _button: Gtk.Button) -> None:
        perf = self.api.performance()
        self.label.set_label(
            "\n".join(
                [
                    f"timestamp: {perf['timestamp']}",
                    f"latency_ms: {perf['latency_ms']}",
                    f"download_mbps: {perf['download_mbps']}",
                    f"upload_mbps: {perf['upload_mbps']}",
                    f"signal_strength_db: {perf['signal_strength_db']}",
                    f"power_draw_w: {perf['power_draw_w']}",
                ]
            )
        )
