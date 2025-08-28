"""Config flow for Orchard Care integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import FlowResult
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN, PLANT_TYPES

class OrchardCareConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Orchard Care."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            return self.async_create_entry(
                title="Orchard Care",
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("hemisphere", default="northern"): vol.In([
                    "northern", "southern"
                ]),
                vol.Required("organic_preference", default=True): bool,
                vol.Required("selected_plants", default=[]): cv.multi_select(PLANT_TYPES),
                vol.Optional("custom_plants", default=""): str,
            }),
            errors=errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OrchardCareOptionsFlow(config_entry)

class OrchardCareOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Orchard Care."""

    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None) -> FlowResult:
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "hemisphere",
                    default=self.config_entry.data.get("hemisphere", "northern")
                ): vol.In(["northern", "southern"]),
                vol.Required(
                    "organic_preference",
                    default=self.config_entry.data.get("organic_preference", True)
                ): bool,
                vol.Required(
                    "selected_plants",
                    default=self.config_entry.data.get("selected_plants", [])
                ): cv.multi_select(PLANT_TYPES),
                vol.Optional(
                    "custom_plants",
                    default=self.config_entry.data.get("custom_plants", "")
                ): str,
            }),
        )