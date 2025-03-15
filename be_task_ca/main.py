from fastapi import FastAPI, Request, Response

from be_task_ca.infrastructure.api.routes.user_routes import user_router
from be_task_ca.infrastructure.api.routes.item_routes import item_router
from be_task_ca.infrastructure.database.config import SessionLocal, engine

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }