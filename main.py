from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()


characters = [
    {"id": 1, "name": "Peppa Pig", "actor": "Lily Snowden-Fine", "description": "A lovable, cheeky little piggy who lives with her little brother George, Mummy Pig and Daddy Pig.", "image": "https://upload.wikimedia.org/wikipedia/en/3/3b/Peppa_Pig_character.png"},
    {"id": 2, "name": "George Pig", "actor": "Oliver May", "description": "Peppa's little brother. He loves dinosaurs and carries his 'Mr. Dinosaur' everywhere.", "image": "https://official-peppa-pig.fandom.com/wiki/George_Pig?file=George_Pig.png"},
    {"id": 3, "name": "Mummy Pig", "actor": "Morwenna Banks", "description": "She works from home on her computer and is very wise.", "image": "https://static.wikia.nocookie.net/peppapig/images/5/52/Mummy_Pig.png"},
    {"id": 4, "name": "Daddy Pig", "actor": "Richard Ridings", "description": "He is quite jolly and stays cheerful even when his 'expertise' goes slightly wrong.", "image": "https://static.wikia.nocookie.net/peppapig/images/3/31/Daddy_Pig.png"},
]

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "characters": characters})


@app.get("/api/characters")
def get_all():
    return characters


@app.get("/api/characters/{char_id}")
def get_one(char_id: int):
    return next((c for c in characters if c["id"] == char_id), {"error": "Not found"})


@app.get("/api/actors")
def get_actors():
    return [{"character": c["name"], "actor": c["actor"]} for c in characters]
