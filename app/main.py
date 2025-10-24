"""FastAPI application factory and configuration"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.api.routes_public import router as public_router
from app.api.routes_admin import router as admin_router
from app.views.pages import router as views_router
from db.session import create_db_and_tables


def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    app = FastAPI(
        title="SA Tax Footprint Calculator",
        description="Calculate your complete South African tax footprint",
        version="1.0.0",
        debug=settings.DEBUG
    )
    
    # Initialize database
    create_db_and_tables()
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
    
    # Add middleware
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    if settings.DEBUG:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    # Include routers
    app.include_router(views_router, tags=["views"])
    app.include_router(public_router, tags=["api"])
    
    if settings.ADMIN_ENABLED:
        app.include_router(admin_router, tags=["admin"])
    
    @app.get("/health")
    def health_check():
        """Health check endpoint"""
        return {"status": "healthy", "version": "1.0.0"}
    
    return app


# Create app instance
app = create_app()
