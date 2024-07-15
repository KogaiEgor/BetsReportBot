import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker, registry
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


load_dotenv()
engine = create_async_engine(os.getenv("DATABASE_URL"), echo=True)
mapper_registry = registry()
Base = mapper_registry.generate_base()

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

