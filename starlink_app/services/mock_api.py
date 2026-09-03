from __future__ import annotations

import json
import random
import time
from dataclasses import dataclass
from datetime import datetime

from .encryption import EncryptionService


@dataclass
class SpeedTestResult:
    satellite_to_router_mbps: float
    router_to_device_mbps: float
    ping_ms: float


class MockStarlinkAPI:
    def __init__(self) -> None:
        self._encryption = EncryptionService()
        self._boot_time = time.time()
        self._firmware_version = "2026.09.1"
        self._pending_firmware = "2026.10.0"
        self._devices = [
            {"name": "Desktop", "ip": "192.168.1.10", "type": "PC"},
            {"name": "Phone", "ip": "192.168.1.11", "type": "Mobile"},
            {"name": "TV", "ip": "192.168.1.12", "type": "Media"},
        ]

    def _secure_roundtrip(self, payload: dict) -> dict:
        raw = json.dumps(payload).encode("utf-8")
        token = self._encryption.encrypt_json_bytes(raw)
        returned = self._encryption.decrypt_json_bytes(token)
        return json.loads(returned.decode("utf-8"))

    def setup_scan(self) -> dict:
        guidance = {
            "recommended_direction": random.choice(["NNE", "ENE", "SSE"]),
            "obstruction_percent": round(random.uniform(0.0, 18.0), 2),
            "quality": random.choice(["Excellent", "Good", "Fair"]),
            "message": "Move dish away from trees/buildings until obstruction < 10%.",
        }
        return self._secure_roundtrip(guidance)

    def connection_diagnostics(self) -> dict:
        result = {
            "wifi_connected": True,
            "service_obstructed": random.choice([False, False, False, True]),
            "service_alerts": random.choice([
                "No active alerts",
                "Minor network congestion detected",
                "No active alerts",
            ]),
        }
        return self._secure_roundtrip(result)

    def speed_test(self) -> SpeedTestResult:
        payload = {
            "satellite_to_router_mbps": round(random.uniform(90, 260), 2),
            "router_to_device_mbps": round(random.uniform(80, 220), 2),
            "ping_ms": round(random.uniform(18, 65), 2),
        }
        data = self._secure_roundtrip(payload)
        return SpeedTestResult(**data)

    def devices(self) -> list[dict]:
        return self._secure_roundtrip({"devices": self._devices})["devices"]

    def performance(self) -> dict:
        uptime_seconds = int(time.time() - self._boot_time)
        payload = {
            "timestamp": datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "uptime_seconds": uptime_seconds,
            "latency_ms": round(random.uniform(20, 55), 2),
            "power_draw_w": round(random.uniform(45, 90), 2),
            "signal_strength_db": round(random.uniform(-88, -58), 2),
            "download_mbps": round(random.uniform(100, 280), 2),
            "upload_mbps": round(random.uniform(12, 35), 2),
        }
        return self._secure_roundtrip(payload)

    def firmware(self) -> dict:
        payload = {
            "current_version": self._firmware_version,
            "pending_version": self._pending_firmware,
            "update_available": self._pending_firmware != self._firmware_version,
        }
        return self._secure_roundtrip(payload)

    def apply_firmware_update(self) -> dict:
        self._firmware_version = self._pending_firmware
        return self._secure_roundtrip({"updated_to": self._firmware_version})
