from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.base import SessionLocal
from database.models import User

router = APIRouter(prefix="/api", tags=["http-api"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/hello")
def hello():
    return {
        "code": 0,
        "msg": "Hello FastAPI HTTP!",
        "data": "This is a simple HTTP response"
    }


@router.post("/users/")
def create_user(username: str, db: Session = Depends(get_db)):
    user = User(username=username)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
