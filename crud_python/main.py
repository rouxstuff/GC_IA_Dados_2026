from fastapi import FastAPI
import uvicorn
from app.database.config import create_db_and_tables
from app.routes.characters import router as character_router

app = FastAPI(title="CRUD Python", description="API for CRUD operations in Python")

# Include routers
app.include_router(character_router)

# Root endpoint
@app.get("/")
async def root():
    """Home page of the API."""
    return {"message": "Welcome to the CRUD Python API!"}

# Database initialization
@app.on_event("startup")
def on_startup():
    """Initialize database when the application starts."""
    create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
