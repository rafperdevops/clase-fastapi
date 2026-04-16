import base64
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from models.user_model import User


PUBLIC_PATHS = ["/auth/request-otp", "/auth/verify-otp", "/docs"]


class AuthenticationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if any(request.url.path.startswith(path) for path in PUBLIC_PATHS):
            return await call_next(request)

        auth_header = request.headers.get("authorization")
        if not auth_header:
            return JSONResponse(
                status_code=401,
                content={"detail": "No autenticado"}
            )

        try:
            auth_decoded = base64.b64decode(auth_header.replace("Bearer ", "")).decode()
            email = auth_decoded.split(":")[0]
        except:
            return JSONResponse(
                status_code=401,
                content={"detail": "Token inválido"}
            )

        db = SessionLocal()
        user = db.query(User).filter(User.email == email).first()
        db.close()

        if not user:
            return JSONResponse(
                status_code=401,
                content={"detail": "Usuario no encontrado"}
            )

        request.state.user = user
        return await call_next(request)