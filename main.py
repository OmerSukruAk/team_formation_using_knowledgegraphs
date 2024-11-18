
import uvicorn
from fastapi import FastAPI
from app.routes import project
from app.services.scheduler import start_scheduler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    
app = FastAPI(lifespan=lifespan)

app.include_router(project.router)

if __name__ == "__main__":
    uvicorn.run(app, port=8000)