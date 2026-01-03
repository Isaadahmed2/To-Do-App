"""Main FastAPI application for To-Do app."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.logger import logger
from app.routes.todos import router as todos_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title="To-Do App API",
        description="A simple To-Do application API with CRUD operations",
        version="1.0.0",
    )

    # Configure CORS for frontend communication
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers with /api prefix
    app.include_router(todos_router, prefix="/api")

    @app.get("/")
    def root() -> dict:
        """Root endpoint for health check."""
        return {"status": "ok", "message": "To-Do App API is running"}

    logger.minor("FastAPI application created successfully")
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
