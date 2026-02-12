from fastapi import HTTPException
from db.config import get_conexion
from models.users_models import UserCreate, UserLogin
import aiomysql as aio
from core.security import hash_password, verify_password, create_token
from controllers.users_controllers import get_user_id

async def register_user(user: UserCreate):
    #password sin hasear
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # aqui se hasea el password
            hashed_password = hash_password(user.password)
            await cursor.execute(
                "INSERT INTO InnoDB.users (name, surname, mail, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
                (user.name, user.surname, user.mail, hashed_password, user.role)
            )
            await conn.commit()
            new_id = cursor.lastrowid
            user = await get_user_id(new_id)
            return {'msg': 'Usuario registrado correctamente', 'item': user}
    except Exception as e:
        raise HTTPException(status_code=500, detail= f" Error: {str(e)}")
    finally:
        conn.close()

async def login_user(user_login : UserLogin):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.users WHERE mail=%s", (user_login.mail,)
                )
            user = await cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario o password incorrecto")
        if not verify_password(user_login.password, user['password_hash']):
            raise HTTPException(status_code=404, detail="Usuario o password incorrecto")
            # crear el token con los datos y funcion de security
        token_data = {
            "id_users": user['id_users'],
            "role": user['role']
        }
        token = create_token(token_data)
        return {'msg': 'Usuario logueado correctamente', 'token': token}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail= f" Error: {str(e)}")
    finally:
        conn.close()