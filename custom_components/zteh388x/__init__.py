# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.0 - 21/07/2026

# __init__.py

import logging
from datetime import timedelta

from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_USERNAME
from homeassistant.helpers.event import async_track_time_interval

from .const import CONF_INTERVAL, CONF_LINETYPE, DEFAULT_INTERVAL, DOMAIN, PLATFORMS
from .router import RouterData

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry):
    """Set up ZTE H388X (TIM HUB+) from a config entry."""
    host = entry.data[CONF_HOST]
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    name = entry.data.get(CONF_NAME)
    linetype = entry.data.get(CONF_LINETYPE)
    interval = entry.data.get(CONF_INTERVAL, DEFAULT_INTERVAL)
    _LOGGER.debug(f"Host: {host}, Username: {username}, Name: {name}, Line type: {linetype}, Update interval: {interval}")

    router_data = RouterData(host, username, password, linetype, name)
    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = router_data

    # Forward to platforms first, so both sensor.py and device_tracker.py register their
    # entity-add listeners with router_data before the first poll below runs.
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Offloaded to the executor since we're on the event loop here
    await hass.async_add_executor_job(router_data.update)

    remove_listener = async_track_time_interval(
        hass, lambda _: router_data.update(), timedelta(seconds=interval)
    )
    entry.async_on_unload(remove_listener)

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id, None)
    return unload_ok
