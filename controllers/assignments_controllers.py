import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.assignments_models import AssignmentCreate
from core.email_config import send_email



# CREAR ASIGNACIÓN (ADMIN)
async def create_assignment(assignment: AssignmentCreate, background_tasks):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # Validar que date_finish no sea antes que date_start
            if assignment.date_finish and assignment.date_finish < assignment.date_start:
                raise HTTPException(status_code=400, detail="La fecha de fin no puede ser anterior a la fecha de inicio")
            
            # Validar que la obra exista
            await cursor.execute(
                "SELECT id_constructions FROM InnoDB.constructionsSites WHERE id_constructions=%s", 
                (assignment.constructionsSites_id,)
            )
            
            if not await cursor.fetchone():
                raise HTTPException(status_code=404, detail="La obra no existe")
            
            # Validar que no exista asignación duplicada en el mismo rango de fechas
            await cursor.execute("""
                SELECT id_assignments FROM InnoDB.assignments 
                WHERE users_id=%s 
                AND constructionsSites_id=%s
                AND status=1
                AND date_start <= %s 
                AND (date_finish IS NULL OR date_finish >= %s)
            """, (assignment.users_id, assignment.constructionsSites_id, assignment.date_finish or assignment.date_start, assignment.date_start))
            
            if await cursor.fetchone():
                raise HTTPException(status_code=409, detail="El operario ya tiene una asignación en ese rango de fechas")
            
            # Validar que exista un admin asignado a esa obra (solo si el usuario a asignar no es admin)
            await cursor.execute("SELECT role FROM InnoDB.users WHERE id_users=%s", (assignment.users_id,))
            user_role = await cursor.fetchone()
            
            if user_role and user_role['role'] != 'admin':
                await cursor.execute("""
                    SELECT a.id_assignments FROM InnoDB.assignments a
                    JOIN InnoDB.users u ON a.users_id = u.id_users
                    WHERE a.constructionsSites_id=%s 
                    AND u.role='admin'
                    AND a.status=1
                """, (assignment.constructionsSites_id,))
                
                if not await cursor.fetchone():
                    raise HTTPException(status_code=403, detail="Un admin debe asignarse primero a esta obra")
            
            # Insertar asignación
            await cursor.execute("""
                INSERT INTO InnoDB.assignments 
                (users_id, constructionsSites_id, date_start, date_finish, status)
                VALUES (%s, %s, %s, %s, 1)
            """, (assignment.users_id, assignment.constructionsSites_id, assignment.date_start, assignment.date_finish))
            
            await conn.commit()
            new_id = cursor.lastrowid
            
            # Obtener datos usuario
            await cursor.execute("SELECT name, mail FROM InnoDB.users WHERE id_users=%s", (assignment.users_id,))
            user = await cursor.fetchone()
            
            # Obtener datos obra
            await cursor.execute("SELECT name, address FROM InnoDB.constructionsSites WHERE id_constructions=%s", (assignment.constructionsSites_id,))
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
            background_tasks.add_task(send_email, user["mail"], subject, body)
            
            return {"msg": "Asignación creada. El correo se está enviando.", "assignment_id": new_id}
            
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
