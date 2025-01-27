from fastapi import FastAPI
from API.endpoints import router

app = FastAPI()
app.include_router(router)
