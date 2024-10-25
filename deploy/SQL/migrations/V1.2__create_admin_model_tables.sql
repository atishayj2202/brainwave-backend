CREATE TABLE message
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    message          VARCHAR NOT NULL,
    user_id          UUID    NOT NULL REFERENCES user_accounts (id),
    role             VARCHAR NOT NULL,
    status           VARCHAR NOT NULL,
    is_deleted       TIMESTAMPTZ DEFAULT NULL
);

CREATE INDEX message_user_id_idx ON message (user_id);

CREATE TABLE category
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    parent_id        UUID        DEFAULT NULL REFERENCES category (id),
    category_name    VARCHAR NOT NULL,
    is_deleted       TIMESTAMPTZ DEFAULT NULL
);

CREATE INDEX category_parent_id_idx ON category (parent_id);

CREATE TABLE questions
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    question         VARCHAR NOT NULL,
    option_a         VARCHAR NOT NULL,
    option_b         VARCHAR NOT NULL,
    option_c         VARCHAR NOT NULL,
    option_d         VARCHAR NOT NULL,
    correct_option   VARCHAR NOT NULL,
    difficulty_level VARCHAR NOT NULL,
    is_deleted       TIMESTAMPTZ DEFAULT NULL
);

CREATE TABLE user_questions
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    user_id          UUID NOT NULL REFERENCES user_accounts (id),
    question_id      UUID NOT NULL REFERENCES questions (id),
    is_correct       BOOLEAN     DEFAULT NULL
);

CREATE TABLE category_info
(
    id               UUID PRIMARY KEY,
    created_at       TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    last_modified_at TIMESTAMPTZ DEFAULT now()::TIMESTAMPTZ,
    category_id      UUID    NOT NULL REFERENCES category (id),
    title            VARCHAR NOT NULL,
    description      VARCHAR NOT NULL,
    article_info     VARCHAR NOT NULL,
    is_deleted       TIMESTAMPTZ DEFAULT NULL,
    remarks          VARCHAR NOT NULL
);

CREATE INDEX category_info_category_id_idx ON category_info (category_id);