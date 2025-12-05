import requests
import json
from .config import settings

def send_kakao_message(message_text: str, web_url: str = "http://localhost:8000/mission/start"):
    """
    Sends a message to the current user using KakaoTalk "Send to Me" API.
    Requires a valid ACCESS_TOKEN in settings.
    """
    header = {"Authorization": f"Bearer {settings.KAKAO_ACCESS_TOKEN}"}
    url = settings.KAKAO_API_URL
    
    post = {
        "object_type": "text",
        "text": message_text,
        "link": {
            "web_url": web_url,
            "mobile_web_url": web_url
        },
        "button_title": "미션 하러 가기"
    }
    
    data = {"template_object": json.dumps(post)}
    
    try:
        response = requests.post(url, headers=header, data=data)
        if response.status_code == 200:
            print("Kakao message sent successfully.")
            return True
        else:
            print(f"Failed to send Kakao message: {response.status_code} {response.text}")
            return False
    except Exception as e:
        print(f"Error sending Kakao message: {e}")
        return False
