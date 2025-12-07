from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ScheduleBase(BaseModel):
    time_of_day: str
    is_active: bool = True

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    class Config:
        from_attributes = True

class MissionBase(BaseModel):
    title: str
    description: str
    type: str
    content: str
    answer: str

class MissionCreate(MissionBase):
    pass

class Mission(MissionBase):
    id: int
    class Config:
        from_attributes = True

class MissionLogBase(BaseModel):
    mission_id: int
    success: bool

class MissionLogCreate(MissionLogBase):
    pass

class MissionLog(MissionLogBase):
    id: int
    completed_at: datetime
    class Config:
        from_attributes = True