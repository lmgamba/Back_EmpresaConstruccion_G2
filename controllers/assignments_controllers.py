import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.assignments_models import AssignmentCreate
from core.email_config import send_email
from datetime import date # Importante para obtener la fecha actual


# CREAR ASIGNACIÓN (ADMIN)

async def create_assignment(assignment: AssignmentCreate, background_tasks):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # 1. Validar que date_finish no sea antes que date_start
            if (
                assignment.date_finish
                and assignment.date_finish < assignment.date_start
            ):
                raise HTTPException(
                    status_code=400,
                    detail="La fecha de fin no puede ser anterior a la fecha de inicio",
                )

            # 2. VALIDAR DISPONIBILIDAD DEL USUARIO (status debe ser 1)
            await cursor.execute(
                "SELECT status, role, name, mail FROM InnoDB.users WHERE id_users=%s",
                (assignment.users_id,),
            )
            user_data = await cursor.fetchone()

            if not user_data:
                raise HTTPException(status_code=404, detail="El usuario no existe")
            
            if user_data["status"] == 0:
                raise HTTPException(
                    status_code=400, 
                    detail="El operario no está disponible (status=0). Finalice su obra actual primero."
                )

            # 3. Validar que la obra exista
            await cursor.execute(
                "SELECT id_constructions, name, address FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (assignment.constructionsSites_id,),
            )
            construction = await cursor.fetchone()

            if not construction:
                raise HTTPException(status_code=404, detail="La obra no existe")

            # 4. Validar que no exista asignación duplicada activa
            await cursor.execute(
                """
                SELECT id_assignments FROM InnoDB.assignments 
                WHERE users_id=%s AND status=1
                """,
                (assignment.users_id,),
            )

            if await cursor.fetchone():
                raise HTTPException(
                    status_code=409,
                    detail="El operario ya tiene una asignación activa",
                )

            # 5. Validar Admin asignado (si el usuario es operario)
            if user_data["role"] != "admin":
                await cursor.execute(
                    """
                    SELECT a.id_assignments FROM InnoDB.assignments a
                    JOIN InnoDB.users u ON a.users_id = u.id_users
                    WHERE a.constructionsSites_id=%s 
                    AND u.role='admin'
                    AND a.status=1
                """,
                    (assignment.constructionsSites_id,),
                )

                if not await cursor.fetchone():
                    raise HTTPException(
                        status_code=403,
                        detail="Un admin debe asignarse primero a esta obra",
                    )

            # 6. INSERTAR ASIGNACIÓN
            await cursor.execute(
                """
                INSERT INTO InnoDB.assignments 
                (users_id, constructionsSites_id, date_start, date_finish, status)
                VALUES (%s, %s, %s, %s, 1)
            """,
                (
                    assignment.users_id,
                    assignment.constructionsSites_id,
                    assignment.date_start,
                    assignment.date_finish,
                ),
            )
            new_id = cursor.lastrowid

            # 7. LÓGICA DE STATUS DE USUARIO (Si hoy está en el rango)
            today = date.today()
            # Si hoy >= inicio AND (no hay fin OR hoy <= fin)
            is_active_today = (today >= assignment.date_start) and (
                assignment.date_finish is None or today <= assignment.date_finish
            )

            if is_active_today:
                await cursor.execute(
                    "UPDATE InnoDB.users SET status=0 WHERE id_users=%s",
                    (assignment.users_id,)
                )

            await conn.commit()

            # 8. Enviar email (usamos los datos que ya teníamos de user_data y construction)
            subject = f"Nueva asignación: {construction['name']}"
            body = f"""
Hola {user_data['name']},

Has sido asignado a la obra:

Nombre: {construction['name']}
Dirección: {construction['address']}
Fecha inicio: {assignment.date_start}
Fecha fin: {assignment.date_finish or 'No definida'}

Estado actual: {"Ocupado (En curso)" if is_active_today else "Programada (Futura)"}

Saludos.
"""
            background_tasks.add_task(send_email, user_data["mail"], subject, body)

            return {
                "msg": "Asignación creada con éxito",
                "assignment_id": new_id,
                "user_status_updated": is_active_today
            }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
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
                (user_id,),
            )
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()


# OBTENER TODAS LAS ASIGNACIONES (ADMIN)
async def get_all_assignments():
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:

            await cursor.execute(
                """
                SELECT a.*, u.name AS user_name, u.surname AS user_surname, c.name AS construction_name
                FROM InnoDB.assignments a
                JOIN InnoDB.users u ON u.id_users = a.users_id
                JOIN InnoDB.constructionsSites c
                    On c.id_constructions = a.constructionsSites_id
                ORDER BY a.date_start DESC
            """
            )

            return await cursor.fetchall()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()


# FINALIZAR ASIGNACIÓN (ADMIN O USUARIO)
async def finish_assignment(assignment_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT id_assignments FROM InnoDB.assignments WHERE id_assignments=%s",
                (assignment_id,),
            )
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="Asignación no existe")
            await cursor.execute(
                "UPDATE InnoDB.assignments SET status=0 WHERE id_assignments=%s",
                (assignment_id,),
            )
            await conn.commit()
            return {"msg": "Asignación finalizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
