import os
import sqlite3
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


DB_PATH = "fanbase.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS characters 
                   (id INTEGER PRIMARY KEY, name TEXT, actor TEXT, description TEXT, image TEXT)''')
    
 
    cursor.execute("SELECT COUNT(*) FROM characters")
    if cursor.fetchone()[0] == 0:
        characters = [
            (1, 'Peppa Pig', 'Lily Snowden-Fine', 'A cheeky little piggy who loves jumping in muddy puddles.', 'https://upload.wikimedia.org/wikipedia/en/3/3b/Peppa_Pig_character.png'),
            (2, 'George Pig', 'Oliver May', 'Peppa\'s little brother who loves his toy Dinosaur.', 'https://static.wikia.nocookie.net/peppapig/images/0/02/George_Pig.png'),
            (3, 'Mummy Pig', 'Morwenna Banks', 'She works from home and is very wise.', 'https://static.wikia.nocookie.net/peppapig/images/5/52/Mummy_Pig.png'),
            (4, 'Daddy Pig', 'Richard Ridings', 'A bit of an expert at everything, even when he isn\'t.', 'https://static.wikia.nocookie.net/peppapig/images/3/31/Daddy_Pig.png')
        ]
        cursor.executemany("INSERT INTO characters VALUES (?,?,?,?,?)", characters)
        conn.commit()
    conn.close()


init_db()



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    chars = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "characters": chars})

@app.get("/api/characters")
def get_all():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM characters")
    data = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return data

@app.get("/api/actors")
def get_actors():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, actor FROM characters")
    data = [{"character": row[0], "actor": row[1]} for row in cursor.fetchall()]
    conn.close()
    return data
