from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from config.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

from model.models import Task, Topic, User  # isort:skip
from model.base import Base  # isort:skip

DATABASE_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

engine: AsyncEngine = create_async_engine(DATABASE_URL)
async_session_maker: sessionmaker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
