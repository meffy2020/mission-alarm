from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas, crud, database

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)

@router.get("/", response_model=List[schemas.Schedule])
def read_schedules(db: Session = Depends(database.get_db)):
    return crud.get_schedules(db)

@router.post("/", response_model=schemas.Schedule)
def create_schedule(schedule: schemas.ScheduleCreate, db: Session = Depends(database.get_db)):
    return crud.create_schedule(db=db, schedule=schedule)

@router.delete("/{schedule_id}", response_model=schemas.Schedule)
def delete_schedule(schedule_id: int, db: Session = Depends(database.get_db)):
    schedule = crud.delete_schedule(db, schedule_id=schedule_id)
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule