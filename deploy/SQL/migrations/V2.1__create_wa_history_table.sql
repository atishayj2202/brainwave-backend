CREATE TABLE wa_history
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    message_id       VARCHAR NOT NULL UNIQUE,
    message VARCHAR NOT NULL,
    output_message VARCHAR NOT NULL,
    wa_id VARCHAR NOT NULL
);

CREATE INDEX user_accounts_number_idx ON user_accounts (firebase_user_id);