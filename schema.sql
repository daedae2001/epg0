DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
DROP TABLE IF EXISTS canales;

CREATE TABLE Canales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    EXTINF INTEGER NOT NULL DEFAULT 1,
    channelid TEXT,
    tvgid TEXT ,
    tvglogo TEXT ,
    grouptitle TEXT ,
    nombre TEXT NOT NULL,
    url TEXT NOT NULL,
    lenguaje TEXT,
    pais TEXT,
    activo INTEGER DEFAULT 1,
    epg INTEGER DEFAULT 0
);
DROP TABLE IF EXISTS canales1;

CREATE TABLE Canales1 (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    EXTINF INTEGER NOT NULL DEFAULT 1,
    channel_id TEXT,
    tvg_id TEXT ,
    tvg_logo TEXT ,
    group_title TEXT ,
    nombre TEXT NOT NULL,
    url TEXT NOT NULL,
    lenguaje TEXT,
    pais TEXT,
    activo INTEGER DEFAULT 1,
    epg INTEGER DEFAULT 0
);