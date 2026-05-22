(function() {
    'use strict';

    // Application state
    let map = null;
    let markers = [];
    let doctorsData = [];
    let activeMarker = null;
    let activeDoctorId = null;
    let googleMapsLoaded = false;
    let defaultCity = { lat: 37.7749, lng: -122.4194 }; // San Francisco center
    let currentSpecialty = '';
    let currentQuery = '';

    // DOM Elements
    const searchInput = document.getElementById('search-input');
    const btnClearSearch = document.getElementById('btn-clear-search');
    const specialtyPills = document.getElementById('specialty-pills');
    const doctorList = document.getElementById('doctor-list');
    const resultsCount = document.getElementById('results-count');
    const detailsDrawer = document.getElementById('details-drawer');
    const drawerContent = document.getElementById('drawer-content');
    const btnCloseDrawer = document.getElementById('btn-close-drawer');
    const btnRecenter = document.getElementById('btn-recenter-map');
    
    // Modal & API key elements
    const apiStatusBadge = document.getElementById('api-status-badge');
    const btnOpenSettings = document.getElementById('btn-open-settings');
    const settingsModal = document.getElementById('settings-modal');
    const btnCloseModal = document.getElementById('btn-close-modal');
    const inputApiKey = document.getElementById('input-api-key');
    const btnSaveApiKey = document.getElementById('btn-save-api-key');
    const btnClearApiKey = document.getElementById('btn-clear-api-key');
    const backendKeyStatus = document.getElementById('backend-key-status');
    const btnSetupMapCenter = document.getElementById('btn-setup-map-center');

    // Custom Map Dark Theme Styling
    const mapDarkStyle = [
        { elementType: "geometry", stylers: [{ color: "#1d2c4d" }] },
        { elementType: "labels.text.fill", stylers: [{ color: "#8ec3b9" }] },
        { elementType: "labels.text.stroke", stylers: [{ color: "#1a3646" }] },
        {
            featureType: "administrative.country",
            elementType: "geometry.stroke",
            stylers: [{ color: "#4b6878" }]
        },
        {
            featureType: "administrative.land_parcel",
            elementType: "labels.text.fill",
            stylers: [{ color: "#64779e" }]
        },
        {
            featureType: "administrative.province",
            elementType: "geometry.stroke",
            stylers: [{ color: "#4b6878" }]
        },
        {
            featureType: "landscape.man_made",
            elementType: "geometry.stroke",
            stylers: [{ color: "#334e87" }]
        },
        {
            featureType: "landscape.natural",
            elementType: "geometry",
            stylers: [{ color: "#023e8a" }, { opacity: 0.1 }]
        },
        {
            featureType: "poi",
            elementType: "geometry",
            stylers: [{ color: "#283d6a" }]
        },
        {
            featureType: "poi",
            elementType: "labels.text.fill",
            stylers: [{ color: "#6f9ba5" }]
        },
        {
            featureType: "poi.park",
            elementType: "geometry.fill",
            stylers: [{ color: "#023e8a" }, { opacity: 0.2 }]
        },
        {
            featureType: "poi.park",
            elementType: "labels.text.fill",
            stylers: [{ color: "#3C7680" }]
        },
        {
            featureType: "road",
            elementType: "geometry",
            stylers: [{ color: "#304a7d" }]
        },
        {
            featureType: "road",
            elementType: "labels.text.fill",
            stylers: [{ color: "#98a5be" }]
        },
        {
            featureType: "road.highway",
            elementType: "geometry",
            stylers: [{ color: "#2c598d" }]
        },
        {
            featureType: "road.highway",
            elementType: "geometry.stroke",
            stylers: [{ color: "#2de2e6" }, { weight: 0.5 }, { opacity: 0.2 }]
        },
        {
            featureType: "road.highway",
            elementType: "labels.text.fill",
            stylers: [{ color: "#e0f2f1" }]
        },
        {
            featureType: "transit",
            elementType: "geometry",
            stylers: [{ color: "#2f3948" }]
        },
        {
            featureType: "transit.station",
            elementType: "labels.text.fill",
            stylers: [{ color: "#d1a8e2" }]
        },
        {
            featureType: "water",
            elementType: "geometry",
            stylers: [{ color: "#0b132b" }]
        },
        {
            featureType: "water",
            elementType: "labels.text.fill",
            stylers: [{ color: "#4c6b8a" }]
        }
    ];

    // SVG Marker markup as data URI
    const getMarkerIcon = (isActive) => {
        const color = isActive ? '00B4D8' : '48CAE4';
        const strokeColor = isActive ? 'FFFFFF' : '0d1428';
        const size = isActive ? 40 : 32;
        
        return {
            url: `data:image/svg+xml;utf-8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="${size}" height="${size}"><path fill="%23${color}" stroke="%23${strokeColor}" stroke-width="2" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>`,
            scaledSize: new google.maps.Size(size, size),
            anchor: new google.maps.Point(size / 2, size)
        };
    };

    // Initialize application logic
    document.addEventListener('DOMContentLoaded', () => {
        initApiKeyConfig();
        setupEventListeners();
    });

    // 1. API Key Check and Map SDK Loading
    function initApiKeyConfig() {
        const backendKey = window.djangoConfig.backendApiKey;
        const localKey = localStorage.getItem('google_maps_api_key');
        
        // Key selection: Prefer backend configuration if available, otherwise local storage fallback
        const activeKey = backendKey || localKey;
        
        updateApiStatusBadge(backendKey, localKey, activeKey);
        
        if (activeKey) {
            loadGoogleMapsSDK(activeKey);
        } else {
            // No API Key, load default cards and show map placeholder
            fetchDoctors();
            showMapPlaceholder();
        }
    }

    function updateApiStatusBadge(backendKey, localKey, activeKey) {
        const pulse = apiStatusBadge.querySelector('.pulse-indicator');
        const text = apiStatusBadge.querySelector('.status-text');
        
        if (backendKey) {
            pulse.className = 'pulse-indicator active';
            text.textContent = 'API Connected (Server)';
            backendKeyStatus.className = 'backend-key-info';
            backendKeyStatus.innerHTML = '<strong>Server Configuration:</strong> An API key is configured on the server settings.';
        } else if (localKey) {
            pulse.className = 'pulse-indicator active';
            text.textContent = 'API Connected (Browser)';
            backendKeyStatus.className = 'backend-key-info';
            backendKeyStatus.innerHTML = '<strong>Browser Configuration:</strong> Using locally saved key.';
            inputApiKey.value = localKey;
        } else {
            pulse.className = 'pulse-indicator error';
            text.textContent = 'Google Maps Key Required';
            backendKeyStatus.className = 'backend-key-info empty';
            backendKeyStatus.innerHTML = '<strong>No API Key Configured:</strong> The map will not render properly without a Google Maps Javascript API Key.';
        }
    }

    function loadGoogleMapsSDK(key) {
        window.initMap = initMap; // Set global callback
        
        const script = document.createElement('script');
        script.src = `https://maps.googleapis.com/maps/api/js?key=${key}&callback=initMap`;
        script.async = true;
        script.defer = true;
        script.onerror = () => {
            console.error('Failed to load Google Maps SDK.');
            showMapPlaceholder('Failed to load Google Maps script. Check your API key or network connection.');
        };
        document.head.appendChild(script);
    }

    function showMapPlaceholder(errorMessage) {
        const mapContainer = document.getElementById('map');
        const message = errorMessage || 'Google Maps requires an API key to display the map. You can supply a key by setting the environment variable or pasting it below.';
        
        mapContainer.innerHTML = `
            <div class="map-placeholder">
                <div class="map-placeholder-card">
                    <h3>Map Configuration Needed</h3>
                    <p>${message}</p>
                    <button class="btn btn-primary" id="btn-placeholder-setup">Configure API Key</button>
                </div>
            </div>
        `;
        
        document.getElementById('btn-placeholder-setup')?.addEventListener('click', () => {
            settingsModal.classList.add('open');
        });
    }

    // 2. Google Maps Callback Initialization
    function initMap() {
        googleMapsLoaded = true;
        btnRecenter.style.display = 'flex';
        
        // Render custom styled map
        map = new google.maps.Map(document.getElementById('map'), {
            center: defaultCity,
            zoom: 13,
            styles: mapDarkStyle,
            disableDefaultUI: false,
            zoomControl: true,
            mapTypeControl: false,
            streetViewControl: false,
            fullscreenControl: true
        });

        // Close drawer on map click
        map.addListener('click', () => {
            closeDrawer();
            deactivateAllCards();
        });

        // Load doctors onto the map
        fetchDoctors();
    }

    // 3. API Doctors Fetching & Filtering
    function fetchDoctors() {
        const url = new URL(window.djangoConfig.apiDoctorsUrl, window.location.origin);
        if (currentSpecialty) {
            url.searchParams.append('specialty', currentSpecialty);
        }
        if (currentQuery) {
            url.searchParams.append('q', currentQuery);
        }

        doctorList.innerHTML = `
            <div class="list-placeholder">
                <div class="spinner"></div>
                <p>Querying medical network...</p>
            </div>
        `;

        fetch(url)
            .then(res => res.json())
            .then(data => {
                doctorsData = data;
                resultsCount.textContent = `${data.length} Doctor${data.length !== 1 ? 's' : ''} Found`;
                renderDoctorsList(data);
                if (googleMapsLoaded) {
                    renderMapMarkers(data);
                }
            })
            .catch(err => {
                console.error(err);
                resultsCount.textContent = 'Error loading doctors';
                doctorList.innerHTML = `
                    <div class="list-placeholder">
                        <p class="error-text" style="color: var(--danger);">Failed to load doctor listings.</p>
                        <button class="btn btn-secondary" onclick="window.location.reload()">Retry</button>
                    </div>
                `;
            });
    }

    // 4. Rendering Sidebar Doctor Cards
    function renderDoctorsList(doctors) {
        if (doctors.length === 0) {
            doctorList.innerHTML = `
                <div class="list-placeholder">
                    <p>No doctors match your query.</p>
                    <small>Try selecting a different specialty or clearing your search term.</small>
                </div>
            `;
            return;
        }

        doctorList.innerHTML = '';
        doctors.forEach(doc => {
            const card = document.createElement('div');
            card.className = `doctor-card ${activeDoctorId === doc.id ? 'active' : ''}`;
            card.dataset.id = doc.id;
            
            // Build rating stars
            let starsHtml = '';
            const fullStars = Math.floor(doc.rating);
            for (let i = 0; i < 5; i++) {
                if (i < fullStars) {
                    starsHtml += `<svg viewBox="0 0 24 24"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
                } else {
                    starsHtml += `<svg viewBox="0 0 24 24" style="fill: rgba(255,255,255,0.1);"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
                }
            }

            card.innerHTML = `
                <div class="card-header">
                    <div class="card-title">
                        <h3>Dr. ${doc.name}</h3>
                        <span class="specialty-tag">${doc.specialty}</span>
                    </div>
                    <div class="rating-badge">
                        <svg viewBox="0 0 24 24"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                        <span>${doc.rating.toFixed(1)}</span>
                    </div>
                </div>
                <div class="card-body">
                    <div class="clinic-info">${doc.clinic_name}</div>
                    <div class="address-info">
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                            <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
                            <circle cx="12" cy="10" r="3"/>
                        </svg>
                        <span>${doc.address}</span>
                    </div>
                </div>
            `;

            card.addEventListener('click', () => handleDoctorSelect(doc.id, true));
            doctorList.appendChild(card);
        });
    }

    // 5. Creating and Handling Map Markers
    function renderMapMarkers(doctors) {
        // Clear old markers
        markers.forEach(m => m.setMap(null));
        markers = [];

        const bounds = new google.maps.LatLngBounds();
        let validCoordsCount = 0;

        doctors.forEach(doc => {
            if (doc.latitude === null || doc.longitude === null) return;

            const latLng = { lat: doc.latitude, lng: doc.longitude };
            bounds.extend(latLng);
            validCoordsCount++;

            const marker = new google.maps.Marker({
                position: latLng,
                map: map,
                title: `Dr. ${doc.name}`,
                icon: getMarkerIcon(activeDoctorId === doc.id),
                animation: google.maps.Animation.DROP
            });

            // Keep reference of doctor ID on marker
            marker.doctorId = doc.id;

            marker.addListener('click', () => {
                handleDoctorSelect(doc.id, false); // select without panning (marker is already centered on screen click)
            });

            markers.push(marker);
        });

        // Fit map bounds to show all markers
        if (validCoordsCount > 0 && map) {
            if (validCoordsCount === 1) {
                map.setCenter(bounds.getCenter());
                map.setZoom(14);
            } else {
                map.fitBounds(bounds);
            }
        }
    }

    // 6. Doctor Selection Sync Logic (List & Map Markers)
    function handleDoctorSelect(id, shouldPan) {
        activeDoctorId = id;
        
        // 1. Highlight list card
        deactivateAllCards();
        const activeCard = doctorList.querySelector(`.doctor-card[data-id="${id}"]`);
        if (activeCard) {
            activeCard.classList.add('active');
            activeCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }

        // Find doctor details
        const doc = doctorsData.find(d => d.id === id);
        if (!doc) return;

        // 2. Highlight map marker
        if (googleMapsLoaded && map) {
            markers.forEach(m => {
                if (m.doctorId === id) {
                    m.setIcon(getMarkerIcon(true));
                    m.setZIndex(1000); // raise marker on top
                    if (shouldPan) {
                        map.panTo(m.getPosition());
                        map.setZoom(15);
                    }
                } else {
                    m.setIcon(getMarkerIcon(false));
                    m.setZIndex(1);
                }
            });
        }

        // 3. Open details drawer
        openDetailsDrawer(doc);
    }

    function deactivateAllCards() {
        doctorList.querySelectorAll('.doctor-card').forEach(c => c.classList.remove('active'));
    }

    // 7. Populating and Displaying Details Drawer
    function openDetailsDrawer(doc) {
        // Build rating stars
        let starsHtml = '';
        const fullStars = Math.floor(doc.rating);
        for (let i = 0; i < 5; i++) {
            if (i < fullStars) {
                starsHtml += `<svg viewBox="0 0 24 24" style="width:16px; height:16px; fill:var(--warning);"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
            } else {
                starsHtml += `<svg viewBox="0 0 24 24" style="width:16px; height:16px; fill:rgba(255,255,255,0.1);"><path d="M12 17.27 18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>`;
            }
        }

        drawerContent.innerHTML = `
            <div class="drawer-title">
                <h2>Dr. ${doc.name}</h2>
                <div style="display:flex; align-items:center; gap: 8px; margin-top: 6px;">
                    <span class="drawer-specialty-badge">${doc.specialty}</span>
                    <span style="display:flex; align-items:center; font-size: 13px; font-weight:600; color:var(--warning); gap:4px;">
                        ${starsHtml}
                        <span>${doc.rating.toFixed(1)}</span>
                    </span>
                </div>
            </div>

            <div class="drawer-section">
                <div class="drawer-section-title">Location & Clinic</div>
                <div class="drawer-meta-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"/>
                        <line x1="9" y1="3" x2="9" y2="21"/>
                    </svg>
                    <span style="font-weight:600;">${doc.clinic_name}</span>
                </div>
                <div class="drawer-meta-item" style="margin-top: 6px; align-items: flex-start;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="margin-top: 2px;">
                        <path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/>
                        <circle cx="12" cy="10" r="3"/>
                    </svg>
                    <span>${doc.address}</span>
                </div>
            </div>

            <div class="drawer-section">
                <div class="drawer-section-title">Contact Information</div>
                <div class="drawer-meta-item">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                    </svg>
                    <a href="tel:${doc.phone_number}">${doc.phone_number}</a>
                </div>
                ${doc.email ? `
                <div class="drawer-meta-item" style="margin-top: 6px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"/>
                        <polyline points="22,6 12,13 2,6"/>
                    </svg>
                    <a href="mailto:${doc.email}">${doc.email}</a>
                </div>
                ` : ''}
                ${doc.website ? `
                <div class="drawer-meta-item" style="margin-top: 6px;">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <circle cx="12" cy="12" r="10"/>
                        <line x1="2" y1="12" x2="22" y2="12"/>
                        <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
                    </svg>
                    <a href="${doc.website}" target="_blank" rel="noopener noreferrer">Visit Website</a>
                </div>
                ` : ''}
            </div>

            <div class="action-buttons">
                <a href="tel:${doc.phone_number}" class="btn btn-primary">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;">
                        <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
                    </svg>
                    Call Clinic
                </a>
                <a href="https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(doc.clinic_name + ' ' + doc.address)}" target="_blank" class="btn btn-secondary">
                    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:16px;height:16px;">
                        <polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"/>
                        <line x1="9" y1="3" x2="9" y2="18"/>
                        <line x1="15" y1="6" x2="15" y2="21"/>
                    </svg>
                    Directions
                </a>
            </div>
        `;
        detailsDrawer.classList.add('open');
    }

    function closeDrawer() {
        detailsDrawer.classList.remove('open');
        activeDoctorId = null;
        if (googleMapsLoaded && map) {
            markers.forEach(m => m.setIcon(getMarkerIcon(false)));
        }
    }

    // 8. Event Binding and Listeners Setup
    function setupEventListeners() {
        // Close drawer button
        btnCloseDrawer.addEventListener('click', () => {
            closeDrawer();
            deactivateAllCards();
        });

        // Search Input listeners
        searchInput.addEventListener('input', (e) => {
            currentQuery = e.target.value.trim();
            btnClearSearch.style.display = currentQuery ? 'block' : 'none';
            fetchDoctors(); // instant update
        });

        // Clear search button
        btnClearSearch.addEventListener('click', () => {
            searchInput.value = '';
            currentQuery = '';
            btnClearSearch.style.display = 'none';
            fetchDoctors();
            searchInput.focus();
        });

        // Specialty filter clicks
        specialtyPills.addEventListener('click', (e) => {
            const pill = e.target.closest('.pill');
            if (!pill) return;

            specialtyPills.querySelectorAll('.pill').forEach(p => p.classList.remove('active'));
            pill.classList.add('active');

            currentSpecialty = pill.dataset.specialty;
            fetchDoctors();
            closeDrawer();
        });

        // Map recenter float button
        btnRecenter.addEventListener('click', () => {
            if (googleMapsLoaded && map) {
                if (markers.length > 0) {
                    const bounds = new google.maps.LatLngBounds();
                    markers.forEach(m => bounds.extend(m.getPosition()));
                    map.fitBounds(bounds);
                } else {
                    map.panTo(defaultCity);
                    map.setZoom(13);
                }
            }
        });

        // Modal triggers
        btnOpenSettings.addEventListener('click', () => settingsModal.classList.add('open'));
        btnCloseModal.addEventListener('click', () => settingsModal.classList.remove('open'));
        btnSetupMapCenter.addEventListener('click', () => settingsModal.classList.add('open'));

        // Close modal on click overlay
        settingsModal.addEventListener('click', (e) => {
            if (e.target === settingsModal) {
                settingsModal.classList.remove('open');
            }
        });

        // Save Local API Key
        btnSaveApiKey.addEventListener('click', () => {
            const key = inputApiKey.value.trim();
            if (key) {
                localStorage.setItem('google_maps_api_key', key);
                settingsModal.classList.remove('open');
                window.location.reload(); // Reload to initialize map script with new key
            }
        });

        // Clear Local API Key
        btnClearApiKey.addEventListener('click', () => {
            localStorage.removeItem('google_maps_api_key');
            inputApiKey.value = '';
            settingsModal.classList.remove('open');
            window.location.reload();
        });
    }

})();
