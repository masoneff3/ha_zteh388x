"""Lifecycle regression tests using a small, isolated Home Assistant API double.

Run with: python -m unittest discover -s tests -v
These tests do not require a router, credentials, or a Home Assistant installation.
"""

import importlib.util
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import patch


class FakeEntity:
    hass = None

    def __init_subclass__(cls):
        cls.writes = 0

    async def async_added_to_hass(self):
        pass

    async def async_will_remove_from_hass(self):
        pass

    def async_write_ha_state(self):
        if self.hass is None:
            raise AssertionError("State published before registration")
        self.writes += 1


def load_modules():
    """Load production modules with explicit, temporary dependency doubles."""
    names = (
        "homeassistant", "homeassistant.components",
        "homeassistant.components.device_tracker", "homeassistant.core",
        "homeassistant.helpers", "homeassistant.helpers.device_registry",
        "homeassistant.helpers.entity", "zte_test", "zte_test.const",
        "zte_test.transform", "requests",
    )
    modules = {name: types.ModuleType(name) for name in names}
    tracker_api = modules["homeassistant.components.device_tracker"]
    tracker_api.ScannerEntity = FakeEntity
    tracker_api.SourceType = types.SimpleNamespace(ROUTER="router")
    modules["homeassistant.core"].callback = lambda fn: fn
    registry = modules["homeassistant.helpers.device_registry"]
    registry.CONNECTION_NETWORK_MAC = "mac"
    registry.format_mac = str.lower
    modules["homeassistant.helpers.entity"].DeviceInfo = dict
    modules["zte_test.const"].DOMAIN = "zteh388x"
    modules["zte_test.const"].REQUEST_TIMEOUT = 10
    modules["zte_test.transform"].apply_transformations = lambda value: value
    modules["zte_test.transform"].derive_uptime_days = lambda value: value
    modules["requests"].Session = object
    modules["requests"].RequestException = Exception
    loaded = []
    root = Path(__file__).resolve().parents[1] / "custom_components" / "zteh388x"
    with patch.dict(sys.modules, modules):
        for name in ("device_tracker", "router"):
            spec = importlib.util.spec_from_file_location(f"zte_test.{name}", root / f"{name}.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            loaded.append(module)
    return loaded


tracker_module, router_module = load_modules()


class TrackerTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.router = router_module.RouterData("router", "user", "unused", "eth")
        self.router.available = True
        self.mac = "aa:bb:cc:dd:ee:ff"
        self.device = {"MACAddress": self.mac, "IPAddress": "192.0.2.2"}

    async def test_pending_active_and_removed_entity(self):
        entity = tracker_module.ZTEScannerEntity(self.mac, self.device, self.router)
        entity.update_from_device(self.device)
        entity.mark_disconnected()
        self.assertEqual(entity.writes, 0)
        entity.hass = object()
        await entity.async_added_to_hass()
        entity.update_from_device({**self.device, "IPAddress": "192.0.2.3"})
        self.assertTrue(entity.is_connected)
        self.assertEqual(entity.ip_address, "192.0.2.3")
        entity.mark_disconnected()
        self.assertFalse(entity.is_connected)
        self.assertEqual(entity.writes, 2)
        await entity.async_will_remove_from_hass()
        entity.hass = None
        entity.update_from_device(self.device)
        entity.mark_disconnected()
        self.assertEqual(entity.writes, 2)

    async def test_worker_snapshot_pending_entity_and_unload(self):
        jobs, added, unload = [], [], []
        hass = types.SimpleNamespace(
            data={"zteh388x": {"entry": self.router}},
            add_job=lambda fn, *args: jobs.append((fn, args)),
        )
        entry = types.SimpleNamespace(entry_id="entry", async_on_unload=unload.append)
        await tracker_module.async_setup_entry(hass, entry, added.extend)
        self.router.access_devices = [dict(self.device)]
        listener = self.router._listeners[0]
        listener()
        self.assertEqual(added, [])
        self.router.access_devices[0]["IPAddress"] = "192.0.2.9"
        fn, args = jobs.pop(0)
        fn(*args)
        self.assertEqual(len(added), 1)
        self.assertEqual(added[0].ip_address, "192.0.2.2")
        # A second poll before HA has registered the entity must not publish state.
        listener()
        fn, args = jobs.pop(0)
        fn(*args)
        self.assertEqual(added[0].writes, 0)
        self.assertEqual(added[0].ip_address, "192.0.2.9")
        added[0].hass = hass
        await added[0].async_added_to_hass()
        self.router.access_devices = []
        listener()
        fn, args = jobs.pop(0)
        fn(*args)
        self.assertFalse(added[0].is_connected)
        self.assertEqual(added[0].writes, 1)
        listener()
        unload[0]()
        self.assertEqual(self.router._listeners, [])
        fn, args = jobs.pop(0)
        fn(*args)
        self.assertEqual(added[0].writes, 1)

    async def test_listener_unsubscribe_is_idempotent(self):
        remove = self.router.add_listener(lambda: None)
        self.assertEqual(len(self.router._listeners), 1)
        remove()
        remove()
        self.assertEqual(self.router._listeners, [])


if __name__ == "__main__":
    unittest.main()
