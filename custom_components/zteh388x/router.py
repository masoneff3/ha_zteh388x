# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.1 - 10/08/2026

# router.py

import hashlib
import logging
import re
import threading
import xml.etree.ElementTree as ET

import requests
from homeassistant.helpers.entity import DeviceInfo

from .const import DOMAIN, REQUEST_TIMEOUT
from .transform import apply_transformations, derive_uptime_days # Import transformations

# Set up logging. If needed, enable debug-level logging in your configuration.yaml
_LOGGER = logging.getLogger(__name__)

def sanitize_host(host):
    """Strip every non-alphanumeric character from a host, for use in entity IDs."""
    return re.sub(r'[^a-zA-Z0-9]', '', host).lower()


class RouterData:
    """Fetch data from the router and notify registered platform listeners.
    Shared by all platforms (sensor, device_tracker) of a config entry, since the
    router only allows a single admin session.
    """

    def __init__(self, host, username, password, linetype, name=None):
        self._host = host
        self._username = username
        self._password = password
        self._linetype = linetype
        self.session = requests.Session()  # Initialize session for persistent cookies
        self.instances = []  # Parsed interface/WAN stats, consumed by sensor.py
        self.access_devices = []  # Parsed Wi-Fi client list, consumed by device_tracker.py
        self.session_token = None  # Initialize session token (needed for the "logout" function)
        self.host_slug = sanitize_host(host)  # Used to make entity IDs unique across multiple routers
        self._update_lock = threading.Lock()  # Prevent overlapping updates if a poll runs long
        self._listeners = []  # Callbacks invoked after every successful data refresh
        self.available = False  # True once the router has been successfully polled
        self.device_info = DeviceInfo(
            identifiers={(DOMAIN, host)},
            name=name or host,
            manufacturer="ZTE",
            model="H388X (TIM HUB+)",
        )

    @property
    def host(self):
        """Return the router's configured host."""
        return self._host

    def add_listener(self, callback):
        """Register a callback to run (in the executor thread) after every successful refresh."""
        self._listeners.append(callback)

    def update(self):
        """Update data from the router, skipping if a previous update is still running."""
        if not self._update_lock.acquire(blocking=False):
            _LOGGER.warning(f"Skipping update for {self._host}: previous update is still in progress")
            return
        try:
            self._update()
        finally:
            self._update_lock.release()

    def _update(self):
        """Fetch fresh data from the router and notify every registered platform listener."""
        # Fetch session token and hashed password
        session_token, hashed_password = self.prelogin()
        if session_token is None or hashed_password is None:
            self.available = False
            return  # Router unreachable or prelogin failed; skip this update
        try:
            # Perform login and fetch data from the router
            if not self.login(session_token, hashed_password):
                self.available = False
                return  # Wrong credentials or unexpected response; skip this update
            self.get_data()
        except requests.RequestException as e:
            _LOGGER.error(f"Error communicating with {self._host}: {e}")
            self.available = False
            return
        finally:
            # Always release the router's single admin session, however this cycle went
            self.logout()
        self.available = True
        for listener in self._listeners:
            try:
                listener()
            except Exception:
                _LOGGER.exception(f"Error notifying a listener for {self._host}")

    def prelogin(self):
        """Get session token and password salt."""
        # Check router availability
        try:
            response = self.session.get(f"http://{self._host}", timeout=REQUEST_TIMEOUT)
            if response.status_code != 200:
                _LOGGER.error(f"Router not responding on {self._host}:80, status code: {response.status_code}")
                return None, None  # Stop further execution if the router is not reachable
        except requests.RequestException:
            _LOGGER.error(f"Router not reachable on {self._host}:80")
            return None, None  # Stop further execution if the router is not reachable
        _LOGGER.debug("Retrieving session token and salt")
        try:
            # Get session token
            url_login_entry = f"http://{self._host}/?_type=loginData&_tag=login_entry"
            response = self.session.get(url_login_entry, timeout=REQUEST_TIMEOUT, verify=False)
            sess_token = response.json().get("sess_token")
            _LOGGER.debug(f"Session token: {sess_token}")
            _LOGGER.debug(f"Pre-login cookie: {self.session.cookies.get_dict()}")
            # Get password salt
            url_login_token = f"http://{self._host}/?_type=loginData&_tag=login_token"
            response = self.session.get(url_login_token, timeout=REQUEST_TIMEOUT, verify=False)
            xml_root = ET.fromstring(response.text)
            salt = xml_root.text
            _LOGGER.debug(f"Salt: {salt}")
        except (requests.RequestException, ET.ParseError) as e:
            _LOGGER.error(f"Error retrieving session token/salt from {self._host}: {e}")
            return None, None
        if not salt:
            _LOGGER.error(f"Empty password salt received from {self._host}")
            return None, None
        # Hash the password with the salt using SHA-256
        hashed_password = hashlib.sha256(f"{self._password}{salt}".encode()).hexdigest()
        _LOGGER.debug(f"Salted password hash: {hashed_password}")
        return sess_token, hashed_password

    def login(self, session_token, hashed_password):
        """Perform login. Returns True on success, False if the router rejected it."""
        _LOGGER.debug("Attempting to log in")
        url_login = f"http://{self._host}/?_type=loginData&_tag=login_entry"
        data = {
            "Password": hashed_password,
            "Username": self._username,
            "_sessionTOKEN": session_token,
            "action": "login"
        }
        self.session_token = session_token
        response = self.session.post(url_login, data=data, timeout=REQUEST_TIMEOUT, verify=False)
        _LOGGER.debug(f"Post-login cookie: {self.session.cookies.get_dict()}")
        # A failed login (e.g. wrong password) returns a JSON body with a "lockingTime" field
        if "lockingTime" in response.text:
            _LOGGER.error(f"Login to {self._host} failed: {response.text.strip()}")
            return False
        return True

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
            response = self.session.post(url_logout, headers=headers, data=data, timeout=REQUEST_TIMEOUT, verify=False)
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

    def _warn_if_not_ok(self, response, label):
        """Log a warning if a request to the router did not return HTTP 200."""
        if response.status_code != 200:
            _LOGGER.warning(f"Unexpected status {response.status_code} for {label} on {self._host}")

    def get_data(self):
        """Get the interface stats and connected Wi-Fi client list from the router."""
        self.instances = []  # Reset before every poll, otherwise it grows forever
        self.access_devices = []
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
                            headers={'Cache-Control': 'no-cache'}, timeout=REQUEST_TIMEOUT, verify=False)
            self._warn_if_not_ok(eth_init_response, 'ethWanStatus')
            eth_linestats_response = self.session.get(eth_linestats,
                            headers={'Cache-Control': 'no-cache'}, timeout=REQUEST_TIMEOUT, verify=False)
            self._warn_if_not_ok(eth_linestats_response, 'eth_interface_status_lua.lua')
            eth_internet_response = self.session.get(eth_internet,
                            headers={'Cache-Control': 'no-cache'}, timeout=REQUEST_TIMEOUT, verify=False)
            self._warn_if_not_ok(eth_internet_response, 'wan_internet_lua.lua (eth)')
            _LOGGER.debug(f"ETH/SFP line stats: {eth_linestats_response.text}")
            _LOGGER.debug(f"ETH/SFP internet: {eth_internet_response.text}")
            # Parse XML responses (eth)
            self.parse_xml(eth_linestats_response.text, 'OBJ_ETH_ID')
            self.parse_xml(eth_internet_response.text, 'ID_WAN_COMFIG')
        elif self._linetype == 'dsl':
            dsl_init_response = self.session.get(dsl_init,
                            headers={'Cache-Control': 'no-cache'}, timeout=REQUEST_TIMEOUT, verify=False)
            self._warn_if_not_ok(dsl_init_response, 'dslWanStatus')
            dsl_linestats_response = self.session.get(dsl_linestats,
                            headers={'Cache-Control': 'no-cache'}, timeout=REQUEST_TIMEOUT, verify=False)
            self._warn_if_not_ok(dsl_linestats_response, 'dsl_interface_status_lua.lua')
            dsl_internet_response = self.session.get(dsl_internet,
                            headers={'Cache-Control': 'no-cache'}, timeout=REQUEST_TIMEOUT, verify=False)
            self._warn_if_not_ok(dsl_internet_response, 'wan_internet_lua.lua (dsl)')
            _LOGGER.debug(f"DSL line stats: {dsl_linestats_response.text}")
            _LOGGER.debug(f"DSL internet: {dsl_internet_response.text}")
            # Parse XML responses (dsl)
            self.parse_xml(dsl_linestats_response.text, 'OBJ_DSLINTERFACE_ID')
            self.parse_xml(dsl_internet_response.text, 'ID_WAN_COMFIG')
        else:
            _LOGGER.error(f"Invalid linetype: {self._linetype}. Supported values are 'eth' and 'dsl'")

        # Fetch the connected Wi-Fi client list
        accessdev_headers = {
            'Cache-Control': 'no-cache',
            'Referer': f'http://{self._host}/',
            'X-Requested-With': 'XMLHttpRequest',
        }
        # The localNetStatus and wlan_status_lua.lua calls are required, otherwise the
        # accessdev_ssiddev_lua.lua request is rejected with IF_ERRORSTR=SessionTimeout.
        # Their responses are unused.
        localnet_status_url = f"http://{self._host}/?_type=menuView&_tag=localNetStatus"
        localnet_status_response = self.session.get(localnet_status_url,
                        headers=accessdev_headers, timeout=REQUEST_TIMEOUT, verify=False)
        self._warn_if_not_ok(localnet_status_response, 'localNetStatus')

        wlan_status_url = f"http://{self._host}/?_type=menuData&_tag=wlan_status_lua.lua"
        wlan_status_response = self.session.get(wlan_status_url,
                        headers=accessdev_headers, timeout=REQUEST_TIMEOUT, verify=False)
        self._warn_if_not_ok(wlan_status_response, 'wlan_status_lua.lua')

        accessdev_url = f"http://{self._host}/?_type=menuData&_tag=accessdev_ssiddev_lua.lua"
        accessdev_response = self.session.get(accessdev_url,
                        headers=accessdev_headers, timeout=REQUEST_TIMEOUT, verify=False)
        self._warn_if_not_ok(accessdev_response, 'accessdev_ssiddev_lua.lua')
        _LOGGER.debug(f"Access devices: {accessdev_response.text}")
        self.parse_access_devices(accessdev_response.text)

    @staticmethod
    def _extract_instances(xml_tree, root_element):
        """Extract Instance/ParaName/ParaValue triples under root_element as a list of raw dicts."""
        instances = []
        for instance in xml_tree.findall(f'.//{root_element}/Instance'):
            data = {}
            para_names = instance.findall('ParaName')
            para_values = instance.findall('ParaValue')
            # Ensure the number of ParaName and ParaValue elements match
            if len(para_names) == len(para_values):
                for i in range(len(para_names)):
                    data[para_names[i].text] = para_values[i].text
                instances.append(data)
            else:
                _LOGGER.warning(
                    f"Skipping instance under {root_element}: "
                    f"{len(para_names)} ParaName vs {len(para_values)} ParaValue elements"
                )
        return instances

    def parse_xml(self, xml_string, root_element):
        """Parse interface/WAN stats XML, applying value transformations, into self.instances."""
        try:
            xml_tree = ET.fromstring(xml_string)
            for data in self._extract_instances(xml_tree, root_element):
                transformed = {}
                for para_name, para_value in data.items():
                    # Apply transformations (uptime, bytes)
                    para_value = apply_transformations(para_name, para_value)
                    transformed[para_name] = para_value
                    # Derive a companion '<ParaName>_Days' entity for uptime parameters
                    if (derived := derive_uptime_days(para_name, para_value)) is not None:
                        derived_name, derived_value = derived
                        transformed[derived_name] = derived_value
                self.instances.append(transformed)
        except ET.ParseError as e:
            _LOGGER.error(f"Error parsing XML: {e}")

    def parse_access_devices(self, xml_string):
        """Parse the connected Wi-Fi client list into self.access_devices."""
        try:
            xml_tree = ET.fromstring(xml_string)
            self.access_devices = self._extract_instances(xml_tree, 'OBJ_ACCESSDEV_ID')
        except ET.ParseError as e:
            _LOGGER.error(f"Error parsing access device XML: {e}")
