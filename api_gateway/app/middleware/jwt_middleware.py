from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from app.auth.jwt_utils import decode_token
from fastapi.routing import APIRoute

OPEN_PATHS = {"/login", "/register", "/docs"}

class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        path = request.url.path

        if request.method == "OPTIONS":
            return await call_next(request)
        
        if any(path == p or path.startswith("/docs") for p in OPEN_PATHS):
            return await call_next(request)

        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return JSONResponse({"detail": "Not authenticated"}, status_code=401)

        token = auth.split(" ", 1)[1].strip()
        try:
            payload = decode_token(token)
        except Exception:
            return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)

        request.state.user = {"sub": payload.get("sub"), "email": payload.get("email")}
        return await call_next(request)
