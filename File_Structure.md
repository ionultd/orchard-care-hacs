# 🗂️ Orchard Care Integration - Complete File Structure

```
orchard-care-hacs/
├── 📁 custom_components/
│   └── 📁 orchard_care/
│       ├── 📄 __init__.py                    # Main integration setup & coordinator
│       ├── 📄 config_flow.py                 # Configuration flow & options
│       ├── 📄 const.py                       # Constants & plant database
│       ├── 📄 sensor.py                      # Pruning & spray sensor entities
│       ├── 📄 calendar.py                    # Calendar integration for events
│       ├── 📄 manifest.json                  # Integration metadata & requirements
│       ├── 📄 strings.json                   # UI configuration strings
│       └── 📁 translations/
│           └── 📄 en.json                    # English translations
│
├── 📁 www/
│   └── 📄 orchard-care-card.js              # Custom Lovelace dashboard card
│
├── 📄 README.md                             # Complete documentation
├── 📄 LICENSE                               # MIT License
├── 📄 CHANGELOG.md                          # Version history
├── 📄 hacs.json                            # HACS repository configuration
├── 📄 .gitignore                           # Git ignore rules
└── 📄 info.md                              # HACS info page
```

## 📋 **Detailed File Contents**

### **🔧 Core Integration Files**

#### `custom_components/orchard_care/__init__.py`
```python
# Main integration setup
- OrchardCareCoordinator class
- Platform loading (sensor, calendar)
- Care schedule calculation logic
- Hemisphere adjustment algorithms
- PLANT_CARE_DATA with 12+ plants
```

#### `custom_components/orchard_care/config_flow.py`
```python
# Configuration interface
- Initial setup flow
- Options flow for modifications
- Validation logic
- Multi-select plant picker
- Hemisphere & organic preference toggles
```

#### `custom_components/orchard_care/const.py`
```python
# Constants and plant database
- DOMAIN = "orchard_care"
- PLANT_TYPES dictionary
- Platform definitions
- Default configurations
```

#### `custom_components/orchard_care/sensor.py`
```python
# Sensor entities
- OrchardCarePruningSensor class
- OrchardCareSpraySensor class
- Timing calculations
- Status attributes
- Product recommendations
```

#### `custom_components/orchard_care/calendar.py`
```python
# Calendar integration
- OrchardCareCalendar class
- Event generation
- Date range handling
- Care event descriptions
```

#### `custom_components/orchard_care/manifest.json`
```json
{
  "domain": "orchard_care",
  "name": "Orchard Care",
  "config_flow": true,
  "dependencies": [],
  "requirements": [],
  "version": "1.0.0"
}
```

### **🎨 Frontend Components**

#### `www/orchard-care-card.js`
```javascript
# Custom Lovelace card
- OrchardCareCard class (main card)
- OrchardCareCardEditor class (configuration)
- Modern glassmorphism styling
- Status indicators & animations
- Responsive design
- Interactive demo features
```

### **📖 Documentation Files**

#### `README.md`
```markdown
# Complete user documentation
- Installation instructions
- Configuration examples
- Supported plants table
- Automation examples
- Troubleshooting guide
- Development info
```

#### `info.md` (HACS Info Page)
```markdown
# HACS repository information
- Quick feature overview
- Installation steps
- Basic configuration
- Screenshot placeholders
```

#### `hacs.json`
```json
{
  "name": "Orchard Care",
  "render_readme": true,
  "domains": ["sensor", "calendar"],
  "homeassistant": "2023.1.0"
}
```

### **🌐 Localization**

#### `custom_components/orchard_care/strings.json`
```json
# Configuration UI strings
- Step titles and descriptions
- Data field labels
- Validation messages
```

#### `custom_components/orchard_care/translations/en.json`
```json
# English translations
- Detailed field descriptions
- Help text
- Error messages
```

## 📦 **Installation Directory Structure**

After installation, files are placed in:

```
homeassistant/
├── 📁 custom_components/
│   └── 📁 orchard_care/           # ← Integration files go here
│       ├── __init__.py
│       ├── config_flow.py
│       ├── const.py
│       ├── sensor.py
│       ├── calendar.py
│       ├── manifest.json
│       ├── strings.json
│       └── translations/
│           └── en.json
│
└── 📁 www/
    └── orchard-care-card.js       # ← Card file goes here
```

## 🔄 **Development Workflow**

### **1. Local Development**
```bash
# Clone to HA dev environment
git clone https://github.com/username/orchard-care-hacs
cd orchard-care-hacs

# Symlink to HA custom_components
ln -s $(pwd)/custom_components/orchard_care ~/.homeassistant/custom_components/

# Copy card to www
cp www/orchard-care-card.js ~/.homeassistant/www/
```

### **2. Testing Structure**
```
tests/
├── 📄 test_config_flow.py         # Configuration flow tests
├── 📄 test_sensor.py              # Sensor entity tests
├── 📄 test_calendar.py            # Calendar tests
├── 📄 test_coordinator.py         # Core logic tests
└── 📁 fixtures/
    └── 📄 plant_data.json         # Test data
```

### **3. GitHub Repository Structure**
```
.github/
├── 📁 workflows/
│   ├── 📄 validate.yml            # HACS validation
│   ├── 📄 release.yml             # Auto-release workflow
│   └── 📄 test.yml                # Automated testing
├── 📄 ISSUE_TEMPLATE.md           # Bug report template
└── 📄 PULL_REQUEST_TEMPLATE.md    # PR template
```

## 🏷️ **Entity Naming Convention**

```
# Sensors
sensor.apple_tree_pruning          # sensor.{plant}_pruning
sensor.apple_tree_spray            # sensor.{plant}_spray

# Calendars
calendar.apple_tree_care_calendar  # calendar.{plant}_care_calendar

# Device Grouping
device: orchard_care.apple         # All entities for one plant
```

## 📱 **Card Configuration Schema**

```yaml
# Minimal config
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning

# Full config
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning
spray_entity: sensor.apple_tree_spray
hemisphere: Northern
organic_preference: true
title: "My Apple Tree"
show_products: true
compact_mode: false
```

## 🔧 **Component Dependencies**

```python
# Python dependencies (none required)
requirements: []

# Home Assistant dependencies
dependencies: []

# Minimum HA version
homeassistant: "2023.1.0"

# Platforms used
platforms: ["sensor", "calendar"]
```

This structure provides a complete, professional HACS integration that follows Home Assistant best practices and includes all necessary files for distribution, development, and maintenance! 🚀