
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from ..db import SessionLocal
from .. import models, schemas, security

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", status_code=201)
def register(payload: schemas.RegisterRequest, db: Session = Depends(get_db)):
    if db.execute(select(models.User).where(models.User.email == payload.email)).scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = models.User(email=payload.email, password_hash=security.hash_password(payload.password))
    db.add(user)
    db.commit()
    return {"ok": True}

@router.post("/login", response_model=schemas.TokenResponse)
def login(payload: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.execute(select(models.User).where(models.User.email == payload.email)).scalar_one_or_none()
    if not user or not security.verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = security.create_access_token(subject=str(user.id))
    return {"access_token": token, "token_type": "bearer"}
