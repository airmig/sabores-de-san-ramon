(function () {
  'use strict';

  const RESTAURANTS = window.SAN_RAMON_RESTAURANTS || [];
  const BOUNDS_GJ = window.SAN_RAMON_BOUNDS || { type: 'FeatureCollection', features: [] };

  const PARQUE_CENTRAL = [10.0872, -84.4704];

  const CAT_STYLE = {
    'Típica y Sodas':          { color: '#10b981', icon: '🍛' },
    'Italiana y Pizzería':     { color: '#ef4444', icon: '🍕' },
    'Comida Rápida y Pollo':   { color: '#f59e0b', icon: '🍔' },
    'Cafeterías y Panaderías': { color: '#b45309', icon: '☕' },
    'Asiática y Sushi':        { color: '#ec4899', icon: '🍣' },
    'Marisquerías y Ceviches': { color: '#06b6d4', icon: '🦐' },
    'Carnes y Parrilla':       { color: '#dc2626', icon: '🥩' },
    'Bares y Cervecerías':     { color: '#8b5cf6', icon: '🍺' },
    'Internacional y Fusión':  { color: '#3b82f6', icon: '🍽️' },
    'Heladerías y Postres':    { color: '#f472b6', icon: '🍨' },
    'Mexicana':                { color: '#84cc16', icon: '🌮' },
    'Viveros y Plantas':       { color: '#15803d', icon: '🪴' }
  };

  const TYPE_INFO = {
    todos:       { label: 'Todos',        icon: '📍', noun: 'lugares' },
    restaurante: { label: 'Restaurantes', icon: '🍽️', noun: 'restaurantes' },
    vivero:      { label: 'Viveros',      icon: '🪴', noun: 'viveros' }
  };
  const typeOf = r => r.type || 'restaurante';

  const DAY_KEYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const DAY_NAMES_ES = {
    Mon: 'Lunes', Tue: 'Martes', Wed: 'Miércoles',
    Thu: 'Jueves', Fri: 'Viernes', Sat: 'Sábado', Sun: 'Domingo'
  };

  // Compute distance (km) from Parque Central
  function haversineKm(lat1, lon1, lat2, lon2) {
    const R = 6371;
    const dLat = (lat2 - lat1) * Math.PI / 180;
    const dLon = (lon2 - lon1) * Math.PI / 180;
    const a = Math.sin(dLat / 2) ** 2 +
              Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) *
              Math.sin(dLon / 2) ** 2;
    return 2 * R * Math.asin(Math.sqrt(a));
  }

  RESTAURANTS.forEach(r => {
    r.distKm = haversineKm(PARQUE_CENTRAL[0], PARQUE_CENTRAL[1], r.lat, r.lng);
  });

  // Check if open right now in Costa Rica time (UTC-6)
  function isOpenNow(r) {
    if (r.status) return false;
    if (!r.hours) return null;
    const now = new Date();
    const utcMs = now.getTime() + now.getTimezoneOffset() * 60000;
    const crNow = new Date(utcMs - 6 * 3600000);
    const dayKey = DAY_KEYS[crNow.getDay()];
    const str = r.hours[dayKey];
    if (!str || /cerrado|closed/i.test(str)) return false;
    const curMin = crNow.getHours() * 60 + crNow.getMinutes();
    const ranges = str.split(',');
    for (const rg of ranges) {
      const m = rg.match(/(\d{1,2}):(\d{2})\s*[–-]\s*(\d{1,2}):(\d{2})/);
      if (m) {
        const s = parseInt(m[1], 10) * 60 + parseInt(m[2], 10);
        let e = parseInt(m[3], 10) * 60 + parseInt(m[4], 10);
        if (e <= s) e += 24 * 60;
        if (curMin >= s && curMin <= e) return true;
      }
    }
    return null;
  }

  // Initialize Leaflet Map
  const map = L.map('map', {
    center: PARQUE_CENTRAL,
    zoom: 15,
    minZoom: 10,
    maxZoom: 19,
    zoomControl: false
  });

  L.control.zoom({ position: 'bottomright' }).addTo(map);

  const TILES = {
    light: L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
      subdomains: 'abc',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors, HOT',
      maxZoom: 19
    }),
    dark: L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
      subdomains: 'abc',
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank">OpenStreetMap</a> contributors, HOT',
      className: 'dark-tiles',
      maxZoom: 19
    }),
    topo: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri',
      maxZoom: 19
    }),
    sat: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
      attribution: '&copy; Esri',
      maxZoom: 19
    })
  };

  TILES.light.addTo(map);

  // Draw San Ramón Canton mask (dims outside San Ramón) + District borders
  const cantonFeat = BOUNDS_GJ.features.find(f => f.properties && f.properties.level === '6');
  const districtFeats = BOUNDS_GJ.features.filter(f => f.properties && f.properties.level === '8');

  if (cantonFeat) {
    const worldRing = [[-90, -180], [90, -180], [90, 180], [-90, 180], [-90, -180]];
    const holes = cantonFeat.geometry.coordinates.map(poly =>
      poly[0].map(pt => [pt[1], pt[0]])
    );
    L.polygon([worldRing, ...holes], {
      stroke: false,
      fillColor: '#080c11',
      fillOpacity: 0.62,
      interactive: false
    }).addTo(map);

    L.geoJSON(cantonFeat, {
      style: {
        color: '#ff7a3d',
        weight: 2.5,
        fillOpacity: 0,
        dashArray: null
      },
      interactive: false
    }).addTo(map);
  }

  if (districtFeats.length) {
    L.geoJSON({ type: 'FeatureCollection', features: districtFeats }, {
      style: {
        color: '#ff7a3d',
        weight: 1,
        opacity: 0.45,
        dashArray: '4 4',
        fillOpacity: 0.01
      },
      onEachFeature: (feat, layer) => {
        const nm = feat.properties.name === 'Ángeles' ? 'Los Ángeles' : feat.properties.name;
        layer.bindTooltip(nm, {
          sticky: true,
          direction: 'center',
          className: 'district-label'
        });
      }
    }).addTo(map);
  }

  // Marker Cluster Group
  const clusterGroup = L.markerClusterGroup({
    showCoverageOnHover: false,
    maxClusterRadius: 36,
    spiderfyOnMaxZoom: true,
    iconCreateFunction: function (cluster) {
      const count = cluster.getChildCount();
      const size = count < 10 ? 34 : count < 30 ? 40 : 46;
      return L.divIcon({
        html: `<span>${count}</span>`,
        className: 'sr-cluster',
        iconSize: [size, size]
      });
    }
  });
  map.addLayer(clusterGroup);

  const markerById = new Map();

  function createPinIcon(r) {
    const st = CAT_STYLE[r.category] || { color: '#ff7a3d', icon: '🍴' };
    const isRich = (r.menu && r.menu.length > 0) || r.phone || r.whatsapp;
    return L.divIcon({
      className: '',
      html: `<div class="sr-pin ${isRich ? 'rich' : ''}" style="background:${st.color}"><span>${st.icon}</span></div>`,
      iconSize: isRich ? [34, 34] : [30, 30],
      iconAnchor: isRich ? [17, 34] : [15, 30],
      popupAnchor: [0, -28]
    });
  }

  // State
  const state = {
    type: 'todos',
    q: '',
    category: 'Todas',
    onlyOpen: false,
    onlyPhone: false,
    onlyMenu: false,
    district: 'Todos',
    sort: 'info',
    selectedId: null
  };

  // Places in the selected type (Todos / Restaurantes / Viveros)
  function scoped() {
    return state.type === 'todos' ? RESTAURANTS : RESTAURANTS.filter(r => typeOf(r) === state.type);
  }

  // Type switcher: Todos / Restaurantes / Viveros
  function renderTypes() {
    const counts = { todos: RESTAURANTS.length, restaurante: 0, vivero: 0 };
    RESTAURANTS.forEach(r => { counts[typeOf(r)] = (counts[typeOf(r)] || 0) + 1; });
    const el = document.getElementById('typeSeg');
    el.innerHTML = Object.entries(TYPE_INFO).map(([k, t]) => `
      <button type="button" role="tab" data-type="${k}" class="${state.type === k ? 'on' : ''}"
        aria-selected="${state.type === k}"><span class="ti" aria-hidden="true">${t.icon}</span> ${t.label} <small>${counts[k] || 0}</small></button>
    `).join('');
    el.querySelectorAll('button').forEach(btn => {
      btn.addEventListener('click', () => {
        if (state.type === btn.dataset.type) return;
        state.type = btn.dataset.type;
        const list = scoped();
        if (!list.some(r => r.category === state.category)) state.category = 'Todas';
        if (!list.some(r => r.district === state.district)) state.district = 'Todos';
        renderTypes();
        renderStats();
        renderCategories();
        renderDistricts();
        updateView();
        fitToResults();
      });
    });
  }

  // Build Stats
  function renderStats() {
    const list = scoped();
    const total = list.length;
    const withPhone = list.filter(r => r.phone || r.delivery || r.whatsapp).length;
    const withMenu = list.filter(r => r.menu && r.menu.length > 0).length;
    const withHours = list.filter(r => r.hours).length;
    const verified = list.filter(r => r.verified).length;
    const totalLabel = state.type === 'vivero' ? 'Viveros en mapa'
      : (state.type === 'restaurante' ? 'Restaurantes' : 'Lugares en mapa');
    const second = state.type === 'vivero'
      ? `<div class="stat-card"><strong>${verified}</strong><span>Verificados</span></div>`
      : `<div class="stat-card"><strong>${withMenu}</strong><span>Con menú</span></div>`;
    document.getElementById('stats').innerHTML = `
      <div class="stat-card"><strong>${total}</strong><span>${totalLabel}</span></div>
      ${second}
      <div class="stat-card"><strong>${withPhone}</strong><span>Con teléfono</span></div>
      <div class="stat-card"><strong>${withHours}</strong><span>Con horario</span></div>
    `;
  }

  // Build Category Chips & Legend
  function renderCategories() {
    const list = scoped();
    const counts = {};
    list.forEach(r => { counts[r.category] = (counts[r.category] || 0) + 1; });
    const cats = ['Todas', ...Object.keys(CAT_STYLE).filter(c => counts[c])];

    const chipsEl = document.getElementById('chips');
    chipsEl.innerHTML = cats.map(c => {
      const st = CAT_STYLE[c];
      const cnt = c === 'Todas' ? list.length : counts[c];
      const active = state.category === c ? 'active' : '';
      const dot = st ? `<span class="dot" style="background:${st.color}"></span>` : '';
      return `<button class="chip ${active}" data-cat="${c}">${dot}${c} (${cnt})</button>`;
    }).join('');

    chipsEl.querySelectorAll('.chip').forEach(btn => {
      btn.addEventListener('click', () => {
        state.category = btn.dataset.cat;
        renderCategories();
        updateView();
      });
    });

    const legEl = document.getElementById('legend');
    legEl.innerHTML = Object.entries(CAT_STYLE)
      .filter(([c]) => counts[c])
      .map(([c, st]) => `
        <span class="legend-item" data-cat="${c}">
          <span class="dot" style="background:${st.color}"></span>${st.icon} ${c}
        </span>
      `).join('');

    legEl.querySelectorAll('.legend-item').forEach(el => {
      el.addEventListener('click', () => {
        state.category = state.category === el.dataset.cat ? 'Todas' : el.dataset.cat;
        renderCategories();
        updateView();
      });
    });
  }

  // Build District Select
  function renderDistricts() {
    const list = scoped();
    const dCounts = {};
    list.forEach(r => { dCounts[r.district] = (dCounts[r.district] || 0) + 1; });
    const dists = Object.keys(dCounts).sort((a, b) =>
      (a === 'Fuera del cantón') - (b === 'Fuera del cantón') || dCounts[b] - dCounts[a]);
    const sel = document.getElementById('fDistrict');
    sel.innerHTML = `<option value="Todos">Todos los distritos (${list.length})</option>` +
      dists.map(d => `<option value="${d}">${d} (${dCounts[d]})</option>`).join('');
    sel.value = state.district;
  }

  // Filter & Sort
  function getFiltered() {
    const q = state.q.trim().toLowerCase();
    const list = RESTAURANTS.filter(r => {
      if (state.type !== 'todos' && typeOf(r) !== state.type) return false;
      if (state.category !== 'Todas' && r.category !== state.category) return false;
      if (state.district !== 'Todos' && r.district !== state.district) return false;
      if (state.onlyOpen && isOpenNow(r) !== true) return false;
      if (state.onlyPhone && !(r.phone || r.delivery || r.whatsapp)) return false;
      if (state.onlyMenu && !(r.menu && r.menu.length > 0)) return false;
      if (q) {
        const hay = [
          r.name, r.category, r.address, r.district, r.description, r.googleName,
          typeOf(r) === 'vivero' ? 'vivero plantas jardín' : 'restaurante comida',
          ...(r.menu || []).map(m => m.item)
        ].join(' ').toLowerCase();
        if (!hay.includes(q)) return false;
      }
      return true;
    });

    if (state.sort === 'name') {
      list.sort((a, b) => a.name.localeCompare(b.name, 'es'));
    } else if (state.sort === 'dist') {
      list.sort((a, b) => a.distKm - b.distKm);
    } else {
      list.sort((a, b) => (b.infoScore - a.infoScore) || a.name.localeCompare(b.name, 'es'));
    }
    return list;
  }

  // Render Sidebar List & Map Markers
  function updateView() {
    const filtered = getFiltered();
    const scopeTotal = scoped().length;
    document.getElementById('count').textContent =
      `Mostrando ${filtered.length} de ${scopeTotal} ${TYPE_INFO[state.type].noun}` +
      (state.type === 'vivero' ? ' en San Ramón y alrededores' : ' en San Ramón');

    // Update map markers
    clusterGroup.clearLayers();
    markerById.clear();

    filtered.forEach(r => {
      const m = L.marker([r.lat, r.lng], { icon: createPinIcon(r) });
      m.on('click', () => selectRestaurant(r.id, true));
      markerById.set(r.id, m);
      clusterGroup.addLayer(m);
    });

    // Update list
    const listEl = document.getElementById('list');
    if (!filtered.length) {
      listEl.innerHTML = `<li class="empty-note">No se encontraron ${TYPE_INFO[state.type].noun} con estos filtros. Prueba limpiar la búsqueda.</li>`;
      return;
    }

    listEl.innerHTML = filtered.map(r => {
      const st = CAT_STYLE[r.category] || { color: '#ff7a3d', icon: '🍴' };
      const openState = isOpenNow(r);
      let openBadge = '';
      if (r.status) openBadge = `<span class="badge closed">${r.status}</span>`;
      else if (openState === true) openBadge = `<span class="badge open">● Abierto</span>`;
      else if (openState === false) openBadge = `<span class="badge closed">Cerrado ahora</span>`;
      const isVivero = typeOf(r) === 'vivero';

      const phoneBadge = (r.phone || r.whatsapp)
        ? `<span class="badge phone">📞 ${r.phone || r.whatsapp}</span>`
        : (r.delivery ? `<span class="badge phone">🛵 ${r.delivery}</span>` : `<span class="badge">Sin teléfono</span>`);

      const menuBadge = isVivero
        ? (r.distanceKm ? `<span class="badge">${r.distanceKm} km del centro</span>` : '')
        : ((r.menu && r.menu.length)
          ? `<span class="badge menu">📋 ${r.menu.length} platos</span>`
          : `<span class="badge">Menú no publicado</span>`);

      const ratingHtml = r.rating
        ? `<span class="rating-pill">★ ${r.rating.toFixed(1)}</span>`
        : '';

      const selClass = state.selectedId === r.id ? 'selected' : '';

      return `
        <li class="card ${selClass}" data-id="${r.id}">
          <div class="card-top">
            <div>
              <div class="card-title">${r.name}</div>
              <div class="card-cat">
                <span class="dot" style="background:${st.color}"></span>
                ${st.icon} ${r.category} · ${r.district}
              </div>
            </div>
            ${ratingHtml}
          </div>
          <div class="card-addr">📍 ${r.address}</div>
          <div class="card-badges">
            ${openBadge}
            ${phoneBadge}
            ${menuBadge}
          </div>
        </li>
      `;
    }).join('');

    listEl.querySelectorAll('.card').forEach(card => {
      card.addEventListener('click', () => {
        const id = parseInt(card.dataset.id, 10);
        selectRestaurant(id, true);
      });
    });
  }

  // Open Detail Drawer & Fly to Marker
  function selectRestaurant(id, fly = true) {
    state.selectedId = id;
    const r = RESTAURANTS.find(x => x.id === id);
    if (!r) return;

    document.querySelectorAll('.card').forEach(el => {
      el.classList.toggle('selected', parseInt(el.dataset.id, 10) === id);
    });

    if (fly) {
      map.flyTo([r.lat, r.lng], Math.max(map.getZoom(), 17), { duration: 0.65 });
    }

    const st = CAT_STYLE[r.category] || { color: '#ff7a3d', icon: '🍴' };
    const openState = isOpenNow(r);
    const isVivero = typeOf(r) === 'vivero';
    const openBadge = r.status
      ? `<span class="badge closed">${r.status}</span>`
      : (openState === true
        ? `<span class="badge open">● Abierto ahora</span>`
        : (openState === false ? `<span class="badge closed">Cerrado en este momento</span>` : ''));

    const cleanTel = (r.phone || r.whatsapp || '').replace(/[^\d+]/g, '');
    const cleanWa = (r.whatsapp || '').replace(/[^\d]/g, '');
    const gmapsUrl = `https://www.google.com/maps/search/?api=1&query=${r.lat},${r.lng}`;
    const wazeUrl = `https://waze.com/ul?ll=${r.lat},${r.lng}&navigate=yes`;

    let actionsHtml = '';
    if (cleanTel) {
      actionsHtml += `<a class="act-btn primary" href="tel:${cleanTel}">📞 ${isVivero ? 'Llamar' : 'Llamar Express'}</a>`;
    }
    if (cleanWa) {
      actionsHtml += `<a class="act-btn wa" href="https://wa.me/${cleanWa}" target="_blank" rel="noopener">💬 WhatsApp</a>`;
    }
    actionsHtml += `<a class="act-btn" href="${wazeUrl}" target="_blank" rel="noopener">🚗 Waze</a>`;
    actionsHtml += `<a class="act-btn" href="${gmapsUrl}" target="_blank" rel="noopener">🗺️ Google Maps</a>`;
    if (r.website || r.facebook) {
      actionsHtml += `<a class="act-btn" href="${r.website || r.facebook}" target="_blank" rel="noopener">🌐 Web / Redes</a>`;
    }

    // Menu section
    let menuHtml = '';
    if (r.menu && r.menu.length > 0) {
      menuHtml = `
        <ul class="menu-list">
          ${r.menu.map(m => `
            <li class="menu-item">
              <span>${m.item}</span>
              <span class="price">${m.price || ''}</span>
            </li>
          `).join('')}
        </ul>
      `;
    } else {
      menuHtml = `<div class="empty-note">Menú digital o precios no publicados en línea para este local.</div>`;
    }

    // Schedule section
    let hoursHtml = '';
    if (r.hours) {
      const now = new Date();
      const utcMs = now.getTime() + now.getTimezoneOffset() * 60000;
      const crNow = new Date(utcMs - 6 * 3600000);
      const todayKey = DAY_KEYS[crNow.getDay()];
      hoursHtml = `
        <table class="hours-table">
          ${['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'].map(k => `
            <tr class="${k === todayKey ? 'today' : ''}">
              <td>${DAY_NAMES_ES[k]}${k === todayKey ? ' (Hoy)' : ''}</td>
              <td>${r.hours[k] === '00:00–23:59' ? 'Abierto 24 horas' : (r.hours[k] || 'No especificado')}</td>
            </tr>
          `).join('')}
        </table>
      `;
    } else {
      hoursHtml = `<div class="empty-note">Horario detallado no disponible en registros públicos.</div>`;
    }

    const body = document.getElementById('drawerBody');
    body.innerHTML = `
      <h2>${r.name}</h2>
      <div class="drawer-meta">
        <span class="badge" style="border-color:${st.color};color:#fff">${st.icon} ${r.category}</span>
        <span class="badge">📍 ${r.district === 'Fuera del cantón' ? 'Fuera del cantón' : 'Distrito ' + r.district}</span>
        ${r.rating ? `<span class="rating-pill">★ ${r.rating.toFixed(1)}${r.votes ? ` (${r.votes} reseñas)` : ''}</span>` : ''}
        ${openBadge}
      </div>
      ${r.description ? `<p class="drawer-desc">${r.description}</p>` : ''}

      <div class="action-grid">${actionsHtml}</div>

      <div class="sec">
        <h3>${isVivero ? 'Ubicación y contacto' : 'Ubicación y Express'}</h3>
        <div class="info-row"><span>Dirección</span><span>${r.address}</span></div>
        <div class="info-row"><span>${isVivero ? 'Teléfono' : 'Teléfono / Express'}</span><span>${r.phone || r.delivery || 'No registrado'}</span></div>
        ${r.whatsapp ? `<div class="info-row"><span>WhatsApp Pedidos</span><span>${r.whatsapp}</span></div>` : ''}
        <div class="info-row"><span>Coordenadas</span><span>${r.lat.toFixed(5)}, ${r.lng.toFixed(5)} ${r.coordsApprox ? '(aprox.)' : '(exactas)'}</span></div>
        <div class="info-row"><span>Distancia al Parque Central</span><span>${r.distKm < 1 ? Math.round(r.distKm * 1000) + ' m' : r.distKm.toFixed(1) + ' km'}</span></div>
        <div class="info-row"><span>Verificación</span><span>${r.verified
          ? `✔ Confirmado en Google Maps${r.googleName && r.googleName !== r.name ? ` como “${r.googleName}”` : ''}`
          : '⚠ No se pudo confirmar en Google Maps'}</span></div>
      </div>

      ${isVivero ? '' : `<div class="sec">
        <h3>Menú y Especialidades</h3>
        ${menuHtml}
      </div>`}

      <div class="sec">
        <h3>Horario de Atención</h3>
        ${hoursHtml}
      </div>
    `;

    const drawer = document.getElementById('drawer');
    drawer.classList.add('open');
    drawer.setAttribute('aria-hidden', 'false');
  }

  document.getElementById('drawerClose').addEventListener('click', () => {
    document.getElementById('drawer').classList.remove('open');
    document.getElementById('drawer').setAttribute('aria-hidden', 'true');
    state.selectedId = null;
    document.querySelectorAll('.card.selected').forEach(el => el.classList.remove('selected'));
  });

  // Search & Filter Controls
  const qInput = document.getElementById('q');
  qInput.addEventListener('input', e => {
    state.q = e.target.value;
    updateView();
  });

  window.addEventListener('keydown', e => {
    if (e.key === '/' && document.activeElement !== qInput) {
      e.preventDefault();
      qInput.focus();
    } else if (e.key === 'Escape') {
      document.getElementById('drawerClose').click();
    }
  });

  document.getElementById('fOpen').addEventListener('change', e => {
    state.onlyOpen = e.target.checked;
    updateView();
  });
  document.getElementById('fPhone').addEventListener('change', e => {
    state.onlyPhone = e.target.checked;
    updateView();
  });
  document.getElementById('fMenu').addEventListener('change', e => {
    state.onlyMenu = e.target.checked;
    updateView();
  });
  document.getElementById('fDistrict').addEventListener('change', e => {
    state.district = e.target.value;
    updateView();
  });
  document.getElementById('sort').addEventListener('change', e => {
    state.sort = e.target.value;
    updateView();
  });

  // Map Base Layer Switcher
  let currentTile = TILES.light;
  document.querySelectorAll('#baseSeg button').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('#baseSeg button').forEach(b => b.classList.remove('on'));
      btn.classList.add('on');
      const next = TILES[btn.dataset.base];
      if (next && next !== currentTile) {
        map.removeLayer(currentTile);
        next.addTo(map);
        currentTile = next;
      }
    });
  });

  document.getElementById('btnCenter').addEventListener('click', () => {
    map.flyTo(PARQUE_CENTRAL, 16, { duration: 0.7 });
  });

  document.getElementById('btnCanton').addEventListener('click', () => {
    if (cantonFeat) {
      const layer = L.geoJSON(cantonFeat);
      map.flyToBounds(layer.getBounds(), { padding: [24, 24], duration: 0.8 });
    }
  });

  function fitToResults() {
    const b = clusterGroup.getBounds();
    if (b.isValid()) map.flyToBounds(b, { padding: [30, 30], maxZoom: 16, duration: 0.7 });
  }

  // Initial render
  renderTypes();
  renderStats();
  renderCategories();
  renderDistricts();
  updateView();
})();
