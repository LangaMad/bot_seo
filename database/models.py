from sqlalchemy import Integer,String,Text,DECIMAL,ForeignKey
from sqlalchemy.orm import (relationship,Mapped,mapped_column,
                            DeclarativeBase,Session)
from sqlalchemy.ext.asyncio import (create_async_engine,AsyncSession,
                                    async_sessionmaker,AsyncAttrs,
                                    AsyncEngine)

from config import MYSQL_URL

engine = create_async_engine(MYSQL_URL,echo=True)
async_session = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase,AsyncAttrs):
    pass


class Department(Base):
    __tablename__ = 'department'

    id:Mapped[str] = mapped_column(Integer, primary_key=True,autoincrement=True)
    name:Mapped[str] = mapped_column(String(20))
    rab = relationship('Rab',back_populates='department')
    

class Rab(Base):
    __tablename__ = 'rab'

    id:Mapped[int] = mapped_column(Integer,primary_key=True,autoincrement=True)
    first_name:Mapped[str] = mapped_column(String(20))
    last_name:Mapped[str] = mapped_column(String(20))
    age:Mapped[int] = mapped_column(Integer)
    salary:Mapped[float] = mapped_column(DECIMAL)
    email:Mapped[str] = mapped_column(String(20),unique=True)
    phone:Mapped[str] = mapped_column(String(20))
    address:Mapped[str] = mapped_column(Text)
    
    department_id:Mapped[int] = mapped_column(ForeignKey('department.id'))
    
    department = relationship('Department', back_populates='rab')
    



async def models_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        
        
        async with async_session() as session:
            department = Department(name = 'IT')
            session.add(department)
            await session.commit()






