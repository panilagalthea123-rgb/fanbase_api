from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(BASE_DIR, "static")),
    name="static"
)

templates = Jinja2Templates(
    directory=os.path.join(BASE_DIR, "templates")
)
# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("fanbase.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        role TEXT,
        actor TEXT,
        description TEXT,
        image TEXT
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM characters")
    if cursor.fetchone()[0] == 0:

        chars = [
            ("Peppa Pig","Main Character","Amelie Bea Smith","A cheerful pig who loves adventures.","https://upload.wikimedia.org/wikipedia/en/8/83/Peppa_Pig.png"),
            ("George Pig","Brother","Alice May","Peppa's little brother who loves dinosaurs.","https://upload.wikimedia.org/wikipedia/en/6/6b/George_Pig.png"),
            ("Mummy Pig","Mother","Morwenna Banks","Works from home and is very caring.","https://upload.wikimedia.org/wikipedia/en/5/55/Mummy_Pig.png"),
            ("Daddy Pig","Father","Richard Ridings","Funny and a bit clumsy.","https://upload.wikimedia.org/wikipedia/en/8/8b/Daddy_Pig.png"),
            ("Suzy Sheep","Best Friend","Bethany Bewley","Peppa’s best friend.","https://upload.wikimedia.org/wikipedia/en/3/3a/Suzy_Sheep.png"),
            ("Rebecca Rabbit","Friend","Alice May","Loves carrots.","https://upload.wikimedia.org/wikipedia/en/3/3a/Rebecca_Rabbit.png"),
            ("Danny Dog","Friend","George Woolford","Wants to be a sailor.","https://upload.wikimedia.org/wikipedia/en/5/5c/Danny_Dog.png"),
            ("Pedro Pony","Friend","Stanley Nickless","Often sleepy.","https://upload.wikimedia.org/wikipedia/en/0/0c/Pedro_Pony.png"),
            ("Zoe Zebra","Friend","Sian Taylor","Helpful and kind.","https://upload.wikimedia.org/wikipedia/en/2/2c/Zoe_Zebra.png"),
            ("Emily Elephant","Friend","Julia Moss","Shy but loud trumpet.","https://upload.wikimedia.org/wikipedia/en/0/0b/Emily_Elephant.png"),
            ("Candy Cat","Friend","Daisy Rudd","Loves skipping.","https://upload.wikimedia.org/wikipedia/en/6/6c/Candy_Cat.png"),
            ("Grandpa Pig","Grandfather","David Graham","Loves gardening.","https://upload.wikimedia.org/wikipedia/en/0/0d/Grandpa_Pig.png"),
            ("Granny Pig","Grandmother","Frances White","Makes cakes.","https://upload.wikimedia.org/wikipedia/en/4/4d/Granny_Pig.png"),
            ("Madame Gazelle","Teacher","Morwenna Banks","Teaches children.","https://upload.wikimedia.org/wikipedia/en/3/3f/Madame_Gazelle.png"),
            ("Mr Bull","Worker","David Rintoul","Loves digging roads.","https://upload.wikimedia.org/wikipedia/en/2/2d/Mr_Bull.png")
        ]

        cursor.executemany("""
        INSERT INTO characters (name, role, actor, description, image)
        VALUES (?, ?, ?, ?, ?)
        """, chars)

    conn.commit()
    conn.close()

init_db()

# ---------- UI ----------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    conn = sqlite3.connect("fanbase.db")
    conn.row_factory = sqlite3.Row  # ✅ FIXED HERE
    data = conn.execute("SELECT * FROM characters").fetchall()
    conn.close()

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "characters": data}
    )

# ---------- API ----------
@app.get("/api/characters")
def get_all():
    conn = sqlite3.connect("fanbase.db")
    data = conn.execute("SELECT * FROM characters").fetchall()
    conn.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "role": row[2],
            "actor": row[3],
            "description": row[4],
            "image": row[5]
        }
        for row in data
    ]

@app.get("/api/characters/{id}")
def get_one(id: int):
    conn = sqlite3.connect("fanbase.db")
    row = conn.execute("SELECT * FROM characters WHERE id=?", (id,)).fetchone()
    conn.close()

    if row:
        return {
            "id": row[0],
            "name": row[1],
            "role": row[2],
            "actor": row[3],
            "description": row[4],
            "image": row[5]
        }
    return {"error": "Character not found"}

@app.get("/api/actors")
def get_actors():
    conn = sqlite3.connect("fanbase.db")
    data = conn.execute("SELECT name, actor FROM characters").fetchall()
    conn.close()

    return [{"character": r[0], "actor": r[1]} for r in data]
