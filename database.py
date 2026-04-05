import sqlite3
from contextlib import contextmanager

DB_PATH = "./my_library.db"

@contextmanager
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn.cursor()
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def initial_db_setup():
  with get_db() as cursor:
    cursor.execute("""CREATE TABLE stories (
                  id integer PRIMARY KEY AUTOINCREMENT, 
                  name text NOT NULL,
                  summary text,
                  notes text,
                  rating integer,
                  filepath text NOT NULL UNIQUE,
                  added_at datetime DEFAULT current_timestamp            
    )""")

    cursor.execute("""CREATE TABLE tags (
                  id integer PRIMARY KEY AUTOINCREMENT,
                  name text NOT NULL UNIQUE
    )""")

    cursor.execute("""CREATE TABLE collections (
                  id integer PRIMARY KEY AUTOINCREMENT, 
                  name text NOT NULL
    )""")

    cursor.execute("""CREATE TABLE story_tag (
                  story_id REFERENCES stories(id),
                  tag_id REFERENCES tags(id),
                  PRIMARY KEY (story_id, tag_id)
    )""")

    cursor.execute("""CREATE TABLE story_collection (
                  story_id REFERENCES stories(id),
                  collection_id REFERENCES collections(id),
                  PRIMARY KEY (story_id, collection_id)
    )""")

def get_stories():
  with get_db() as cursor:
    return cursor.execute("""SELECT * FROM stories""").fetchall()

def get_story_info(story_id: int):
  with get_db() as cursor:
    return cursor.execute("SELECT * FROM stories WHERE id = ?", (story_id,)).fetchone()

# Gets any story that has any of these tags
def get_tagged_stories_any(tags: list):
  parsedTags = ""
  if (len(tags) > 1):
    for tag in tags:
      parsedTags += f"OR st.tag_id = {tag} "
      
    parsedTags = parsedTags[3:]
  
  with get_db() as cursor:
    return cursor.execute("""SELECT st.id
                          FROM story_tag st
                          JOIN stories s on st.story_id = s.id
                          WHERE ?
    """, (parsedTags,)).fetchall()
  
