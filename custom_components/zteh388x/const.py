# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.0 - 21/07/2026

# const.py

DOMAIN = "zteh388x"
PLATFORMS = ["sensor", "device_tracker"]

CONF_LINETYPE = "linetype"
CONF_INTERVAL = "interval"

DEFAULT_INTERVAL = 120  # Seconds
REQUEST_TIMEOUT = 10  # Seconds, applied to every HTTP request made to the router
