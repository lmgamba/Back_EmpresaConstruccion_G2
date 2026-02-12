import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.logs_models import LogCreate
from core.email_config import send_email
import os

#CREAR UN LOG
async def create_log(user_id: int, log):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute("""
                INSERT INTO InnoDB.logs 
                (description, type, user_id, constructionsSites_id)
                VALUES (%s, %s, %s, %s)
            """, (
                log.description,
                log.type,
                user_id,
                log.construction_id
            ))
            await conn.commit()
            subject = "Nuevo log registrado"
            body = f"""
Se ha registrado un nuevo log:

Usuario ID: {user_id}
Obra ID: {log.construction_id}
Tipo: {log.type}
Descripción: {log.description}
"""
            await send_email(os.getenv("ADMIN_EMAIL"), subject, body)
            return {"msg": "Log creado y email enviado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# LISTAR LOGS POR OBRA
async def get_logs_by_construction(construction_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.logs WHERE constructionsSites_id=%s ORDER BY date_register DESC", (construction_id,)
            )
            logs = await cursor.fetchall()
            return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# LISTAR LOGS POR USUARIO
async def get_logs_by_user(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.logs WHERE user_id=%s ORDER BY date_register DESC", (user_id,)
            )
            logs = await cursor.fetchall()
            return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()