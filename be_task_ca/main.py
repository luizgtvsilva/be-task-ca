from fastapi import FastAPI, Request, Response

from be_task_ca.infrastructure.api.routes.user_routes import user_router
from be_task_ca.infrastructure.api.routes.item_routes import item_router
from be_task_ca.infrastructure.database.config import SessionLocal
from be_task_ca.config import REPOSITORY_TYPE

app = FastAPI()
app.include_router(user_router)
app.include_router(item_router)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        if REPOSITORY_TYPE == "sql":
            request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        if REPOSITORY_TYPE == "sql" and hasattr(request.state, "db"):
            request.state.db.close()
    return response

@app.get("/")
async def root():
    return {
        "message": "Thanks for shopping at Nile!"
    }