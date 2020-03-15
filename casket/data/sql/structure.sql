CREATE TABLE accounts (
  id_account INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  pswd       TEXT NOT NULL,
  email      TEXT NOT NULL,
  other_json TEXT NOT NULL,
  id_session INTEGER NOT NULL REFERENCES sessions(id_session)
);

CREATE TABLE sessions (
  username   TEXT PRIMARY KEY,
  email      TEXT NOT NULL
);
