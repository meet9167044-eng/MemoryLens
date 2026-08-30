import psycopg2
conn = psycopg2.connect('postgresql://postgres:Meet%4012@localhost:5432/memorylens_db')
conn.autocommit = True
cur = conn.cursor()

# Check if relationships table already exists
cur.execute("SELECT EXISTS (SELECT 1 FROM pg_tables WHERE schemaname='public' AND tablename='relationships')")
exists = cur.fetchone()[0]

if not exists:
    print("Creating relationship_type enum if not exists...")
    cur.execute("DO $$ BEGIN CREATE TYPE relationship_type AS ENUM ('shared_entity', 'shared_tag', 'semantic'); EXCEPTION WHEN duplicate_object THEN NULL; END $$")

    print("Creating relationships table...")
    cur.execute("""
        CREATE TABLE relationships (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            source_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
            target_id UUID NOT NULL REFERENCES memories(id) ON DELETE CASCADE,
            rel_type relationship_type NOT NULL,
            score FLOAT NOT NULL DEFAULT 0.0,
            explanation TEXT,
            created_at TIMESTAMP NOT NULL DEFAULT NOW()
        )
    """)
    print("relationships table created!")
else:
    print("relationships table already exists, skipping.")

# Stamp alembic to latest
cur.execute("SELECT version_num FROM alembic_version")
row = cur.fetchone()
print(f"Alembic version: {row}")

conn.close()
print("Done!")
