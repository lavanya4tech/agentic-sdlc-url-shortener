from fastapi import FastAPI

from .api.routes import router

from .infrastructure.database import Base, engine

app = FastAPI(

    title="Agentic SDLC URL Shortener",

    version="1.0.0",

    description="URL shortener service built with controlled agentic SDLC orchestration.",

)

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/health")

def health_check():

    return {

        "status": "healthy",

        "service": "url-shortener",

    }
