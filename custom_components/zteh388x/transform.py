# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.1 - 10/08/2026

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

def derive_uptime_days(para_name, para_value):
    if 'uptime' not in para_name.lower():
        return None
    try:
        days_value = round(float(para_value) / 24, 2)  # para_value is already in hours
    except (ValueError, TypeError) as e:
        _LOGGER.error(f"Error deriving uptime days from '{para_value}' for parameter '{para_name}': {e}")
        return None
    return f"{para_name}_days", days_value

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
