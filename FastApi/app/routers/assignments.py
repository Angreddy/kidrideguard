from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, database, schemas
from ..auth import get_current_user_token

router = APIRouter()

@router.post("/{student_id}/{route_id}", response_model=schemas.AssignmentOut)
def assign_student(student_id: int, route_id: int, db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    assigned_count = db.query(models.Assignment).filter(models.Assignment.route_id == route_id).count()
    if assigned_count >= route.capacity:
        raise HTTPException(status_code=400, detail="Route capacity reached")

    assignment = models.Assignment(student_id=student_id, route_id=route_id)
    db.add(assignment)
    db.commit()
    db.refresh(assignment)
    return assignment
