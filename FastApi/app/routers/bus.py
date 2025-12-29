from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas, database
from ..auth import get_current_user_token

router = APIRouter()

@router.post("/{route_id}/location", response_model=schemas.BusLocationOut)
def update_location(route_id: int, location: schemas.BusLocationCreate, db: Session = Depends(database.get_db), u=Depends(get_current_user_token)):
    # Optional role check: only driver or admin
    if u["role"] not in {"driver", "admin"}:
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if not route:
        raise HTTPException(status_code=404, detail="Route not found")

    loc = models.BusLocation(
        route_id=route_id,
        latitude=location.latitude,
        longitude=location.longitude,
        timestamp=location.timestamp or datetime.utcnow(),
    )
    db.add(loc)
    db.commit()
    db.refresh(loc)
    return loc

@router.get("/{route_id}/location", response_model=list[schemas.BusLocationOut])
def get_locations(route_id: int, db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    return db.query(models.BusLocation).filter(models.BusLocation.route_id == route_id).order_by(models.BusLocation.timestamp.desc()).all()

@router.get("/{route_id}/location/latest", response_model=schemas.BusLocationOut)
def get_latest_location(route_id: int, db: Session = Depends(database.get_db), _u=Depends(get_current_user_token)):
    loc = (
        db.query(models.BusLocation)
        .filter(models.BusLocation.route_id == route_id)
        .order_by(models.BusLocation.timestamp.desc())
        .first()
    )
    if not loc:
        raise HTTPException(status_code=404, detail="No location found")
    return loc

