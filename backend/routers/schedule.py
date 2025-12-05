from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud, auth, database

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)

@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return crud.get_schedules(db, user_id=current_user.id)

@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    return crud.create_schedule(db=db, schedule=schedule, user_id=current_user.id)

@router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(database.get_db)):
    schedule = crud.delete_schedule(db, schedule_id=schedule_id, user_id=current_user.id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule
