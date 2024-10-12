# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V1.0 - 10/08/2024

# transform.py

import logging
_LOGGER = logging.getLogger(__name__)

def transform_uptime(para_name, para_value):
    if 'uptime' in para_name.lower():
        try:
            para_value = round(float(para_value) / 3600, 2) # Convert seconds to hours
        except (ValueError, TypeError) as e:
            _LOGGER.error(f"Error converting uptime value '{para_value}' for parameter '{para_name}': {e}")
    return para_value

def transform_bytes(para_name, para_value):
    if 'bytes' in para_name.lower():
        try:
            para_value = round(float(para_value) / 1e9, 2)  # Convert bytes to gigabytes
        except (ValueError, TypeError) as e:
            _LOGGER.error(f"Error converting bytes value '{para_value}' for parameter '{para_name}': {e}")
    return para_value

def apply_transformations(para_name, para_value):
    para_value = transform_uptime(para_name, para_value)
    para_value = transform_bytes(para_name, para_value)
    return para_value