from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import get_current_user_token

from app import database, models, schemas
from ..auth import verify_password, hash_password, create_access_token

router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    print(f"DEBUG: received password={user.password!r}, length={len(user.password)}")
    exists = db.query(models.User).filter(models.User.username == user.username).first()
    if exists:
        raise HTTPException(status_code=400, detail="Username already exists")
    db_user = models.User(username=user.username, hashed_password=hash_password(user.password), role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=schemas.Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.username == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Create JWT (only needs username)
    token = create_access_token({"sub": user.username})

    # ✅ Include role in response
    return {
        "access_token": token,
        "token_type": "bearer",
        "role": user.role
    }


# NEW: GET all users
@router.get("/", response_model=list[schemas.UserListOut])
def get_users(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user_token)
):
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="Admins only")
    return db.query(models.User).all()


'''
@router.get("/", response_model=list[dict]) 
def get_allusers(db: Session = Depends(get_db)): 
    users = db.query(models.User).all() 
    return [{"id": u.id, "username": u.username, "role": u.role} for u in users]

'''

