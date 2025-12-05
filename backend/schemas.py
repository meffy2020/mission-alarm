from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class ScheduleBase(BaseModel):
    time_of_day: str
    is_active: bool = True

class ScheduleCreate(ScheduleBase):
    pass

class Schedule(ScheduleBase):
    id: int
    user_id: int
    class Config:
        orm_mode = True

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
        orm_mode = True

class MissionLogBase(BaseModel):
    mission_id: int
    success: bool

class MissionLogCreate(MissionLogBase):
    pass

class MissionLog(MissionLogBase):
    id: int
    user_id: int
    completed_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
