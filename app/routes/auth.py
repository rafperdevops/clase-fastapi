from pydantic import BaseModel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.controllers.auth_controller import AuthController


class RequestOtpSchema(BaseModel):
    email: str


class VerifyOtpSchema(BaseModel):
    email: str
    otp: str


router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/request-otp")
def request_otp(data: RequestOtpSchema, db: Session = Depends(get_db)):
    return AuthController.request_otp(data.email, db)


@router.post("/verify-otp")
def verify_otp(data: VerifyOtpSchema, db: Session = Depends(get_db)):
    result = AuthController.verify_otp(data.email, data.otp, db)
    if not result:
        return {"error": "Código inválido o expirado"}, 401
    return {"message": "Logueado exitosamente", "email": result["user"].email, "token": result["token"]}