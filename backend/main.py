import os
import logging
from datetime import datetime
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from fastapi.responses import JSONResponse
from backend.routes.auth import router as auth_router
from backend.routes.documents import router as documents_router
from backend.routes.conversations import router as conversations_router
from ai.routes import router as ai_router
from database.config import get_db, Base, engine
from sqlalchemy.exc import SQLAlchemyError

# Initialize logging
logging.basicConfig(level=logging.INFO)

app = FastAPI()

# CORS middleware
origins = [
    "http://localhost:3000",
    "http://frontend-origin.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)
    logging.info("Database tables created/verified.")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}

# Include routers
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(conversations_router)
app.include_router(ai_router)

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.errors()},
    )

@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )