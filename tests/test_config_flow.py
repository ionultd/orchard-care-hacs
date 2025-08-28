"""Test the Orchard Care config flow."""
import pytest
from homeassistant import config_entries
from custom_components.orchard_care.const import DOMAIN

async def test_form(hass):
    """Test we get the form."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] == "form"
    assert result["errors"] == {}