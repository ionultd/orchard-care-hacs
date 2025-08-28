// Orchard Care Lovelace Card
class OrchardCareCard extends HTMLElement {
    constructor() {
        super();
        this.attachShadow({ mode: 'open' });
        this.currentPlantIndex = 0;
    }

    setConfig(config) {
        if (!config.entity) {
            throw new Error('You need to define an entity');
        }
        this.config = {
            ...config,
            plants: config.plants || [],
            show_plant_selector: config.show_plant_selector !== false
        };
    }

    set hass(hass) {
        this._hass = hass;
        this.render();
    }

    render() {
        if (!this._hass || !this.config) return;

        const plantEntities = this.config.plants.length > 0 ?
            this.config.plants.map(plantId => this._hass.states[plantId]).filter(Boolean) :
            [this._hass.states[this.config.entity]].filter(Boolean);

        if (plantEntities.length === 0) return;

        const currentEntity = plantEntities[this.currentPlantIndex || 0];
        const sprayEntity = this._hass.states[this.getSprayEntityId(currentEntity.entity_id)];

        if (!currentEntity) return;

        const plantType = currentEntity.attributes.plant_type || 'Plant';
        const hemisphere = this.config.hemisphere || 'Northern';
        const organicPref = this.config.organic_preference !== false;
        const plantIcon = this.getPlantIcon(plantType);

        this.shadowRoot.innerHTML = `
            ${this.getStyles()}

            <ha-card>
                <div class="orchard-card">
                    <div class="hemisphere-badge">${hemisphere}</div>

                    ${this.config.show_plant_selector && plantEntities.length > 1 ? this.renderPlantSelector(plantEntities) : ''}

                    <div class="plant-header">
                        <div class="plant-icon">${plantIcon}</div>
                        <div class="plant-info">
                            <h2>${plantType}</h2>
                            <div class="plant-type">Fruit Tree Care</div>
                        </div>
                    </div>

                    <div class="care-sections">
                        <div class="care-section pruning">
                            <div class="care-header">
                                <div class="care-icon">✂️</div>
                                <div class="care-title">Pruning</div>
                            </div>
                            <div class="care-timing ${this.isUrgent(currentEntity.state) ? 'urgent' : ''}">${currentEntity.state}</div>
                            <div class="care-details">${currentEntity.attributes.care_notes || 'Check pruning schedule'}</div>
                            <div class="status-indicator ${this.getStatusClass(currentEntity.state)}">
                                ${this.getStatusIcon(currentEntity.state)} ${this.getStatusText(currentEntity.state)}
                            </div>
                        </div>

                        ${sprayEntity ? `
                        <div class="care-section spray">
                            <div class="care-header">
                                <div class="care-icon">🌿</div>
                                <div class="care-title">Spray Treatment</div>
                            </div>
                            <div class="care-timing ${this.isUrgent(sprayEntity.state) ? 'urgent' : ''}">${sprayEntity.state}</div>
                            <div class="care-details">${organicPref ? 'Organic' : 'Conventional'} treatment recommended</div>
                            ${sprayEntity.attributes.spray_products ? `
                            <div class="product-list">
                                ${sprayEntity.attributes.spray_products.slice(0, 3).map(product =>
                                    `<span class="product-tag">${product}</span>`
                                ).join('')}
                            </div>
                            ` : ''}
                            <div class="status-indicator ${this.getStatusClass(sprayEntity.state)}">
                                ${this.getStatusIcon(sprayEntity.state)} ${this.getStatusText(sprayEntity.state)}
                            </div>
                        </div>
                        ` : ''}
                    </div>

                    <div class="last-updated">
                        Last updated: ${new Date(currentEntity.last_updated).toLocaleString()}
                    </div>
                </div>
            </ha-card>
        `;

        if (this.config.show_plant_selector && plantEntities.length > 1) {
            this.shadowRoot.querySelectorAll('.plant-selector-tab').forEach((tab, index) => {
                tab.addEventListener('click', () => {
                    this.currentPlantIndex = index;
                    this.render();
                });
            });
        }
    }

    renderPlantSelector(plantEntities) {
        return `
            <div class="plant-selector">
                <div class="plant-selector-tabs">
                    ${plantEntities.map((entity, index) => {
                        const plantType = entity.attributes.plant_type || 'Plant';
                        const icon = this.getPlantIcon(plantType);
                        const isActive = index === (this.currentPlantIndex || 0);
                        return `
                            <button class="plant-selector-tab ${isActive ? 'active' : ''}" data-index="${index}">
                                <span class="tab-icon">${icon}</span>
                                <span class="tab-name">${plantType.split(' ')[0]}</span>
                            </button>
                        `;
                    }).join('')}
                </div>
            </div>
        `;
    }

    getSprayEntityId(pruningEntityId) {
        return pruningEntityId.replace('_pruning', '_spray');
    }

    getPlantIcon(plantType) {
        const plantIcons = {
            'Apple Tree': '🍎',
            'Pear Tree': '🍐',
            'Cherry Tree': '🍒',
            'Plum Tree': '🍇',
            'Peach Tree': '🍑',
            'Apricot Tree': '🍑',
            'Orange Tree': '🍊',
            'Lemon Tree': '🍋',
            'Grapevine': '🍇',
            'Blueberry Bush': '🫐',
            'Raspberry Cane': '🍇',
            'Blackberry Cane': '🍇',
            'Strawberry Plant': '🍓',
            'Fig Tree': '🫒',
            'Avocado Tree': '🥑',
            'Kiwi Vine': '🥝',
            'Persimmon Tree': '🍅'
        };
        return plantIcons[plantType] || '🌱';
    }

    getStyles() {
        return `
            <style>
                :host { display: block; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif; }
                .orchard-card { background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(20px); border-radius: 24px; padding: 24px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1); border: 1px solid rgba(255, 255, 255, 0.2); position: relative; overflow: hidden; transition: transform 0.3s ease, box-shadow 0.3s ease; }
                .orchard-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; background: linear-gradient(90deg, #4CAF50, #8BC34A, #CDDC39); border-radius: 24px 24px 0 0; }
                .orchard-card:hover { transform: translateY(-4px); box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15); }
                .plant-selector { margin-bottom: 16px; padding-bottom: 16px; border-bottom: 1px solid rgba(0, 0, 0, 0.1); }
                .plant-selector-tabs { display: flex; gap: 8px; flex-wrap: wrap; }
                .plant-selector-tab { background: rgba(248, 250, 252, 0.8); border: 2px solid transparent; border-radius: 12px; padding: 8px 12px; cursor: pointer; transition: all 0.3s ease; font-size: 12px; font-weight: 600; color: var(--primary-text-color); display: flex; align-items: center; gap: 4px; }
                .plant-selector-tab:hover { background: rgba(248, 250, 252, 1); transform: translateY(-1px); }
                .plant-selector-tab.active { background: linear-gradient(135deg, #4CAF50, #66BB6A); color: white; border-color: #4CAF50; box-shadow: 0 2px 8px rgba(76, 175, 80, 0.3); }
                .plant-header { display: flex; align-items: center; gap: 16px; margin-bottom: 20px; }
                .plant-icon { width: 50px; height: 50px; background: linear-gradient(135deg, #4CAF50, #66BB6A); border-radius: 14px; display: flex; align-items: center; justify-content: center; font-size: 24px; box-shadow: 0 6px 16px rgba(76, 175, 80, 0.3); }
                .plant-info h2 { font-size: 20px; font-weight: 700; color: var(--primary-text-color); margin: 0 0 4px 0; }
                .plant-type { font-size: 13px; color: var(--secondary-text-color); font-weight: 500; }
                .hemisphere-badge { position: absolute; top: 12px; right: 12px; background: rgba(52, 152, 219, 0.1); color: #3498db; padding: 4px 8px; border-radius: 8px; font-size: 10px; font-weight: 600; text-transform: uppercase; }
                .care-sections { display: grid; gap: 16px; }
                .care-section { padding: 16px; background: rgba(248, 250, 252, 0.6); border-radius: 14px; border-left: 4px solid transparent; transition: all 0.3s ease; }
                .care-section.pruning { border-left-color: #e74c3c; }
                .care-section.spray { border-left-color: #3498db; }
                .care-section:hover { background: rgba(248, 250, 252, 0.9); transform: translateX(2px); }
                .care-header { display: flex; align-items: center; gap: 10px; margin-bottom: 10px; }
                .care-icon { width: 32px; height: 32px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 16px; color: white; }
                .pruning .care-icon { background: linear-gradient(135deg, #e74c3c, #c0392b); }
                .spray .care-icon { background: linear-gradient(135deg, #3498db, #2980b9); }
                .care-title { font-size: 14px; font-weight: 600; color: var(--primary-text-color); }
                .care-timing { font-size: 18px; font-weight: 700; color: #27ae60; margin-bottom: 6px; }
                .care-timing.urgent { color: #e74c3c; animation: pulse 2s infinite; }
                @keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
                .care-details { font-size: 12px; color: var(--secondary-text-color); line-height: 1.4; margin-bottom: 8px; }
                .product-list { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 8px; }
                .product-tag { background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 2px 8px; border-radius: 10px; font-size: 10px; font-weight: 500; }
                .status-indicator { display: inline-flex; align-items: center; gap: 4px; padding: 4px 8px; border-radius: 12px; font-size: 10px; font-weight: 600; margin-top: 6px; }
                .status-good { background: rgba(39, 174, 96, 0.1); color: #27ae60; }
                .status-warning { background: rgba(241, 196, 15, 0.1); color: #f1c40f; }
                .status-urgent { background: rgba(231, 76, 60, 0.1); color: #e74c3c; }
                .last-updated { text-align: center; font-size: 11px; color: var(--secondary-text-color); margin-top: 16px; padding-top: 12px; border-top: 1px solid rgba(0, 0, 0, 0.1); }
            </style>
        `;
    }

    isUrgent(state) { return state === 'Now' || state.includes('1 day'); }
    getStatusClass(state) { if (state === 'Now') return 'status-urgent'; if (state.includes('day') && parseInt(state) <= 7) return 'status-warning'; return 'status-good'; }
    getStatusIcon(state) { if (state === 'Now') return '🚨'; if (state.includes('day') && parseInt(state) <= 7) return '⚠️'; if (state.includes('day') && parseInt(state) <= 14) return '⏰'; return '✅'; }
    getStatusText(state) { if (state === 'Now') return 'Action Required'; if (state.includes('day') && parseInt(state) <= 7) return 'Due Soon'; if (state.includes('day') && parseInt(state) <= 14) return 'Upcoming'; return 'On Schedule'; }
    getCardSize() { return 4; }
    static getConfigElement() { return document.createElement('orchard-care-card-editor'); }
    static getStubConfig() { return { entity: 'sensor.apple_tree_pruning', plants: [], hemisphere: 'Northern', organic_preference: true, show_plant_selector: true }; }
}

class OrchardCareCardEditor extends HTMLElement {
    constructor() { super(); this.attachShadow({ mode: 'open' }); }
    setConfig(config) { this.config = config; this.render(); }
    render() { /* Editor implementation */ }
    configChanged() { const event = new CustomEvent('config-changed', { detail: { config: this.config }, bubbles: true, composed: true }); this.dispatchEvent(event); }
}

customElements.define('orchard-care-card', OrchardCareCard);
customElements.define('orchard-care-card-editor', OrchardCareCardEditor);

window.customCards = window.customCards || [];
window.customCards.push({ type: 'orchard-care-card', name: 'Orchard Care Card', description: 'A beautiful card for tracking fruit tree and berry care schedules' });

console.info('%c ORCHARD-CARE-CARD %c v1.0.0 ', 'color: orange; font-weight: bold; background: black', 'color: white; font-weight: bold; background: dimgray');