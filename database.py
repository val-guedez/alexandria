import sqlite3

def initial_db_setup():
  conn = sqlite3.connect('my_library.db')
  cursor = conn.cursor()

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

  conn.commit()

  conn.close()
  