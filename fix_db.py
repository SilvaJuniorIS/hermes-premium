import sqlite3

DB_PATH = "hermes.db"  # ajuste se necessário

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

def add_column(name, definition):
    try:
        cursor.execute(f"ALTER TABLE api_runs ADD COLUMN {name} {definition}")
        print(f"✔ Coluna criada: {name}")
    except Exception as e:
        print(f"⚠️ {name} já existe ou erro: {e}")

add_column("end_time", "TEXT")
add_column("stats", "TEXT")
add_column("notes", "TEXT")

conn.commit()
conn.close()

print("\n✅ Banco atualizado com sucesso")