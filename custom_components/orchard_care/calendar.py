"""Calendar platform for Orchard Care integration."""
from datetime import datetime, timedelta
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from . import DOMAIN, OrchardCareCoordinator, PLANT_CARE_DATA

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Orchard Care calendar based on a config entry."""
    coordinator = hass.data[DOMAIN][config_entry.entry_id]

    entities = []
    selected_plants = config_entry.data.get("selected_plants", [])

    for plant in selected_plants:
        entities.append(OrchardCareCalendar(coordinator, plant, config_entry))

    async_add_entities(entities)

class OrchardCareCalendar(CalendarEntity):
    """Calendar entity for Orchard Care events."""

    def __init__(self, coordinator: OrchardCareCoordinator, plant: str, config_entry: ConfigEntry):
        """Initialize the calendar."""
        self.coordinator = coordinator
        self.plant = plant
        self.config_entry = config_entry
        self.plant_data = PLANT_CARE_DATA.get(plant, {})

    @property
    def unique_id(self):
        """Return unique ID."""
        return f"{DOMAIN}_{self.plant}_calendar"

    @property
    def name(self):
        """Return the name."""
        return f"{self.plant_data.get('name', self.plant.title())} Care Calendar"

    @property
    def device_info(self):
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.plant)},
            "name": self.plant_data.get("name", self.plant.title()),
            "manufacturer": "Orchard Care",
            "model": "Fruit Tree/Berry Care",
        }

    @property
    def event(self):
        """Return the current event."""
        events = self._get_events(datetime.now(), datetime.now() + timedelta(days=1))
        return events[0] if events else None

    def get_events(self, hass, start_date, end_date):
        """Get all events in a specific time range."""
        return self._get_events(start_date, end_date)

    def _get_events(self, start_date, end_date):
        """Generate care events for the specified date range."""
        events = []
        plant_schedule = self.coordinator._data.get(self.plant, {})

        # Generate pruning events
        pruning_months = plant_schedule.get("pruning_months", [])
        for year in range(start_date.year, end_date.year + 2):
            for month in pruning_months:
                event_date = datetime(year, month, 15)  # Mid-month
                if start_date <= event_date <= end_date:
                    events.append(CalendarEvent(
                        start=event_date,
                        end=event_date + timedelta(hours=2),
                        summary=f"Prune {self.plant_data.get('name', self.plant.title())}",
                        description=f"Pruning time for {self.plant_data.get('name')}. {self.plant_data.get('care_notes', '')}"
                    ))

        # Generate spray events
        spray_months = plant_schedule.get("spray_months", [])
        organic_pref = self.config_entry.data.get("organic_preference", True)
        spray_products = plant_schedule.get("spray_products", [])

        for year in range(start_date.year, end_date.year + 2):
            for month in spray_months:
                event_date = datetime(year, month, 1)  # First of month
                if start_date <= event_date <= end_date:
                    spray_type = "Organic" if organic_pref else "Conventional"
                    products_text = ", ".join(spray_products[:3]) if spray_products else "See care guide"

                    events.append(CalendarEvent(
                        start=event_date,
                        end=event_date + timedelta(hours=1),
                        summary=f"Spray {self.plant_data.get('name', self.plant.title())}",
                        description=f"{spray_type} spray treatment. Recommended products: {products_text}"
                    ))

        return sorted(events, key=lambda x: x.start)