from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Note, User
from schemas import NoteCreate, NoteUpdate, NoteResponse
from auth import verify_token
from fastapi.security import OAuth2PasswordBearer
from typing import List

router = APIRouter(prefix="/notes", tags=["Notes"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Current user nikalo
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    email = verify_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user

# Sari notes dekho
@router.get("/", response_model=List[NoteResponse])
def get_notes(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Note).filter(Note.user_id == current_user.id).all()

# Note banao
@router.post("/", response_model=NoteResponse)
def create_note(note: NoteCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_note = Note(**note.dict(), user_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

# Note update karo
@router.put("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    for key, value in note.dict(exclude_unset=True).items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note

# Note delete karo
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_note = db.query(Note).filter(Note.id == note_id, Note.user_id == current_user.id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}

# Note search karo
@router.get("/search", response_model=List[NoteResponse])
def search_notes(q: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.query(Note).filter(
        Note.user_id == current_user.id,
        (Note.title.contains(q) | Note.content.contains(q))
    ).all()