from sqlalchemy.orm import Session
from . import models, schemas

def get_schedules(db: Session):
    return db.query(models.Schedule).all()

def create_schedule(db: Session, schedule: schemas.ScheduleCreate):
    db_schedule = models.Schedule(**schedule.dict())
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def delete_schedule(db: Session, schedule_id: int):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if db_schedule:
        db.delete(db_schedule)
        db.commit()
    return db_schedule

def get_random_mission(db: Session):
    # Simple random fetch. Ideally use func.random() but let's keep it simple
    import random
    missions = db.query(models.Mission).all()
    if not missions:
        return None
    return random.choice(missions)

def create_mission_log(db: Session, log: schemas.MissionLogCreate):
    db_log = models.MissionLog(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log