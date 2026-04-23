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
    # Drop table and recreate to ensure the new schema (description/emoji) is applied
    cursor.execute("DROP TABLE IF EXISTS characters")
    cursor.execute('''CREATE TABLE characters 
                      (id INTEGER PRIMARY KEY, name TEXT, role TEXT, 
                       actor TEXT, species TEXT, description TEXT, emoji TEXT)''')
    
    characters = [
        (1, "Peppa Pig", "Main Protagonist", "Amelie Bea Smith", "Pig", "Loves jumping in muddy puddles and playing with Teddy.", "🐷"),
        (2, "George Pig", "Little Brother", "Alice May", "Pig", "Peppa's baby brother who absolutely loves Dinosaurs! 'Dine-saw!'", "🐷"),
        (3, "Mummy Pig", "Mother", "Morwenna Banks", "Pig", "Works from home on her computer and is very sensible.", "🐷"),
        (4, "Daddy Pig", "Father", "Richard Ridings", "Pig", "An expert at reading maps and jumping in puddles.", "🐷"),
        (5, "Suzy Sheep", "Best Friend", "Libby Shaw", "Sheep", "Peppa's best friend who likes to dress up as a nurse.", "🐑"),
        (6, "Rebecca Rabbit", "Friend", "Alice May", "Rabbit", "She lives in a hill and really, really likes carrots.", "🐰"),
        (7, "Danny Dog", "Friend", "Joshua Sasse", "Dog", "Likes helping his Grandad Dog at the garage.", "🐶"),
        (8, "Pedro Pony", "Friend", "Stanley Nickless", "Pony", "A bit shy and clumsy, but he loves being a Cowboy.", "🐴"),
        (9, "Zoe Zebra", "Friend", "Sian Taylor", "Zebra", "The postman's daughter who helps deliver the mail.", "🦓"),
        (10, "Candy Cat", "Friend", "Daisy Humphrey", "Cat", "Very good at tigers' prowling and making a 'Meow' sound.", "🐱"),
        (11, "Emily Elephant", "Friend", "Starlight Huang", "Elephant", "She has a very loud trumpet and is quite shy.", "🐘"),
        (12, "Gerald Giraffe", "Friend", "Leo Templer", "Giraffe", "The tallest child in the group, which helps him see far away.", "🦒"),
        (13, "Grandpa Pig", "Grandfather", "David Graham", "Pig", "A great gardener who loves his miniature train, Gertrude.", "🐷"),
        (14, "Granny Pig", "Grandmother", "Frances White", "Pig", "She grows the best vegetables in her garden.", "🐷"),
        (15, "Madame Gazelle", "Teacher", "Gigglebiz", "Gazelle", "The teacher at the playgroup who once played in a rock band!", "🦌")
    ]
    cursor.executemany("INSERT INTO characters VALUES (?,?,?,?,?,?,?)", characters)
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
    description: str
    emoji: str

# --- MAIN UI ROUTE ---
@app.get("/", response_class=HTMLResponse)
async def read_root():
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, emoji, description, species, id FROM characters")
    rows = cursor.fetchall()
    conn.close()

    cards_html = ""
    for row in rows:
        cards_html += f"""
        <div class="card">
            <div class="emoji">{row[1]}</div>
            <h3>{row[0]}</h3>
            <p class="species">{row[3]}</p>
            <p class="desc">{row[2]}</p>
            <a href="/characters/{row[4]}" class="view-btn">View API Data</a>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
        <head>
            <title>Peppa Pig Universe</title>
            <link href="https://fonts.googleapis.com/css2?family=Fredoka+One&family=Quicksand:wght@500&display=swap" rel="stylesheet">
            <style>
                body {{ font-family: 'Quicksand', sans-serif; background: #FFF0F5; margin: 0; padding: 20px; }}
                h1 {{ font-family: 'Fredoka One', cursive; color: #FF69B4; font-size: 3.5rem; text-align: center; text-shadow: 2px 2px 0px #fff; }}
                .container {{ max-width: 1100px; margin: auto; }}
                .nav-buttons {{ text-align: center; margin-bottom: 40px; }}
                .btn {{ background: #FF69B4; color: white; padding: 12px 25px; border-radius: 50px; text-decoration: none; font-weight: bold; margin: 5px; display: inline-block; box-shadow: 0 4px 0 #D02090; transition: 0.2s; }}
                .btn:hover {{ background: #ff85c2; }}
                .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; }}
                .card {{ background: white; padding: 25px; border-radius: 30px; box-shadow: 0 10px 20px rgba(0,0,0,0.05); text-align: center; transition: 0.3s; border: 2px solid #FFE4E1; }}
                .card:hover {{ transform: translateY(-8px); box-shadow: 0 15px 30px rgba(255,105,180,0.2); }}
                .emoji {{ font-size: 55px; margin-bottom: 15px; }}
                h3 {{ margin: 5px 0; color: #D02090; font-family: 'Fredoka One'; font-size: 1.5rem; }}
                .species {{ color: #FF69B4; font-weight: bold; letter-spacing: 1px; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 15px; }}
                .desc {{ color: #555; font-size: 0.95rem; line-height: 1.5; min-height: 60px; }}
                .view-btn {{ font-size: 0.7rem; color: #bbb; text-decoration: none; border-top: 1px solid #eee; display: block; margin-top: 15px; padding-top: 10px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🐷 Peppa Pig Fanbase</h1>
                <div class="nav-buttons">
                    <a href="/characters" class="btn">GET ALL (JSON)</a>
                    <a href="/actors" class="btn">VIEW ACTORS</a>
                </div>
                <div class="grid">
                    {cards_html}
                </div>
            </div>
        </body>
    </html>
    """

# --- API ENDPOINTS (GET ALL, GET SPECIFIC, GET ACTORS) ---

@app.get("/characters", response_model=List[Character])
def get_all_characters():
    """Endpoint to Get All Characters"""
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "role": r[2], "actor": r[3], "species": r[4], "description": r[5], "emoji": r[6]} for r in rows]

@app.get("/characters/{char_id}", response_model=Character)
def get_specific_character(char_id: int):
    """Endpoint to Get a Specific Character"""
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters WHERE id = ?", (char_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "role": row[2], "actor": row[3], "species": row[4], "description": row[5], "emoji": row[6]}
    raise HTTPException(status_code=404, detail="Character not found")

@app.get("/actors")
def get_actors():
    """Endpoint to Get All Actors"""
    conn = sqlite3.connect("peppa_fanbase.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT actor, name FROM characters")
    rows = cursor.fetchall()
    conn.close()
    return {"voice_cast": [{"actor": r[0], "character": r[1]} for r in rows]}
