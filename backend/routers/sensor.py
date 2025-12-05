from fastapi import APIRouter
from .. import serial_service

router = APIRouter(
    prefix="/sensor",
    tags=["sensor"],
)

@router.get("/current")
def get_current_sensor_data():
    return serial_service.latest_sensor_data
