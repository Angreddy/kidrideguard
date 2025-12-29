from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas, database
from ..auth import get_current_user_token

router = APIRouter()

@router.post("/", response_model=schemas.RouteOut)
def create_route(route: schemas.RouteCreate, db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    db_route = models.Route(**route.dict())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route

@router.get("/", response_model=list[schemas.RouteOut])
def list_routes(db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    return db.query(models.Route).all()

@router.get("/{route_id}", response_model=schemas.RouteOut)
def get_route(route_id: int, db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")
    return route
