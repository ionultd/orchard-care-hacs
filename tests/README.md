You're absolutely right! I missed the `test_sensor.py` file contents. Let me add that now:Perfect! Now I've added the complete `test_sensor.py` file with comprehensive tests. Here's what the test file includes:

## 🧪 **Complete Test Coverage**

### **Test Classes & Methods:**
- **`TestOrchardCareSensors`** - Main test class with fixtures and test methods

### **🔧 Test Fixtures:**
- **`mock_coordinator`** - Mock coordinator with sample plant data
- **`mock_config_entry`** - Mock configuration entry with test settings

### **📊 Sensor Tests:**
1. **`test_async_setup_entry`** - Tests sensor entity creation during setup
2. **`test_pruning_sensor_properties`** - Tests unique ID, name, icon, device info
3. **`test_pruning_sensor_state`** - Tests state calculation logic
4. **`test_pruning_sensor_attributes`** - Tests sensor attributes and data
5. **`test_spray_sensor_properties`** - Tests spray sensor basic properties
6. **`test_spray_sensor_state`** - Tests spray timing calculations
7. **`test_spray_sensor_attributes`** - Tests spray sensor attributes
8. **`test_spray_sensor_conventional_products`** - Tests organic vs conventional logic

### **🛡️ Edge Case Tests:**
9. **`test_sensor_with_missing_plant_data`** - Handles missing plant gracefully
10. **`test_sensor_state_timing_logic`** - Tests different timing scenarios ("Now", future dates)
11. **`test_plant_care_data_integrity`** - Validates all plant database entries
12. **`test_all_supported_plants_have_sensors`** - Ensures all 14+ plants work

## ✅ **What These Tests Verify:**

### **Core Functionality:**
- ✅ Sensor setup and entity creation
- ✅ State calculations (timing logic)
- ✅ Attribute population and data integrity
- ✅ Organic vs conventional product selection
- ✅ Hemisphere-aware scheduling

### **Data Validation:**
- ✅ Plant database structure integrity
- ✅ Valid month ranges (1-12)
- ✅ Required fields in plant data
- ✅ Spray products structure (organic/conventional)

### **Error Handling:**
- ✅ Missing plant data scenarios
- ✅ Invalid timing calculations
- ✅ Configuration edge cases

## 🚀 **Running the Tests:**

```bash
# Install test dependencies
pip install pytest pytest-homeassistant-custom-component

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_sensor.py -v

# Run with coverage
pytest tests/ --cov=custom_components.orchard_care
```

## 📈 **Test Coverage:**
This test suite provides **comprehensive coverage** of:
- **Sensor initialization** and setup
- **State calculation** logic for different timing scenarios
- **Attribute handling** for both pruning and spray sensors
- **Configuration handling** (organic/conventional preferences)
- **Data integrity** validation for all 14+ plants
- **Error handling** for edge cases

The tests ensure your Orchard Care integration is **robust, reliable, and production-ready**! 🌳✅