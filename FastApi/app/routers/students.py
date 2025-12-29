from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user_token

router = APIRouter()

@router.post("/", response_model=schemas.StudentOut)
def create_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    db_student = models.Student(name=student.name, grade=student.grade)
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@router.get("/", response_model=list[schemas.StudentOut])
def list_students(db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    return db.query(models.Student).all()
