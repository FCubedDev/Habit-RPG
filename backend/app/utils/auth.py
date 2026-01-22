from clerk_backend_api import Clerk
from clerk_backend_api.security import authenticate_request
from clerk_backend_api.security.types import AuthenticateRequestOptions
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.config import settings
from app.database import get_db
from app.models import User

# Inicializar el SDK
sdk = Clerk(bearer_auth=settings.clerk_secret_key)

# Definir el esquema de seguridad para Swagger
security = HTTPBearer()

async def get_current_user_id(
    request: Request, 
    auth: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Verifica el token usando el SDK oficial de Clerk.
    Lanza una excepción 401 si el token no es válido.
    """
    request_state = sdk.authenticate_request(
        request,
        AuthenticateRequestOptions()
    )
    
    if not request_state.is_signed_in:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"No autorizado: {request_state.reason}"
        )
    
    return request_state.payload.get("sub")

async def get_optional_user_id(
    request: Request,
    auth: HTTPAuthorizationCredentials | None = Depends(HTTPBearer(auto_error=False))
) -> str | None:
    """
    Versión opcional de get_current_user_id.
    Devuelve None si el usuario no está autenticado en lugar de lanzar error.
    """
    request_state = sdk.authenticate_request(
        request,
        AuthenticateRequestOptions()
    )
    
    if not request_state.is_signed_in:
        return None
        
    return request_state.payload.get("sub")

async def get_current_user(
    clerk_user_id: str = Depends(get_current_user_id), db: Session = Depends(get_db)) -> User:
    """
    Obtiene el usuario completo de nuestra base de datos basado en el ID de Clerk.
    """
    user = db.query(User).filter(User.clerk_user_id == clerk_user_id).first()
    
    if not user:
        # 1. Pedir todos los detalles del usuario al SDK de Clerk
        clerk_user = sdk.users.get(user_id=clerk_user_id)
        
        # 2. Extraer los datos que necesitamos
        email = clerk_user.email_addresses[0].email_address if clerk_user.email_addresses else f"{clerk_user_id}@no-email.com"
        username = clerk_user.username or "NewHero"
        # 3. Crear el usuario en nuestra base de datos local
        user = User(
            clerk_user_id=clerk_user_id,
            email=email,
            username=username,
            global_xp=0,
            global_level=1,
            coins=0
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    return user