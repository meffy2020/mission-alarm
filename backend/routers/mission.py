from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from .. import models, schemas, crud, database, serial_service, kakao_service # Import kakao_service
import json

router = APIRouter(
    prefix="/mission",
    tags=["mission"],
)

templates = Jinja2Templates(directory="frontend/templates")

@router.get("/start", response_class=HTMLResponse)
def mission_start_page(request: Request):
    return templates.TemplateResponse("mission_start.html", {"request": request})

@router.get("/play", response_class=HTMLResponse)
def mission_play_page(request: Request):
    return templates.TemplateResponse("mission_play.html", {"request": request})

@router.get("/success", response_class=HTMLResponse)
def mission_success_page(request: Request):
    return templates.TemplateResponse("mission_success.html", {"request": request})

@router.get("/data/random", response_model=schemas.Mission)
def get_random_mission_data(db: Session = Depends(database.get_db)):
    mission = crud.get_random_mission(db)
    if not mission:
         # Fallback if DB is empty
        return schemas.Mission(
            id=0, 
            title="기본 숫자 퀴즈", 
            description="다음 문제를 푸세요.", 
            type="quiz", 
            content='{"question": "12 + 34 = ?", "options": ["44", "46", "56", "48"]}', 
            answer="46"
        )
    return mission

@router.post("/log", response_model=schemas.MissionLog)
def log_mission_attempt(log: schemas.MissionLogCreate, db: Session = Depends(database.get_db)):
    # Server-side validation for sensor missions
    mission = db.query(models.Mission).filter(models.Mission.id == log.mission_id).first()
    
    if mission and mission.type == "sensor" and log.success:
        content = json.loads(mission.content)
        sensor_type = content.get("sensor_type")
        threshold = float(content.get("threshold", 0))
        condition = content.get("condition")
        
        current_data = serial_service.latest_sensor_data
        current_val = 0.0
        
        if sensor_type == "distance":
            current_val = current_data["distance"]
        elif sensor_type == "ldr":
            current_val = float(current_data["ldr"])
            
        # Verify condition
        is_valid = False
        if condition == "lower" and current_val < threshold:
            is_valid = True
        elif condition == "higher" and current_val > threshold:
            is_valid = True
        elif condition == "range":
            min_val = float(content.get("min", 0))
            max_val = float(content.get("max", 100))
            if min_val <= current_val <= max_val:
                is_valid = True
            
        if not is_valid:
             # Reject if sensor value doesn't match (Strict Mode)
             print(f"Mission Failed: {current_val} is not {condition} than {threshold}")
             log.success = False
             # Send Kakao message for sensor failure
             kakao_service.send_kakao_message(message_text=f"🚨 미션 실패 (센서): {current_val} {content.get('unit')} 값이 조건({condition} {threshold})에 맞지 않습니다.")
    
    db_log = crud.create_mission_log(db, log) # Store the result in a variable

    if not db_log.success:
        # Send Kakao message for any mission failure (e.g., quiz failure)
        # Only send if not already sent by sensor failure logic above
        if not (mission and mission.type == "sensor" and not is_valid):
            kakao_service.send_kakao_message(message_text=f"🚨 미션 실패: '{mission.title}' 미션을 통과하지 못했습니다.")
    
    return db_log
