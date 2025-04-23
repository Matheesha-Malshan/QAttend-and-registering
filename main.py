from fastapi import FastAPI
from app.api.endpoints.websocket import router
from app.api.endpoints.post import post_handler

app=FastAPI()

app.include_router(router)
app.include_router(post_handler)