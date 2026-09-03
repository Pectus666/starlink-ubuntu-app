from starlink_app.config import DEFAULT_CONFIG, load_config, save_config
from starlink_app.services.mock_api import MockStarlinkAPI


def test_speedtest_has_expected_ranges():
    api = MockStarlinkAPI()
    result = api.speed_test()
    assert 90 <= result.satellite_to_router_mbps <= 260
    assert 80 <= result.router_to_device_mbps <= 220
    assert 18 <= result.ping_ms <= 65


def test_firmware_update_flow():
    api = MockStarlinkAPI()
    before = api.firmware()
    assert before["update_available"] is True

    updated = api.apply_firmware_update()
    assert updated["updated_to"] == before["pending_version"]

    after = api.firmware()
    assert after["update_available"] is False


def test_config_persistence(tmp_path, monkeypatch):
    import starlink_app.config as cfg

    monkeypatch.setattr(cfg, "CONFIG_DIR", tmp_path / "config")
    monkeypatch.setattr(cfg, "STATE_DIR", tmp_path / "state")
    monkeypatch.setattr(cfg, "CONFIG_FILE", (tmp_path / "config" / "config.json"))

    initial = load_config()
    assert initial["subscription"] == DEFAULT_CONFIG["subscription"]

    initial["wifi_ssid"] = "UnitTestSSID"
    save_config(initial)

    loaded = load_config()
    assert loaded["wifi_ssid"] == "UnitTestSSID"
