from starlette import middleware
import uvicorn
from fastapi import FastAPI
from router.api import api_router
from starlette.middleware.cors import CORSMiddleware

app = FastAPI(debug=True)

middleware = [
    middleware.Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods="*",
        allow_headers=["*"]
    )]

app = FastAPI(middleware=middleware)

app.include_router(api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
