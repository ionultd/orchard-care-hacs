# custom_components/orchard_care/calendar.py - ENHANCED VERSION
"""Enhanced Calendar platform for Orchard Care integration with smart reminders."""
from datetime import datetime, timedelta
from typing import Optional, List
from homeassistant.components.calendar import CalendarEntity, CalendarEvent
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.event import async_track_time_interval, async_call_later
from homeassistant.const import EVENT_HOMEASSISTANT_STARTED

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

    # Add a master calendar that combines all plants
    if selected_plants:
        entities.append(OrchardCareMasterCalendar(coordinator, config_entry))

    async_add_entities(entities)

class OrchardCareCalendar(CalendarEntity):
    """Calendar entity for individual Orchard Care plants with smart reminders."""

    def __init__(self, coordinator: OrchardCareCoordinator, plant: str, config_entry: ConfigEntry):
        """Initialize the calendar."""
        self.coordinator = coordinator
        self.plant = plant
        self.config_entry = config_entry
        self.plant_data = PLANT_CARE_DATA.get(plant, {})
        self._upcoming_events = []
        self._last_reminder_dates = {}

    async def async_added_to_hass(self):
        """When entity is added to hass."""
        await super().async_added_to_hass()

        # Start reminder checking every hour
        async_track_time_interval(
            self.hass, self._check_reminders, timedelta(hours=1)
        )

        # Check reminders on startup
        if self.hass.is_running:
            await self._check_reminders()
        else:
            self.hass.bus.async_listen_once(
                EVENT_HOMEASSISTANT_STARTED, self._check_reminders
            )

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
        """Return the current or next event."""
        now = datetime.now()
        events = self._get_events(now, now + timedelta(days=7))

        # Return the most urgent event (closest to now)
        if events:
            return min(events, key=lambda x: abs((x.start - now).total_seconds()))
        return None

    def get_events(self, hass, start_date, end_date):
        """Get all events in a specific time range."""
        return self._get_events(start_date, end_date)

    def _get_events(self, start_date, end_date):
        """Generate care events for the specified date range with enhanced details."""
        events = []
        plant_schedule = self.coordinator._data.get(self.plant, {})

        # Generate pruning events with reminders
        pruning_months = plant_schedule.get("pruning_months", [])
        self._generate_pruning_events(events, pruning_months, start_date, end_date)

        # Generate spray events with weather considerations
        spray_months = plant_schedule.get("spray_months", [])
        self._generate_spray_events(events, spray_months, start_date, end_date)

        # Generate reminder events (1 week and 3 days before)
        self._generate_reminder_events(events, start_date, end_date)

        return sorted(events, key=lambda x: x.start)

    def _generate_pruning_events(self, events: List[CalendarEvent], pruning_months: List[int], start_date: datetime, end_date: datetime):
        """Generate pruning events with detailed information."""
        for year in range(start_date.year, end_date.year + 2):
            for month in pruning_months:
                # Main pruning event (mid-month)
                event_date = datetime(year, month, 15, 9, 0)  # 9 AM
                if start_date <= event_date <= end_date:
                    plant_name = self.plant_data.get('name', self.plant.title())
                    care_notes = self.plant_data.get('care_notes', '')

                    # Enhanced description with tips
                    description = self._get_pruning_description(plant_name, care_notes, month)

                    events.append(CalendarEvent(
                        start=event_date,
                        end=event_date + timedelta(hours=3),
                        summary=f"🌳 Prune {plant_name}",
                        description=description,
                        location="Orchard/Garden"
                    ))

    def _generate_spray_events(self, events: List[CalendarEvent], spray_months: List[int], start_date: datetime, end_date: datetime):
        """Generate spray events with product recommendations."""
        organic_pref = self.config_entry.data.get("organic_preference", True)
        spray_products = self.coordinator._data.get(self.plant, {}).get("spray_products", [])

        for year in range(start_date.year, end_date.year + 2):
            for month in spray_months:
                # Spray event (first week of month, weather permitting)
                event_date = datetime(year, month, 7, 7, 0)  # 7 AM (good spraying time)
                if start_date <= event_date <= end_date:
                    plant_name = self.plant_data.get('name', self.plant.title())
                    spray_type = "Organic" if organic_pref else "Conventional"

                    # Enhanced description with weather and product info
                    description = self._get_spray_description(plant_name, spray_type, spray_products, month)

                    events.append(CalendarEvent(
                        start=event_date,
                        end=event_date + timedelta(hours=2),
                        summary=f"🌿 Spray {plant_name} ({spray_type})",
                        description=description,
                        location="Orchard/Garden"
                    ))

    def _generate_reminder_events(self, events: List[CalendarEvent], start_date: datetime, end_date: datetime):
        """Generate reminder events for upcoming care tasks."""
        main_events = [e for e in events if not e.summary.startswith("📅")]

        for event in main_events:
            # 1 week reminder
            reminder_1w = event.start - timedelta(days=7)
            if start_date <= reminder_1w <= end_date:
                events.append(CalendarEvent(
                    start=reminder_1w,
                    end=reminder_1w + timedelta(minutes=15),
                    summary=f"📅 Reminder: {event.summary} in 1 week",
                    description=f"Prepare for upcoming care task: {event.description[:100]}...",
                    location="Reminder"
                ))

            # 3 day reminder
            reminder_3d = event.start - timedelta(days=3)
            if start_date <= reminder_3d <= end_date:
                events.append(CalendarEvent(
                    start=reminder_3d,
                    end=reminder_3d + timedelta(minutes=15),
                    summary=f"📅 Reminder: {event.summary} in 3 days",
                    description=f"Check weather and prepare materials for: {event.description[:100]}...",
                    location="Reminder"
                ))

    def _get_pruning_description(self, plant_name: str, care_notes: str, month: int) -> str:
        """Get detailed pruning description with seasonal tips."""
        seasonal_tips = {
            12: "Dormant season pruning - trees are fully dormant. Best time for major structural work.",
            1: "Peak dormant season - ideal pruning conditions. Wounds heal quickly in spring.",
            2: "Late dormant season - complete pruning before buds break. Last chance for major cuts.",
            6: "Summer pruning - active growth period. Light pruning only, avoid heavy cuts.",
            7: "Mid-summer pruning - good for stone fruits. Reduces disease risk.",
            8: "Late summer pruning - healing time before winter. Focus on dead/diseased wood."
        }

        tip = seasonal_tips.get(month, "Follow seasonal pruning guidelines for your plant type.")

        return f"""
🌳 PRUNING TASK: {plant_name}

📋 Care Notes: {care_notes}

🕐 Best Time: Early morning when cool
🌡️ Temperature: Above freezing, dry conditions
🛠️ Tools Needed: Clean, sharp pruning shears, loppers, saw (if needed)

💡 Seasonal Tip: {tip}

✅ Checklist:
• Check weather forecast (avoid rain for 24-48hrs)
• Sanitize tools with rubbing alcohol
• Remove dead, diseased, damaged wood first
• Thin overcrowded branches
• Make clean cuts at 45° angle above buds
• Apply wound sealant if cuts are large (>2 inches)

⚠️ Safety: Wear gloves and eye protection. Be aware of power lines.
        """.strip()

    def _get_spray_description(self, plant_name: str, spray_type: str, products: List[str], month: int) -> str:
        """Get detailed spray description with weather and product info."""
        weather_conditions = """
🌤️ IDEAL CONDITIONS:
• Temperature: 60-80°F (15-27°C)
• Wind: Less than 10 mph
• Humidity: 40-70%
• No rain expected for 4-6 hours
• Early morning or evening application
        """.strip()

        products_text = ", ".join(products[:3]) if products else "See care guide for recommendations"

        return f"""
🌿 SPRAY TREATMENT: {plant_name} ({spray_type})

📦 Recommended Products: {products_text}

{weather_conditions}

✅ Pre-Spray Checklist:
• Check weather forecast
• Inspect plant for beneficial insects
• Ensure calm wind conditions
• Mix chemicals according to label
• Wear appropriate PPE

🎯 Application Tips:
• Cover all leaf surfaces (top and bottom)
• Spray early morning or late evening
• Avoid spraying during bloom (protect pollinators)
• Keep pets and children away during application
• Clean equipment thoroughly after use

📱 Weather Check: Monitor conditions 24hrs before spraying
⚠️ Safety: Always read and follow product labels
        """.strip()

    @callback
    async def _check_reminders(self, now=None):
        """Check for upcoming events and send notifications."""
        if now is None:
            now = datetime.now()

        # Get events for the next 14 days
        upcoming_events = self._get_events(now, now + timedelta(days=14))

        for event in upcoming_events:
            days_until = (event.start.date() - now.date()).days

            # Send notifications for care tasks (not reminders)
            if not event.summary.startswith("📅") and days_until in [7, 3, 1, 0]:
                await self._send_care_notification(event, days_until)

    async def _send_care_notification(self, event: CalendarEvent, days_until: int):
        """Send notification for upcoming care task."""
        event_key = f"{event.summary}_{event.start.date()}"

        # Avoid duplicate notifications
        if event_key in self._last_reminder_dates:
            return

        self._last_reminder_dates[event_key] = datetime.now()

        # Create notification based on urgency
        if days_until == 0:
            urgency = "🚨 TODAY"
            message = f"Today is the day for: {event.summary}"
        elif days_until == 1:
            urgency = "⏰ TOMORROW"
            message = f"Don't forget: {event.summary} is tomorrow"
        elif days_until == 3:
            urgency = "📅 3 DAYS"
            message = f"Coming up: {event.summary} in 3 days"
        else:
            urgency = "📅 1 WEEK"
            message = f"Plan ahead: {event.summary} in 1 week"

        # Send to Home Assistant notification service
        await self.hass.services.async_call(
            "persistent_notification",
            "create",
            {
                "title": f"{urgency} - Orchard Care",
                "message": message,
                "notification_id": f"orchard_care_{event_key}",
            },
        )

class OrchardCareMasterCalendar(CalendarEntity):
    """Master calendar combining all orchard care plants."""

    def __init__(self, coordinator: OrchardCareCoordinator, config_entry: ConfigEntry):
        """Initialize the master calendar."""
        self.coordinator = coordinator
        self.config_entry = config_entry
        self.selected_plants = config_entry.data.get("selected_plants", [])

    @property
    def unique_id(self):
        """Return unique ID."""
        return f"{DOMAIN}_master_calendar"

    @property
    def name(self):
        """Return the name."""
        return "Orchard Care - All Plants"

    @property
    def event(self):
        """Return the most urgent event across all plants."""
        now = datetime.now()
        all_events = []

        for plant in self.selected_plants:
            plant_calendar = OrchardCareCalendar(self.coordinator, plant, self.config_entry)
            events = plant_calendar._get_events(now, now + timedelta(days=30))
            all_events.extend(events)

        if all_events:
            return min(all_events, key=lambda x: abs((x.start - now).total_seconds()))
        return None

    def get_events(self, hass, start_date, end_date):
        """Get all events from all plants."""
        all_events = []

        for plant in self.selected_plants:
            plant_calendar = OrchardCareCalendar(self.coordinator, plant, self.config_entry)
            events = plant_calendar._get_events(start_date, end_date)
            all_events.extend(events)

        return sorted(all_events, key=lambda x: x.start)

# Additional automation helper for advanced users
ORCHARD_CARE_AUTOMATIONS = """
# Example automations to add to your configuration.yaml

automation:
  # Morning care reminder
  - alias: "Orchard Care - Morning Briefing"
    trigger:
      - platform: time
        at: "07:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "🌳 Daily Orchard Update"
          message: >
            {% set events = state_attr('calendar.orchard_care_all_plants', 'events') %}
            {% if events %}
              Today's tasks: {{ events[0].summary }}
            {% else %}
              No orchard tasks scheduled for today.
            {% endif %}

  # Weather-aware spray reminder
  - alias: "Orchard Care - Weather Check for Spraying"
    trigger:
      - platform: calendar
        event: start
        entity_id: calendar.orchard_care_all_plants
    condition:
      - condition: template
        value_template: "{{ 'Spray' in trigger.calendar_event.summary }}"
      - condition: numeric_state
        entity_id: weather.forecast
        attribute: wind_speed
        below: 15
      - condition: state
        entity_id: weather.forecast
        state:
          - 'sunny'
          - 'partlycloudy'
    action:
      - service: notify.family
        data:
          title: "🌿 Perfect Spraying Conditions!"
          message: >
            Weather is ideal for: {{ trigger.calendar_event.summary }}
            Wind: {{ states.weather.forecast.attributes.wind_speed }} mph
            Conditions: {{ states.weather.forecast.state }}

  # Preparation reminder
  - alias: "Orchard Care - Prep Reminder"
    trigger:
      - platform: calendar
        event: start
        entity_id: calendar.orchard_care_all_plants
        offset: "-24:00:00"
    action:
      - service: notify.mobile_app_your_phone
        data:
          title: "📋 Orchard Care Prep"
          message: >
            Tomorrow: {{ trigger.calendar_event.summary }}
            Time to check tools and supplies!
"""