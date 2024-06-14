from database.models import *
from sqlalchemy import select, update, delete, insert


async def get_departments():
    async with async_session() as session:
        result = await session.scalars(select(Department))
        return result


async def get_rabs(department_id):
    async with async_session() as session:
        result = await session.scalars(select(Rab).where(
            Rab.department_id == department_id))
        return result


async def get_rab(rab_id):
    async with async_session() as session:
        result = await session.scalar(select(Rab).where(
            Rab.id == rab_id))
        return result


async def get_worker():
    async with async_session() as session:
        result = await session.scalars(select(Rab))
        return result
    

async def delete_rab(rab_id):
    async with async_session() as session:
        await session.execute(delete(Rab).where(
            Rab.id == rab_id))
        await session.commit()


async def create_rab(rab):
    async with async_session() as session:
        
        session.add(rab)
        await session.commit()
        await session.refresh(rab)
        return rab

# async def rab_data():
#     rab_list = []
#     rab = await get_worker()
#     for i in rab:
#         rab_list.append([i.first_name,i.last_name])
#     return rab_list
