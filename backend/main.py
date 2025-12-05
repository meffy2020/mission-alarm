from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from .database import engine, Base, SessionLocal
from .routers import auth, schedule, mission, sensor
from .scheduler import start_scheduler
from . import models, serial_service

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mission Alarm")

app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

templates = Jinja2Templates(directory="frontend/templates")

app.include_router(auth.router)
app.include_router(schedule.router)
app.include_router(mission.router)
app.include_router(sensor.router)

@app.on_event("startup")
def startup_event():
    start_scheduler()
    serial_service.start_serial_reader()
    
    # Initialize some dummy missions if empty
    db = SessionLocal()
    if db.query(models.Mission).count() == 0:
        dummy_missions = [
            models.Mission(
                title="수학 퀴즈", 
                description="간단한 덧셈 문제입니다.", 
                type="quiz", 
                content='{"question": "15 + 27 = ?", "options": ["32", "42", "45", "52"]}', 
                answer="42"
            ),
            models.Mission(
                title="거리 조절 훈련", 
                description="초음파 센서에 손을 가까이 대세요!", 
                type="sensor", 
                content='{"sensor_type": "distance", "condition": "lower", "threshold": 10, "unit": "cm", "guide": "손을 10cm 이내로 가져가세요."}', 
                answer="sensor_check"
            ),
            models.Mission(
                title="암전 미션", 
                description="센서를 가려 어둡게 만드세요.", 
                type="sensor", 
                content='{"sensor_type": "ldr", "condition": "lower", "threshold": 200, "unit": "lux", "guide": "조도 센서를 손으로 덮어 200 이하로 만드세요."}', 
                answer="sensor_check"
            ),
             models.Mission(
                title="멀리 떨어지기", 
                description="센서에서 손을 멀리 치우세요.", 
                type="sensor", 
                content='{"sensor_type": "distance", "condition": "higher", "threshold": 50, "unit": "cm", "guide": "센서 앞을 50cm 이상 비우세요."}', 
                answer="sensor_check"
            ),
            models.Mission(
                title="섬광탄 투척! 💣", 
                description="스마트폰 플래시로 센서를 공격하세요!", 
                type="sensor", 
                content='{"sensor_type": "ldr", "condition": "higher", "threshold": 800, "unit": "lux", "guide": "조도 센서에 강한 빛을 쏘세요! (800 lux 이상)"}', 
                answer="sensor_check"
            ),
            models.Mission(
                title="ET와의 교신 👽", 
                description="손가락을 정확한 위치에 두세요.", 
                type="sensor", 
                content='{"sensor_type": "distance", "condition": "range", "min": 15, "max": 20, "unit": "cm", "guide": "센서와의 거리를 15cm ~ 20cm 사이로 유지하세요."}', 
                answer="sensor_check"
            ),
            models.Mission(
                title="투명인간 모드 👻", 
                description="센서가 아무것도 못 보게 만드세요.", 
                type="sensor", 
                content='{"sensor_type": "distance", "condition": "higher", "threshold": 100, "unit": "cm", "guide": "센서를 허공으로 돌려 1m 이상 공간을 확보하세요."}', 
                answer="sensor_check"
            )
        ]
        db.add_all(dummy_missions)
        db.commit()
    db.close()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
