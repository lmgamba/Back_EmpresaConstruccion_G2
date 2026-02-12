import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.assignments_models import AssignmentCreate


# CREAR ASIGNACIÓN (ADMIN)
async def create_assignment(assignment: AssignmentCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            #verificar usuario existe y es operario
            await cursor.execute(
                "SELECT id_users FROM InnoDB.users WHERE id_users=%s AND role='user'",
                (assignment.users_id,)
            )
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no existe")
            # verificar obra existe
            await cursor.execute(
                "SELECT id_constructions FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (assignment.constructionsSites_id,)
            )
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Obra no existe")
            # verificar que no tenga asignación activa en esa obra
            await cursor.execute(
                "SELECT id_assignments FROM InnoDB.assignments WHERE users_id=%s AND constructionsSites_id=%s AND status='active'", (assignment.users_id, assignment.constructionsSites_id)
            )
            if await cursor.fetchone():
                raise HTTPException(status_code=400, detail="Ya tiene asignación activa en esta obra")
            # crear asignación
            await cursor.execute(
                "INSERT INTO InnoDB.assignments (date_start, date_finish, status, users_id, constructionsSites_id)VALUES (%s, %s, 'active', %s, %s)", (assignment.date_start, assignment.date_finish, 
                assignment.users_id, assignment.constructionsSites_id)
            )
            await conn.commit()
            return {"msg": "Asignación creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
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
