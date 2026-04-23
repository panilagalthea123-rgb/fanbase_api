from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# 1. Database Setup
DATABASE_URL = "sqlite:///./peppa.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# 2. Character Model
class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    actor = Column(String)
    species = Column(String)

Base.metadata.create_all(bind=engine)

# 3. App and UI Setup
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Seed Data (Adds 15 characters if DB is empty)
def seed_db():
    db = SessionLocal()
    if db.query(Character).count() == 0:
        pigs = [
            {"name": "Peppa Pig", "actor": "Amelie Bea Smith", "species": "Pig"},
            {"name": "George Pig", "actor": "Vincent van Hulzen", "species": "Pig"},
            {"name": "Mummy Pig", "actor": "Morwenna Banks", "species": "Pig"},
            {"name": "Daddy Pig", "actor": "Richard Ridings", "species": "Pig"},
            {"name": "Suzy Sheep", "actor": "Ava Lovell", "species": "Sheep"},
            {"name": "Rebecca Rabbit", "actor": "Alice May", "species": "Rabbit"},
            {"name": "Danny Dog", "actor": "George Woolford", "species": "Dog"},
            {"name": "Pedro Pony", "actor": "Harrison Oldroyd", "species": "Pony"},
            {"name": "Candy Cat", "actor": "Madison Turner", "species": "Cat"},
            {"name": "Zoe Zebra", "actor": "Saffron Prior", "species": "Zebra"},
            {"name": "Emily Elephant", "actor": "Starlight Huang", "species": "Elephant"},
            {"name": "Madame Gazelle", "actor": "Morwenna Banks", "species": "Gazelle"},
            {"name": "Mr. Bull", "actor": "David Rintoul", "species": "Bull"},
            {"name": "Grandpa Pig", "actor": "David Graham", "species": "Pig"},
            {"name": "Granny Pig", "actor": "Frances White", "species": "Pig"},
        ]
        for p in pigs:
            db.add(Character(**p))
        db.commit()
    db.close()

seed_db()

# 4. API Routes
@app.get("/", response_class=HTMLResponse)
async def read_ui(request: Request):
    db = SessionLocal()
    chars = db.query(Character).all()
    return templates.TemplateResponse("index.html", {"request": request, "characters": chars})

@app.get("/api/characters")
def get_all_characters():
    db = SessionLocal()
    return db.query(Character).all()

@app.get("/api/characters/{char_id}")
def get_character(char_id: int):
    db = SessionLocal()
    return db.query(Character).filter(Character.id == char_id).first()

@app.get("/api/actors")
def get_actors():
    db = SessionLocal()
    return [{"character": c.name, "actor": c.actor} for c in db.query(Character).all()]
