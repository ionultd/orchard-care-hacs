"""Sensor platform for Orchard Care integration."""
from datetime import datetime, timedelta
from homeassistant.components.sensor import SensorEntity, SensorDeviceClass
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.entity import EntityCategory

from . import DOMAIN, OrchardCareCoordinator, PLANT_CARE_DATA

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Orchard Care sensor based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    selected_plants = config_entry.data.get("selected_plants", [])

    for plant in selected_plants:
        entities.extend([
            OrchardCarePruningSensor(coordinator, plant, config_entry),
            OrchardCareSpraySensor(coordinator, plant, config_entry),
        ])

    async_add_entities(entities)

class OrchardCareBaseSensor(SensorEntity):
    """Base sensor for Orchard Care."""

    def __init__(self, coordinator: OrchardCareCoordinator, plant: str, config_entry: ConfigEntry):
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.plant = plant
        self.config_entry = config_entry
        self.plant_data = PLANT_CARE_DATA.get(plant, {})

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.plant)},
            "name": self.plant_data.get("name", self.plant.title()),
            "manufacturer": "Orchard Care",
            "model": "Fruit Tree/Berry Care",
        }

class OrchardCarePruningSensor(OrchardCareBaseSensor):
    """Sensor for pruning schedule."""

    @property
    def unique_id(self):
        """Return unique ID."""
        return f"{DOMAIN}_{self.plant}_pruning"

    @property
    def name(self):
        """Return the name."""
        return f"{self.plant_data.get('name', self.plant.title())} Pruning"

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:content-cut"

    @property
    def native_value(self):
        """Return the state."""
        plant_schedule = self.coordinator._data.get(self.plant, {})
        next_pruning = plant_schedule.get("next_pruning")

        if next_pruning:
            days_until = (next_pruning - datetime.now()).days
            if days_until <= 0:
                return "Now"
            elif days_until <= 30:
                return f"In {days_until} days"
            else:
                return next_pruning.strftime("%B %Y")
        return "Not scheduled"

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        plant_schedule = self.coordinator._data.get(self.plant, {})
        return {
            "pruning_months": plant_schedule.get("pruning_months", []),
            "next_pruning_date": plant_schedule.get("next_pruning"),
            "care_notes": self.plant_data.get("care_notes", ""),
            "plant_type": self.plant_data.get("name", self.plant.title())
        }

class OrchardCareSpraySensor(OrchardCareBaseSensor):
    """Sensor for spraying schedule."""

    @property
    def unique_id(self):
        """Return unique ID."""
        return f"{DOMAIN}_{self.plant}_spray"

    @property
    def name(self):
        """Return the name."""
        return f"{self.plant_data.get('name', self.plant.title())} Spray"

    @property
    def icon(self):
        """Return the icon."""
        return "mdi:spray"

    @property
    def native_value(self):
        """Return the state."""
        plant_schedule = self.coordinator._data.get(self.plant, {})
        next_spray = plant_schedule.get("next_spray")

        if next_spray:
            days_until = (next_spray - datetime.now()).days
            if days_until <= 0:
                return "Now"
            elif days_until <= 30:
                return f"In {days_until} days"
            else:
                return next_spray.strftime("%B %Y")
        return "Not scheduled"

    @property
    def extra_state_attributes(self):
        """Return additional attributes."""
        plant_schedule = self.coordinator._data.get(self.plant, {})
        organic_pref = self.config_entry.data.get("organic_preference", True)
        spray_type = "organic" if organic_pref else "conventional"

        return {
            "spray_months": plant_schedule.get("spray_months", []),
            "next_spray_date": plant_schedule.get("next_spray"),
            "spray_products": plant_schedule.get("spray_products", []),
            "spray_type": spray_type,
            "care_notes": self.plant_data.get("care_notes", ""),
            "plant_type": self.plant_data.get("name", self.plant.title())
        }