from sqlalchemy.orm import Session
from . import models, schemas, auth

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_schedules(db: Session, user_id: int):
    return db.query(models.Schedule).filter(models.Schedule.user_id == user_id).all()

def create_schedule(db: Session, schedule: schemas.ScheduleCreate, user_id: int):
    db_schedule = models.Schedule(**schedule.dict(), user_id=user_id)
    db.add(db_schedule)
    db.commit()
    db.refresh(db_schedule)
    return db_schedule

def delete_schedule(db: Session, schedule_id: int, user_id: int):
    db_schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id, models.Schedule.user_id == user_id).first()
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

def create_mission_log(db: Session, log: schemas.MissionLogCreate, user_id: int):
    db_log = models.MissionLog(**log.dict(), user_id=user_id)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log
