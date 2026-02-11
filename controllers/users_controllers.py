import aiomysql as aio
from core.security import hash_password
from db.config import get_conexion
from fastapi import HTTPException
from models.users_models import User, UserCreate, UserUpdate

async def get_user_id(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.users WHERE id_users=%s", (user_id,)
            )
            user = await cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return user
    except Exception as e:
        raise HTTPException(status_code=500 , detail=f"Error: {str(e)}")
    finally:
        conn.close()
        

# ADMIN OBTIENE TODOS LOS USUARIOS
async def get_all_users():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("SELECT * FROM InnoDB.users WHERE role = 'user'")
            lista = await cursor.fetchall()
            return lista
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# ADMINISTRADOR CREA USUARIOS
async def create_user(user: UserCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # verificar si el correo existe
            await cursor.execute(
                "SELECT id_users FROM InnoDB.users WHERE mail=%s", (user.mail,)
            )
            existing_user = await cursor.fetchone()
            if existing_user:
                raise HTTPException(status_code=400, detail="El correo ya existe")
            #hasear el password
            hashed_password = hash_password(user.password)
            await cursor.execute(
                " INSERT INTO InnoDB.users (name, surname, mail, password, role) VALUES (%s, %s, %s, %s, %s)",
                (user.name, user.surname, user.mail, hashed_password, 'user')
            )
            await conn.commit()
            new_id = cursor.lastrowid
            return await get_user_id(new_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# ADMIN ACTUALIZA USUARIOS
async def update_user(user_id: int, user: UserUpdate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                " SELECT id_users FROM InnoDB.users WHERE id_users=%s AND role='user'", (user_id,)
            )
            existing_user = await cursor.fetchone()
            if not existing_user:
                raise HTTPException(status_code=404, detail="Usuario no existe")
            await cursor.execute(
                " UPDATE InnoDB.users SET name=%s, surname=%s, mail=%s WHERE id_users=%s ", (user.name, user.surname, user.mail, user_id)
            )
            await conn.commit()
            return await get_user_id(user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

#ADMIN ELIMINA USUARIOS
async def delete_user(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id_users FROM InnoDB.users WHERE id_users=%s AND role='user'", (user_id,)
            )
            existing_user = await cursor.fetchone()
            if not existing_user:
                raise HTTPException(status_code=404, detail="Usuario no existe")
            
            await cursor.execute(
                "DELETE FROM InnoDB.users WHERE id_users=%s", (user_id,)
            )
            await conn.commit()
            return {'msg': 'Usuario eliminado correctamente'}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()