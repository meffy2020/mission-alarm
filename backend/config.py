from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str
    
    KAKAO_API_KEY: str
    KAKAO_REDIRECT_URI: str
    KAKAO_TOKEN_URL: str
    KAKAO_API_URL: str
    KAKAO_ACCESS_TOKEN: str = "" # Optional for simple testing

    SERIAL_PORT: str = "/dev/cu.usbmodem1101" # Default for Mac, change as needed
    SERIAL_BAUDRATE: int = 9600

    class Config:
        env_file = ".env"

settings = Settings()
