-- Migration: Create unified lyrics table with pgvector
-- Status: Ready to execute (after 001_enable_pgvector.sql)
-- Vector dimension: 1536 (OpenAI text-embedding-3-large)

-- Create enum for song status
DO $$ BEGIN
    CREATE TYPE lyric_status AS ENUM ('pending', 'processing', 'complete', 'failed');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create unified lyrics table with vector embeddings
CREATE TABLE IF NOT EXISTS lyrics (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title TEXT NOT NULL,
    artist TEXT,
    album TEXT,
    era TEXT,
    genre TEXT,
    lyrics_khmer TEXT,
    lyrics_romanized TEXT,
    lyrics_english TEXT,
    vocabulary JSONB DEFAULT '[]'::jsonb,
    metadata JSONB DEFAULT '{}'::jsonb,
    embedding VECTOR(1536),
    status lyric_status DEFAULT 'pending',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE lyrics ENABLE ROW LEVEL SECURITY;

-- Create policies for Supabase Auth
CREATE POLICY "Enable read access for authenticated users" ON lyrics
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Enable insert for authenticated users" ON lyrics
    FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Enable update for authenticated users" ON lyrics
    FOR UPDATE TO authenticated USING (true);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_lyrics_artist ON lyrics(artist);
CREATE INDEX IF NOT EXISTS idx_lyrics_era ON lyrics(era);
CREATE INDEX IF NOT EXISTS idx_lyrics_status ON lyrics(status);
CREATE INDEX IF NOT EXISTS idx_lyrics_created_at ON lyrics(created_at DESC);

-- Create vector index for fast similarity search (IVFFlat)
-- Note: For best results, insert data before creating this index
CREATE INDEX IF NOT EXISTS idx_lyrics_embedding_cosine
    ON lyrics USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);

-- Create function for automatic updated_at
CREATE OR REPLACE FUNCTION update_lyrics_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create trigger
DROP TRIGGER IF EXISTS trigger_lyrics_updated_at ON lyrics;
CREATE TRIGGER trigger_lyrics_updated_at
    BEFORE UPDATE ON lyrics
    FOR EACH ROW
    EXECUTE FUNCTION update_lyrics_updated_at();

-- Create function for hybrid search (combines SQL filters with vector similarity)
CREATE OR REPLACE FUNCTION hybrid_search_lyrics(
    query_embedding VECTOR(1536),
    match_threshold FLOAT,
    match_count INT,
    filter_artist TEXT DEFAULT NULL,
    filter_era TEXT DEFAULT NULL,
    filter_status TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    title TEXT,
    artist TEXT,
    era TEXT,
    lyrics_khmer TEXT,
    lyrics_romanized TEXT,
    lyrics_english TEXT,
    embedding VECTOR(1536),
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        l.id,
        l.title,
        l.artist,
        l.era,
        l.lyrics_khmer,
        l.lyrics_romanized,
        l.lyrics_english,
        l.embedding,
        1 - (l.embedding <=> query_embedding) AS similarity
    FROM lyrics l
    WHERE
        (filter_artist IS NULL OR l.artist = filter_artist) AND
        (filter_era IS NULL OR l.era = filter_era) AND
        (filter_status IS NULL OR l.status::TEXT = filter_status) AND
        l.embedding IS NOT NULL AND
        1 - (l.embedding <=> query_embedding) > match_threshold
    ORDER BY l.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Comment on table for documentation
COMMENT ON TABLE lyrics IS 'Unified lyrics storage with vector embeddings for semantic search';
COMMENT ON COLUMN lyrics.embedding IS 'OpenAI text-embedding-3-large vector (1536 dimensions)';
