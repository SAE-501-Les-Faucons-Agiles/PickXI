/**
 * PickXI - Script Principal & Moteur d'Interactions
 * Direction Artistique & Expérience Utilisateur
 * Gestion du Terrain Tactique, Comparateur, Radar SVG et Modales
 */

document.addEventListener('DOMContentLoaded', () => {
  initHeroPrompts();
  initTacticalPitch();
  initCompareManager();
  initCompareSearch();
  initModalQuickView();
  initRangeSliders();
  initCriteriaSearchModule();
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
   3.B SYSTÈME DE RECHERCHE & REMPLACEMENT RAPIDE SUR LA PAGE COMPARE
   ========================================================================== */
const COMPARE_PLAYERS_DB = [
  {
    sofifa_id: 252371,
    name: "J. Bellingham",
    overall: 90,
    position: "CAM",
    club: "Real Madrid",
    nationality: "Angleterre",
    league: "La Liga",
    pace: 80,
    shooting: 86,
    passing: 83,
    dribbling: 90,
    defending: 78,
    physicality: 85,
    market_value_eur: 174500000,
    face_url: "https://cdn.sofifa.net/players/252/371/26_120.png",
    playstyle: "Relentless +"
  },
  {
    sofifa_id: 239053,
    name: "F. Valverde",
    overall: 89,
    position: "CM",
    club: "Real Madrid",
    nationality: "Uruguay",
    league: "La Liga",
    pace: 88,
    shooting: 84,
    passing: 84,
    dribbling: 84,
    defending: 83,
    physicality: 85,
    market_value_eur: 120500000,
    face_url: "https://cdn.sofifa.net/players/239/053/26_120.png",
    playstyle: "Rapid +"
  },
  {
    sofifa_id: 231747,
    name: "K. Mbappé",
    overall: 91,
    position: "ST",
    club: "Real Madrid",
    nationality: "France",
    league: "La Liga",
    pace: 97,
    shooting: 90,
    passing: 81,
    dribbling: 92,
    defending: 37,
    physicality: 76,
    market_value_eur: 173500000,
    face_url: "https://cdn.sofifa.net/players/231/747/26_120.png",
    playstyle: "Quick Step +"
  },
  {
    sofifa_id: 239085,
    name: "E. Haaland",
    overall: 90,
    position: "ST",
    club: "Manchester City",
    nationality: "Norvège",
    league: "Premier League",
    pace: 86,
    shooting: 91,
    passing: 70,
    dribbling: 80,
    defending: 45,
    physicality: 88,
    market_value_eur: 157000000,
    face_url: "https://cdn.sofifa.net/players/239/085/26_120.png",
    playstyle: "Low Driven Shot +"
  },
  {
    sofifa_id: 235212,
    name: "A. Hakimi",
    overall: 89,
    position: "RB",
    club: "Paris Saint-Germain",
    nationality: "Maroc",
    league: "Ligue 1",
    pace: 92,
    shooting: 79,
    passing: 82,
    dribbling: 83,
    defending: 82,
    physicality: 79,
    market_value_eur: 111000000,
    face_url: "https://cdn.sofifa.net/players/235/212/26_120.png",
    playstyle: "Quick Step +"
  },
  {
    sofifa_id: 231866,
    name: "Rodri",
    overall: 90,
    position: "CDM",
    club: "Manchester City",
    nationality: "Espagne",
    league: "Premier League",
    pace: 65,
    shooting: 80,
    passing: 86,
    dribbling: 84,
    defending: 86,
    physicality: 85,
    market_value_eur: 102000000,
    face_url: "https://cdn.sofifa.net/players/231/866/26_120.png",
    playstyle: "Power Shot +"
  },
  {
    sofifa_id: 243715,
    name: "W. Saliba",
    overall: 87,
    position: "CB",
    club: "Arsenal",
    nationality: "France",
    league: "Premier League",
    pace: 77,
    shooting: 39,
    passing: 68,
    dribbling: 72,
    defending: 87,
    physicality: 83,
    market_value_eur: 92000000,
    face_url: "https://cdn.sofifa.net/players/243/715/26_120.png",
    playstyle: "Anticipate +"
  },
  {
    sofifa_id: 209331,
    name: "M. Salah",
    overall: 91,
    position: "RW",
    club: "Liverpool",
    nationality: "Égypte",
    league: "Premier League",
    pace: 89,
    shooting: 88,
    passing: 86,
    dribbling: 90,
    defending: 45,
    physicality: 76,
    market_value_eur: 82000000,
    face_url: "https://cdn.sofifa.net/players/209/331/26_120.png",
    playstyle: "Finesse Shot +"
  },
  {
    sofifa_id: 277643,
    name: "Lamine Yamal",
    overall: 89,
    position: "RW",
    club: "FC Barcelona",
    nationality: "Espagne",
    league: "La Liga",
    pace: 85,
    shooting: 81,
    passing: 86,
    dribbling: 90,
    defending: 23,
    physicality: 53,
    market_value_eur: 147000000,
    face_url: "https://cdn.sofifa.net/players/277/643/26_120.png",
    playstyle: "Technical +"
  },
  {
    sofifa_id: 246669,
    name: "B. Saka",
    overall: 88,
    position: "RW",
    club: "Arsenal",
    nationality: "Angleterre",
    league: "Premier League",
    pace: 84,
    shooting: 82,
    passing: 85,
    dribbling: 88,
    defending: 60,
    physicality: 73,
    market_value_eur: 118500000,
    face_url: "https://cdn.sofifa.net/players/246/669/26_120.png",
    playstyle: "Whipped Pass +"
  },
  {
    sofifa_id: 256790,
    name: "J. Musiala",
    overall: 88,
    position: "CAM",
    club: "FC Bayern München",
    nationality: "Allemagne",
    league: "Bundesliga",
    pace: 80,
    shooting: 82,
    passing: 80,
    dribbling: 90,
    defending: 64,
    physicality: 65,
    market_value_eur: 133500000,
    face_url: "https://cdn.sofifa.net/players/256/790/26_120.png",
    playstyle: "Technical +"
  },
  {
    sofifa_id: 256630,
    name: "F. Wirtz",
    overall: 89,
    position: "CAM",
    club: "Liverpool",
    nationality: "Allemagne",
    league: "Premier League",
    pace: 80,
    shooting: 82,
    passing: 88,
    dribbling: 90,
    defending: 54,
    physicality: 67,
    market_value_eur: 150500000,
    face_url: "https://cdn.sofifa.net/players/256/630/26_120.png",
    playstyle: "Incisive Pass +"
  },
  {
    sofifa_id: 203376,
    name: "V. van Dijk",
    overall: 90,
    position: "CB",
    club: "Liverpool",
    nationality: "Pays-Bas",
    league: "Premier League",
    pace: 73,
    shooting: 60,
    passing: 72,
    dribbling: 72,
    defending: 90,
    physicality: 87,
    market_value_eur: 57000000,
    face_url: "https://cdn.sofifa.net/players/203/376/26_120.png",
    playstyle: "Intercept +"
  },
  {
    sofifa_id: 232293,
    name: "V. Osimhen",
    overall: 87,
    position: "ST",
    club: "Galatasaray SK",
    nationality: "Nigéria",
    league: "Süper Lig",
    pace: 92,
    shooting: 84,
    passing: 65,
    dribbling: 81,
    defending: 42,
    physicality: 84,
    market_value_eur: 100000000,
    face_url: "https://cdn.sofifa.net/players/232/293/26_120.png",
    playstyle: "Chip Shot"
  },
  {
    sofifa_id: 232656,
    name: "T. Hernández",
    overall: 84,
    position: "LB",
    club: "Al Hilal",
    nationality: "France",
    league: "Pro League",
    pace: 90,
    shooting: 76,
    passing: 78,
    dribbling: 83,
    defending: 79,
    physicality: 83,
    market_value_eur: 44500000,
    face_url: "https://cdn.sofifa.net/players/232/656/26_120.png",
    playstyle: "Rapid"
  },
  {
    sofifa_id: 234396,
    name: "A. Davies",
    overall: 84,
    position: "LB",
    club: "FC Bayern München",
    nationality: "Canada",
    league: "Bundesliga",
    pace: 94,
    shooting: 66,
    passing: 78,
    dribbling: 85,
    defending: 74,
    physicality: 76,
    market_value_eur: 53500000,
    face_url: "https://cdn.sofifa.net/players/234/396/26_120.png",
    playstyle: "Rapid"
  },
  {
    sofifa_id: 194765,
    name: "A. Griezmann",
    overall: 85,
    position: "ST",
    club: "Atlético Madrid",
    nationality: "France",
    league: "La Liga",
    pace: 77,
    shooting: 86,
    passing: 85,
    dribbling: 88,
    defending: 59,
    physicality: 73,
    market_value_eur: 26000000,
    face_url: "https://cdn.sofifa.net/players/194/765/26_120.png",
    playstyle: "Chip Shot +"
  },
  {
    sofifa_id: 192985,
    name: "K. De Bruyne",
    overall: 87,
    position: "CM",
    club: "Napoli",
    nationality: "Belgique",
    league: "Serie A",
    pace: 66,
    shooting: 83,
    passing: 92,
    dribbling: 84,
    defending: 65,
    physicality: 72,
    market_value_eur: 36500000,
    face_url: "https://cdn.sofifa.net/players/192/985/26_120.png",
    playstyle: "Whipped Pass +"
  },
  {
    sofifa_id: 212831,
    name: "Alisson",
    overall: 89,
    position: "GK",
    club: "Liverpool",
    nationality: "Brésil",
    league: "Premier League",
    pace: 80,
    shooting: 70,
    passing: 70,
    dribbling: 70,
    defending: 70,
    physicality: 70,
    market_value_eur: 51000000,
    face_url: "https://cdn.sofifa.net/players/212/831/26_120.png",
    playstyle: "Rush Out +"
  }
];

let currentCompareP1 = null;
let currentCompareP2 = null;
let activeCompareSlot = 1;

function initCompareSearch() {
  const modal = document.getElementById('compareSearchModal');
  if (!modal) return; // Pas sur la page compare

  const searchInput = document.getElementById('compareSearchInput');
  const resultsContainer = document.getElementById('compareResultsList');
  const countSpan = document.getElementById('compareResultsCount');
  const closeBtn = document.getElementById('compareModalCloseBtn');
  const badge = document.getElementById('compareModalSlotBadge');
  const filterChips = document.querySelectorAll('.compare-filter-chip');

  // Initialisation des joueurs actuels depuis les paramètres d'URL ou défaut
  const params = new URLSearchParams(window.location.search);
  const p1Id = Number(params.get('p1')) || 252371;
  const p2Id = Number(params.get('p2')) || 239053;

  currentCompareP1 = COMPARE_PLAYERS_DB.find(p => p.sofifa_id === p1Id) || COMPARE_PLAYERS_DB[0];
  currentCompareP2 = COMPARE_PLAYERS_DB.find(p => p.sofifa_id === p2Id) || COMPARE_PLAYERS_DB[1];

  let currentPosFilter = 'ALL';
  let currentMinOvrFilter = null;

  function openModal(slot) {
    activeCompareSlot = Number(slot);
    if (badge) {
      badge.textContent = `Joueur ${activeCompareSlot}`;
      badge.className = `compare-search-slot-badge slot-${activeCompareSlot}`;
    }
    modal.classList.add('open');
    if (searchInput) {
      searchInput.value = '';
      setTimeout(() => searchInput.focus(), 120);
    }
    currentPosFilter = 'ALL';
    currentMinOvrFilter = null;
    filterChips.forEach(c => c.classList.remove('active'));
    const defaultChip = document.querySelector('.compare-filter-chip[data-pos="ALL"]');
    if (defaultChip) defaultChip.classList.add('active');

    renderSearchResults();
  }

  function closeModal() {
    modal.classList.remove('open');
  }

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal) closeModal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('open')) closeModal();
  });

  // Déclencheurs pour ouvrir la recherche (barre supérieure & boutons sous les cartes)
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('.btn-open-search') || e.target.closest('.btn-open-player-search');
    if (trigger) {
      e.preventDefault();
      const slot = trigger.getAttribute('data-slot') || 1;
      openModal(slot);
    }
  });

  // Filtres par puce (Attaquants, Milieux, Défenseurs, Gardiens, Top Note)
  filterChips.forEach(chip => {
    chip.addEventListener('click', () => {
      filterChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      currentPosFilter = chip.getAttribute('data-pos') || 'ALL';
      currentMinOvrFilter = chip.getAttribute('data-min-ovr') ? Number(chip.getAttribute('data-min-ovr')) : null;
      renderSearchResults();
    });
  });

  if (searchInput) {
    searchInput.addEventListener('input', () => {
      renderSearchResults();
    });
  }

  // Inversion des deux joueurs (Swap)
  const btnSwap = document.getElementById('btnSwapPlayers');
  const btnSwapRadar = document.getElementById('btnSwapRadar');
  function handleSwap() {
    const temp = currentCompareP1;
    currentCompareP1 = currentCompareP2;
    currentCompareP2 = temp;
    updateComparisonUI(currentCompareP1, currentCompareP2);
  }
  if (btnSwap) btnSwap.addEventListener('click', handleSwap);
  if (btnSwapRadar) btnSwapRadar.addEventListener('click', handleSwap);

  function matchesCategory(pos, cat) {
    if (cat === 'ALL') return true;
    if (cat === 'ATT') return ['ST', 'CF', 'RW', 'LW', 'RM', 'LM'].includes(pos);
    if (cat === 'MID') return ['CAM', 'CM', 'CDM', 'RM', 'LM'].includes(pos);
    if (cat === 'DEF') return ['CB', 'LB', 'RB', 'LWB', 'RWB'].includes(pos);
    if (cat === 'GK') return pos === 'GK';
    return true;
  }

  function renderSearchResults() {
    if (!resultsContainer) return;
    const query = searchInput ? searchInput.value.trim().toLowerCase() : '';

    /**
     * =========================================================================
     * POINT DE CONNEXION AVEC LA BASE DE DONNÉES SQLite (BACKEND) :
     * Lorsque tu voudras brancher directement ta base de données, tu pourras appeler :
     * 
     * fetch(`/api/players/search?q=${encodeURIComponent(query)}&pos=${currentPosFilter}`)
     *   .then(res => res.json())
     *   .then(data => { ... });
     * =========================================================================
     */

    const filtered = COMPARE_PLAYERS_DB.filter(p => {
      // Éviter de sélectionner le même joueur que dans l'autre slot
      const otherSlotPlayer = activeCompareSlot === 1 ? currentCompareP2 : currentCompareP1;
      if (otherSlotPlayer && otherSlotPlayer.sofifa_id === p.sofifa_id) return false;

      // Filtre texte
      if (query) {
        const matchName = p.name.toLowerCase().includes(query);
        const matchClub = p.club.toLowerCase().includes(query);
        const matchNation = p.nationality.toLowerCase().includes(query);
        const matchPos = p.position.toLowerCase().includes(query);
        if (!matchName && !matchClub && !matchNation && !matchPos) return false;
      }

      // Filtre poste
      if (!matchesCategory(p.position, currentPosFilter)) return false;

      // Filtre note min
      if (currentMinOvrFilter && p.overall < currentMinOvrFilter) return false;

      return true;
    });

    if (countSpan) {
      countSpan.textContent = `${filtered.length} joueur${filtered.length > 1 ? 's' : ''} disponible${filtered.length > 1 ? 's' : ''}`;
    }

    if (filtered.length === 0) {
      resultsContainer.innerHTML = `
        <div style="padding: 30px; text-align: center; color: var(--text-muted);">
          <div style="font-size: 1.1rem; margin-bottom: 6px; color: var(--text-secondary);">Aucun joueur trouvé</div>
          <p style="font-size: 0.85rem;">Essaie avec un autre nom, un club ou réinitialise les filtres de poste.</p>
        </div>
      `;
      return;
    }

    resultsContainer.innerHTML = filtered.map(p => {
      const priceFormatted = p.market_value_eur >= 1000000 
        ? (p.market_value_eur / 1000000).toFixed(1) + 'M €'
        : (p.market_value_eur > 0 ? Math.round(p.market_value_eur / 1000) + 'k €' : 'Éco');

      return `
        <div class="compare-result-card" data-player-id="${p.sofifa_id}">
          <div class="compare-result-avatar">
            <img src="${p.face_url}" alt="${p.name}" onerror="this.src='/static/img/logo.png'">
          </div>
          <div class="compare-result-info">
            <div class="compare-result-top">
              <span class="compare-result-name">${p.name}</span>
              <span class="compare-result-ovr">${p.overall}</span>
              <span class="compare-result-pos">${p.position}</span>
            </div>
            <div class="compare-result-sub">
              <span>${p.club}</span> • <span>${p.nationality}</span> • <span style="color: var(--accent-mint);">${p.playstyle || 'Méta'}</span>
            </div>
            <div class="compare-result-stats-row">
              <span>PAC <strong>${p.pace}</strong></span>
              <span>SHO <strong>${p.shooting}</strong></span>
              <span>PAS <strong>${p.passing}</strong></span>
              <span>DRI <strong>${p.dribbling}</strong></span>
              <span>DEF <strong>${p.defending}</strong></span>
              <span>PHY <strong>${p.physicality}</strong></span>
            </div>
          </div>
          <div class="compare-result-action">
            <span class="compare-result-price">${priceFormatted}</span>
            <button type="button" class="compare-result-btn">
              Choisir
            </button>
          </div>
        </div>
      `;
    }).join('');

    // Sélection d'un joueur
    resultsContainer.querySelectorAll('.compare-result-card').forEach(card => {
      card.addEventListener('click', () => {
        const id = Number(card.getAttribute('data-player-id'));
        const player = COMPARE_PLAYERS_DB.find(p => p.sofifa_id === id);
        if (player) {
          if (activeCompareSlot === 1) {
            currentCompareP1 = player;
          } else {
            currentCompareP2 = player;
          }
          updateComparisonUI(currentCompareP1, currentCompareP2);
          closeModal();
        }
      });
    });
  }
}

function updateComparisonUI(p1, p2) {
  if (!p1 || !p2) return;

  // 1. Mise à jour de la top barre
  const av1 = document.getElementById('topBarAvatar1');
  const name1 = document.getElementById('topBarName1');
  const ovr1 = document.getElementById('topBarOvr1');
  const club1 = document.getElementById('topBarClub1');

  if (av1) av1.src = p1.face_url;
  if (name1) name1.textContent = p1.name;
  if (ovr1) ovr1.textContent = `${p1.overall} ${p1.position}`;
  if (club1) club1.textContent = p1.club;

  const av2 = document.getElementById('topBarAvatar2');
  const name2 = document.getElementById('topBarName2');
  const ovr2 = document.getElementById('topBarOvr2');
  const club2 = document.getElementById('topBarClub2');

  if (av2) av2.src = p2.face_url;
  if (name2) name2.textContent = p2.name;
  if (ovr2) ovr2.textContent = `${p2.overall} ${p2.position}`;
  if (club2) club2.textContent = p2.club;

  // 2. Mise à jour des cartes FUT
  const slot1Card = document.getElementById('slot1CardContainer');
  const slot2Card = document.getElementById('slot2CardContainer');
  if (slot1Card) slot1Card.innerHTML = renderFutCardHtml(p1);
  if (slot2Card) slot2Card.innerHTML = renderFutCardHtml(p2);

  // 3. Mise à jour du radar SVG
  const radarContainer = document.getElementById('compareRadarContainer');
  if (radarContainer) {
    const s1 = [p1.pace, p1.shooting, p1.passing, p1.dribbling, p1.defending, p1.physicality];
    const s2 = [p2.pace, p2.shooting, p2.passing, p2.dribbling, p2.defending, p2.physicality];
    radarContainer.setAttribute('data-stats-1', JSON.stringify(s1));
    radarContainer.setAttribute('data-stats-2', JSON.stringify(s2));
    renderRadarSvg(radarContainer, s1, s2);
  }

  // 4. Légende sous le radar
  const legName1 = document.getElementById('legendName1');
  const legOvr1 = document.getElementById('legendOvr1');
  const legName2 = document.getElementById('legendName2');
  const legOvr2 = document.getElementById('legendOvr2');

  if (legName1) legName1.textContent = p1.name;
  if (legOvr1) legOvr1.textContent = p1.overall;
  if (legName2) legName2.textContent = p2.name;
  if (legOvr2) legOvr2.textContent = p2.overall;

  // 5. Tableau des 6 attributs
  const statsMapping = [
    { key: 'pace', label: 'Vitesse (PAC)', val1: p1.pace, val2: p2.pace },
    { key: 'shooting', label: 'Tir (SHO)', val1: p1.shooting, val2: p2.shooting },
    { key: 'passing', label: 'Passe (PAS)', val1: p1.passing, val2: p2.passing },
    { key: 'dribbling', label: 'Dribble (DRI)', val1: p1.dribbling, val2: p2.dribbling },
    { key: 'defending', label: 'Défense (DEF)', val1: p1.defending, val2: p2.defending },
    { key: 'physicality', label: 'Physique (PHY)', val1: p1.physicality, val2: p2.physicality }
  ];

  statsMapping.forEach(stat => {
    const row = document.querySelector(`.stat-compare-row[data-stat-key="${stat.key}"]`);
    if (!row) return;

    const diff = stat.val1 - stat.val2;

    const val1El = row.querySelector('.stat-val-1');
    const bar1El = row.querySelector('.stat-bar-1');
    const val2El = row.querySelector('.stat-val-2');
    const bar2El = row.querySelector('.stat-bar-2');

    if (val1El) {
      val1El.innerHTML = `${stat.val1}${diff > 0 ? ` <span style="font-size: 0.75rem; color: var(--accent-mint);">(+${diff})</span>` : ''}`;
      val1El.style.color = diff > 0 ? 'var(--accent-mint)' : 'var(--text-main)';
    }

    if (bar1El) {
      bar1El.style.width = `${stat.val1}%`;
      bar1El.style.background = diff > 0 ? 'var(--accent-mint)' : 'var(--accent-pitch)';
    }

    if (val2El) {
      val2El.innerHTML = `${stat.val2}${diff < 0 ? ` <span style="font-size: 0.75rem; color: var(--accent-gold);">(+${-diff})</span>` : ''}`;
      val2El.style.color = diff < 0 ? 'var(--accent-gold)' : 'var(--text-main)';
    }

    if (bar2El) {
      bar2El.style.width = `${stat.val2}%`;
      bar2El.style.background = diff < 0 ? 'var(--accent-gold)' : 'rgba(229, 184, 66, 0.5)';
    }
  });

  // 6. Synthèse textuelle dynamique
  const summaryEl = document.getElementById('compareSummaryText');
  if (summaryEl) {
    if (p1.pace > p2.pace + 3) {
      summaryEl.innerHTML = `<strong>${p1.name}</strong> possède un avantage net en accélération et vitesse de pointe (+${p1.pace - p2.pace} PAC) pour percer les lignes ou conclure en transition rapide.`;
    } else if (p2.pace > p1.pace + 3) {
      summaryEl.innerHTML = `<strong>${p2.name}</strong> domine largement sur le plan athlétique et la vitesse pure (+${p2.pace - p1.pace} PAC), idéal pour les contre-attaques verticales.`;
    } else if (p1.defending > p2.defending + 4) {
      summaryEl.innerHTML = `<strong>${p1.name}</strong> apporte une assise défensive bien supérieure (+${p1.defending - p2.defending} DEF) et une meilleure récupération dans les duels.`;
    } else if (p2.defending > p1.defending + 4) {
      summaryEl.innerHTML = `<strong>${p2.name}</strong> surclasse son adversaire sur les phases de repli et de pressing (+${p2.defending - p1.defending} DEF).`;
    } else if (p1.shooting > p2.shooting + 3) {
      summaryEl.innerHTML = `<strong>${p1.name}</strong> est un finisseur bien plus redoutable (+${p1.shooting - p2.shooting} SHO) aux abords de la surface adverse.`;
    } else if (p2.shooting > p1.shooting + 3) {
      summaryEl.innerHTML = `<strong>${p2.name}</strong> a un avantage décisif au tir (+${p2.shooting - p1.shooting} SHO) pour déclencher de loin ou tromper le gardien.`;
    } else {
      summaryEl.innerHTML = `Duel équilibré entre <strong>${p1.name}</strong> (${p1.overall}) et <strong>${p2.name}</strong> (${p2.overall}). Leurs PlayStyles (${p1.playstyle || 'Méta'} vs ${p2.playstyle || 'Méta'}) et votre dispositif tactique feront la différence.`;
    }
  }

  // 7. Synchronisation de l'URL navigateur sans rechargement
  const newUrl = `${window.location.pathname}?p1=${p1.sofifa_id}&p2=${p2.sofifa_id}`;
  window.history.replaceState({ p1: p1.sofifa_id, p2: p2.sofifa_id }, '', newUrl);
}

function renderFutCardHtml(player) {
  const isMeta = player.overall >= 88 ? 'card-meta' : '';
  const paceClass = player.pace >= 90 ? 'elite' : (player.pace >= 85 ? 'high' : '');
  const driClass = player.dribbling >= 90 ? 'elite' : (player.dribbling >= 85 ? 'high' : '');
  const shoClass = player.shooting >= 90 ? 'elite' : (player.shooting >= 85 ? 'high' : '');
  const defClass = player.defending >= 90 ? 'elite' : (player.defending >= 85 ? 'high' : '');
  const pasClass = player.passing >= 90 ? 'elite' : (player.passing >= 85 ? 'high' : '');
  const phyClass = player.physicality >= 90 ? 'elite' : (player.physicality >= 85 ? 'high' : '');

  const nationCode = (player.nationality || 'ENG').substring(0, 3).toUpperCase();
  const priceFormatted = player.market_value_eur >= 1000000 
    ? (player.market_value_eur / 1000000).toFixed(1) + 'M €'
    : (player.market_value_eur > 0 ? Math.round(player.market_value_eur / 1000) + 'k €' : 'Éco');

  const playstyleName = typeof player.playstyle === 'string' 
    ? player.playstyle 
    : (player.playstyles && player.playstyles[0] ? (player.playstyles[0].name || player.playstyles[0]) : 'Méta');

  return `
    <div class="fut-card ${isMeta}" data-player-id="${player.sofifa_id}">
      <div class="fut-card-header">
        <div class="fut-card-badge">
          <div class="fut-rating">${player.overall}</div>
          <div class="fut-position">${player.position}</div>
          <div class="fut-meta-icons">
            <span class="fut-nation-flag" title="${player.nationality}">${nationCode}</span>
            <span class="fut-club-pill" title="${player.club}">${player.club}</span>
          </div>
        </div>
        <div class="fut-player-visual">
          <img src="${player.face_url}" alt="${player.name}" loading="lazy" onerror="this.src='/static/img/logo.png'">
        </div>
      </div>
      <div class="fut-player-name" title="${player.name}">${player.name}</div>
      <div class="fut-stats-grid">
        <div class="fut-stat-item"><span class="fut-stat-value ${paceClass}">${player.pace}</span><span class="fut-stat-label">PAC</span></div>
        <div class="fut-stat-item"><span class="fut-stat-value ${driClass}">${player.dribbling}</span><span class="fut-stat-label">DRI</span></div>
        <div class="fut-stat-item"><span class="fut-stat-value ${shoClass}">${player.shooting}</span><span class="fut-stat-label">SHO</span></div>
        <div class="fut-stat-item"><span class="fut-stat-value ${defClass}">${player.defending}</span><span class="fut-stat-label">DEF</span></div>
        <div class="fut-stat-item"><span class="fut-stat-value ${pasClass}">${player.passing}</span><span class="fut-stat-label">PAS</span></div>
        <div class="fut-stat-item"><span class="fut-stat-value ${phyClass}">${player.physicality}</span><span class="fut-stat-label">PHY</span></div>
      </div>
      <div class="fut-card-footer">
        <div class="fut-playstyle-badge" title="PlayStyle Méta">
          <span class="fut-playstyle-icon"></span>
          ${playstyleName}
        </div>
        <div class="fut-price-tag">${priceFormatted}</div>
      </div>
      <div class="fut-card-actions">
        <button type="button" class="fut-card-btn btn-quick-view" data-id="${player.sofifa_id}" title="Aperçu rapide">Fiche</button>
        <button type="button" class="fut-card-btn btn-action-compare" data-id="${player.sofifa_id}" data-name="${player.name}" data-img="${player.face_url}" title="Comparer ce joueur">Duel</button>
        <a href="/player/${player.sofifa_id}" class="fut-card-btn btn-accent" title="Dossier complet">Scout</a>
      </div>
    </div>
  `;
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
   5. SLIDERS PERSONNALISÉS (RETEX VISUEL EN DIRECT) & RECHERCHE CRITÈRES
   ========================================================================== */
function initRangeSliders() {
  document.querySelectorAll('.range-slider').forEach(slider => {
    const outputId = slider.getAttribute('data-target');
    const output = document.getElementById(outputId);
    const suffix = slider.getAttribute('data-suffix') || '';
    const prefix = slider.getAttribute('data-prefix') || '';
    const maxLabel = slider.getAttribute('data-max-label');
    const minLabel = slider.getAttribute('data-min-label');

    function updateDisplay() {
      if (!output) return;
      const val = Number(slider.value);
      const maxVal = Number(slider.max);
      const minVal = Number(slider.min);

      if (maxLabel && val >= maxVal) {
        output.textContent = maxLabel;
      } else if (minLabel && val <= minVal) {
        output.textContent = minLabel;
      } else {
        output.textContent = `${prefix}${slider.value}${suffix}`;
      }
    }

    if (output) {
      slider.addEventListener('input', () => {
        updateDisplay();
        syncQuickChips(slider);
        updateFilterLiveSummary();
      });
      updateDisplay();
    }
  });
}

function syncQuickChips(slider) {
  if (!slider || !slider.id) return;
  const chips = document.querySelectorAll(`.quick-chip-btn[data-slider="${slider.id}"]`);
  chips.forEach(chip => {
    const val = chip.getAttribute('data-value');
    const isGold = chip.classList.contains('active-gold') || chip.getAttribute('data-gold') === 'true';
    if (val !== null && Number(val) === Number(slider.value)) {
      chip.classList.add(isGold ? 'active-gold' : 'active');
    } else {
      chip.classList.remove('active', 'active-gold');
    }
  });
}

function initCriteriaSearchModule() {
  const form = document.getElementById('homeCriteriaForm');
  if (!form) return;

  // 1. Boutons rapides de sélection (Quick chips)
  document.querySelectorAll('.quick-chip-btn').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const sliderId = btn.getAttribute('data-slider');
      const val = btn.getAttribute('data-value');
      const slider = document.getElementById(sliderId);
      if (slider && val !== null) {
        slider.value = val;
        slider.dispatchEvent(new Event('input', { bubbles: true }));
      }
    });
  });

  // 2. Boutons d'étoiles / Gestes techniques & Mauvais pied
  document.querySelectorAll('.star-pill-input').forEach(radio => {
    radio.addEventListener('change', () => {
      const targetId = radio.getAttribute('data-display-target');
      const label = radio.getAttribute('data-label') || radio.value || 'Tous';
      const displayEl = document.getElementById(targetId);
      if (displayEl) {
        displayEl.textContent = label;
      }
      updateFilterLiveSummary();
    });
  });

  // 3. Dépliage des filtres avancés (Pied fort, Potentiel, Stats détaillées)
  const toggleBtn = document.getElementById('toggleAdvancedFiltersBtn');
  const panel = document.getElementById('advancedFiltersPanel');
  if (toggleBtn && panel) {
    toggleBtn.addEventListener('click', () => {
      const isOpen = panel.classList.toggle('open');
      toggleBtn.classList.toggle('expanded', isOpen);
      toggleBtn.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
      const textSpan = document.getElementById('advancedToggleText');
      if (textSpan) {
        textSpan.textContent = isOpen 
          ? "Masquer les critères avancés (Pied fort, Potentiel, PlayStyles, Stats)"
          : "Critères avancés (Pied fort, Potentiel, PlayStyles, Stats détaillées)";
      }
    });
  }

  // 4. Réinitialisation des critères
  const resetBtn = document.getElementById('resetCriteriaBtn');
  if (resetBtn) {
    resetBtn.addEventListener('click', (e) => {
      e.preventDefault();
      form.reset();

      // Mettre à jour tous les sliders et leurs affichages
      form.querySelectorAll('.range-slider').forEach(slider => {
        slider.dispatchEvent(new Event('input', { bubbles: true }));
      });

      // Mettre à jour les libellés des boutons radios étoilés
      form.querySelectorAll('.star-pill-input:checked').forEach(radio => {
        const targetId = radio.getAttribute('data-display-target');
        const label = radio.getAttribute('data-label') || 'Tous';
        const displayEl = document.getElementById(targetId);
        if (displayEl) displayEl.textContent = label;
      });

      updateFilterLiveSummary();
    });
  }

  // 5. Écoute sur tous les selects pour rafraîchir le résumé
  form.querySelectorAll('select').forEach(sel => {
    sel.addEventListener('change', updateFilterLiveSummary);
  });

  // Initialisation du résumé dès le chargement
  updateFilterLiveSummary();
}

function updateFilterLiveSummary() {
  const container = document.getElementById('liveFiltersChips');
  if (!container) return;

  const chips = [];

  // Poste
  const posSelect = document.getElementById('homePosSelect');
  if (posSelect && posSelect.value && posSelect.value !== 'ALL') {
    chips.push({ text: `Poste: ${posSelect.value}`, type: 'mint' });
  }

  // Budget max
  const budgetSlider = document.getElementById('homeBudgetSlider');
  if (budgetSlider) {
    const val = Number(budgetSlider.value);
    if (val < 150) {
      chips.push({ text: `Budget ≤ ${val} M€`, type: 'gold' });
    } else {
      chips.push({ text: 'Budget: Illimité', type: 'gold' });
    }
  }

  // Vitesse min
  const paceSlider = document.getElementById('homePaceSlider');
  if (paceSlider) {
    chips.push({ text: `Vitesse ≥ ${paceSlider.value} PAC`, type: 'mint' });
  }

  // Gestes techniques
  const skillRadio = document.querySelector('input[name="skill_moves"]:checked');
  if (skillRadio && skillRadio.value) {
    chips.push({ text: `${skillRadio.value}★+ Gestes`, type: 'gold' });
  }

  // Note min
  const ovrSlider = document.getElementById('homeOvrSlider');
  if (ovrSlider && Number(ovrSlider.value) > 70) {
    chips.push({ text: `Note ≥ ${ovrSlider.value}`, type: 'mint' });
  }

  // Mauvais pied
  const weakRadio = document.querySelector('input[name="weak_foot"]:checked');
  if (weakRadio && weakRadio.value) {
    chips.push({ text: `${weakRadio.value}★+ Pied faible`, type: 'mint' });
  }

  // Âge max
  const ageSlider = document.getElementById('homeAgeSlider');
  if (ageSlider && Number(ageSlider.value) < 38) {
    chips.push({ text: `Âge ≤ ${ageSlider.value} ans`, type: 'mint' });
  }

  // Championnat
  const leagueSelect = document.getElementById('homeLeagueSelect');
  if (leagueSelect && leagueSelect.value && leagueSelect.value !== 'ALL') {
    chips.push({ text: leagueSelect.value, type: 'mint' });
  }

  // Pied fort
  const footSelect = document.getElementById('homeFootSelect');
  if (footSelect && footSelect.value) {
    chips.push({ text: `Pied: ${footSelect.value === 'Right' ? 'Droit' : 'Gauche'}`, type: 'mint' });
  }

  // PlayStyle
  const playstyleSelect = document.getElementById('homePlaystyleSelect');
  if (playstyleSelect && playstyleSelect.value && playstyleSelect.value !== 'ALL') {
    chips.push({ text: `Style: ${playstyleSelect.value}`, type: 'mint' });
  }

  // Potentiel
  const potSlider = document.getElementById('homePotSlider');
  if (potSlider && Number(potSlider.value) > 75) {
    chips.push({ text: `Potentiel ≥ ${potSlider.value}`, type: 'mint' });
  }

  // Rendu des puces
  if (chips.length === 0) {
    container.innerHTML = `<span style="color: var(--text-muted); font-size: 0.78rem;">Tous les joueurs de la base de données</span>`;
  } else {
    container.innerHTML = chips.map(c => `
      <span class="live-chip-tag ${c.type === 'gold' ? 'gold' : ''}">
        ${c.text}
      </span>
    `).join('');
  }
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

