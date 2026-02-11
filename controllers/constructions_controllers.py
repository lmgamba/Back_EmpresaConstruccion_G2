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
async def update_construction(construction_id: int, construction: ConstructionUpdate):
    try:
        conn = await get_conexion()
        async with conn.cursor(aio.DictCursor) as cursor:
            await cursor.execute(
                """
                UPDATE InnoDB.constructionsSites
                SET name=%s, description=%s, address=%s,
                latitude=%s, longitude=%s, status=%s
                WHERE id_constructions=%s
                """,
                (
                    construction.name,
                    construction.description,
                    construction.address,
                    construction.latitude,
                    construction.longitude,
                    construction.status,
                    construction_id
                )
            )
            await conn.commit()
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
                AND status='active'
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
                AND a.status='active'
                """, (construction_id,)
            )
            return await cursor.fetchall()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
    finally:
        conn.close()
