import aiomysql as aio
from core.security import hash_password
from db.config import get_conexion
from fastapi import HTTPException
from models.users_models import User, UserCreate, UserUpdate

# ADMIN OBTIENE USUARIOS POR ID
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
    exist = await search_mail(user.mail)
    if not exist:
        try:
            conn = await get_conexion()
            async with conn.cursor(aio.DictCursor) as cursor:
            # verificar si el correo existe
            #hasear el password
                hashed_password = hash_password(user.password)
                await cursor.execute(
                    " INSERT INTO InnoDB.users (name, surname, mail, password_hash, role) VALUES (%s, %s, %s, %s, %s)",
                    (user.name, user.surname, user.mail, hashed_password, 'user')
                )
                await conn.commit()
                new_id = cursor.lastrowid
                return await get_user_id(new_id)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        raise HTTPException(status_code=400, detail="El correo ya existe")


# ADMIN ACTUALIZA USUARIOS
async def update_user(user_id: int, user: UserUpdate):
    exist = await get_user_id(user_id)
    if exist:
        try:
            new_name = user.name if user.name is not None else exist['name']
            new_surname = user.surname if user.surname is not None else exist['surname']
            new_mail = user.mail if user.mail is not None else exist['mail']
            
            conn = await get_conexion()
            async with conn.cursor(aio.DictCursor) as cursor:
                await cursor.execute(
                " UPDATE InnoDB.users SET name=%s, surname=%s, mail=%s WHERE id_users=%s ", (new_name, new_surname, new_mail, user_id)
            )
                await conn.commit()
                
            exist['name'] =new_name
            exist['surname'] =new_surname
            exist['mail'] =new_mail
            return {"Mensaje": "Usuario actualizado correctamente", "item": exist}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        raise HTTPException(status_code=404, detail="Usuario no existe")

#ADMIN ELIMINA USUARIOS
async def delete_user(user_id: int):
    exist = await get_user_id(user_id)
    if exist:
        try:
            conn = await get_conexion()
            async with conn.cursor(aio.DictCursor) as cursor:        
                await cursor.execute("DELETE FROM InnoDB.users WHERE id_users=%s", (user_id,))
                await conn.commit()
            return {'msg': 'Usuario eliminado correctamente', "item": exist}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
        finally:
            conn.close()
    else:
        raise HTTPException(status_code=404, detail="Usuario no existe") 
    
    
# TODO:  DESACTIVA USER

async def deactivate_user(user_id: int, status: bool):
        pass
# ENCONTRAR USUARIO POR CORREO
async def search_mail(mail: str):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.users WHERE mail LIKE %s", (f"%{mail}%")
            )
            user = await cursor.fetchone()
            if user is None:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return user
    except Exception as e:
        raise HTTPException(status_code=500 , detail=f"Error: {str(e)}")
    finally:
        conn.close()