import os
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncEngine
from app.schema.schema import base
from influxdb_client import InfluxDBClient
from contextlib import asynccontextmanager
from app.routers import (cities_router, readings_router, sensors_router)
from app.utils.insert_postges_mock_data import insert_postgres_mock_data
from app.utils.insert_influx_mock_data import insert_influx_mock_data
from starlette.middleware.cors import CORSMiddleware
from starlette import middleware


middleware = [
    middleware.Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods="*",
        allow_headers=["*"]
    )]

POSTGRES_USERNAME = os.environ.get("POSTGRES_USERNAME")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT")
POSTGRES_DB = os.environ.get("POSTGRES_DB")

POSTGRES_URL = f"postgresql+asyncpg://{POSTGRES_USERNAME}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

INFLUX_TOKEN = os.environ.get("INFLUX_TOKEN")
INFLUX_HOST = os.environ.get("INFLUX_HOST")
INFLUX_PORT = os.environ.get("INFLUX_PORT")
INFLUX_ORG_NAME = os.environ.get("INFLUX_ORG_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    ''' Run at startup
        Initialise the Client and add it to request.state
    '''
    print("Creating PostgreSQL engine...")
    app.state.engine: AsyncEngine = create_async_engine(
                        POSTGRES_URL,
                        echo=False,
                        future=True
                    )
    async with app.state.engine.begin() as conn:
        await conn.run_sync(base.metadata.create_all)
    await insert_postgres_mock_data(POSTGRES_URL)

    print("Creating InfluxDB client...")
    app.state.influx_client: InfluxDBClient = InfluxDBClient(url=f"http://{INFLUX_HOST}:{INFLUX_PORT}", token=str(INFLUX_TOKEN), org=INFLUX_ORG_NAME)
    await insert_influx_mock_data(app.state.influx_client)

    yield
    ''' Run on shutdown
        Close the connection
        Clear variables and release the resources
    '''
    print("Disposing PostgreSQL engine...")
    async with app.state.engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
    await app.state.engine.dispose()
    print("Closing InfluxDB client...")
    app.state.influx_client.close()


def create_application() -> FastAPI:
    application = FastAPI(lifespan=lifespan, openapi_url="/openapi.json", docs_url="/docs", middleware=middleware)
    application.include_router(cities_router.router, tags=["cities"])
    application.include_router(readings_router.router, tags=["readings"])
    application.include_router(sensors_router.router, tags=["sensors"])
    return application

app = create_application()