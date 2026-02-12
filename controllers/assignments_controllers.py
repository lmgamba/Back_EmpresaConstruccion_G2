import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.assignments_models import AssignmentCreate
from core.email_config import send_email


# CREAR ASIGNACIÓN (ADMIN)
async def create_assignment(assignment):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # Insertar asignación
            await cursor.execute("""
                INSERT INTO InnoDB.assignments 
                (users_id, constructionsSites_id, date_start, date_finish, status)
                VALUES (%s, %s, %s, %s, 'activo')
            """, (
                assignment.user_id,
                assignment.construction_id,
                assignment.date_start,
                assignment.date_finish
            ))
            await conn.commit()
            new_id = cursor.lastrowid
            # Obtener datos usuario
            await cursor.execute(
                "SELECT name, mail FROM InnoDB.users WHERE id_users=%s",
                (assignment.user_id,)
            )
            user = await cursor.fetchone()
            # Obtener datos obra
            await cursor.execute(
                "SELECT name, address FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (assignment.construction_id,)
            )
            construction = await cursor.fetchone()
            # Enviar email
            subject = f"Nueva asignación: {construction['name']}"
            body = f"""
Hola {user['name']},

Has sido asignado a la obra:

Nombre: {construction['name']}
Dirección: {construction['address']}
Fecha inicio: {assignment.date_start}
Fecha fin: {assignment.date_finish or 'No definida'}

Saludos.
"""
            await send_email(user["mail"], subject, body)
            return {"msg": "Asignación creada y email enviado", "assignment_id": new_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# OBTENER ASIGNACIONES POR USUARIO (ADMIN O USUARIO)
async def get_assignments_by_user(user_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT a.*, c.name AS construction_name
                FROM InnoDB.assignments a
                JOIN InnoDB.constructionsSites c
                ON a.constructionsSites_id = c.id_constructions
                WHERE a.users_id=%s
                """,
                (user_id,)
            )
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# FINALIZAR ASIGNACIÓN (ADMIN O USUARIO)
async def finish_assignment(assignment_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id_assignments FROM InnoDB.assignments WHERE id_assignments=%s", (assignment_id,)
            )
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Asignación no existe")
            await cursor.execute(
                "UPDATE InnoDB.assignments SET status='finished' WHERE id_assignments=%s", (assignment_id,)
            )
            await conn.commit()
            return {"msg": "Asignación finalizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
