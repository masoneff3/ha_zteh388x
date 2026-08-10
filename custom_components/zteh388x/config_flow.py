# ZTE H388X (TIM HUB+) Custom Component for Home Assistant
# Author: masoneff3 | https://github.com/masoneff3
# V2.1 - 10/08/2026

# config_flow.py

import logging

import requests
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_NAME, CONF_PASSWORD, CONF_USERNAME

from .const import CONF_INTERVAL, CONF_LINETYPE, DEFAULT_INTERVAL, DOMAIN, REQUEST_TIMEOUT

_LOGGER = logging.getLogger(__name__)

DATA_SCHEMA = vol.Schema({
    vol.Required(CONF_HOST): str,
    vol.Required(CONF_USERNAME): str,
    vol.Required(CONF_PASSWORD): str,
    vol.Required(CONF_LINETYPE): vol.In(["eth", "dsl"]),
    vol.Optional(CONF_NAME): str,
    vol.Optional(CONF_INTERVAL, default=DEFAULT_INTERVAL): vol.All(int, vol.Range(min=10)),
})


class ZteH388xConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZTE H388X (TIM HUB+)."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial setup step."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(user_input[CONF_HOST])
            self._abort_if_unique_id_configured()
            try:
                reachable = await self.hass.async_add_executor_job(
                    self._is_reachable, user_input[CONF_HOST]
                )
            except Exception:
                _LOGGER.exception("Unexpected error testing connection to %s", user_input[CONF_HOST])
                errors["base"] = "unknown"
            else:
                if not reachable:
                    errors["base"] = "cannot_connect"
                else:
                    title = user_input.get(CONF_NAME) or user_input[CONF_HOST]
                    return self.async_create_entry(title=title, data=user_input)
        return self.async_show_form(step_id="user", data_schema=DATA_SCHEMA, errors=errors)

    @staticmethod
    def _is_reachable(host):
        """Check whether the router responds. Does not validate credentials."""
        try:
            response = requests.get(f"http://{host}", timeout=REQUEST_TIMEOUT)
            return response.status_code == 200
        except requests.RequestException:
            return False
