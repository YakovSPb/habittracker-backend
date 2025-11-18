from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import auth, habits

app = FastAPI(
    title="HabitTracker API",
    description="Personal habit tracking application",
    version="1.0.0"
)

# CORS middleware с исправленными настройками
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(auth.router)
# app.include_router(habits.router)

@app.get("/")
def root():
    return {"message": "HabitTracker API is running!"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}