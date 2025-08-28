# 🍎 Orchard Care - Home Assistant Integration

A comprehensive Home Assistant integration for managing fruit tree and berry care schedules. Get timely reminders for pruning and spraying based on your hemisphere and organic preferences.

## ✨ Features

- **🌍 Hemisphere Support**: Automatic seasonal adjustment for Northern/Southern hemispheres
- **🌱 Organic Options**: Choose between organic and conventional treatment recommendations
- **📅 Smart Scheduling**: Intelligent pruning and spray timing based on plant types
- **🎨 Beautiful Dashboard**: Modern, responsive card with status indicators
- **📊 Calendar Integration**: Care events appear in your Home Assistant calendar
- **🤖 Automation Ready**: Sensor entities trigger notifications and automations
- **🌿 Extensive Plant Database**: 12+ pre-configured fruit trees and berries
- **➕ Custom Plants**: Add your own plants to the care schedule

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
4. Configure your preferences:
   - **Hemisphere**: Northern or Southern
   - **Organic Preference**: Organic vs conventional treatments
   - **Plant Selection**: Choose from 12+ available plants
   - **Custom Plants**: Add your own varieties

### Dashboard Card
Add this to your Lovelace dashboard:

```yaml
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning
spray_entity: sensor.apple_tree_spray
hemisphere: Northern
organic_preference: true
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

## 🎯 Entity Types

### Sensors
- `sensor.{plant}_pruning` - Next pruning date and timing
- `sensor.{plant}_spray` - Next spray date and products

### Attributes
- **Pruning months**: Optimal pruning schedule
- **Spray months**: Treatment timing
- **Product recommendations**: Organic/conventional options
- **Care notes**: Plant-specific guidance
- **Next dates**: Calculated upcoming care dates

### Calendar
- `calendar.{plant}_care_calendar` - All care events
- Pruning and spray events with descriptions
- Product recommendations in event details

## 🤖 Automation Examples

### Pruning Reminder
```yaml
automation:
  - alias: "Pruning Reminder"
    trigger:
      - platform: state
        entity_id: sensor.apple_tree_pruning
        to: "Now"
    action:
      - service: notify.mobile_app
        data:
          title: "🌳 Orchard Care"
          message: "Time to prune your {{ trigger.to_state.attributes.plant_type }}!"
```

### Spray Alert
```yaml
automation:
  - alias: "Spray Weather Check"
    trigger:
      - platform: state
        entity_id: sensor.apple_tree_spray
        to: "Now"
    condition:
      - condition: numeric_state
        entity_id: weather.forecast
        attribute: wind_speed
        below: 15
    action:
      - service: notify.family
        data:
          title: "🌿 Spray Day"
          message: "Perfect weather for spraying! Products: {{ trigger.to_state.attributes.spray_products | join(', ') }}"
```

## 🌍 Hemisphere Support

The integration automatically adjusts care schedules based on your hemisphere setting:

- **Northern Hemisphere**: Standard seasonal calendar
- **Southern Hemisphere**: 6-month offset for opposite seasons

## 🌱 Organic vs Conventional

Choose your treatment preference for tailored product recommendations:

### Organic Options
- Neem oil, Copper fungicide, Horticultural oil
- Bacillus thuringiensis, Spinosad, Kaolin clay
- Sulfur sprays, Insecticidal soap

### Conventional Options
- Captan, Imidacloprid, Malathion
- Propiconazole, Carbaryl, Mancozeb
- Systemic fungicides and insecticides

## 📱 Card Features

- **🎨 Modern Design**: Glassmorphism styling with smooth animations
- **📊 Status Indicators**: Visual urgency levels (Good/Warning/Urgent)
- **📅 Smart Timing**: "Now", "In X days", or month/year display
- **💊 Product Tags**: Recommended treatment products
- **🏠 Responsive**: Works on desktop, tablet, and mobile
- **🎯 Interactive**: Click elements to cycle through options (demo mode)

## 🛠️ Development

### File Structure
```
custom_components/orchard_care/
├── __init__.py          # Main integration setup
├── config_flow.py       # Configuration interface
├── const.py            # Constants and plant data
├── sensor.py           # Sensor entities
├── calendar.py         # Calendar integration
├── manifest.json       # Integration metadata
├── strings.json        # UI strings
└── translations/
    └── en.json         # English translations

www/
└── orchard-care-card.js # Lovelace dashboard card
```

### Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 🐛 Troubleshooting

### Integration Not Loading
- Check `custom_components/orchard_care/` exists
- Verify all Python files are present
- Restart Home Assistant completely

### Card Not Displaying
- Ensure `www/orchard-care-card.js` exists
- Add resource in Lovelace Resources
- Clear browser cache and refresh

### Wrong Seasons
- Verify hemisphere setting in integration options
- Check that plant entities have updated attributes
- Force refresh by reloading integration

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Credits

- Plant care data sourced from agricultural extension services
- Modern UI design inspired by contemporary dashboard trends
- Built with Home Assistant's excellent integration framework

## 📞 Support

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/example/orchard-care/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/example/orchard-care/discussions)
- 📚 **Documentation**: [Wiki Pages](https://github.com/example/orchard-care/wiki)
- 💬 **Community**: [Home Assistant Community](https://community.home-assistant.io/)

---

**Happy Gardening!** 🌳🍎🌿