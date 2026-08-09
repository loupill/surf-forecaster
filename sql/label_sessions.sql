
-- ============================================================
-- LABELING SESSIONS
-- ============================================================


create table if not exists gold.labeling_sessions (
	id            SERIAL PRIMARY key,
	token         TEXT NOT null unique,
	break_id      TEXT NOT null,
	session_date  DATE NOT null,
	sent_at       TIMESTAMPTZ NOT null,
	responded_at  TIMESTAMPTZ,
	
	unique (break_id, session_date)
);

-- ============================================================
-- HUMAN LABELS
-- ============================================================

create table if not exists gold.human_labels (
	id         SERIAL PRIMARY key,
	session_id    INT not null REFERENCES gold.labeling_sessions(id),
	time_block    TEXT NOT null,   -- 'morning', 'midday', 'evening'
	rating        SMALLINT NOT null,   -- 1-5
	comment       TEXT,
	
	CHECK (time_block IN ('morning', 'midday', 'evening')),
    CHECK (rating BETWEEN 1 AND 5),
    UNIQUE (session_id, time_block)

);