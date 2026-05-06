from fastapi import FastAPI
from database import engine, Base
from routers import users, notes

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Personal Notes API",
    description="A secure notes app with JWT authentication",
    version="1.0.0"
)
# test comment
app.include_router(users.routerssssssssss)

app.include_router(notes.router)


# separate both
@app.get("/")
def root():
    return {"message": "Welcome to Notes API! 📝"}

#hi
@app.post("/")
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    new_post = Post(title=post.title, content=post.content, user_id=1)
    db.add(new_post)
    db.commit()     
    db.refresh(new_posts)
    return new_post