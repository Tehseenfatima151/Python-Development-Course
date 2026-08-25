/**
 * PropVal.AI - Frontend Interactions & Dynamic Unit Conversion
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const toggleMarlaBtn = document.getElementById('toggle-marla');
    const toggleSqftBtn = document.getElementById('toggle-sqft');
    const unitSelectContainer = document.getElementById('unit-select-container');
    const areaValInput = document.getElementById('area-val-input');
    const areaUnitSelect = document.getElementById('area-unit-select');
    const convertedSqftLabel = document.getElementById('converted-sqft-label');
    const hiddenSqftInput = document.getElementById('sqft');
    const quickPresetButtons = document.querySelectorAll('.quick-preset-btn');
    
    const predictionForm = document.getElementById('price-prediction-form');
    const submitBtn = document.getElementById('submit-btn');
    const btnText = document.getElementById('btn-text');
    const btnLoader = document.getElementById('btn-loader');
    const instantAjaxBtn = document.getElementById('instant-ajax-btn');
    const liveResultBox = document.getElementById('live-result-box');
    const ajaxPricePkr = document.getElementById('ajax-price-pkr');
    const ajaxPriceCrore = document.getElementById('ajax-price-crore');
    const ajaxSqftRate = document.getElementById('ajax-sqft-rate');

    // Constants (Pakistani Real Estate Standard Conversions)
    // 1 Marla = 225 sqft (Development/LDA standard) or 272.25 sqft (Punjab standard)
    // Here we use 225 sqft / Marla and 4500 sqft / Kanal (20 Marla) matching reference image (5 Marla = 1,125 sqft)
    const SQFT_PER_MARLA = 225;
    const SQFT_PER_KANAL = 4500;

    let currentMode = 'marla'; // 'marla' or 'sqft'

    // Synchronize and update converted labels & hidden sqft input
    function updateCalculations() {
        if (!areaValInput || !hiddenSqftInput) return;

        const rawVal = parseFloat(areaValInput.value);
        if (isNaN(rawVal) || rawVal <= 0) {
            hiddenSqftInput.value = 1125;
            if (convertedSqftLabel) convertedSqftLabel.textContent = '~ 1,125 sqft';
            return;
        }

        let calculatedSqft = 1125;

        if (currentMode === 'marla') {
            const unit = areaUnitSelect ? areaUnitSelect.value : 'marla';
            if (unit === 'kanal') {
                calculatedSqft = Math.round(rawVal * SQFT_PER_KANAL);
                if (convertedSqftLabel) {
                    convertedSqftLabel.textContent = `~ ${calculatedSqft.toLocaleString()} sqft`;
                }
            } else {
                calculatedSqft = Math.round(rawVal * SQFT_PER_MARLA);
                if (convertedSqftLabel) {
                    convertedSqftLabel.textContent = `~ ${calculatedSqft.toLocaleString()} sqft`;
                }
            }
        } else {
            // Square Feet mode
            calculatedSqft = Math.round(rawVal);
            if (convertedSqftLabel) {
                if (calculatedSqft >= SQFT_PER_KANAL) {
                    const kanal = (calculatedSqft / SQFT_PER_KANAL).toFixed(1);
                    convertedSqftLabel.textContent = `~ ${kanal} Kanal`;
                } else {
                    const marla = (calculatedSqft / SQFT_PER_MARLA).toFixed(1);
                    convertedSqftLabel.textContent = `~ ${marla} Marla`;
                }
            }
        }

        hiddenSqftInput.value = calculatedSqft;
        checkPresetMatch(calculatedSqft);
    }

    // Check if current sqft matches any preset button
    function checkPresetMatch(currentSqft) {
        quickPresetButtons.forEach(btn => {
            const presetSqft = parseInt(btn.getAttribute('data-sqft'));
            if (presetSqft === currentSqft) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }

    // Mode Toggle Handlers
    if (toggleMarlaBtn && toggleSqftBtn) {
        toggleMarlaBtn.addEventListener('click', () => {
            if (currentMode === 'marla') return;
            currentMode = 'marla';
            toggleMarlaBtn.classList.add('active');
            toggleSqftBtn.classList.remove('active');

            if (unitSelectContainer) unitSelectContainer.classList.remove('hidden');

            // Convert current sqft back to marla value
            const currentSqft = parseFloat(hiddenSqftInput.value) || 1125;
            if (currentSqft >= SQFT_PER_KANAL) {
                if (areaUnitSelect) areaUnitSelect.value = 'kanal';
                areaValInput.value = (currentSqft / SQFT_PER_KANAL).toFixed(1);
            } else {
                if (areaUnitSelect) areaUnitSelect.value = 'marla';
                areaValInput.value = (currentSqft / SQFT_PER_MARLA).toFixed(1);
            }
            updateCalculations();
        });

        toggleSqftBtn.addEventListener('click', () => {
            if (currentMode === 'sqft') return;
            currentMode = 'sqft';
            toggleSqftBtn.classList.add('active');
            toggleMarlaBtn.classList.remove('active');

            if (unitSelectContainer) unitSelectContainer.classList.add('hidden');

            const currentSqft = parseFloat(hiddenSqftInput.value) || 1125;
            areaValInput.value = currentSqft;
            updateCalculations();
        });
    }

    // Input listeners
    if (areaValInput) {
        areaValInput.addEventListener('input', updateCalculations);
    }

    if (areaUnitSelect) {
        areaUnitSelect.addEventListener('change', updateCalculations);
    }

    // Preset button click handlers
    quickPresetButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            quickPresetButtons.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const unit = btn.getAttribute('data-unit');
            const val = parseFloat(btn.getAttribute('data-val'));
            const sqft = parseInt(btn.getAttribute('data-sqft'));

            if (currentMode === 'marla') {
                if (areaUnitSelect) areaUnitSelect.value = unit;
                if (areaValInput) areaValInput.value = val;
            } else {
                if (areaValInput) areaValInput.value = sqft;
            }

            hiddenSqftInput.value = sqft;
            updateCalculations();
        });
    });

    // Form submission
    if (predictionForm && submitBtn) {
        predictionForm.addEventListener('submit', (e) => {
            const locationSelect = document.getElementById('location');
            if (locationSelect && !locationSelect.value) {
                e.preventDefault();
                alert('Please select a property location.');
                locationSelect.focus();
                return;
            }

            if (btnText && btnLoader) {
                btnText.textContent = 'CALCULATING AI VALUATION...';
                btnLoader.classList.remove('hidden');
                submitBtn.setAttribute('disabled', 'true');
                submitBtn.style.opacity = '0.8';
            }
        });
    }

    // Instant AJAX prediction button
    if (instantAjaxBtn && liveResultBox) {
        instantAjaxBtn.addEventListener('click', async () => {
            const locationSelect = document.getElementById('location');
            const bedroomsSelect = document.getElementById('bedrooms');
            const bathroomsSelect = document.getElementById('bathrooms');

            const sqft = parseFloat(hiddenSqftInput.value) || 1125;
            const bedrooms = parseInt(bedroomsSelect.value);
            const bathrooms = parseInt(bathroomsSelect.value);
            const location = locationSelect.value;

            if (!location) {
                alert('Please select a city location from the dropdown first.');
                locationSelect.focus();
                return;
            }

            instantAjaxBtn.innerHTML = '<div class="spinner"></div> Calculating...';
            instantAjaxBtn.setAttribute('disabled', 'true');

            try {
                const response = await fetch('/api/predict', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        sqft: sqft,
                        bedrooms: bedrooms,
                        bathrooms: bathrooms,
                        location: location
                    })
                });

                const data = await response.json();

                if (data.success) {
                    if (ajaxPricePkr) ajaxPricePkr.textContent = data.formatted_price;
                    if (ajaxPriceCrore) ajaxPriceCrore.textContent = `(${data.formatted_crore})`;
                    if (ajaxSqftRate) ajaxSqftRate.textContent = `Rate: PKR ${data.price_per_sqft.toLocaleString()} / sqft`;

                    liveResultBox.classList.remove('hidden');
                    liveResultBox.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                } else {
                    alert('Prediction Error: ' + (data.error || 'Failed to calculate valuation'));
                }
            } catch (err) {
                console.error('API Error:', err);
                alert('Failed to connect to ML prediction API.');
            } finally {
                instantAjaxBtn.innerHTML = 'Live AJAX';
                instantAjaxBtn.removeAttribute('disabled');
            }
        });
    }

    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileMenuToggle && mobileMenu) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }

    // Modal links
    const modalLinks = document.querySelectorAll('.open-modal-link');
    modalLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const modalId = link.getAttribute('data-modal');
            const targetModal = document.getElementById(modalId);
            if (targetModal) {
                targetModal.classList.remove('hidden');
            }
        });
    });

    // Close modal handlers
    const closeButtons = document.querySelectorAll('.close-modal-btn');
    closeButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.custom-modal-backdrop');
            if (modal) modal.classList.add('hidden');
        });
    });

    // Click backdrop to close modal
    const modalBackdrops = document.querySelectorAll('.custom-modal-backdrop');
    modalBackdrops.forEach(backdrop => {
        backdrop.addEventListener('click', (e) => {
            if (e.target === backdrop) {
                backdrop.classList.add('hidden');
            }
        });
    });

    // Initial calculation on load
    updateCalculations();
});
