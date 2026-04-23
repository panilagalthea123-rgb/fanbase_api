from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3

app = FastAPI()

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Initialize SQLite Database
def init_db():
    conn = sqlite3.connect("fanbase.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS characters 
                      (id INTEGER PRIMARY KEY, name TEXT, role TEXT, actor TEXT, desc TEXT, img TEXT)''')
    
    # 15 Characters Data
    chars = [
        ( "Peppa Pig", "Main Character", "Amelie Bea Smith", "A lovable, cheeky little piggy who lives with her family.", ""peppa.png""),
        ( "George Pig", "Little Brother", "Alice May", "Peppa's little brother who loves dinosaurs.", "George_s9.png"),
        ( "Mummy Pig", "Mother", "Morwenna Banks", "She works from home on her computer.", "Mummy_Pig.png"),
        ( "Daddy Pig", "Father", "Richard Ridings", "He is very jolly but a bit clumsy.", "Daddy_Pig.png"),
        ( "Suzy Sheep", "Best Friend", "Bethany Bewley", "Peppa's best friend who likes to dress up as a nurse.", "SuzySheep.png"),
        ( "Rebecca Rabbit", "Friend", "Alice May", "She loves carrots more than anything.", "https://static.wikia.nocookie.net/peppapig/images/3/3a/Rebecca_Rabbit.png"),
        ( "Candy Cat", "Friend", "Daisy Rudd", "A kind cat who is very good at skipping.", "Candy_Cat.png"),
        ( "Danny Dog", "Friend", "George Woolford", "He wants to be a sailor like his dad.", "Danny_Dog.png"),
        ( "Pedro Pony", "Friend", "Stanley Nickless", "He is a bit sleepy and often loses his glasses.", "Pedro_Pony.png"),
        ( "Zoe Zebra", "Friend", "Sian Taylor", "The postman's daughter who helps deliver letters.", "zoe.png"),
        ( "Emily Elephant", "Friend", "Julia Moss", "She is a bit shy but has a very loud trumpet.", "emily.png"),
        ( "Grandpa Pig", "Grandfather", "David Graham", "He loves gardening and sailing his boat.", "Grandpapig1.png"),
        ( "Granny Pig", "Grandmother", "Frances White", "She makes the best chocolate cakes.", "granny.png"),
        ( "Madame Gazelle", "Teacher", "Morwenna Banks", "She taught all the parents when they were young.", "madamn.png"),
        ( "Mr. Bull", "Worker", "David Rintoul", "He loves digging up roads and building things.", "mrbull.png")
    ]
    cursor.executemany("INSERT OR REPLACE INTO characters VALUES (?,?,?,?,?,?)", chars)
    conn.commit()
    conn.close()

init_db()

# --- API ENDPOINTS ---

@app.get("/", response_class=HTMLResponse)
async def read_ui(request: Request):
    conn = sqlite3.connect("fanbase.db")
    conn.row_factory = sqlite3.Row
    chars = conn.execute("SELECT * FROM characters").fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "characters": chars})

@app.get("/api/characters")
def get_all():
    conn = sqlite3.connect("fanbase.db")
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM characters").fetchall()
    conn.close()
    return {"characters": data}

@app.get("/api/characters/{char_id}")
def get_one(char_id: int):
    conn = sqlite3.connect("fanbase.db")
    char = conn.execute("SELECT * FROM characters WHERE id = ?", (char_id,)).fetchone()
    conn.close()
    return char

@app.get("/api/actors")
def get_actors():
    conn = sqlite3.connect("fanbase.db")
    actors = conn.execute("SELECT name, actor FROM characters").fetchall()
    conn.close()
    return {"actors": actors}
