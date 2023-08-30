from fastapi import FastAPI
from app.api import chat, users, files, bots  # Assuming all these routers are defined
from app.core import config, database  # Assuming you have configurations and database setup

app = FastAPI(title="Chat App", version="1.0", description="A chat application with FastAPI")

# Middleware for database session management (if using a database)
@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = database.SessionLocal()  # Assuming SessionLocal is your session factory
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# Include the API routers
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(files.router, prefix="/files", tags=["files"])
app.include_router(bots.router, prefix="/bots", tags=["bots"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
