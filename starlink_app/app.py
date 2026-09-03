from __future__ import annotations

import logging

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GLib, Gtk

from .logging_config import setup_logging
from .services.mock_api import MockStarlinkAPI
from .ui.screens import (
    AccountSettingsView,
    DebugStatsView,
    DevicesView,
    DiagnosticsView,
    FirmwareView,
    PerformanceView,
    SetupAssistantView,
    TroubleshootingView,
)

LOGGER = logging.getLogger(__name__)


class StarlinkApplication(Gtk.Application):
    def __init__(self) -> None:
        super().__init__(application_id="com.starlink.UbuntuDesktop")
        self.api = MockStarlinkAPI()
        self.log_file = setup_logging()

    def do_activate(self) -> None:  # type: ignore[override]
        window = Gtk.ApplicationWindow(application=self)
        window.set_title("Starlink Ubuntu Desktop App")
        window.set_default_size(1200, 760)

        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        container.set_margin_top(8)
        container.set_margin_bottom(8)
        container.set_margin_start(8)
        container.set_margin_end(8)

        stack = Gtk.Stack()
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)
        stack.set_transition_duration(200)

        switcher = Gtk.StackSwitcher()
        switcher.set_stack(stack)
        container.append(switcher)

        setup = SetupAssistantView(self.api)
        diagnostics = DiagnosticsView(self.api)
        devices = DevicesView(self.api)
        performance = PerformanceView(self.api)
        troubleshooting = TroubleshootingView(self.log_file)
        account = AccountSettingsView()
        firmware = FirmwareView(self.api)
        debug = DebugStatsView(self.api)

        pages = [
            (setup, "Setup Assistant"),
            (diagnostics, "Diagnostics"),
            (devices, "Devices"),
            (performance, "Performance"),
            (troubleshooting, "Troubleshooting"),
            (account, "Account/Settings"),
            (firmware, "Firmware"),
            (debug, "Debug/Stats"),
        ]

        for content, title in pages:
            stack.add_titled(content, title, title)
        container.append(stack)

        window.set_child(container)
        window.present()

        GLib.timeout_add_seconds(3, self._refresh_live, performance, debug)
        LOGGER.info("Application activated")

    def _refresh_live(self, performance: PerformanceView, debug: DebugStatsView) -> bool:
        performance._refresh(performance.refresh_button)
        debug._refresh(debug.refresh_button)
        return True
