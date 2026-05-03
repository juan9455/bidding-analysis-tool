"""
FastAPI Application Main Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import APP_NAME, APP_VERSION, CORS_ORIGINS, API_V1_STR
from app.database import init_db

# Initialize FastAPI app
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Intelligent bidding document analysis tool",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    print(f"{APP_NAME} v{APP_VERSION} started successfully!")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": APP_NAME}


# Import and include routes
# TODO: Include routes from routes module
# from app.routes import upload, projects, analysis
# app.include_router(upload.router, prefix=API_V1_STR, tags=["upload"])
# app.include_router(projects.router, prefix=API_V1_STR, tags=["projects"])
# app.include_router(analysis.router, prefix=API_V1_STR, tags=["analysis"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
