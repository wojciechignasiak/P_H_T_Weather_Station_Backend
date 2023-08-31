from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import Request

async def get_session(request: Request) -> AsyncGenerator:
    AsyncSessionFactory = sessionmaker(request.app.state.engine, class_=AsyncSession, autoflush=False, expire_on_commit=False)
    async with AsyncSessionFactory() as session:
        yield session