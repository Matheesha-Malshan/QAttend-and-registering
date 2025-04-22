from fastapi import FastAPI
from app.api.endpoints.websocket import router

app=FastAPI()
app.include_router(router)