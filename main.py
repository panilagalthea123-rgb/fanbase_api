from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session


SQLALCHEMY_DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    role = Column(String)
    actor = Column(String)

Base.metadata.create_all(bind=engine)


app = FastAPI()
templates = Jinja2Templates(directory="templates")


def seed_db():
    db = SessionLocal()
    if db.query(Character).count() == 0:
        chars = [
            Character(name="Dom Cobb", role="The Extractor", actor="Leonardo DiCaprio"),
            Character(name="Arthur", role="The Point Man", actor="Joseph Gordon-Levitt"),
            Character(name="Ariadne", role="The Architect", actor="Elliot Page"),
            Character(name="Eames", role="The Forger", actor="Tom Hardy"),
            Character(name="Robert Fischer", role="The Mark", actor="Cillian Murphy"),
            Character(name="Mal Cobb", role="The Shade", actor="Marion Cotillard"),
            Character(name="Saito", role="The Tourist", actor="Ken Watanabe"),
            Character(name="Yusuf", role="The Chemist", actor="Dileep Rao"),
        ]
        db.add_all(chars)
        db.commit()
    db.close()

seed_db()


def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    characters = db.query(Character).all()
    return templates.TemplateResponse("index.html", {"request": request, "characters": characters})

@app.get("/api/characters")
def get_all_characters(db: Session = Depends(get_db)):
    return db.query(Character).all()

@app.get("/api/characters/{char_id}")
def get_character(char_id: int, db: Session = Depends(get_db)):
    return db.query(Character).filter(Character.id == char_id).first()

@app.get("/api/actors")
def get_actors(db: Session = Depends(get_db)):
    return [{"character": c.name, "actor": c.actor} for c in db.query(Character).all()]
