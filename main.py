from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
import sqlite3

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Connect DB
def get_db():
    conn = sqlite3.connect("fanbase.db")
    conn.row_factory = sqlite3.Row
    return conn

# Create table + insert data
def init_db():
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY,
        name TEXT,
        role TEXT,
        actor TEXT
    )
    """)

    cursor.execute("DELETE FROM characters")

    data = [
        ("Peppa Pig", "Main Character", "Harley Bird"),
        ("George Pig", "Peppa's Brother", "Oliver May"),
        ("Mummy Pig", "Mother", "Morwenna Banks"),
        ("Daddy Pig", "Father", "Richard Ridings"),
        ("Suzy Sheep", "Best Friend", "Isabella Acres"),
        ("Rebecca Rabbit", "Friend", "Alice May"),
        ("Pedro Pony", "Friend", "Harry Guest"),
        ("Danny Dog", "Friend", "Jay Ruckley"),
        ("Candy Cat", "Friend", "Madison Turner"),
        ("Emily Elephant", "Friend", "Chloe Dolandis"),
        ("Zoe Zebra", "Friend", "Sian Taylor"),
        ("Freddy Fox", "Friend", "Jamie Oram"),
        ("Madame Gazelle", "Teacher", "Morwenna Banks"),
        ("Grandpa Pig", "Grandfather", "David Graham"),
        ("Granny Pig", "Grandmother", "Frances White")
    ]

    cursor.executemany("INSERT INTO characters (name, role, actor) VALUES (?, ?, ?)", data)

    conn.commit()
    conn.close()

init_db()

# ROUTES

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/characters")
def get_characters():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result

@app.get("/characters/{char_id}")
def get_character(char_id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE id=?", (char_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else {"error": "Character not found"}

@app.get("/actors")
def get_actors():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name, actor FROM characters")
    result = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return result
