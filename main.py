from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
from typing import List

app = FastAPI()

# --- DATABASE SETUP ---
def init_db():
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS characters 
                      (id INTEGER PRIMARY KEY, name TEXT, role TEXT, actor TEXT, species TEXT)''')
    
    # Check if data exists, if not, insert 15 characters
    cursor.execute("SELECT COUNT(*) FROM characters")
    if cursor.fetchone()[0] == 0:
        characters = [
            (1, "Peppa Pig", "Main Character", "Amelie Bea Smith", "Pig"),
            (2, "George Pig", "Peppa's Brother", "Alice May", "Pig"),
            (3, "Mummy Pig", "Mother", "Morwenna Banks", "Pig"),
            (4, "Daddy Pig", "Father", "Richard Ridings", "Pig"),
            (5, "Suzy Sheep", "Best Friend", "Libby Shaw", "Sheep"),
            (6, "Rebecca Rabbit", "Friend", "Alice May", "Rabbit"),
            (7, "Danny Dog", "Friend", "Joshua Sasse", "Dog"),
            (8, "Pedro Pony", "Friend", "Stanley Nickless", "Pony"),
            (9, "Zoe Zebra", "Friend", "Sian Taylor", "Zebra"),
            (10, "Candy Cat", "Friend", "Daisy Humphrey", "Cat"),
            (11, "Emily Elephant", "Friend", "Starlight Huang", "Elephant"),
            (12, "Gerald Giraffe", "Friend", "Leo Templer", "Giraffe"),
            (13, "Grandpa Pig", "Grandfather", "David Graham", "Pig"),
            (14, "Granny Pig", "Grandmother", "Frances White", "Pig"),
            (15, "Madame Gazelle", "Teacher", "Gigglebiz", "Gazelle")
        ]
        cursor.executemany("INSERT INTO characters VALUES (?,?,?,?,?)", characters)
        conn.commit()
    conn.close()

init_db()

# --- API MODELS ---
class Character(BaseModel):
    id: int
    name: str
    role: str
    actor: str
    species: str

# --- ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Peppa Pig Fanbase API</title>
            <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&display=swap" rel="stylesheet">
            <style>
                body { font-family: 'Fredoka One', cursive; background-color: #ffc0cb; color: #333; text-align: center; padding: 50px; }
                .container { background: white; padding: 30px; border-radius: 20px; box-shadow: 0 10px 20px rgba(0,0,0,0.1); max-width: 800px; margin: auto; }
                h1 { color: #e91e63; font-size: 3em; }
                .btn { background: #e91e63; color: white; padding: 15px 25px; text-decoration: none; border-radius: 50px; display: inline-block; margin: 10px; transition: 0.3s; }
                .btn:hover { background: #c2185b; transform: scale(1.05); }
                .endpoints { text-align: left; background: #fff5f7; padding: 20px; border-radius: 10px; margin-top: 20px; border-left: 5px solid #e91e63; }
                code { background: #eee; padding: 2px 5px; border-radius: 4px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐷 Peppa's Fanbase</h1>
                <p>Welcome to the ultimate Peppa Pig Character API!</p>
                <a href="/characters" class="btn">View All Characters</a>
                <a href="/actors" class="btn">View Voice Actors</a>
                <div class="endpoints">
                    <h3>API Documentation:</h3>
                    <ul>
                        <li><code>GET /characters</code> - List all 15 characters</li>
                        <li><code>GET /characters/{id}</code> - Get details of one character</li>
                        <li><code>GET /actors</code> - List all voice actors</li>
                    </ul>
                </div>
            </div>
        </body>
    </html>
    """

@app.get("/characters", response_model=List[Character])
def get_characters():
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "role": r[2], "actor": r[3], "species": r[4]} for r in rows]

@app.get("/characters/{char_id}", response_model=Character)
def get_character(char_id: int):
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE id = ?", (char_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "role": row[2], "actor": row[3], "species": row[4]}
    raise HTTPException(status_code=404, detail="Character not found")

@app.get("/actors")
def get_actors():
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT actor FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return {"actors": [r[0] for r in rows]}
