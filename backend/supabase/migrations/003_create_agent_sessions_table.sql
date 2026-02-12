-- Migration: Create agent sessions table for persistent memory
-- Status: Ready to execute (after 002_create_lyrics_table.sql)

-- Create enum for agent session status
DO $$ BEGIN
    CREATE TYPE agent_session_status AS ENUM ('active', 'completed', 'escalated');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create agent sessions table
CREATE TABLE IF NOT EXISTS agent_sessions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    session_id TEXT NOT NULL,
    agent_id TEXT NOT NULL,
    parent_session_id TEXT,
    task_description TEXT,
    summary TEXT,
    decisions JSONB DEFAULT '[]'::jsonb,
    artifacts JSONB DEFAULT '[]'::jsonb,
    context_embedding VECTOR(1536),
    status agent_session_status DEFAULT 'active',
    metadata JSONB DEFAULT '{}'::jsonb,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    completed_at TIMESTAMP WITH TIME ZONE DEFAULT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE agent_sessions ENABLE ROW LEVEL SECURITY;

-- Create policies (readable by authenticated agents)
CREATE POLICY "Enable read access for authenticated agents" ON agent_sessions
    FOR SELECT TO authenticated USING (true);

CREATE POLICY "Enable insert for authenticated agents" ON agent_sessions
    FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Enable update for authenticated agents" ON agent_sessions
    FOR UPDATE TO authenticated USING (true);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_agent_sessions_agent_id ON agent_sessions(agent_id);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_session_id ON agent_sessions(session_id);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_status ON agent_sessions(status);
CREATE INDEX IF NOT EXISTS idx_agent_sessions_started_at ON agent_sessions(started_at DESC);

-- Create vector index for semantic search over sessions
CREATE INDEX IF NOT EXISTS idx_agent_sessions_embedding_cosine
    ON agent_sessions USING ivfflat (context_embedding vector_cosine_ops)
    WITH (lists = 50);

-- Create function for similar session search
CREATE OR REPLACE FUNCTION search_similar_sessions(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 5,
    agent_filter TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    session_id TEXT,
    agent_id TEXT,
    task_description TEXT,
    summary TEXT,
    decisions JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        s.id,
        s.session_id,
        s.agent_id,
        s.task_description,
        s.summary,
        s.decisions,
        1 - (s.context_embedding <=> query_embedding) AS similarity
    FROM agent_sessions s
    WHERE
        (agent_filter IS NULL OR s.agent_id = agent_filter) AND
        s.context_embedding IS NOT NULL AND
        1 - (s.context_embedding <=> query_embedding) > match_threshold
    ORDER BY s.context_embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- Create function for session memory consolidation
CREATE OR REPLACE FUNCTION consolidate_session_memory(
    p_session_id TEXT
)
RETURNS JSONB
LANGUAGE plpgsql
AS $$
DECLARE
    v_lyrics_count INT;
    v_decisions_count INT;
    v_memory_embedding VECTOR(1536);
    v_result JSONB;
BEGIN
    -- Count related content
    SELECT COUNT(*) INTO v_lyrics_count
    FROM lyrics l
    WHERE l.metadata->>'related_session' = p_session_id;

    -- Count decisions
    SELECT COUNT(*) INTO v_decisions_count
    FROM agent_sessions s
    WHERE s.session_id = p_session_id AND
          jsonb_array_length(s.decisions) > 0;

    -- Generate embedding from summary for memory
    -- In production, this would use the actual embedding model
    v_memory_embedding := NULL;

    -- Build memory summary
    v_result := jsonb_build_object(
        'session_id', p_session_id,
        'lyrics_processed', v_lyrics_count,
        'decisions_made', v_decisions_count,
        'consolidated_at', NOW()::TEXT
    );

    RETURN v_result;
END;
$$;

-- Create function to update session status
CREATE OR REPLACE FUNCTION complete_agent_session(
    p_session_id TEXT,
    p_summary TEXT,
    p_decisions JSONB DEFAULT '[]'::jsonb,
    p_artifacts JSONB DEFAULT '[]'::jsonb
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
    v_session_id UUID;
BEGIN
    UPDATE agent_sessions
    SET
        summary = p_summary,
        decisions = p_decisions,
        artifacts = p_artifacts,
        status = 'completed',
        completed_at = NOW()
    WHERE session_id = p_session_id
    RETURNING id INTO v_session_id;

    RETURN v_session_id;
END;
$$;

-- Comment on table
COMMENT ON TABLE agent_sessions IS 'Persistent agent memory for context retrieval and learning';
COMMENT ON COLUMN agent_sessions.context_embedding IS 'Vector embedding of session summary for semantic search';
