# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V1.0 - 10/08/2024

# sensor.py

import hashlib
import logging
import os
import xml.etree.ElementTree as ET
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity, SensorDeviceClass
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.event import async_track_time_interval  # Required for sensors update

from .transform import apply_transformations  # Import transformations

# Define platform schema
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional('linetype'): cv.string,
    vol.Optional('interval', default=120): cv.positive_int,  # Sensors update interval (seconds)
}, extra=vol.ALLOW_EXTRA)

# Set up logging. If needed, enable debug-level logging in your configuration.yaml
_LOGGER = logging.getLogger(__name__)

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the ZTE H388X (TIM HUB+) router sensors."""
    # Read settings from YAML file
    host = config.get(CONF_HOST)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    linetype = config.get('linetype')
    interval = config.get('interval')
    _LOGGER.debug(f"Host: {host}, Username: {username}, Line type: {linetype}, Update interval: {interval}")

    # Initialize an instance of RouterData class
    router_data = RouterData(host, username, password, linetype, add_entities, hass)
    # Call the update method
    router_data.update()

    # Set the scan interval for sensors update
    SCAN_INTERVAL = timedelta(seconds=interval)

    # Schedule regular sensors updates
    async_track_time_interval(hass, lambda _: router_data.update(), SCAN_INTERVAL)

def interface_friendly_name(inst_id):
    """Replace inst_id with corresponding values from the mapping file."""
    # Define interface mapping file
    current_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(current_dir, 'interface_mapping.conf')
    # Load interface mapping file
    inst_id_mapping = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if '=' in line and not line.startswith('#'):  # Ignore commented-out lines
                key, value = line.split('=', 1)
                inst_id_mapping[key.strip()] = value.strip()
    # Perform the replacement
    inst_id = inst_id.lower()  # Convert to lowercase for consistent matching
    for raw_name, friendly_name in inst_id_mapping.items():
        if raw_name in inst_id:
            inst_id = inst_id.replace(raw_name, friendly_name)
    return inst_id  # Return the friendly name for inst_id


class ZTESensor(SensorEntity):
    """Set up sensor entities."""

    def __init__(self, inst_id, param_name, param_value, router_data):
        self._inst_id = interface_friendly_name(inst_id)
        self._param_name = param_name
        self._state = param_value
        self._name = f"zteh388x_{self._inst_id}_{param_name.lower()}"
        self._unique_id = f"zteh388x_{self._inst_id}_{param_name.lower()}"  # Assign a unique ID for each entity
        self._router_data = router_data  # Store router_data object to allow for sensors update
        self._previous_value = None  # Store the previous value for byte sensors
        self._cumulative_value = None  # Store the cumulative value for byte sensors

    @property
    def unique_id(self):
        """Return a unique ID for the sensor."""
        return self._unique_id

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

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


class RouterData:
    """Fetch data from the router."""

    def __init__(self, host, username, password, linetype, add_entities, hass):
        self._host = host
        self._username = username
        self._password = password
        self._linetype = linetype
        self.session = requests.Session()  # Initialize session for persistent cookies
        self.instances = []
        self.sensors_by_unique_id = {}  # Dictionary to store sensors by unique ID
        self._add_entities = add_entities
        self.hass = hass
        self.session_token = None  # Initialize session token (needed for the "logout" function)

    def update(self):
        """Update data from the router."""
        # Fetch session token and hashed password
        session_token, hashed_password = self.prelogin()
        # Perform login and fetch data from the router
        self.login(session_token, hashed_password)
        self.get_data()
        # Store the new sensor states temporarily
        updated_sensor_data = {}
        # Collect the new sensor data from all instances
        for instance in self.instances:
            inst_id = instance.get('_InstID')
            for param_name, param_value in instance.items():
                if param_name != '_InstID' and param_name != 'LastChange':  # Skip the '_InstID' and 'LastChange' entities
                    unique_id = f"zteh388x_{inst_id}_{param_name.lower()}"  # Define sensors naming
                    # Add the new sensor data to the dictionary
                    updated_sensor_data[unique_id] = (inst_id, param_name, param_value)
        # Iterate through the new data and update the sensors
        new_sensors = []
        for unique_id, (inst_id, param_name, param_value) in updated_sensor_data.items():
            if unique_id in self.sensors_by_unique_id:
                # Update existing sensor if the value has changed
                sensor = self.sensors_by_unique_id[unique_id]
                sensor.set_new_state(param_value)
            else:
                # Create new sensor if it doesn't exist
                new_sensor = ZTESensor(inst_id, param_name, param_value, self)
                new_sensors.append(new_sensor)
                self.sensors_by_unique_id[unique_id] = new_sensor
        # Add new sensors if any
        if new_sensors:
            self._add_entities(new_sensors, True)

    def prelogin(self):
        """Get session token and password salt."""
        # Check router availability
        try:
            response = self.session.get(f"http://{self._host}", timeout=4)
            if response.status_code != 200:
                _LOGGER.error(f"Router not responding on {self._host}:80, status code: {response.status_code}")
                return  # Stop further execution if the router is not reachable
        except requests.RequestException as e:
            _LOGGER.error(f"Router not reachable on {self._host}:80")
            return  # Stop further execution if the router is not reachable
        _LOGGER.debug("Retrieving session token and salt")
        # Get session token
        url_login_entry = f"http://{self._host}/?_type=loginData&_tag=login_entry"
        response = self.session.get(url_login_entry, verify=False)
        sess_token = response.json().get("sess_token")
        _LOGGER.debug(f"Session token: {sess_token}")
        _LOGGER.debug(f"Pre-login cookie: {self.session.cookies.get_dict()}")
        # Get password salt
        url_login_token = f"http://{self._host}/?_type=loginData&_tag=login_token"
        response = self.session.get(url_login_token, verify=False)
        xml_root = ET.fromstring(response.text)
        salt = xml_root.text
        _LOGGER.debug(f"Salt: {salt}")
        # Hash the password with the salt using SHA-256
        hashed_password = hashlib.sha256(f"{self._password}{salt}".encode()).hexdigest()
        _LOGGER.debug(f"Salted password hash: {hashed_password}")
        return sess_token, hashed_password

    def login(self, session_token, hashed_password):
        """Perform login."""
        _LOGGER.debug("Attempting to log in")
        url_login = f"http://{self._host}/?_type=loginData&_tag=login_entry"
        data = {
            "Password": hashed_password,
            "Username": self._username,
            "_sessionTOKEN": session_token,
            "action": "login"
        }
        self.session_token = session_token
        response = self.session.post(url_login, data=data, verify=False)
        _LOGGER.debug(f"Post-login cookie: {self.session.cookies.get_dict()}")

    def logout(self):
        """Perform logout."""
        _LOGGER.debug("Attempting to log out")
        if not self.session.cookies:
            _LOGGER.debug("No active session found, skipping logout")
            return False
        url_logout = f"http://{self._host}/?_type=loginData&_tag=logout_entry"
        headers = {
            'Cookie': f'SID={self.session.cookies.get("SID")}',
        }
        data = {
            'IF_LogOff': '1',
            '_sessionTOKEN': self.session_token
        }
        try:
            response = self.session.post(url_logout, headers=headers, data=data, verify=False)
            if response.ok:
                _LOGGER.debug(f"Logged out successfully: {response.text}")
            else:
                _LOGGER.debug(f"Logout failed with status code: {response.text}")
        except Exception as e:
            _LOGGER.error(f"Failed to logout: {e}")
        finally:
            self.session.close()
            self.session.cookies.clear()
            _LOGGER.debug("Session closed")

    def get_data(self):
        """Get the interface stats from the router."""
        # Define Ethernet/SFP stats URLs
        eth_init = f"http://{self._host}/?_type=menuView&_tag=ethWanStatus"
        eth_linestats = f"http://{self._host}/?_type=menuData&_tag=eth_interface_status_lua.lua"
        eth_internet = f"http://{self._host}/?_type=menuData&_tag=wan_internet_lua.lua&TypeUplink=2&pageType=1"
        # Define DSL stats URLs
        dsl_init = f"http://{self._host}/?_type=menuView&_tag=dslWanStatus"
        dsl_linestats = f"http://{self._host}/?_type=menuData&_tag=dsl_interface_status_lua.lua"
        dsl_internet = f"http://{self._host}/?_type=menuData&_tag=wan_internet_lua.lua&TypeUplink=1&pageType=1"
        # Get data based on linetype
        if self._linetype == 'eth':
            eth_init_response = self.session.get(eth_init,
                            headers={'Cache-Control': 'no-cache'}, verify=False)
            eth_linestats_response = self.session.get(eth_linestats,
                            headers={'Cache-Control': 'no-cache'}, verify=False)
            eth_internet_response = self.session.get(eth_internet,
                            headers={'Cache-Control': 'no-cache'}, verify=False)
            _LOGGER.debug(f"ETH/SFP line stats: {eth_linestats_response.text}")
            _LOGGER.debug(f"ETH/SFP internet: {eth_internet_response.text}")
            # Parse XML responses (eth)
            self.parse_xml(eth_linestats_response.text, 'OBJ_ETH_ID')
            self.parse_xml(eth_internet_response.text, 'ID_WAN_COMFIG')
        elif self._linetype == 'dsl':
            dsl_init_response = self.session.get(dsl_init,
                            headers={'Cache-Control': 'no-cache'}, verify=False)
            dsl_linestats_response = self.session.get(dsl_linestats,
                            headers={'Cache-Control': 'no-cache'}, verify=False)
            dsl_internet_response = self.session.get(dsl_internet,
                            headers={'Cache-Control': 'no-cache'}, verify=False)
            _LOGGER.debug(f"DSL line stats: {dsl_linestats_response.text}")
            _LOGGER.debug(f"DSL internet: {dsl_internet_response.text}")
            # Parse XML responses (dsl)
            self.parse_xml(dsl_linestats_response.text, 'OBJ_DSLINTERFACE_ID')
            self.parse_xml(dsl_internet_response.text, 'ID_WAN_COMFIG')
        else:
            _LOGGER.error(f"Invalid linetype: {self._linetype}. Supported values are 'eth' and 'dsl'")
        # Call the logout function
        self.logout()

    def parse_xml(self, xml_string, root_element):
        """Parse the XML response based on the root element."""
        try:
            xml_tree = ET.fromstring(xml_string)
            # Initialize instances list if not already
            if not hasattr(self, 'instances') or self.instances is None:
                self.instances = []
            # Find all instances under the root element (e.g., 'OBJ_ETH_ID', 'OBJ_DSLINTERFACE_ID', 'ID_WAN_COMFIG')
            for instance in xml_tree.findall(f'.//{root_element}/Instance'):
                data = {}
                # Extract 'ParaName' and 'ParaValue' pairs for each instance
                para_names = instance.findall('ParaName')
                para_values = instance.findall('ParaValue')
                # Ensure the number of ParaName and ParaValue elements match
                if len(para_names) == len(para_values):
                    for i in range(len(para_names)):
                        para_name = para_names[i].text
                        para_value = para_values[i].text
                        # Apply transformations (uptime, bytes)
                        para_value = apply_transformations(para_name, para_value)
                        # Store the key-value pairs in the data dictionary
                        data[para_name] = para_value
                # Add parsed instance data to the instances list
                self.instances.append(data)
        except ET.XMLSyntaxError as e:
            _LOGGER.error(f"Error parsing XML: {e}")