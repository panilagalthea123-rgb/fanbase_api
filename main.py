import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# --- 1. SAFETY CONFIGURATION ---
# This ensures Render uses a persistent path for the database
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'peppa_v4.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- 2. DATA MODEL ---
class Character(Base):
    __tablename__ = "characters"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    actor = Column(String)
    description = Column(String)
    image_url = Column(String)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

# --- 3. DATABASE SEEDING (Auto-fill) ---
def seed_db():
    db = SessionLocal()
    if db.query(Character).count() == 0:
        data = [
            {"name": "Peppa Pig", "actor": "Harley Bird", "description": "A lovable, cheeky little piggy.", "image_url": "PASTE_LINK_HERE"},
            {"name": "George Pig", "actor": "Alice May", "description": "Loves dinosaurs! RAWWR!", "image_url": "PASTE_LINK_HERE"},
            {"name": "Mummy Pig", "actor": "Morwenna Banks", "description": "Very wise and kind.", "image_url": "PASTE_LINK_HERE"},
            {"name": "Daddy Pig", "actor": "Richard Ridings", "description": "An expert at reading maps.", "image_url": "PASTE_LINK_HERE"},
            {"name": "Suzy Sheep", "actor": "Meg Hall", "description": "Peppa's best friend.", "image_url": "PASTE_LINK_HERE"}
        ]
        for item in data:
            db.add(Character(**item))
        db.commit()
    db.close()

seed_db()

# --- 4. API LOGIC ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/characters")
def get_all(db: Session = Depends(get_db)):
    return db.query(Character).all()

# --- 5. INTERACTIVE UI ---
@app.get("/", response_class=HTMLResponse)
async def home_ui(request: Request, db: Session = Depends(get_db)):
    chars = db.query(Character).all()
    
    char_cards = ""
    for c in chars:
        # Safety: Show a placeholder icon if the link is empty
        img_src = c.image_url if "http" in c.image_url else "https://cdn-icons-png.flaticon.com/512/2632/2632839.png"
        
        char_cards += f"""
        <div class="col-md-4 mb-4">
            <div class="card h-100 shadow-sm border-0" style="border-radius: 20px;">
                <div style="background: white; border-radius: 20px 20px 0 0; padding: 15px; text-align: center;">
                    <img src="{img_src}" style="height: 150px; object-fit: contain;" alt="{c.name}">
                </div>
                <div class="card-body text-center">
                    <h5 class="fw-bold" style="color: #d81b60;">{c.name}</h5>
                    <p class="small text-muted mb-1">Actor: {c.actor}</p>
                    <p class="card-text">{c.description}</p>
                </div>
            </div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Peppa Pig Fanbase</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
        <style>
            body {{ background: #fce4ec; min-height: 100vh; }}
            .hero {{ background: #f06292; color: white; padding: 60px 0; text-align: center; margin-bottom: 40px; }}
        </style>
    </head>
    <body>
        <div class="hero">
            <h1 class="display-4 fw-bold">🐷 Peppa Pig Fanbase</h1>
            <p class="lead">Interactive Character Database</p>
        </div>
        <div class="container">
            <div class="row">{char_cards}</div>
        </div>
    </body>
    </html>
    """
