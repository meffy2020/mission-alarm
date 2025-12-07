from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    time_of_day = Column(String) # Format "HH:MM"
    is_active = Column(Boolean, default=True)

class Mission(Base):
    __tablename__ = "missions"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    type = Column(String) # "quiz", "puzzle", "image"
    content = Column(String) # JSON string or simple text for the question/data
    answer = Column(String) # The expected answer

class MissionLog(Base):
    __tablename__ = "mission_log"

    id = Column(Integer, primary_key=True, index=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    success = Column(Boolean, default=False)

    mission = relationship("Mission")