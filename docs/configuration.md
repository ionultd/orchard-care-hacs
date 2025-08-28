# Configuration Guide

## Integration Configuration

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search "Orchard Care"
4. Configure options:
   - Hemisphere (Northern/Southern)
   - Organic preference
   - Select plants

## Card Configuration

```yaml
type: custom:orchard-care-card
entity: sensor.apple_tree_pruning
plants:
  - sensor.pear_tree_pruning
  - sensor.cherry_tree_pruning
show_plant_selector: true
```