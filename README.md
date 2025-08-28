# 🍎 Orchard Care - Home Assistant Integration

A comprehensive Home Assistant integration for managing fruit tree and berry care schedules. Get timely reminders for pruning and spraying based on your hemisphere and organic preferences.

## ✨ Features

- **🌍 Hemisphere Support**: Automatic seasonal adjustment for Northern/Southern hemispheres
- **🌱 Organic Options**: Choose between organic and conventional treatment recommendations
- **📅 Smart Scheduling**: Intelligent pruning and spray timing based on plant types
- **🎨 Beautiful Dashboard**: Modern, responsive card with status indicators
- **📊 Calendar Integration**: Care events appear in your Home Assistant calendar
- **🤖 Automation Ready**: Sensor entities trigger notifications and automations
- **🌿 Extensive Plant Database**: 14+ pre-configured fruit trees and berries
- **➕ Custom Plants**: Add your own plants to the care schedule
- **🎛️ Plant Selection**: Choose which plants to display in dashboard cards

## 🚀 Installation

### HACS (Recommended)
1. Open HACS in Home Assistant
2. Go to "Integrations"
3. Click the "+" button
4. Search for "Orchard Care"
5. Download and restart Home Assistant

### Manual Installation
1. Copy the `orchard_care` folder to `custom_components/`
2. Copy `orchard-care-card.js` to `www/`
3. Restart Home Assistant
4. Add the card resource in Lovelace

## ⚙️ Configuration

### Integration Setup
1. Go to **Settings** → **Devices & Services**
2. Click **"Add Integration"**
3. Search for **"Orchard Care"**
4. Configure your preferences

### Dashboard Card
```yaml
# Single plant card
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning
hemisphere: Northern
organic_preference: true

# Multiple plants with selector tabs
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning
plants:
  - sensor.pear_tree_pruning
  - sensor.cherry_tree_pruning
hemisphere: Northern
organic_preference: true
show_plant_selector: true
```

## 🌱 Supported Plants

| Plant | Pruning Season | Spray Seasons | Special Notes |
|-------|----------------|---------------|---------------|
| **Apple** | Winter (Dec-Feb) | Spring & Fall | Dormant season pruning |
| **Pear** | Winter (Dec-Feb) | Spring & Fall | Watch for fire blight |
| **Cherry** | Summer (Jun-Aug) | Spring only | Prevent silver leaf |
| **Plum** | Summer (Jun-Aug) | Spring only | Summer pruning preferred |
| **Peach** | Winter (Dec-Feb) | Spring/Summer | Heavy pruning needed |
| **Citrus** | Late Winter (Mar-May) | Multiple seasons | Light pruning only |
| **Grape** | Winter (Dec-Feb) | Growing season | Heavy winter pruning |
| **Blueberry** | Winter (Dec-Feb) | Spring | Light pruning of old wood |
| **Raspberry** | Late Fall/Winter | Spring | Remove old canes |
| **Blackberry** | Late Fall/Winter | Spring | Train new growth |
| **Strawberry** | Late Fall/Winter | Spring & Fall | Remove runners |
| **Fig** | Winter/Early Spring | Spring & Late Summer | Minimal pruning needed |
| **Avocado** | Late Winter/Early Spring | Multiple seasons | Light pruning only |

## 📄 License

This project is licensed under the MIT License.

---

**Happy Gardening!** 🌳🍎🌿
