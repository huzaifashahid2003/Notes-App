from fastapi import FastAPI
from database import engine, Base
from routers import users, notes

# Database tables banao
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Personal Notes API",
    description="A secure notes app with JWT authentication",
    version="1.0.0"
)

# Routers add karo
app.include_router(users.router)
app.include_router(notes.router)

@app.get("/")
def root():
    return {"message": "Welcome to Notes API! 📝"}