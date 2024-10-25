CREATE TABLE user_accounts
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    email            VARCHAR NOT NULL,
    name             VARCHAR NOT NULL,
    firebase_user_id VARCHAR NOT NULL
);

CREATE INDEX user_accounts_number_idx ON user_accounts (firebase_user_id);