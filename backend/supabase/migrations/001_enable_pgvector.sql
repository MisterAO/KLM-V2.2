-- Migration: Enable pgvector extension
-- Run this first in Supabase SQL Editor
-- Status: Ready to execute

-- Enable pgvector extension for vector embeddings
CREATE EXTENSION IF NOT EXISTS vector;

-- Verify installation
SELECT extname, extversion FROM pg_extension WHERE extname = 'vector';

-- Confirm pgvector is available
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') THEN
        RAISE NOTICE 'pgvector extension enabled successfully';
    ELSE
        RAISE EXCEPTION 'pgvector extension not enabled';
    END IF;
END $$;

-- Note: After running this, you can create vector columns
-- Example: embedding VECTOR(1536) for OpenAI embeddings
