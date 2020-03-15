CREATE TABLE accounts (
  id_account INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  pswd       TEXT NOT NULL,
  email      TEXT NOT NULL,
  other_json TEXT NOT NULL
);

CREATE TABLE sessions (
  id_session INTEGER PRIMARY KEY AUTOINCREMENT,
  username   TEXT NOT NULL,
  pswd       TEXT NOT NULL,
  email      TEXT NOT NULL,
);
