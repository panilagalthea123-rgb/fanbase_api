from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


characters_db = [
    {
        "id": 1, 
        "name": "Peppa Pig", 
        "actor": "Lily Snowden-Fine", 
        "description": "A cheeky little piggy who loves playing games, dressing up, and jumping in muddy puddles.",
        "image": "https://upload.wikimedia.org/wikipedia/en/3/3b/Peppa_Pig_character.png"
    },
    {
        "id": 2, 
        "name": "George Pig", 
        "actor": "Oliver May", 
        "description": "Peppa's little brother. He loves dinosaurs and carries his 'Mr. Dinosaur' everywhere he goes.",
        "image": "https://static.wikia.nocookie.net/peppapig/images/0/02/George_Pig.png"
    },
    {
        "id": 3, 
        "name": "Mummy Pig", 
        "actor": "Morwenna Banks", 
        "description": "She works from home on her computer and is very good at jumping in muddy puddles too.",
        "image": "https://static.wikia.nocookie.net/peppapig/images/5/52/Mummy_Pig.png"
    },
    {
        "id": 4, 
        "name": "Daddy Pig", 
        "actor": "Richard Ridings", 
        "description": "He is very jolly, stays cheerful even when things go wrong, and is a bit of an expert at everything.",
        "image": "https://static.wikia.nocookie.net/peppapig/images/3/31/Daddy_Pig.png"
    }
]


@app.get("/", response_class=HTMLResponse)
async def home_ui(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "characters": characters_db})


@app.get("/api/characters")
def get_all_characters():
    return characters_db

@app.get("/api/characters/{char_id}")
def get_character(char_id: int):
    character = next((c for c in characters_db if c["id"] == char_id), None)
    return character if character else {"error": "Character not found"}

@app.get("/api/actors")
def get_actors():
    return [{"character": c["name"], "actor": c["actor"]} for c in characters_db]
