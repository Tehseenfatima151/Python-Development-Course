import sqlite3, os

db_path = os.path.join(os.path.dirname(__file__), 'flask-blog-platform', 'instance', 'blog.db')
print(f"DB path: {db_path}")
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Create categories table if not exists
c.execute("""
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# Add category_id column to posts if not exists
try:
    c.execute("ALTER TABLE posts ADD COLUMN category_id INTEGER REFERENCES categories(id)")
    print("Added category_id column")
except Exception as e:
    print(f"category_id column: {e}")

# Insert predefined categories
cats = ["Technology","Python","Web Development","AI & Machine Learning",
        "Software Engineering","Programming","Tutorials","Career","Other"]
for cat in cats:
    try:
        c.execute("INSERT INTO categories (name) VALUES (?)", (cat,))
    except:
        pass

conn.commit()

# Verify
rows = conn.execute("SELECT id, name FROM categories").fetchall()
print("Categories:", rows)
posts = conn.execute("SELECT id, title, category_id FROM posts").fetchall()
print("Posts:", posts)
conn.close()
print("Migration complete.")
