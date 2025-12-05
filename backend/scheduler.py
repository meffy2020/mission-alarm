from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from .database import SessionLocal
from . import models, kakao_service
from datetime import datetime

scheduler = BackgroundScheduler()

def check_schedules_and_send_notifications():
    """
    This job runs every minute. It checks the database for schedules that match the current time.
    """
    print(f"Checking schedules at {datetime.now().strftime('%H:%M')}...")
    db: Session = SessionLocal()
    try:
        current_time = datetime.now().strftime("%H:%M")
        schedules = db.query(models.Schedule).filter(models.Schedule.time_of_day == current_time, models.Schedule.is_active == True).all()
        
        for schedule in schedules:
            # In a real app, you'd get the user's specific token. 
            # For now, we use the global env token for simplicity or assume the user is the admin.
            print(f"Triggering schedule for user {schedule.user_id} at {current_time}")
            kakao_service.send_kakao_message(f"⏰ 미션 시간입니다! 지금 바로 도전하세요.")
            
    except Exception as e:
        print(f"Scheduler Error: {e}")
    finally:
        db.close()

def start_scheduler():
    scheduler.add_job(check_schedules_and_send_notifications, 'interval', minutes=1)
    scheduler.start()
