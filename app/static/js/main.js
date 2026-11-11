/**
 * PickXI - Script Principal & Moteur d'Interactions
 * Direction Artistique & Expérience Utilisateur
 * Gestion du Terrain Tactique, Comparateur, Radar SVG et Modales
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeroPrompts();
  initTacticalPitch();
  initCompareManager();
  initModalQuickView();
  initRangeSliders();
  initRadarCharts();
  initSearchModeSwitcher();
  initChatbox();
});

/* ==========================================================================
   1. HERO PROMPTS SUGGESTIONS
   ========================================================================== */
function initHeroPrompts() {
  const promptInput = document.getElementById('heroPromptInput');
  const promptPills = document.querySelectorAll('.prompt-pill');

  if (!promptInput || !promptPills.length) return;

  promptPills.forEach(pill => {
    pill.addEventListener('click', () => {
      const text = pill.getAttribute('data-prompt') || pill.textContent.trim();
      promptInput.value = text;
      promptInput.focus();

      // Effet visuel de pulsation
      promptInput.parentElement.classList.add('pulse-mint');
      setTimeout(() => {
        promptInput.parentElement.classList.remove('pulse-mint');
      }, 1000);
    });
  });
}

/* ==========================================================================
   2. LE TERRAIN TACTIQUE INTERACTIF (PICK XI PITCH)
   ========================================================================== */
const FORMATIONS_COORDS = {
  "4-3-3": [
    { pos: "GK", top: "88%", left: "50%" },
    { pos: "LB", top: "72%", left: "15%" },
    { pos: "CB", top: "75%", left: "38%" },
    { pos: "CB", top: "75%", left: "62%" },
    { pos: "RB", top: "72%", left: "85%" },
    { pos: "CDM", top: "54%", left: "50%" },
    { pos: "CM", top: "42%", left: "30%" },
    { pos: "CM", top: "42%", left: "70%" },
    { pos: "LW", top: "20%", left: "18%" },
    { pos: "ST", top: "14%", left: "50%" },
    { pos: "RW", top: "20%", left: "82%" }
  ],
  "4-2-3-1": [
    { pos: "GK", top: "88%", left: "50%" },
    { pos: "LB", top: "72%", left: "15%" },
    { pos: "CB", top: "75%", left: "38%" },
    { pos: "CB", top: "75%", left: "62%" },
    { pos: "RB", top: "72%", left: "85%" },
    { pos: "CDM", top: "58%", left: "35%" },
    { pos: "CDM", top: "58%", left: "65%" },
    { pos: "CAM", top: "35%", left: "50%" },
    { pos: "LM", top: "32%", left: "18%" },
    { pos: "RM", top: "32%", left: "82%" },
    { pos: "ST", top: "14%", left: "50%" }
  ],
  "4-4-2": [
    { pos: "GK", top: "88%", left: "50%" },
    { pos: "LB", top: "72%", left: "15%" },
    { pos: "CB", top: "75%", left: "38%" },
    { pos: "CB", top: "75%", left: "62%" },
    { pos: "RB", top: "72%", left: "85%" },
    { pos: "LM", top: "46%", left: "16%" },
    { pos: "CM", top: "50%", left: "38%" },
    { pos: "CM", top: "50%", left: "62%" },
    { pos: "RM", top: "46%", left: "84%" },
    { pos: "ST", top: "18%", left: "38%" },
    { pos: "ST", top: "18%", left: "62%" }
  ],
  "3-5-2": [
    { pos: "GK", top: "88%", left: "50%" },
    { pos: "CB", top: "74%", left: "26%" },
    { pos: "CB", top: "76%", left: "50%" },
    { pos: "CB", top: "74%", left: "74%" },
    { pos: "CDM", top: "56%", left: "38%" },
    { pos: "CDM", top: "56%", left: "62%" },
    { pos: "LM", top: "42%", left: "14%" },
    { pos: "CAM", top: "34%", left: "50%" },
    { pos: "RM", top: "42%", left: "86%" },
    { pos: "ST", top: "16%", left: "38%" },
    { pos: "ST", top: "16%", left: "62%" }
  ]
};

function initTacticalPitch() {
  const pitchContainer = document.getElementById('tacticalPitchSurface');
  const formationSelect = document.getElementById('pitchFormationSelect');
  const autoFillBtn = document.getElementById('pitchAutoFillBtn');

  if (!pitchContainer) return;

  let currentFormation = formationSelect ? formationSelect.value : "4-3-3";

  function renderSlots(formationName) {
    pitchContainer.querySelectorAll('.pitch-slot').forEach(el => el.remove());
    const coords = FORMATIONS_COORDS[formationName] || FORMATIONS_COORDS["4-3-3"];

    coords.forEach((item, index) => {
      const slot = document.createElement('div');
      slot.className = 'pitch-slot';
      slot.style.top = item.top;
      slot.style.left = item.left;
      slot.setAttribute('data-pos', item.pos);
      slot.setAttribute('data-index', index);

      slot.innerHTML = `
        <div class="slot-node">
          <span class="slot-empty-icon">+</span>
        </div>
        <span class="slot-label">${item.pos}</span>
      `;

      slot.addEventListener('click', () => {
        handlePitchSlotClick(item.pos, slot);
      });

      pitchContainer.appendChild(slot);
    });
  }

  renderSlots(currentFormation);

  if (formationSelect) {
    formationSelect.addEventListener('change', (e) => {
      currentFormation = e.target.value;
      renderSlots(currentFormation);
    });
  }

  if (autoFillBtn) {
    autoFillBtn.addEventListener('click', () => {
      fillDemoSquad();
    });
  }
}

function handlePitchSlotClick(position, slotEl) {
  // Sélection visuelle
  document.querySelectorAll('.pitch-slot').forEach(s => s.classList.remove('active'));
  slotEl.classList.add('active');

  // Si on est sur la page /pitch, ouvrir le tiroir des recommandations pour ce poste
  const scoutDrawer = document.getElementById('pitchScoutDrawer');
  const drawerTitle = document.getElementById('pitchDrawerTitle');
  const drawerPosBadge = document.getElementById('pitchDrawerPosBadge');

  if (scoutDrawer && drawerTitle) {
    drawerTitle.textContent = `Pépites recommandées pour le poste :`;
    if (drawerPosBadge) drawerPosBadge.textContent = position;
    scoutDrawer.classList.add('open');

    // Mettre à jour l'iframe ou la liste de suggestion
    filterDrawerByPosition(position);
  } else {
    // Redirection directe vers le scout avec filtre de poste
    window.location.href = `/scout?pos=${position}`;
  }
}

function fillDemoSquad() {
  const samplePicks = [
    { pos: "GK", name: "Alisson", ovr: 89, img: "https://cdn.sofifa.net/players/212/831/26_120.png" },
    { pos: "LB", name: "T. Hernandez", ovr: 87, img: "https://cdn.sofifa.net/players/232/656/26_120.png" },
    { pos: "CB", name: "Saliba", ovr: 87, img: "https://cdn.sofifa.net/players/243/780/26_120.png" },
    { pos: "CB", name: "Van Dijk", ovr: 89, img: "https://cdn.sofifa.net/players/203/376/26_120.png" },
    { pos: "RB", name: "Hakimi", ovr: 89, img: "https://cdn.sofifa.net/players/235/212/26_120.png" },
    { pos: "CDM", name: "Rodri", ovr: 91, img: "https://cdn.sofifa.net/players/231/869/26_120.png" },
    { pos: "CM", name: "Valverde", ovr: 89, img: "https://cdn.sofifa.net/players/239/053/26_120.png" },
    { pos: "CM", name: "Bellingham", ovr: 90, img: "https://cdn.sofifa.net/players/252/371/26_120.png" },
    { pos: "LW", name: "Vinicius Jr", ovr: 90, img: "https://cdn.sofifa.net/players/238/794/26_120.png" },
    { pos: "ST", name: "Mbappé", ovr: 91, img: "https://cdn.sofifa.net/players/231/747/26_120.png" },
    { pos: "RW", name: "Salah", ovr: 89, img: "https://cdn.sofifa.net/players/209/331/26_120.png" }
  ];

  const slots = document.querySelectorAll('.pitch-slot');
  slots.forEach((slot, idx) => {
    const data = samplePicks[idx % samplePicks.length];
    if (data) {
      const node = slot.querySelector('.slot-node');
      node.innerHTML = `<img src="${data.img}" alt="${data.name}" onerror="this.src='/static/img/logo.png'">`;
      node.style.borderColor = "var(--accent-mint)";
      slot.querySelector('.slot-label').textContent = `${data.ovr} ${data.name}`;
    }
  });

  // Mise à jour des stats globales
  const squadOvr = document.getElementById('squadOverallVal');
  const squadCost = document.getElementById('squadCostVal');
  if (squadOvr) squadOvr.textContent = "89 OVR";
  if (squadCost) squadCost.textContent = "420M €";
}

/* ==========================================================================
   3. GESTION DU COMPARATEUR (COMPARE MANAGER)
   ========================================================================== */
let compareList = JSON.parse(localStorage.getItem('pickxi_compare') || '[]');

function initCompareManager() {
  updateCompareBar();

  // Boutons 'Comparer' sur les cartes
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('.btn-action-compare');
    if (!btn) return;

    e.preventDefault();
    e.stopPropagation();

    const id = btn.getAttribute('data-id');
    const name = btn.getAttribute('data-name');
    const img = btn.getAttribute('data-img');

    toggleComparePlayer(id, name, img);
  });

  const clearBtn = document.getElementById('compareClearBtn');
  if (clearBtn) {
    clearBtn.addEventListener('click', () => {
      compareList = [];
      localStorage.setItem('pickxi_compare', JSON.stringify(compareList));
      updateCompareBar();
    });
  }
}

function toggleComparePlayer(id, name, img) {
  const existingIdx = compareList.findIndex(p => p.id === id);
  if (existingIdx >= 0) {
    compareList.splice(existingIdx, 1);
  } else {
    if (compareList.length >= 2) {
      compareList.shift(); // Remplace le premier
    }
    compareList.push({ id, name, img });
  }

  localStorage.setItem('pickxi_compare', JSON.stringify(compareList));
  updateCompareBar();
}

function updateCompareBar() {
  const bar = document.getElementById('compareFloatingBar');
  const slotsContainer = document.getElementById('compareBarSlots');
  const launchBtn = document.getElementById('compareLaunchBtn');

  if (!bar) return;

  if (compareList.length > 0) {
    bar.classList.add('active');
    if (slotsContainer) {
      slotsContainer.innerHTML = compareList.map(p => `
        <div class="compare-slot-thumb" title="${p.name}">
          <img src="${p.img}" alt="${p.name}" onerror="this.src='/static/img/logo.png'">
        </div>
      `).join('');
    }

    if (launchBtn) {
      if (compareList.length === 2) {
        launchBtn.href = `/compare?p1=${compareList[0].id}&p2=${compareList[1].id}`;
        launchBtn.style.pointerEvents = "auto";
        launchBtn.style.opacity = "1";
        launchBtn.textContent = "Lancer le Duel (2/2)";
      } else {
        launchBtn.href = "#";
        launchBtn.style.pointerEvents = "none";
        launchBtn.style.opacity = "0.6";
        launchBtn.textContent = "Choisis un 2e joueur (1/2)";
      }
    }
  } else {
    bar.classList.remove('active');
  }
}

/* ==========================================================================
   4. MODALE DE FICHE DÉTAILLÉE DU JOUEUR (QUICK VIEW)
   ========================================================================== */
function initModalQuickView() {
  const backdrop = document.getElementById('playerDetailModal');
  const closeBtn = document.getElementById('modalCloseBtn');

  if (!backdrop) return;

  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.btn-quick-view');
    if (!trigger) return;

    e.preventDefault();
    const playerId = trigger.getAttribute('data-id');
    openPlayerModal(playerId);
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      backdrop.classList.remove('open');
    });
  }

  backdrop.addEventListener('click', (e) => {
    if (e.target === backdrop) {
      backdrop.classList.remove('open');
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && backdrop.classList.contains('open')) {
      backdrop.classList.remove('open');
    }
  });
}

function openPlayerModal(playerId) {
  const backdrop = document.getElementById('playerDetailModal');
  const modalContent = document.getElementById('modalPlayerContent');
  if (!backdrop || !modalContent) return;

  modalContent.innerHTML = `
    <div style="padding: 40px; text-align: center; color: var(--accent-mint); font-family: var(--font-display);">
      <div style="font-size: 1.2rem; margin-bottom: 10px;">Chargement du dossier de détection...</div>
      <p style="color: var(--text-secondary);">Analyse des PlayStyles & ratios tactiques en cours.</p>
    </div>
  `;

  backdrop.classList.add('open');

  fetch(`/player/${playerId}?format=json`)
    .then(res => res.json())
    .then(data => {
      renderModalPlayerData(data);
    })
    .catch(() => {
      // Fallback avec redirection vers page joueur
      window.location.href = `/player/${playerId}`;
    });
}

function renderModalPlayerData(player) {
  const modalContent = document.getElementById('modalPlayerContent');
  if (!modalContent || !player) return;

  modalContent.innerHTML = `
    <div style="padding: 24px; display: grid; grid-template-columns: 280px 1fr; gap: 28px;">
      <!-- Colonne Carte -->
      <div>
        <div class="fut-card card-meta" style="margin: 0 auto;">
          <div class="fut-card-header">
            <div class="fut-card-badge">
              <div class="fut-rating">${player.overall}</div>
              <div class="fut-position">${player.position}</div>
              <div class="fut-meta-icons">
                <span class="fut-nation-flag">${player.nationality}</span>
                <span class="fut-club-pill">${player.club}</span>
              </div>
            </div>
            <div class="fut-player-visual">
              <img src="${player.face_url}" alt="${player.name}" onerror="this.src='/static/img/logo.png'">
            </div>
          </div>
          <div class="fut-player-name">${player.name}</div>
          <div class="fut-stats-grid">
            <div class="fut-stat-item"><span class="fut-stat-value">${player.pace}</span><span class="fut-stat-label">PAC</span></div>
            <div class="fut-stat-item"><span class="fut-stat-value">${player.dribbling}</span><span class="fut-stat-label">DRI</span></div>
            <div class="fut-stat-item"><span class="fut-stat-value">${player.shooting}</span><span class="fut-stat-label">SHO</span></div>
            <div class="fut-stat-item"><span class="fut-stat-value">${player.defending}</span><span class="fut-stat-label">DEF</span></div>
            <div class="fut-stat-item"><span class="fut-stat-value">${player.passing}</span><span class="fut-stat-label">PAS</span></div>
            <div class="fut-stat-item"><span class="fut-stat-value">${player.physicality}</span><span class="fut-stat-label">PHY</span></div>
          </div>
          <div class="fut-card-footer">
            <span class="fut-price-tag">${player.market_value_eur ? (player.market_value_eur / 1000000).toFixed(1) + 'M €' : 'N/C'}</span>
          </div>
        </div>
      </div>

      <!-- Colonne Détails & Scout -->
      <div style="display: flex; flex-direction: column; gap: 18px;">
        <div>
          <div class="badge-tag">Verdict du Scout PickXI</div>
          <h2 style="margin: 6px 0; font-size: 1.8rem;">${player.name}</h2>
          <p style="color: var(--text-secondary); font-size: 0.95rem;">
            ${player.club} • ${player.league || 'Élite'} • ${player.age} ans (${player.birth_date})
          </p>
        </div>

        <div style="background: var(--bg-deep); padding: 14px 18px; border-radius: var(--radius-md); border: 1px solid var(--border-medium);">
          <div style="font-family: var(--font-display); font-weight: 700; color: var(--accent-mint); text-transform: uppercase; font-size: 0.85rem; margin-bottom: 6px;">
            Points Clés Méta & PlayStyles
          </div>
          <p style="font-size: 0.9rem; color: var(--text-main);">
            Profil athlétique chirurgical. Excellente tenue physique sur 90 minutes. 
            Idéal pour amorcer des transitions verticales ou verrouiller les phases de contre-attaque adverse.
          </p>
        </div>

        <div style="display: flex; gap: 12px; margin-top: auto;">
          <a href="/player/${player.sofifa_id}" class="btn btn-primary" style="flex: 1;">Voir Fiche Complète</a>
          <button class="btn btn-secondary btn-action-compare" data-id="${player.sofifa_id}" data-name="${player.name}" data-img="${player.face_url}">
            Ajouter au Comparateur
          </button>
        </div>
      </div>
    </div>
  `;
}

/* ==========================================================================
   5. SLIDERS PERSONNALISÉS (RETEX VISUEL EN DIRECT)
   ========================================================================== */
function initRangeSliders() {
  document.querySelectorAll('.range-slider').forEach(slider => {
    const outputId = slider.getAttribute('data-target');
    const output = document.getElementById(outputId);

    if (output) {
      slider.addEventListener('input', () => {
        output.textContent = slider.value;
      });
    }
  });
}

/* ==========================================================================
   6. GÉNÉRATEUR MATHEMATIQUE DE RADAR 6 AXES (SVG)
   ========================================================================== */
function initRadarCharts() {
  const radarContainers = document.querySelectorAll('[data-radar-chart]');
  radarContainers.forEach(container => {
    const s1 = JSON.parse(container.getAttribute('data-stats-1') || '[]');
    const s2 = JSON.parse(container.getAttribute('data-stats-2') || '[]');
    renderRadarSvg(container, s1, s2);
  });
}

function renderRadarSvg(container, stats1, stats2) {
  const size = 300;
  const center = size / 2;
  const radius = 110;
  const axes = ["PAC", "SHO", "PAS", "DRI", "DEF", "PHY"];
  const totalAxes = 6;

  function getPoint(index, value) {
    const angle = (Math.PI * 2 / totalAxes) * index - (Math.PI / 2);
    const r = (value / 100) * radius;
    const x = center + r * Math.cos(angle);
    const y = center + r * Math.sin(angle);
    return { x, y };
  }

  // Création des niveaux circulaires (20%, 40%, 60%, 80%, 100%)
  let gridPolygons = "";
  [0.2, 0.4, 0.6, 0.8, 1.0].forEach(level => {
    let pts = [];
    for (let i = 0; i < totalAxes; i++) {
      const p = getPoint(i, level * 100);
      pts.push(`${p.x},${p.y}`);
    }
    gridPolygons += `<polygon points="${pts.join(' ')}" class="radar-axis-grid"/>`;
  });

  // Rayons d'axes et labels
  let axisLines = "";
  let labels = "";
  for (let i = 0; i < totalAxes; i++) {
    const pMax = getPoint(i, 100);
    const pLabel = getPoint(i, 118);
    axisLines += `<line x1="${center}" y1="${center}" x2="${pMax.x}" y2="${pMax.y}" class="radar-axis-line"/>`;
    labels += `<text x="${pLabel.x}" y="${pLabel.y}" class="radar-label">${axes[i]}</text>`;
  }

  // Polygone Joueur 1
  let poly1 = "";
  if (stats1.length === 6) {
    let pts1 = stats1.map((v, i) => {
      const p = getPoint(i, v);
      return `${p.x},${p.y}`;
    }).join(' ');
    poly1 = `<polygon points="${pts1}" class="radar-poly-1"/>`;
  }

  // Polygone Joueur 2
  let poly2 = "";
  if (stats2.length === 6) {
    let pts2 = stats2.map((v, i) => {
      const p = getPoint(i, v);
      return `${p.x},${p.y}`;
    }).join(' ');
    poly2 = `<polygon points="${pts2}" class="radar-poly-2"/>`;
  }

  container.innerHTML = `
    <svg viewBox="0 0 ${size} ${size}" class="radar-chart-svg">
      ${gridPolygons}
      ${axisLines}
      ${poly1}
      ${poly2}
      ${labels}
    </svg>
  `;
}

/* ==========================================================================
   7. GESTION DES DEUX MODES DE RECHERCHE (CRITÈRES BD vs CHATBOT IA)
   ========================================================================== */
function initSearchModeSwitcher() {
  const modeBtns = document.querySelectorAll('.search-mode-btn');
  const criteriaSection = document.getElementById('searchModeCriteria');
  const chatSection = document.getElementById('searchModeChat');

  if (!modeBtns.length || !criteriaSection || !chatSection) return;

  modeBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const targetMode = btn.getAttribute('data-mode'); // 'criteria' ou 'chat'
      
      modeBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');

      if (targetMode === 'chat') {
        criteriaSection.style.display = 'none';
        chatSection.style.display = 'block';
        const chatInput = document.getElementById('chatInput');
        if (chatInput) chatInput.focus();
      } else {
        chatSection.style.display = 'none';
        criteriaSection.style.display = 'block';
      }
    });
  });
}

function initChatbox() {
  const chatForm = document.getElementById('chatForm');
  const chatInput = document.getElementById('chatInput');
  const chatMessages = document.getElementById('chatMessages');
  const quickBtns = document.querySelectorAll('.chat-quick-btn');

  if (!chatForm || !chatInput || !chatMessages) return;

  function appendMessage(sender, text) {
    const bubble = document.createElement('div');
    bubble.className = `chat-bubble ${sender}`;
    bubble.textContent = text;
    chatMessages.appendChild(bubble);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return bubble;
  }

  function handleSend(userText) {
    if (!userText.trim()) return;
    appendMessage('user', userText);
    chatInput.value = '';

    // Réponse de l'assistant (naturelle, directe et football)
    setTimeout(() => {
      const lower = userText.toLowerCase();
      let reply = "Je regarde dans la base de données. ";

      if (lower.includes("buteur") || lower.includes("st") || lower.includes("attaquant") || lower.includes("bu")) {
        reply += "En pointe, regarde Victor Osimhen ou Viktor Gyökeres : grosse vitesse, physique solide et finition efficace pour un prix raisonnable.";
      } else if (lower.includes("milieu") || lower.includes("cm") || lower.includes("mdc") || lower.includes("valverde") || lower.includes("bellingham")) {
        reply += "Si tu cherches un milieu infatigable avec du volume de jeu, regarde Manuel Ugarte ou Douglas Luiz qui ont un profil très proche pour bien moins cher.";
      } else if (lower.includes("défenseur") || lower.includes("dc") || lower.includes("cb") || lower.includes("saliba")) {
        reply += "En défense centrale, William Saliba ou Bremer sont excellents dans les duels et ont de très bons tacles debout.";
      } else if (lower.includes("ailier") || lower.includes("lw") || lower.includes("rw") || lower.includes("ag") || lower.includes("ad")) {
        reply += "Sur les côtés, Nico Williams et Moussa Diaby apportent une accélération immédiate sur les premiers mètres.";
      } else {
        reply += "Voici les profils correspondants avec un bon équilibre entre note, vitesse et valeur sur le marché.";
      }

      appendMessage('bot', reply);
    }, 400);
  }

  chatForm.addEventListener('submit', (e) => {
    e.preventDefault();
    handleSend(chatInput.value);
  });

  quickBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const text = btn.getAttribute('data-query') || btn.textContent.trim();
      handleSend(text);
    });
  });
}

