
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .routers import user, event, auth, upvote
from .database import engine
from .config import Settings

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router, prefix="/login", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["Users"])
app.include_router(event.router, prefix="/events", tags=["Events"])
app.include_router(upvote.router, prefix="/upvote", tags=["Upvotes"])
