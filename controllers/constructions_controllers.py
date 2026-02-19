import aiomysql as aio
from db.config import get_conexion
from fastapi import HTTPException
from models.constructions_models import ConstructionCreate, ConstructionUpdate

# Obtener todas las construciones
async def get_all_constructions(status: str = None):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            if status:
                await cursor.execute(
                    "SELECT * FROM InnoDB.constructionsSites WHERE status=%s",
                    (status,)
                )
            else:
                await cursor.execute(
                    "SELECT * FROM InnoDB.constructionsSites"
                )

            return await cursor.fetchall()
    finally:
        conn.close()

async def get_construction_by_id(construction_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                "SELECT * FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (construction_id,)
            )
            construction = await cursor.fetchone()
            if not construction:
                raise HTTPException(status_code=404, detail="Obra no encontrada")
            return construction
    finally:
        conn.close()

# Crear una obra nueva (solo admin)
async def create_construction(construction: ConstructionCreate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                INSERT INTO InnoDB.constructionsSites
                (name, description, address, latitude, longitude, status)
                VALUES (%s, %s, %s, %s, %s, 'active')
                """,
                (
                    construction.name,
                    construction.description,
                    construction.address,
                    construction.latitude,
                    construction.longitude
                )
            )
            await conn.commit()
            return {"msg": "Obra creada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# Actualizar una obra (admin)
# Actualizar una obra (admin)
async def update_construction(construction_id: int, construction: ConstructionUpdate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # Construir query dinámica para actualización parcial
            update_data = construction.model_dump(exclude_unset=True)
            
            if not update_data:
                return {"msg": "No se proporcionaron datos para actualizar"}
                
            set_clause = ", ".join([f"{key}=%s" for key in update_data.keys()])
            values = list(update_data.values())
            values.append(construction_id)
            
            await cursor.execute(
                f"UPDATE InnoDB.constructionsSites SET {set_clause} WHERE id_constructions=%s",
                tuple(values)
            )
            
            await conn.commit()
            
            if cursor.rowcount == 0:
                 # Verificar si no se actualizó porque no existe o porque los datos eran iguales
                await cursor.execute("SELECT id_constructions FROM InnoDB.constructionsSites WHERE id_constructions=%s", (construction_id,))
                if not await cursor.fetchone():
                    raise HTTPException(status_code=404, detail="Obra no encontrada")
            
            return {"msg": "Obra actualizada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# Eliminar una obra (admin)
async def delete_construction(construction_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            # verificar que la obra exista
            await cursor.execute(
                "SELECT id_constructions FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (construction_id,)
            )
            construction = await cursor.fetchone()
            if not construction:
                raise HTTPException(status_code=404, detail="Obra no existe")
            # verificar que no tenga asignaciones activas
            await cursor.execute(
                """
                SELECT id_assignments 
                FROM InnoDB.assignments 
                WHERE constructionsSites_id=%s 
                AND status='IN_PROGRESS'
                """,
                (construction_id,)
            )
            active_assignment = await cursor.fetchone()
            if active_assignment:
                raise HTTPException(
                    status_code=400,
                    detail="No puedes eliminar una obra con asignaciones activas"
                )
            # eliminar
            await cursor.execute(
                "DELETE FROM InnoDB.constructionsSites WHERE id_constructions=%s",
                (construction_id,)
            )
            await conn.commit()
            return {"msg": "Obra eliminada correctamente"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()

# OBTENER USUARIO POR OBRA
async def get_workers_by_construction(construction_id: int):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                SELECT u.id_users, u.name, u.surname, u.mail
                FROM InnoDB.users u
                JOIN InnoDB.assignments a
                ON u.id_users = a.users_id
                WHERE a.constructionsSites_id=%s
                AND a.status='IN_PROGRESS'
                """, (construction_id,)
            )
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
