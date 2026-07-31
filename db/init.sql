CREATE TABLE stations (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE topics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE measurements (
    station_id INTEGER NOT NULL REFERENCES stations(id),
    topic_id INTEGER NOT NULL REFERENCES topics(id),
    timestamp TIMESTAMPTZ NOT NULL,
    value DOUBLE PRECISION NOT NULL,

    PRIMARY KEY (station_id, topic_id, timestamp)
);

INSERT INTO stations (id, name) VALUES
(101794, 'Oulu Vihreäsaari satama'),
(101786, 'Oulu lentoasema'),
(134248, 'Oulu Toppila'),
(103807, 'Oulu Santapankki'),
(12001, 'vt4_Oulu_Ouluntulli'),
(12017, 'vt8_Liminka_Lapinkangas'),
(12022, 'vt4_Liminka_Haaransilta'),
(12033, 'vt22_Muhos_Kosulankylä'),
(12053, 'Liminka-Tupos');

INSERT INTO topics (id, name) VALUES
(22,  'SADE'),
(23,  'SADE_INTENSITEETTI'),
(24,  'SADESUMMA'),
(25,  'SATEEN_OLOMUOTO_PWDXX'),
(26,  'NÄKYVYYS_KM'),
(176, 'KITKA_1'),
(177, 'VEDEN_MÄÄRÄ_1'),
(181, 'KITKA1_LUKU'),
(186, 'KITKA_2'),
(187, 'VEDEN_MÄÄRÄ_2'),
(191, 'KITKA2_LUKU'),
(300, 'WATER_TEMPERATURE'),
(301, 'AIR_TEMPERATURE'),
(302, 'RELATIVE_HUMIDITY'),
(303, 'PRESSURE_MSL'),
(304, 'WIND_SPEED'),
(305, 'WIND_DIRECTION'),
(306, 'GUST_SPEED'),
(307, 'DEWPOINT'),
(308, 'PRECIPITATION_AMOUNT'),
(309, 'HORIZONTAL_VISIBILITY');

CREATE INDEX idx_measurements_station_topic_timestamp
ON measurements (station_id, topic_id, timestamp);

CREATE INDEX idx_measurements_station_topic_value
ON measurements (station_id, topic_id, value);

