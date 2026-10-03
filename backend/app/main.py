from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.core.config import settings
from app.api.tasks import router as tasks_router
from app.api.notes import router as notes_router
from app.api.memory import router as memory_router
from app.api.guests import router as guests_router
from app.api.meetings import router as meetings_router
from app.api.digital_friend import router as digital_friend_router
from app.api.preferences import router as preferences_router
from app.api.calendar import router as calendar_router
from app.api.integrations import router as integrations_router


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(notes_router)
app.include_router(memory_router)
app.include_router(guests_router)
app.include_router(meetings_router)
app.include_router(digital_friend_router)
app.include_router(preferences_router)
app.include_router(calendar_router)
app.include_router(integrations_router)

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "persynta-api",
    }