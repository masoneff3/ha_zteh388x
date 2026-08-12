# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.1 - 10/08/2026

# device_tracker.py

from homeassistant.components.device_tracker import ScannerEntity, SourceType
from homeassistant.helpers.device_registry import CONNECTION_NETWORK_MAC, format_mac
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up ZTE H388X (TIM HUB+) device trackers from a config entry."""
    router_data = hass.data[DOMAIN][entry.entry_id]

    def threadsafe_add_entities(new_entities, update_before_add=False):
        """Schedule async_add_entities on the event loop; called from a worker thread."""
        hass.add_job(async_add_entities, list(new_entities), update_before_add)

    trackers_by_mac = {}  # Dictionary to store tracker entities by MAC address

    def handle_update():
        """Create/update tracker entities from router_data.access_devices (runs in the executor)."""
        seen_macs = set()
        new_trackers = []
        for device in router_data.access_devices:
            raw_mac = device.get('MACAddress')
            if not raw_mac:
                continue
            mac = format_mac(raw_mac)
            seen_macs.add(mac)
            if mac in trackers_by_mac:
                trackers_by_mac[mac].update_from_device(device)
            else:
                tracker = ZTEScannerEntity(mac, device, router_data)
                trackers_by_mac[mac] = tracker
                new_trackers.append(tracker)
        # Any previously-seen device missing from this poll is no longer connected
        for mac, tracker in trackers_by_mac.items():
            if mac not in seen_macs:
                tracker.mark_disconnected()
        if new_trackers:
            threadsafe_add_entities(new_trackers, True)

    router_data.add_listener(handle_update)


class ZTEScannerEntity(ScannerEntity):
    """Represent a device tracked via the router's connected Wi-Fi client list."""

    _attr_has_entity_name = True   
    
    def __init__(self, mac, device, router_data):
        self._router_data = router_data
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
        return DeviceInfo(
            identifiers={(DOMAIN, self._mac)},
            connections={(CONNECTION_NETWORK_MAC, self._mac)},
            name=self._hostname,
            via_device=(DOMAIN, self._router_data.host),
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
        self.schedule_update_ha_state()

    def mark_disconnected(self):
        """Mark a previously-seen device as no longer connected."""
        self._connected = False
        self.schedule_update_ha_state()
