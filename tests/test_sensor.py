"""Test the Orchard Care sensors."""
import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from custom_components.orchard_care.sensor import (
    async_setup_entry,
    OrchardCarePruningSensor,
    OrchardCareSpraySensor,
)
from custom_components.orchard_care import OrchardCareCoordinator, PLANT_CARE_DATA


class TestOrchardCareSensors:
    """Test Orchard Care sensor functionality."""

    @pytest.fixture
    def mock_coordinator(self):
        """Create a mock coordinator."""
        coordinator = Mock(spec=OrchardCareCoordinator)
        coordinator._data = {
            "apple": {
                "pruning_months": [12, 1, 2],
                "spray_months": [3, 4, 5, 9],
                "spray_products": ["Neem oil", "Copper fungicide"],
                "next_pruning": datetime.now() + timedelta(days=15),
                "next_spray": datetime.now() + timedelta(days=5),
                "care_notes": "Test care notes"
            }
        }
        return coordinator

    @pytest.fixture
    def mock_config_entry(self):
        """Create a mock config entry."""
        config_entry = Mock(spec=ConfigEntry)
        config_entry.data = {
            "hemisphere": "northern",
            "organic_preference": True,
            "selected_plants": ["apple", "pear"]
        }
        return config_entry

    async def test_async_setup_entry(self, hass: HomeAssistant, mock_coordinator, mock_config_entry):
        """Test sensor setup."""
        with patch('custom_components.orchard_care.sensor.DOMAIN', 'orchard_care'):
            # Mock hass data
            hass.data = {
                'orchard_care': {
                    'test_entry': mock_coordinator
                }
            }
            mock_config_entry.entry_id = 'test_entry'

            entities = []
            async def mock_add_entities(new_entities):
                entities.extend(new_entities)

            await async_setup_entry(hass, mock_config_entry, mock_add_entities)

            # Should create 2 sensors per plant (pruning + spray) * 2 plants = 4 sensors
            assert len(entities) == 4
            assert any(isinstance(entity, OrchardCarePruningSensor) for entity in entities)
            assert any(isinstance(entity, OrchardCareSpraySensor) for entity in entities)

    def test_pruning_sensor_properties(self, mock_coordinator, mock_config_entry):
        """Test pruning sensor properties."""
        sensor = OrchardCarePruningSensor(mock_coordinator, "apple", mock_config_entry)

        # Test basic properties
        assert sensor.unique_id == "orchard_care_apple_pruning"
        assert sensor.name == "Apple Tree Pruning"
        assert sensor.icon == "mdi:content-cut"

        # Test device info
        device_info = sensor.device_info
        assert device_info["name"] == "Apple Tree"
        assert device_info["manufacturer"] == "Orchard Care"

    def test_pruning_sensor_state(self, mock_coordinator, mock_config_entry):
        """Test pruning sensor state calculation."""
        sensor = OrchardCarePruningSensor(mock_coordinator, "apple", mock_config_entry)

        # Test state value
        state = sensor.native_value
        assert "15 days" in state or state == "In 15 days"

    def test_pruning_sensor_attributes(self, mock_coordinator, mock_config_entry):
        """Test pruning sensor attributes."""
        sensor = OrchardCarePruningSensor(mock_coordinator, "apple", mock_config_entry)

        attributes = sensor.extra_state_attributes
        assert "pruning_months" in attributes
        assert "next_pruning_date" in attributes
        assert "care_notes" in attributes
        assert "plant_type" in attributes
        assert attributes["plant_type"] == "Apple Tree"

    def test_spray_sensor_properties(self, mock_coordinator, mock_config_entry):
        """Test spray sensor properties."""
        sensor = OrchardCareSpraySensor(mock_coordinator, "apple", mock_config_entry)

        # Test basic properties
        assert sensor.unique_id == "orchard_care_apple_spray"
        assert sensor.name == "Apple Tree Spray"
        assert sensor.icon == "mdi:spray"

    def test_spray_sensor_state(self, mock_coordinator, mock_config_entry):
        """Test spray sensor state calculation."""
        sensor = OrchardCareSpraySensor(mock_coordinator, "apple", mock_config_entry)

        # Test state value
        state = sensor.native_value
        assert "5 days" in state or state == "In 5 days"

    def test_spray_sensor_attributes(self, mock_coordinator, mock_config_entry):
        """Test spray sensor attributes."""
        sensor = OrchardCareSpraySensor(mock_coordinator, "apple", mock_config_entry)

        attributes = sensor.extra_state_attributes
        assert "spray_months" in attributes
        assert "next_spray_date" in attributes
        assert "spray_products" in attributes
        assert "spray_type" in attributes
        assert attributes["spray_type"] == "organic"  # Based on config preference

    def test_spray_sensor_conventional_products(self, mock_coordinator, mock_config_entry):
        """Test spray sensor with conventional preference."""
        mock_config_entry.data["organic_preference"] = False
        sensor = OrchardCareSpraySensor(mock_coordinator, "apple", mock_config_entry)

        attributes = sensor.extra_state_attributes
        assert attributes["spray_type"] == "conventional"

    def test_sensor_with_missing_plant_data(self, mock_coordinator, mock_config_entry):
        """Test sensor behavior with missing plant data."""
        # Test with a plant not in coordinator data
        sensor = OrchardCarePruningSensor(mock_coordinator, "nonexistent", mock_config_entry)

        # Should handle gracefully
        state = sensor.native_value
        assert state == "Not scheduled"

    def test_sensor_state_timing_logic(self, mock_coordinator, mock_config_entry):
        """Test different timing scenarios."""
        # Test "Now" state
        mock_coordinator._data["apple"]["next_pruning"] = datetime.now() - timedelta(days=1)
        sensor = OrchardCarePruningSensor(mock_coordinator, "apple", mock_config_entry)
        assert sensor.native_value == "Now"

        # Test future date beyond 30 days
        mock_coordinator._data["apple"]["next_pruning"] = datetime.now() + timedelta(days=45)
        sensor = OrchardCarePruningSensor(mock_coordinator, "apple", mock_config_entry)
        state = sensor.native_value
        # Should show month/year format
        assert any(month in state for month in ["January", "February", "March", "April", "May", "June",
                                               "July", "August", "September", "October", "November", "December"])

    def test_plant_care_data_integrity(self):
        """Test that plant care data is properly structured."""
        for plant_key, plant_data in PLANT_CARE_DATA.items():
            # Check required fields
            assert "name" in plant_data
            assert "pruning_months" in plant_data
            assert "spray_months" in plant_data
            assert "spray_products" in plant_data
            assert "care_notes" in plant_data

            # Check spray products structure
            spray_products = plant_data["spray_products"]
            assert "organic" in spray_products
            assert "conventional" in spray_products
            assert isinstance(spray_products["organic"], list)
            assert isinstance(spray_products["conventional"], list)

            # Check months are valid (1-12)
            for month in plant_data["pruning_months"]:
                assert 1 <= month <= 12
            for month in plant_data["spray_months"]:
                assert 1 <= month <= 12

    def test_all_supported_plants_have_sensors(self, mock_config_entry):
        """Test that all plants in PLANT_CARE_DATA can create sensors."""
        mock_coordinator = Mock(spec=OrchardCareCoordinator)
        mock_coordinator._data = {}

        for plant_key in PLANT_CARE_DATA.keys():
            # Should not raise exceptions
            pruning_sensor = OrchardCarePruningSensor(mock_coordinator, plant_key, mock_config_entry)
            spray_sensor = OrchardCareSpraySensor(mock_coordinator, plant_key, mock_config_entry)

            assert pruning_sensor.unique_id.endswith("_pruning")
            assert spray_sensor.unique_id.endswith("_spray")
            assert pruning_sensor.plant_data["name"]  # Should have plant data