"""
Database configuration and models
"""

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
import redis.asyncio as redis
from app.config import settings

# Database setup
engine = create_async_engine(settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://"))
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()
metadata = MetaData()

# Redis setup
redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        # Import all models here to ensure they are registered
        from app.models import call, agent, tool
        await conn.run_sync(Base.metadata.create_all)

async def get_db():
    """Database dependency"""
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def get_redis():
    """Redis dependency"""
    return redis_client
