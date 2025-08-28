# Installation Guide Simple

## HACS Installation (Recommended)

1. Open HACS in Home Assistant
2. Click "Integrations"
3. Click the "+" button
4. Search for "Orchard Care"
5. Click "Download"
6. Restart Home Assistant

## Manual Installation

1. Download the latest release
2. Extract to `custom_components/orchard_care/`
3. Copy `orchard-care-card.js` to `www/`
4. Restart Home Assistant
5. Add integration via Settings

# 🏠 Complete Home Assistant Installation Guide

## 📋 **Prerequisites**

Before installing, make sure you have:
- ✅ Home Assistant Core 2023.1.0 or later
- ✅ Access to your Home Assistant file system
- ✅ Basic text editor (like VSCode, Notepad++, or nano)
- ✅ Weather integration configured (for enhanced features)

---

## 🚀 **Method 1: Manual Installation (Recommended for Custom Setup)**

### **Step 1: Download the Files**
You have two options to get the files:

#### **Option A: Create Files Manually**
1. Create the directory structure in your Home Assistant config folder
2. Copy each file content from the artifacts provided earlier

#### **Option B: Download from Repository**
```bash
# If you have git access to your HA system
git clone https://github.com/your-username/orchard-care-hacs.git
```

### **Step 2: Create Directory Structure**
Navigate to your Home Assistant configuration directory and create:

```bash
# SSH into Home Assistant or use File Editor add-on
cd /config

# Create the integration directory
mkdir -p custom_components/orchard_care
mkdir -p custom_components/orchard_care/translations
mkdir -p www
```

### **Step 3: Copy Integration Files**
Create these files in `custom_components/orchard_care/`:

#### **File 1: `__init__.py`**
```bash
# Create the file
nano custom_components/orchard_care/__init__.py
```
Copy the content from the "Updated __init__.py" artifact

#### **File 2: `const.py`**
```bash
nano custom_components/orchard_care/const.py
```
Copy the content from the "Updated const.py" artifact

#### **File 3: `config_flow.py`**
```bash
nano custom_components/orchard_care/config_flow.py
```
Copy the content from the main project files artifact

#### **File 4: `sensor.py`**
```bash
nano custom_components/orchard_care/sensor.py
```
Copy the content from the main project files artifact

#### **File 5: `calendar.py`**
```bash
nano custom_components/orchard_care/calendar.py
```
Copy the content from the "Enhanced Calendar Implementation" artifact

#### **File 6: `manifest.json`**
```bash
nano custom_components/orchard_care/manifest.json
```
```json
{
    "domain": "orchard_care",
    "name": "Orchard Care",
    "codeowners": [],
    "config_flow": true,
    "dependencies": [],
    "documentation": "https://github.com/example/orchard-care",
    "iot_class": "calculated",
    "issue_tracker": "https://github.com/example/orchard-care/issues",
    "requirements": [],
    "version": "1.0.0",
    "integration_type": "service"
}
```

#### **File 7: `strings.json`**
```bash
nano custom_components/orchard_care/strings.json
```
```json
{
    "config": {
        "step": {
            "user": {
                "title": "Orchard Care Setup",
                "description": "Configure your orchard care preferences",
                "data": {
                    "hemisphere": "Seasonal Hemisphere",
                    "organic_preference": "Prefer Organic Products",
                    "selected_plants": "Select Your Plants",
                    "custom_plants": "Custom Plants (comma-separated)"
                }
            }
        }
    },
    "options": {
        "step": {
            "init": {
                "title": "Orchard Care Options",
                "description": "Update your orchard care settings",
                "data": {
                    "hemisphere": "Seasonal Hemisphere",
                    "organic_preference": "Prefer Organic Products",
                    "selected_plants": "Select Your Plants",
                    "custom_plants": "Custom Plants (comma-separated)"
                }
            }
        }
    }
}
```

#### **File 8: `translations/en.json`**
```bash
nano custom_components/orchard_care/translations/en.json
```
Copy the content from the main project files artifact

### **Step 4: Copy Dashboard Card**
```bash
# Copy the Lovelace card to www directory
nano www/orchard-care-card.js
```
Copy the content from the "Updated orchard-care-card.js" artifact

### **Step 5: Restart Home Assistant**
```bash
# Restart Home Assistant to load the new integration
# Via UI: Settings > System > Restart
# Via CLI: ha core restart
```

---

## 🔧 **Method 2: HACS Installation (Future)**

*Note: This integration is not yet published to HACS default repositories*

### **Add as Custom Repository:**
1. Go to **HACS** > **Integrations**
2. Click the **three dots menu** > **Custom repositories**
3. Add repository URL: `https://github.com/your-username/orchard-care-hacs`
4. Category: **Integration**
5. Click **Add**
6. Find **Orchard Care** and click **Download**

---

## ⚙️ **Step 6: Configure the Integration**

### **Add the Integration:**
1. Go to **Settings** > **Devices & Services**
2. Click **+ Add Integration**
3. Search for **"Orchard Care"**
4. Click **Orchard Care** from the list

### **Configure Your Orchard:**
1. **Hemisphere**: Select Northern or Southern
2. **Organic Preference**: Choose organic or conventional treatments
3. **Select Plants**: Choose from 17+ available plants:
   - Apple Tree
   - Pear Tree
   - Cherry Tree
   - Plum Tree
   - Peach Tree
   - Apricot Tree
   - Orange Tree
   - Lemon Tree
   - Grapevine
   - Blueberry Bush
   - Raspberry Cane
   - Blackberry Cane
   - Strawberry Plant
   - Fig Tree
   - Avocado Tree
   - Kiwi Vine
   - Persimmon Tree
4. **Custom Plants**: Add any additional plants (comma-separated)

### **Click Submit** to complete setup

---

## 📱 **Step 7: Add Dashboard Card**

### **Add Card Resource:**
1. Go to **Settings** > **Dashboards** > **Resources**
2. Click **+ Add Resource**
3. URL: `/local/orchard-care-card.js`
4. Resource Type: **JavaScript Module**
5. Click **Create**

### **Add Card to Dashboard:**
1. Go to your **Dashboard**
2. Click **Edit Dashboard**
3. Click **+ Add Card**
4. Search for **"Orchard Care Card"**
5. Configure the card:

```yaml
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning
plants:
  - sensor.pear_tree_pruning
  - sensor.cherry_tree_pruning
hemisphere: Northern
organic_preference: true
show_plant_selector: true
```

---

## 🔔 **Step 8: Set Up Notifications (Optional)**

### **For Mobile App Notifications:**
1. Install **Home Assistant Companion App** on your phone
2. Configure mobile notifications in HA
3. The integration will automatically send care reminders

### **For Advanced Automations:**
Add the automation examples to your `configuration.yaml`:

```yaml
# Add to configuration.yaml
automation: !include automations.yaml

# Create automations.yaml with content from "Enhanced Automation Examples" artifact
```

---

## ✅ **Step 9: Verify Installation**

### **Check Integration Status:**
1. Go to **Settings** > **Devices & Services**
2. Look for **Orchard Care** integration
3. Should show "X devices, Y entities"

### **Check Entities Created:**
1. Go to **Settings** > **Devices & Services** > **Entities**
2. Filter by **orchard_care**
3. Should see entities like:
   - `sensor.apple_tree_pruning`
   - `sensor.apple_tree_spray`
   - `calendar.apple_tree_care_calendar`

### **Check Calendar:**
1. Go to **Calendar** tab in Home Assistant
2. Look for your plant care calendars
3. Events should appear for current season

### **Test Dashboard Card:**
1. View your dashboard
2. Orchard Care card should display
3. Try switching between plants (if multiple configured)

---

## 🐛 **Troubleshooting**

### **Integration Not Showing:**
- Check file permissions (should be readable)
- Verify all files are in correct locations
- Check Home Assistant logs for Python errors
- Ensure manifest.json is valid JSON

### **Entities Not Created:**
- Check that you selected plants during configuration
- Verify hemisphere setting is correct
- Check coordinator is running (look for errors in logs)

### **Card Not Loading:**
- Verify resource was added correctly
- Clear browser cache
- Check browser console for JavaScript errors
- Ensure card file is in `/config/www/` directory

### **Calendar Not Working:**
- Check calendar platform is enabled
- Verify entities are created in developer tools
- Look for calendar-specific errors in logs

### **Check Logs:**
```bash
# View Home Assistant logs
ha core logs

# Or via UI: Settings > System > Logs
```

---

## 📊 **What You'll Get After Installation**

### **Entities Created:**
- **2 sensors per plant**: Pruning and spray sensors
- **1 calendar per plant**: Individual plant care calendars
- **1 master calendar**: Combined view of all plants

### **Example Entities (for Apple Tree):**
- `sensor.apple_tree_pruning`
- `sensor.apple_tree_spray`
- `calendar.apple_tree_care_calendar`

### **Dashboard Features:**
- Beautiful modern card with plant icons
- Status indicators (Good/Warning/Urgent)
- Plant selector tabs (if multiple plants)
- Organic/conventional product recommendations
- Real-time timing updates

### **Calendar Features:**
- Automatic pruning and spray events
- Detailed care instructions
- Weather-aware notifications
- Seasonal adjustments for hemisphere
- Advance reminders (7 days, 3 days, day-of)

### **Automation Ready:**
- Sensor states trigger automations
- Calendar events trigger notifications
- Weather-aware spray reminders
- Morning briefings and weekly summaries

---

## 🎯 **Next Steps After Installation**

1. **Configure Automations**: Add the example automations for enhanced features
2. **Set Up Weather**: Ensure you have weather integration for spray alerts
3. **Customize Cards**: Adjust card settings for your preferences
4. **Test Notifications**: Verify mobile app notifications work
5. **Plan Your Season**: Review the generated calendar events
6. **Add More Plants**: Use the options flow to add/remove plants

Your orchard care system is now fully automated and ready to help you maintain healthy, productive fruit trees! 🌳✨