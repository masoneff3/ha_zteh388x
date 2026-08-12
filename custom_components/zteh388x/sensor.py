# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.2 - 12/08/2026

# sensor.py

import os

from homeassistant.components.sensor import SensorEntity, SensorDeviceClass

from .const import DOMAIN

_INTERFACE_MAPPING = None  # Cache for interface_mapping.conf, populated on first use

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up the ZTE H388X (TIM HUB+) router sensors from a config entry."""
    router_data = hass.data[DOMAIN][entry.entry_id]

    def threadsafe_add_entities(new_entities, update_before_add=False):
        """Schedule async_add_entities on the event loop; called from a worker thread."""
        hass.add_job(async_add_entities, list(new_entities), update_before_add)

    sensors_by_unique_id = {}  # Dictionary to store sensors by unique ID

    def handle_update():
        """Create/update sensor entities from router_data.instances (runs in the executor)."""
        # Store the new sensor states temporarily
        updated_sensor_data = {}
        # Collect the new sensor data from all instances
        for instance in router_data.instances:
            inst_id = instance.get('_InstID')
            for param_name, param_value in instance.items():
                if param_name != '_InstID' and param_name != 'LastChange':  # Skip the '_InstID' and 'LastChange' entities
                    sensor_key = f"{DOMAIN}_{inst_id}_{param_name.lower()}"  # Local dedup key, not the entity's unique_id
                    # Add the new sensor data to the dictionary
                    updated_sensor_data[sensor_key] = (inst_id, param_name, param_value)
        # Iterate through the new data and update the sensors
        new_sensors = []
        for sensor_key, (inst_id, param_name, param_value) in updated_sensor_data.items():
            if sensor_key in sensors_by_unique_id:
                # Update existing sensor if the value has changed
                sensor = sensors_by_unique_id[sensor_key]
                sensor.set_new_state(param_value)
            else:
                # Create new sensor if it doesn't exist
                new_sensor = ZTESensor(inst_id, param_name, param_value, router_data)
                new_sensors.append(new_sensor)
                sensors_by_unique_id[sensor_key] = new_sensor
        # Add new sensors if any
        if new_sensors:
            threadsafe_add_entities(new_sensors, True)

    router_data.add_listener(handle_update)

def _load_interface_mapping():
    """Load and cache the interface mapping file (read from disk once)."""
    global _INTERFACE_MAPPING
    if _INTERFACE_MAPPING is None:
        current_dir = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(current_dir, 'interface_mapping.conf')
        mapping = {}
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if '=' in line and not line.startswith('#'):  # Ignore commented-out lines
                    key, value = line.split('=', 1)
                    mapping[key.strip()] = value.strip()
        _INTERFACE_MAPPING = mapping
    return _INTERFACE_MAPPING

def interface_friendly_name(inst_id):
    """Replace inst_id with corresponding values from the mapping file."""
    inst_id_mapping = _load_interface_mapping()
    # Perform the replacement
    inst_id = inst_id.lower()  # Convert to lowercase for consistent matching
    for raw_name, friendly_name in inst_id_mapping.items():
        if raw_name in inst_id:
            inst_id = inst_id.replace(raw_name, friendly_name)
    return inst_id  # Return the friendly name for inst_id


class ZTESensor(SensorEntity):
    """Set up sensor entities."""

    _attr_has_entity_name = True  # HA combines this with the router device's name for display    
    
    def __init__(self, inst_id, param_name, param_value, router_data):
        self._inst_id = interface_friendly_name(inst_id)
        self._param_name = param_name
        self._router_data = router_data  # Store router_data object to allow for sensors update
        self._entity_name = f"{DOMAIN}_{self._inst_id}_{param_name.lower()}"  # Displayed name (no host segment)
        self._unique_id = f"{DOMAIN}_{router_data.host_slug}_{self._inst_id}_{param_name.lower()}"  # Assign a unique ID for each entity (internal only, never shown to the user)
        self._previous_value = None  # Store the previous value for byte sensors
        self._cumulative_value = None  # Store the cumulative value for byte sensors
        self._state = param_value
        if 'bytes' in param_name.lower():  # Initialize the cumulative value right away
            self.byte_counter_reset(param_value)

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._entity_name

    @property
    def device_info(self):
        """Return device info so this sensor is grouped under its router's device."""
        return self._router_data.device_info

    @property
    def available(self):
        """Return False if the router hasn't been successfully polled yet/anymore."""
        return self._router_data.available

    @property
    def state(self):
        """Return the state of the sensor."""
        if 'bytes' in self._param_name.lower():
            return self._cumulative_value  # Handle byte counter reset
        else:
            return self._state

    @property
    def icon(self):
        """Return the icon for the sensor, based on its type."""
        icon_mapping = {
            'received': 'mdi:download-circle',
            'sent': 'mdi:upload-circle',
            'time': 'mdi:clock-time-ten',
            'linkspeed': 'mdi:speedometer',
            'rate': 'mdi:speedometer',
            'ipaddress':'mdi:ip-network',
            'dns':'mdi:dns',
            'status':"mdi:lan-connect",
            'wan':'mdi:wan',
            'mac':'mdi:expansion-card'
        }
        # Return the appropriate icon if found
        for key, icon in icon_mapping.items():
            if key in self._param_name.lower():
                return icon
        return 'mdi:router'  # Return default icon if no match is found

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement for the sensor, based on its type."""
        unit_mapping = {
            'bytes': 'GB',
            'uptime_days': 'd',  # Must be checked before 'uptime' below, since it's a substring match
            'uptime': 'h',
            'linkspeed': 'Mbit/s',
            'rate': 'kbit/s',
            'noise': 'dB',
            'attenuation': 'dB',
            'power': 'dBm',
            'strength': 'dBm',
            'interleavedelay': 'ms'
        }
        # Return the appropriate unit of measurement if found
        for key, unit in unit_mapping.items():
            if key in self._param_name.lower():
                return unit
        return None  # Return None if no match is found

    @property
    def device_class(self):
        """Return the device class for the sensor, based on its type."""
        device_class_mapping = {
            'bytes': SensorDeviceClass.DATA_SIZE,
            'uptime': SensorDeviceClass.DURATION,
            'linkspeed': SensorDeviceClass.DATA_RATE,
            'rate': SensorDeviceClass.DATA_RATE,
            'noise': SensorDeviceClass.SIGNAL_STRENGTH,
            'attenuation': SensorDeviceClass.SIGNAL_STRENGTH,
            'power': SensorDeviceClass.SIGNAL_STRENGTH,
            'strength': SensorDeviceClass.SIGNAL_STRENGTH,
            'interleavedelay': SensorDeviceClass.DURATION
        }
        # Return the appropriate device class if found
        for key, device_class in device_class_mapping.items():
            if key in self._param_name.lower():
                return device_class
        return None  # Return None if no match is found

    def set_new_state(self, new_state):
        """Set a new state and update the entity."""
        if new_state != self._state:
            if 'bytes' in self._param_name.lower():  # Handle byte counter reset
                self.byte_counter_reset(new_state)
            else:
                self._state = new_state
        self.schedule_update_ha_state()

    def byte_counter_reset(self, new_value):
        """Handle byte counter reset and maintain a cumulative value."""
        new_value_in_bytes = float(new_value) * 1e9  # Convert GB back to bytes for comparison
        # If this is the first time setting the value, initialize the cumulative value
        if self._previous_value is None:
            self._cumulative_value = round(float(new_value), 2)  # Start with current value in GB and round to 2 decimals
        else:
            # Detect if the counter has reset (new value is smaller than the previous one)
            if new_value_in_bytes < self._previous_value:
                # Counter reset detected, add 4 GB (4294967296 bytes)
                max_value = 2**32
                self._cumulative_value += (max_value - self._previous_value + new_value_in_bytes) / 1e9
            else:
                # No reset, just add the difference
                self._cumulative_value += (new_value_in_bytes - self._previous_value) / 1e9
            # Round cumulative value to 2 decimals
            self._cumulative_value = round(self._cumulative_value, 2)
        # Update previous value for next comparison
        self._previous_value = new_value_in_bytes
