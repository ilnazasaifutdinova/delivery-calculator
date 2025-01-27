from fastapi import FastAPI
from API.endpoints import router  #Importing the router

app = FastAPI()

# Подключаем роутер
app.include_router(router)
