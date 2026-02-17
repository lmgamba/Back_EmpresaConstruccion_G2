from datetime import datetime, timezone
from fastapi import HTTPException, Depends, Path
from fastapi.security import OAuth2PasswordBearer
from controllers.users_controllers import get_user_id
from core.security import decode_token

oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(token: str = Depends(oauth2)):
    # decodificar el token
    payload = decode_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Token inválido")
    expire = payload.get("expire")
    if not expire or expire < datetime.now(timezone.utc).timestamp():
        raise HTTPException(status_code=401, detail="Token expirado")
    user_id = payload.get("id_users")
    if not user_id:
        raise HTTPException(status_code=404, detail="Usuario no existe")

    # obtener los datos del usuario logado
    user = await get_user_id(user_id)
    return user


async def is_admin_or_owner(user=Depends(get_current_user), user_id: int = Path(...)):
    # si es admin
    if user["role"] == "admin":
        return user
    # si es el propietario
    if user["id_users"] == user_id:
        return user

    # si no es admin ni user no tiene acceso
    raise HTTPException(
        status_code=403, detail="No tienes permisos para realizar esta acción"
    )


async def is_admin(user=Depends(get_current_user)):
    if user["role"] == "admin":
        return user
    # si no es admin
    raise HTTPException(status_code=403, detail="No eres administrador")
