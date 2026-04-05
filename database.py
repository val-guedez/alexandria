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
                  file_path text NOT NULL UNIQUE,
                  added_at datetime DEFAULT current_timestamp            
    )""")

    cursor.execute("""CREATE TABLE tags (
                  id integer PRIMARY KEY AUTOINCREMENT,
                  name text NOT NULL UNIQUE
                  created_at datetime DEFAULT current_timestamp
    )""")

    cursor.execute("""CREATE TABLE collections (
                  id integer PRIMARY KEY AUTOINCREMENT, 
                  name text NOT NULL UNIQUE
                  description text
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

def create_story(name, summary, notes, rating, file_path):
  cols = "name"
  values = f"{name}"
  if summary != None:
    cols += ", summary"
    values += f", {summary}"
  if notes != None:
    cols += ", notes"
    values += f", {notes}"
  if rating != None:
    cols += ", rating"
    values += f", {rating}"
  
  cols += ", file_path"
  values += f", {file_path}"
  
  with get_db() as cursor:
    cursor.execute("""INSERT INTO stories (?) VALUES (?)""", (cols, values))

def update_story_name(story_id, name):
  with get_db() as cursor:
    cursor.execute("""UPDATE stories
                   SET name = ?
                   WHERE story_id = ?
    """, (name, story_id))

def update_story_summary(story_id, summary):
  with get_db() as cursor:
    cursor.execute("""UPDATE stories
                   SET summary = ?
                   WHERE story_id = ?
    """, (summary, story_id))

def update_story_notes(story_id, notes):
  with get_db() as cursor:
    cursor.execute("""UPDATE stories
                   SET notes = ?
                   WHERE story_id = ?
    """, (notes, story_id))

def update_story_rating(story_id, rating):
  with get_db() as cursor:
    cursor.execute("""UPDATE stories
                   SET rating = ?
                   WHERE story_id = ?
    """, (rating, story_id))

def update_story_file_path(story_id, file_path):
  with get_db() as cursor:
    cursor.execute("""UPDATE stories
                   SET file_path = ?
                   WHERE story_id = ?
    """, (file_path, story_id))

# Only deletes record from database - not file itself
def delete_story(story_id):
  with get_db() as cursor:
    cursor.execute("""DELETE FROM stories
                   WHERE id = ?
    """, (story_id,))
    cursor.execute("DELETE FROM story_tag WHERE story_id = ?", (story_id,))
    cursor.execute("DELETE FROM story_collection WHERE story_id = ?", (story_id,))

def create_tag(name):
  with get_db() as cursor:
    cursor.execute("""INSERT INTO tags (name) VALUES (?)""", (name,))

def add_tags_to_story(story_id, tags):
  with get_db() as cursor:
    for tag in tags:
      cursor.execute("""INSERT INTO story_tag (story_id, tag_id)
                     VALUES (?, ?)
      """, (story_id, tag))

def delete_tag(tag_id):
  with get_db() as cursor:
    cursor.execute("DELETE FROM tags WHERE id = ?", (tag_id,))
    cursor.execute("DELETE FROM story_tag WHERE tag_id = ?", (tag_id,))

def create_collection(name, description):
  cols = "name"
  values = f"{name}"
  if description != None:
    cols += ", description"
    values += f", {description}"
  with get_db() as cursor:
    cursor.execute("""INSERT INTO collections (?)
                   VALUES (?)
    """, (cols, values))

def update_collection_name(collection_id, name):
  with get_db() as cursor:
    cursor.execute("UPDATE collections SET name = ? WHERE collection_id = ?", (name, collection_id))

def update_collection_description(collection_id, description):
  with get_db() as cursor:
    cursor.execute("UPDATE collections SET description = ? WHERE collection_id = ?", (description, collection_id))

def delete_collection(collection_id):
  with get_db() as cursor:
    cursor.execute("DELETE FROM collections WHERE id = ?", (collection_id,))
    cursor.execute("DELETE FROM story_collection WHERE collection_id = ?", (collection_id,))

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
    return cursor.execute("""SELECT s.id, s.name
                          FROM story_tag st
                          JOIN stories s on st.story_id = s.id
                          WHERE ?
    """, (parsedTags,)).fetchall()

def get_stories_with_rating(rating):
  with get_db() as cursor:
    return cursor.execute("""SELECT id, name
                          FROM stories
                          WHERE rating = ?
  """, (rating,)).fetchall()
  
