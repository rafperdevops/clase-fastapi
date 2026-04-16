import time
import base64
import random
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models.user_model import User
from services.email_service import send_otp_email


def create_token(email: str) -> str:
    token = f"{email}:{int(time.time())}"
    return "Bearer " + base64.b64encode(token.encode()).decode()


class AuthController:
    @staticmethod
    def request_otp(email: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user:
            user = User(email=email)
            db.add(user)
        
        otp = str(random.randint(100000, 999999))
        user.otp_code = otp
        user.otp_expires_at = datetime.utcnow() + timedelta(minutes=5)
        db.commit()
        
        send_otp_email(email, otp)
        return {"message": "Código enviado a tu correo"}

    @staticmethod
    def verify_otp(email: str, otp: str, db: Session):
        user = db.query(User).filter(User.email == email).first()
        if not user or not user.otp_code:
            return None
        
        if user.otp_expires_at and user.otp_expires_at < datetime.utcnow():
            return None
        
        if user.otp_code == otp:
            user.otp_code = None
            user.otp_expires_at = None
            db.commit()
            return {"user": user, "token": create_token(email)}
        
        return None