from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🐷 Fake database (15 characters)
characters = [
    {"id": 1, "name": "Peppa Pig", "desc": "Main character", "image": "https://i.imgur.com/peppa.png", "actor": "Amelie Bea Smith"},
    {"id": 2, "name": "George Pig", "desc": "Peppa's brother", "image": "https://i.imgur.com/george.png", "actor": "Oliver May"},
    {"id": 3, "name": "Daddy Pig", "desc": "Funny dad", "image": "https://i.imgur.com/daddy.png", "actor": "Richard Ridings"},
    {"id": 4, "name": "Mummy Pig", "desc": "Smart mom", "image": "https://i.imgur.com/mummy.png", "actor": "Morwenna Banks"},
    {"id": 5, "name": "Suzy Sheep", "desc": "Best friend", "image": "https://i.imgur.com/suzy.png", "actor": "Harley Bird"},
    {"id": 6, "name": "Rebecca Rabbit", "desc": "Kind friend", "image": "https://i.imgur.com/rabbit.png", "actor": "Alice May"},
    {"id": 7, "name": "Pedro Pony", "desc": "Sleepy friend", "image": "https://i.imgur.com/pony.png", "actor": "David Rintoul"},
    {"id": 8, "name": "Danny Dog", "desc": "Energetic", "image": "https://i.imgur.com/dog.png", "actor": "Jake Harris"},
    {"id": 9, "name": "Emily Elephant", "desc": "Shy friend", "image": "https://i.imgur.com/elephant.png", "actor": "Unknown"},
    {"id": 10, "name": "Zoe Zebra", "desc": "Friendly", "image": "https://i.imgur.com/zebra.png", "actor": "Unknown"},
    {"id": 11, "name": "Candy Cat", "desc": "Playful", "image": "https://i.imgur.com/cat.png", "actor": "Unknown"},
    {"id": 12, "name": "Gerald Giraffe", "desc": "Tall friend", "image": "https://i.imgur.com/giraffe.png", "actor": "Unknown"},
    {"id": 13, "name": "Freddy Fox", "desc": "Clever fox", "image": "https://i.imgur.com/fox.png", "actor": "Unknown"},
    {"id": 14, "name": "Madame Gazelle", "desc": "Teacher", "image": "https://i.imgur.com/gazelle.png", "actor": "Morwenna Banks"},
    {"id": 15, "name": "Grandpa Pig", "desc": "Old but fun", "image": "https://i.imgur.com/grandpa.png", "actor": "David Graham"},
]

# 🌐 UI HOME
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {
        "request": request,
        "characters": characters
    })

# 📦 API: all characters
@app.get("/characters")
def get_all():
    return characters

# 🔎 API: specific character
@app.get("/characters/{id}")
def get_one(id: int):
    for c in characters:
        if c["id"] == id:
            return c
    return {"error": "Character not found"}

# 🎤 API: actors only
@app.get("/actors")
def get_actors():
    return [{"name": c["name"], "actor": c["actor"]} for c in characters]
