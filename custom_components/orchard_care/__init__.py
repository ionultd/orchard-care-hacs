"""The Orchard Care integration."""
import logging
from datetime import datetime, timedelta
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry
from homeassistant.const import Platform

_LOGGER = logging.getLogger(__name__)

DOMAIN = "orchard_care"
PLATFORMS = [Platform.SENSOR, Platform.CALENDAR]

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Orchard Care component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Orchard Care from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = OrchardCareCoordinator(hass, entry)

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok

class OrchardCareCoordinator:
    """Coordinator for Orchard Care data."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self._data = {}
        self._update_interval = timedelta(hours=1)

        # Start periodic updates
        async_track_time_interval(hass, self._async_update, self._update_interval)

    async def _async_update(self, now):
        """Update orchard care data."""
        await self._calculate_care_schedules()

    async def _calculate_care_schedules(self):
        """Calculate care schedules for all configured plants."""
        hemisphere = self.entry.data.get("hemisphere", "northern")
        organic_preference = self.entry.data.get("organic_preference", True)
        selected_plants = self.entry.data.get("selected_plants", [])

        for plant in selected_plants:
            plant_data = PLANT_CARE_DATA.get(plant, {})
            if plant_data:
                self._data[plant] = self._get_plant_schedule(plant_data, hemisphere, organic_preference)

    def _get_plant_schedule(self, plant_data, hemisphere, organic_preference):
        """Get care schedule for a specific plant."""
        current_date = datetime.now()

        # Adjust months for southern hemisphere (6 month offset)
        month_offset = 6 if hemisphere == "southern" else 0

        pruning_months = plant_data.get("pruning_months", [])
        spray_months = plant_data.get("spray_months", [])

        # Adjust months for hemisphere
        if month_offset:
            pruning_months = [(m + month_offset - 1) % 12 + 1 for m in pruning_months]
            spray_months = [(m + month_offset - 1) % 12 + 1 for m in spray_months]

        # Get spray recommendations based on preference
        spray_type = "organic" if organic_preference else "conventional"
        spray_products = plant_data.get("spray_products", {}).get(spray_type, [])

        return {
            "pruning_months": pruning_months,
            "spray_months": spray_months,
            "spray_products": spray_products,
            "next_pruning": self._get_next_occurrence(pruning_months),
            "next_spray": self._get_next_occurrence(spray_months),
            "care_notes": plant_data.get("care_notes", "")
        }

    def _get_next_occurrence(self, months):
        """Get the next occurrence date for given months."""
        current_date = datetime.now()
        current_month = current_date.month
        current_year = current_date.year

        for month in sorted(months):
            if month >= current_month:
                return datetime(current_year, month, 1)

        # If no month this year, return first month next year
        if months:
            return datetime(current_year + 1, min(months), 1)

        return None

# Plant care data with seasonal care schedules
PLANT_CARE_DATA = {
    "apple": {
        "name": "Apple Tree",
        "pruning_months": [12, 1, 2],  # Winter pruning
        "spray_months": [3, 4, 5, 9],  # Early spring and fall
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Horticultural oil", "Bacillus thuringiensis"],
            "conventional": ["Captan", "Imidacloprid", "Malathion", "Fungicide spray"]
        },
        "care_notes": "Prune during dormancy. Spring sprays prevent scab and insects."
    },
    "pear": {
        "name": "Pear Tree",
        "pruning_months": [12, 1, 2],
        "spray_months": [3, 4, 5, 9],
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Kaolin clay", "Spinosad"],
            "conventional": ["Captan", "Imidacloprid", "Carbaryl", "Streptomycin"]
        },
        "care_notes": "Similar care to apples. Watch for fire blight."
    },
    "cherry": {
        "name": "Cherry Tree",
        "pruning_months": [6, 7, 8],  # Summer pruning to avoid disease
        "spray_months": [3, 4, 5],
        "spray_products": {
            "organic": ["Copper fungicide", "Neem oil", "Bacillus subtilis"],
            "conventional": ["Captan", "Propiconazole", "Imidacloprid"]
        },
        "care_notes": "Prune in summer to prevent silver leaf disease."
    },
    "plum": {
        "name": "Plum Tree",
        "pruning_months": [6, 7, 8],
        "spray_months": [3, 4, 5],
        "spray_products": {
            "organic": ["Copper fungicide", "Neem oil", "Horticultural oil"],
            "conventional": ["Captan", "Chlorpyrifos", "Fungicide spray"]
        },
        "care_notes": "Summer pruning prevents disease. Watch for brown rot."
    },
    "peach": {
        "name": "Peach Tree",
        "pruning_months": [12, 1, 2],
        "spray_months": [3, 4, 5, 6],
        "spray_products": {
            "organic": ["Copper fungicide", "Neem oil", "Sulfur spray", "Spinosad"],
            "conventional": ["Captan", "Imidacloprid", "Propiconazole", "Malathion"]
        },
        "care_notes": "Heavy pruning needed. Susceptible to peach leaf curl."
    },
    "apricot": {
        "name": "Apricot Tree",
        "pruning_months": [12, 1, 2],  # Winter pruning during dormancy
        "spray_months": [3, 4, 5, 6],  # Spring and early summer
        "spray_products": {
            "organic": ["Copper fungicide", "Neem oil", "Sulfur spray", "Horticultural oil", "Bacillus subtilis"],
            "conventional": ["Captan", "Imidacloprid", "Propiconazole", "Malathion", "Fungicide spray"]
        },
        "care_notes": "Prune during dormancy to maintain shape and airflow. Susceptible to brown rot and bacterial canker. Thin fruit for better quality."
    },
    "citrus_orange": {
        "name": "Orange Tree",
        "pruning_months": [3, 4, 5],  # Late winter/early spring
        "spray_months": [2, 3, 4, 8, 9],
        "spray_products": {
            "organic": ["Neem oil", "Horticultural oil", "Insecticidal soap", "Copper fungicide"],
            "conventional": ["Imidacloprid", "Abamectin", "Copper sulfate", "Fungicide spray"]
        },
        "care_notes": "Light pruning only. Watch for citrus canker and scale."
    },
    "citrus_lemon": {
        "name": "Lemon Tree",
        "pruning_months": [3, 4, 5],
        "spray_months": [2, 3, 4, 8, 9, 10],
        "spray_products": {
            "organic": ["Neem oil", "Horticultural oil", "Insecticidal soap", "Copper fungicide"],
            "conventional": ["Imidacloprid", "Abamectin", "Copper sulfate", "Systemic insecticide"]
        },
        "care_notes": "Minimal pruning. Regular feeding and watering important."
    },
    "grape": {
        "name": "Grapevine",
        "pruning_months": [12, 1, 2],
        "spray_months": [4, 5, 6, 7],
        "spray_products": {
            "organic": ["Copper fungicide", "Sulfur spray", "Bacillus subtilis", "Neem oil"],
            "conventional": ["Captan", "Mancozeb", "Imidacloprid", "Fungicide spray"]
        },
        "care_notes": "Heavy winter pruning required. Watch for powdery mildew."
    },
    "blueberry": {
        "name": "Blueberry Bush",
        "pruning_months": [12, 1, 2],
        "spray_months": [3, 4, 5],
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Horticultural oil", "Bacillus thuringiensis"],
            "conventional": ["Captan", "Imidacloprid", "Fungicide spray", "Insecticide spray"]
        },
        "care_notes": "Light pruning of old wood. Acidic soil preferred."
    },
    "raspberry": {
        "name": "Raspberry Cane",
        "pruning_months": [11, 12, 1, 2],
        "spray_months": [3, 4, 5],
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Horticultural oil"],
            "conventional": ["Captan", "Malathion", "Fungicide spray"]
        },
        "care_notes": "Remove old canes after fruiting. Thin new growth."
    },
    "blackberry": {
        "name": "Blackberry Cane",
        "pruning_months": [11, 12, 1, 2],
        "spray_months": [3, 4, 5],
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Horticultural oil"],
            "conventional": ["Captan", "Malathion", "Systemic fungicide"]
        },
        "care_notes": "Prune old canes to ground level. Train new growth."
    },
    "strawberry": {
        "name": "Strawberry Plant",
        "pruning_months": [11, 12, 1],  # Remove old leaves
        "spray_months": [3, 4, 5, 9],
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Bacillus subtilis"],
            "conventional": ["Captan", "Imidacloprid", "Fungicide spray"]
        },
        "care_notes": "Remove runners and old leaves. Watch for gray mold."
    },
    "fig": {
        "name": "Fig Tree",
        "pruning_months": [12, 1, 2, 3],  # Winter/early spring pruning
        "spray_months": [3, 4, 5, 8, 9],  # Spring and late summer
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Horticultural oil", "Insecticidal soap"],
            "conventional": ["Captan", "Imidacloprid", "Malathion", "Systemic fungicide"]
        },
        "care_notes": "Minimal pruning needed. Remove suckers and dead wood. Watch for fig rust and scale insects."
    },
    "avocado": {
        "name": "Avocado Tree",
        "pruning_months": [2, 3, 4],  # Late winter/early spring
        "spray_months": [2, 3, 4, 5, 8, 9, 10],  # Multiple seasons for pest control
        "spray_products": {
            "organic": ["Neem oil", "Horticultural oil", "Copper fungicide", "Bacillus thuringiensis", "Spinosad"],
            "conventional": ["Imidacloprid", "Abamectin", "Copper sulfate", "Systemic insecticide", "Fungicide spray"]
        },
        "care_notes": "Light pruning only - remove dead branches and suckers. Sensitive to over-pruning. Watch for thrips, mites, and root rot."
    },
    "kiwi": {
        "name": "Kiwi Vine",
        "pruning_months": [6, 7, 8],  # Winter pruning (dormant season)
        "spray_months": [9, 10, 11, 3, 4],  # Spring and early summer
        "spray_products": {
            "organic": ["Copper fungicide", "Neem oil", "Horticultural oil", "Bacillus thuringiensis", "Spinosad"],
            "conventional": ["Captan", "Imidacloprid", "Mancozeb", "Systemic insecticide", "Fungicide spray"]
        },
        "care_notes": "Heavy winter pruning required. Train on strong trellis system. Separate male and female plants needed. Watch for scale insects and bacterial canker."
    },
    "persimmon": {
        "name": "Persimmon Tree",
        "pruning_months": [12, 1, 2],  # Winter pruning during dormancy
        "spray_months": [3, 4, 5, 8, 9],  # Spring and late summer
        "spray_products": {
            "organic": ["Neem oil", "Copper fungicide", "Horticultural oil", "Bacillus subtilis", "Kaolin clay"],
            "conventional": ["Captan", "Imidacloprid", "Propiconazole", "Malathion", "Fungicide spray"]
        },
        "care_notes": "Minimal pruning needed - persimmons fruit on new wood. Remove water sprouts and dead branches. Watch for persimmon psylla and scale insects."
    }
}