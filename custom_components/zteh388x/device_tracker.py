# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.3 - 22/11/2026

# device_tracker.py

from homeassistant.components.device_tracker import ScannerEntity, SourceType
from homeassistant.core import callback
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, format_mac
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up ZTE H388X (TIM HUB+) device trackers from a config entry."""
    router_data = hass.data[DOMAIN][entry.entry_id]

    trackers_by_mac = {}  # Dictionary to store tracker entities by MAC address
    active = True  # Set to False on unload so any already-queued process_update calls exit early

    # Restore previously-known trackers as disconnected so they show "not home" on restart rather than "unavailable", before the first poll runs.
    entity_reg = er.async_get(hass)
    device_reg = dr.async_get(hass)
    prefix = f"{DOMAIN}_{router_data.host_slug}_devicetracker_"
    seed_trackers = []
    for reg_entry in er.async_entries_for_config_entry(entity_reg, entry.entry_id):
        if reg_entry.domain != "device_tracker" or not reg_entry.unique_id.startswith(prefix):
            continue
        mac = format_mac(reg_entry.unique_id[len(prefix):])
        client_device = device_reg.async_get_device_by_identifier((DOMAIN, mac), entry.entry_id)
        hostname = client_device.name if client_device else mac
        tracker = ZTEScannerEntity(mac, {'HostName': hostname}, router_data, entry.entry_id)
        tracker._connected = False
        trackers_by_mac[mac] = tracker
        seed_trackers.append(tracker)
    if seed_trackers:
        async_add_entities(seed_trackers)

    @callback
    def process_update(devices):
        """Create and update trackers on the Home Assistant event loop."""
        if not active:
            return
        seen_macs = set()
        new_trackers = []
        for device in devices:
            raw_mac = device.get('MACAddress')
            if not raw_mac:
                continue
            mac = format_mac(raw_mac)
            seen_macs.add(mac)
            if mac in trackers_by_mac:
                trackers_by_mac[mac].update_from_device(device)
            else:
                tracker = ZTEScannerEntity(mac, device, router_data, entry.entry_id)
                trackers_by_mac[mac] = tracker
                new_trackers.append(tracker)
        # Any previously-seen device missing from this poll is no longer connected
        for mac, tracker in trackers_by_mac.items():
            if mac not in seen_macs:
                tracker.mark_disconnected()
        if new_trackers:
            async_add_entities(new_trackers)

    def handle_update():
        """Copy the worker snapshot and schedule it on the event loop."""
        hass.add_job(process_update, [dict(device) for device in router_data.access_devices])

    remove_listener = router_data.add_listener(handle_update)

    @callback
    def stop_updates():
        """Unsubscribe and ignore any updates queued before unload."""
        nonlocal active
        active = False
        remove_listener()

    entry.async_on_unload(stop_updates)


class ZTEScannerEntity(ScannerEntity):
    """Represent a device tracked via the router's connected Wi-Fi client list."""

    _attr_has_entity_name = True   
    _attr_should_poll = False  # State is pushed by router callbacks, HA must not poll independently
    
    def __init__(self, mac, device, router_data, config_entry_id):
        self._router_data = router_data
        self._config_entry_id = config_entry_id  # Required by async_get_device_by_identifier
        self._mac = mac
        self._hostname = device.get('HostName') or mac
        self._ip_address = device.get('IPAddress')
        self._connected = True
        self._unique_id = f"{DOMAIN}_{router_data.host_slug}_devicetracker_{mac.replace(':', '')}"

    @property
    def unique_id(self):
        """Return a unique ID for the entity."""
        return self._unique_id

    @property
    def name(self):
        """Return None so HA uses the device's own name."""
        return None

    @property
    def source_type(self):
        """Return the source type of the device."""
        return SourceType.ROUTER

    @property
    def is_connected(self):
        """Return true if the device is currently associated with the router's Wi-Fi."""
        return self._connected

    @property
    def ip_address(self):
        """Return the device's IP address."""
        return self._ip_address

    @property
    def mac_address(self):
        """Return the device's MAC address."""
        return self._mac

    @property
    def hostname(self):
        """Return the device's hostname."""
        return self._hostname

    @property
    def device_info(self):
        """Group this tracker under its own device, linked to the router."""
        # via_device_id replaces the deprecated via_device tuple; requires a registry lookup
        via_id = None
        if self.hass is not None:
            router = dr.async_get(self.hass).async_get_device_by_identifier(
                (DOMAIN, self._router_data.host), self._config_entry_id
            )
            if router is not None:
                via_id = router.id
        return DeviceInfo(
            identifiers={(DOMAIN, self._mac)},
            connections={(CONNECTION_NETWORK_MAC, self._mac)},
            name=self._hostname,
            via_device_id=via_id,
        )

    @property
    def available(self):
        """Return False if the router hasn't been successfully polled yet/anymore."""
        return self._router_data.available

    def update_from_device(self, device):
        """Refresh state for a device seen in the latest poll."""
        self._connected = True
        self._hostname = device.get('HostName') or self._hostname
        self._ip_address = device.get('IPAddress')
        if self.hass is not None:  # Guard against updates before registration or after removal
            self.async_write_ha_state()

    def mark_disconnected(self):
        """Mark a previously-seen device as no longer connected."""
        self._connected = False
        if self.hass is not None:  # Guard against updates before registration or after removal
            self.async_write_ha_state()
