
CREATE TABLE user (
    id BIGINT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    name TEXT DEFAULT ''::text,
    user_info JSONB,
    token VARCHAR DEFAULT ''::character varying,
    updated_at TIMESTAMP NOT NULL DEFAULT now(),
    openid VARCHAR,
    current_level VARCHAR DEFAULT 'free'::character varying
);

