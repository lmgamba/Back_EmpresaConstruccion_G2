import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.logs_models import LogCreate
from core.email_config import send_email
import os

# CREAR UN LOG
async def create_log(user_id: int, log, background_tasks):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            
            # Obtener datos del Operario que crea el log (para el cuerpo del mail)
            await cursor.execute(
                "SELECT name, surname FROM InnoDB.users WHERE id_users=%s",
                (user_id,)
            )
            user = await cursor.fetchone()
            
            # Verificar que la construcción esté activa
            await cursor.execute(
                "SELECT status FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (log.constructionsSites_id,)
            )
            construction_status = await cursor.fetchone()
            if not construction_status or construction_status['status'] != 'active':
                raise HTTPException(status_code=400, detail="La obra no está activa. No puedes crear logs para ella.")
            
            # Verificar que el usuario esté asignado a esta obra
            await cursor.execute("""
                SELECT COUNT(*) AS count 
                FROM InnoDB.assignments 
                WHERE users_id=%s AND constructionsSites_id=%s
            """, (user_id, log.constructionsSites_id))
            result = await cursor.fetchone()
            if result['count'] == 0:
                raise HTTPException(status_code=403, detail="No estás asignado a esta obra. No puedes crear logs para ella.")
            
            # Insertar el log
            await cursor.execute("""
                INSERT INTO InnoDB.logs 
                (description, type, users_id, constructionsSites_id)
                VALUES (%s, %s, %s, %s)
            """, (
                log.description,
                log.type,
                user_id,
                log.constructionsSites_id
            ))
            await conn.commit()
            

            # Obtener datos de la Obra (para el cuerpo del mail)
            await cursor.execute(
                "SELECT name FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (log.constructionsSites_id,)
            )
            construction = await cursor.fetchone()
            
            # QUERY CLAVE: Buscar el mail del Administrador asignado a esta obra
            # Se busca en tabla assigment el unico con rol 'admin' de esta obra específica
            await cursor.execute("""
                SELECT u.mail, u.name 
                FROM InnoDB.users u
                JOIN InnoDB.assignments a ON u.id_users = a.users_id
                WHERE a.constructionsSites_id = %s 
                AND u.role = 'admin'
                LIMIT 1
            """, (log.constructionsSites_id,))
            
            admin = await cursor.fetchone()

            # 5. Si encontramos un admin, enviamos la tarea de correo
            if admin:
                subject = f"🔔 Nuevo Log: {construction['name']}"
                body = f"""
Hola {admin['name']},

Se ha registrado una nueva actividad en una obra bajo tu supervisión:

Obra: {construction['name']}
Registrado por: {user['name']} {user['surname']} (ID: {user_id})
Tipo de log: {log.type}
Descripción: {log.description}

Saludos,
Sistema de Gestión de Obras.
"""
                # Enviamos el mail al correo del ADMIN encontrado
                background_tasks.add_task(send_email, admin["mail"], subject, body)
            
            return {"msg": "Log creado correctamente y notificado al administrador"}

    except Exception as e:
        print(f"ERROR EN CONTROLADOR LOGS: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

# LISTAR LOGS POR OBRA
async def get_logs_by_construction(constructionsSites_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.logs WHERE constructionsSites_id=%s ORDER BY date_register DESC", (constructionsSites_id,)
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