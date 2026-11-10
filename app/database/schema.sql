
PRAGMA foreign_keys = ON;

-- Pays et nationalités
CREATE TABLE IF NOT EXISTS countries (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

-- Championnats
CREATE TABLE IF NOT EXISTS leagues (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

-- Clubs
CREATE TABLE IF NOT EXISTS clubs (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL COLLATE NOCASE,
    league_id INTEGER REFERENCES leagues(id)
        ON DELETE SET NULL
);

CREATE UNIQUE INDEX IF NOT EXISTS ux_clubs_name_league
ON clubs(name, COALESCE(league_id, -1));

-- Identité des joueurs EA FC
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY,
    sofifa_id INTEGER NOT NULL UNIQUE,
    name TEXT NOT NULL,
    full_name TEXT,
    birth_date TEXT,
    country_id INTEGER REFERENCES countries(id)
);

-- Versions du jeu
CREATE TABLE IF NOT EXISTS game_editions (
    id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE
);

-- Fiche d'un joueur dans une édition
CREATE TABLE IF NOT EXISTS player_editions (
    id INTEGER PRIMARY KEY,
    player_id INTEGER NOT NULL
        REFERENCES players(id) ON DELETE CASCADE,
    edition_id INTEGER NOT NULL
        REFERENCES game_editions(id) ON DELETE CASCADE,
    club_id INTEGER REFERENCES clubs(id),
    overall INTEGER CHECK (overall BETWEEN 0 AND 99),
    potential INTEGER CHECK (potential BETWEEN 0 AND 99),
    age INTEGER,
    preferred_foot TEXT,
    height_cm INTEGER,
    weight_kg INTEGER,
    skill_moves INTEGER,
    weak_foot INTEGER,
    source_json TEXT NOT NULL,
    UNIQUE(player_id, edition_id)
);

-- Postes possibles
CREATE TABLE IF NOT EXISTS positions (
    code TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS player_positions (
    player_edition_id INTEGER NOT NULL
        REFERENCES player_editions(id) ON DELETE CASCADE,
    position_code TEXT NOT NULL REFERENCES positions(code),
    is_primary INTEGER NOT NULL DEFAULT 0
        CHECK (is_primary IN (0, 1)),
    PRIMARY KEY(player_edition_id, position_code)
);

-- Statistiques du jeu
CREATE TABLE IF NOT EXISTS player_stats (
    player_edition_id INTEGER PRIMARY KEY
        REFERENCES player_editions(id) ON DELETE CASCADE,

    pace INTEGER,
    shooting INTEGER,
    passing INTEGER,
    dribbling INTEGER,
    defending INTEGER,
    physicality INTEGER,

    attacking_finishing INTEGER,
    attacking_crossing INTEGER,
    attacking_short_passing INTEGER,

    skill_ball_control INTEGER,
    skill_dribbling INTEGER,

    movement_acceleration INTEGER,
    movement_sprint_speed INTEGER,
    movement_agility INTEGER,

    power_stamina INTEGER,
    power_strength INTEGER,

    mentality_vision INTEGER,
    mentality_composure INTEGER,

    defending_standing_tackle INTEGER,
    defending_sliding_tackle INTEGER,

    goalkeeping_diving INTEGER,
    goalkeeping_handling INTEGER,
    goalkeeping_kicking INTEGER,
    goalkeeping_positioning INTEGER,
    goalkeeping_reflexes INTEGER
);

-- PlayStyles
CREATE TABLE IF NOT EXISTS playstyles (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE
);

CREATE TABLE IF NOT EXISTS player_playstyles (
    player_edition_id INTEGER NOT NULL
        REFERENCES player_editions(id) ON DELETE CASCADE,
    playstyle_id INTEGER NOT NULL
        REFERENCES playstyles(id),
    is_plus INTEGER NOT NULL CHECK (is_plus IN (0, 1)),
    PRIMARY KEY(player_edition_id, playstyle_id)
);

-- Joueurs provenant de Transfermarkt
CREATE TABLE IF NOT EXISTS tm_players (
    tm_player_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    birth_date TEXT,
    club_name TEXT,
    nationality TEXT,
    current_market_value_eur INTEGER
        CHECK (current_market_value_eur >= 0)
);

-- Historique des valeurs marchandes
CREATE TABLE IF NOT EXISTS market_values (
    tm_player_id INTEGER NOT NULL
        REFERENCES tm_players(tm_player_id) ON DELETE CASCADE,
    valuation_date TEXT NOT NULL,
    value_eur INTEGER NOT NULL CHECK (value_eur >= 0),
    PRIMARY KEY(tm_player_id, valuation_date)
);

-- Correspondances EA FC / Transfermarkt
CREATE TABLE IF NOT EXISTS player_links (
    player_id INTEGER PRIMARY KEY
        REFERENCES players(id) ON DELETE CASCADE,
    tm_player_id INTEGER NOT NULL UNIQUE
        REFERENCES tm_players(tm_player_id) ON DELETE CASCADE,
    method TEXT NOT NULL
        CHECK (method IN ('auto_exact', 'manual'))
);

-- Index pour accélérer les recherches
CREATE INDEX IF NOT EXISTS ix_player_editions_overall
ON player_editions(overall);

CREATE INDEX IF NOT EXISTS ix_market_values_recent
ON market_values(tm_player_id, valuation_date DESC);

CREATE INDEX IF NOT EXISTS ix_players_birth
ON players(birth_date);

CREATE INDEX IF NOT EXISTS ix_tm_players_birth
ON tm_players(birth_date);


-- Vue destinée aux futurs algorithmes

DROP VIEW IF EXISTS v_recommendations;

CREATE VIEW v_recommendations AS
SELECT
    p.sofifa_id,
    p.name,
    p.birth_date,
    co.name AS nationality,
    ge.code AS edition,
    c.name AS club,
    pe.overall,
    pe.potential,
    pe.age,

    (
        SELECT pp.position_code
        FROM player_positions pp
        WHERE pp.player_edition_id = pe.id
        ORDER BY pp.is_primary DESC, pp.position_code
        LIMIT 1
    ) AS position,

    s.pace,
    s.shooting,
    s.passing,
    s.dribbling,
    s.defending,
    s.physicality,

    COALESCE(
        mv.value_eur,
        tm.current_market_value_eur
    ) AS market_value_eur,

    mv.valuation_date AS market_value_date

FROM player_editions pe

JOIN players p
    ON p.id = pe.player_id

JOIN game_editions ge
    ON ge.id = pe.edition_id

LEFT JOIN countries co
    ON co.id = p.country_id

LEFT JOIN clubs c
    ON c.id = pe.club_id

LEFT JOIN player_stats s
    ON s.player_edition_id = pe.id

LEFT JOIN player_links l
    ON l.player_id = p.id

LEFT JOIN tm_players tm
    ON tm.tm_player_id = l.tm_player_id

LEFT JOIN market_values mv
    ON mv.tm_player_id = tm.tm_player_id
    AND mv.valuation_date = (
        SELECT MAX(v2.valuation_date)
        FROM market_values v2
        WHERE v2.tm_player_id = tm.tm_player_id
    );
