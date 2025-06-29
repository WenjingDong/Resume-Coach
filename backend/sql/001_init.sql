-- 1. Extension (adds the VECTOR type & ops)
CREATE EXTENSION IF NOT EXISTS vector;

-- 2. Chunk table
CREATE TABLE resume_chunks (
    id         BIGSERIAL PRIMARY KEY,
    resume_id  TEXT          NOT NULL,
    chunk      TEXT          NOT NULL,
    embedding  VECTOR(1536)  NOT NULL
);

-- 3. Approx-NN index (cosine)
CREATE INDEX resume_chunks_embedding_idx
    ON resume_chunks
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

