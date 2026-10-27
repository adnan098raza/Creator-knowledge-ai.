-- =========================================
-- CREATORS TABLE
-- =========================================

CREATE TABLE creators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,

    channel_url TEXT,

    platform VARCHAR(50) DEFAULT 'youtube',

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- VIDEOS TABLE
-- =========================================

CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    creator_id UUID NOT NULL,

    title TEXT NOT NULL,

    video_url TEXT UNIQUE NOT NULL,

    platform VARCHAR(50) DEFAULT 'youtube',

    duration_seconds INTEGER,

    published_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (creator_id)
        REFERENCES creators(id)
        ON DELETE CASCADE
);


-- =========================================
-- TRANSCRIPTS TABLE
-- =========================================

CREATE TABLE transcripts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    video_id UUID NOT NULL UNIQUE,

    full_text TEXT NOT NULL,

    language VARCHAR(50),

    source VARCHAR(100),

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (video_id)
        REFERENCES videos(id)
        ON DELETE CASCADE
);


-- =========================================
-- TRANSCRIPT CHUNKS TABLE
-- =========================================

CREATE TABLE transcript_chunks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    transcript_id UUID NOT NULL,

    chunk_index INTEGER NOT NULL,

    chunk_text TEXT NOT NULL,

    start_time_seconds INTEGER,

    end_time_seconds INTEGER,

    qdrant_point_id UUID UNIQUE,

    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (transcript_id)
        REFERENCES transcripts(id)
        ON DELETE CASCADE
);