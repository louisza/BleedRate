"""FastAPI application factory and configuration"""
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response
from app.config import settings
from app.api.routes_public import router as public_router
from app.api.routes_admin import router as admin_router
from app.views.pages import router as views_router
from db.session import create_db_and_tables


class CacheHeaderMiddleware(BaseHTTPMiddleware):
    """Add cache headers for performance optimization"""
    
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        
        # Static assets: cache for 1 year
        if request.url.path.startswith("/static/"):
            response.headers["Cache-Control"] = "public, max-age=31536000, immutable"
        
        # HTML pages: cache for 1 hour (allow validation)
        elif request.url.path in ["/", "/calculator", "/about", "/privacy", "/faq", "/terms"]:
            response.headers["Cache-Control"] = "public, max-age=3600, must-revalidate"
        
        # API endpoints: no caching
        elif request.url.path.startswith("/api/"):
            response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
            response.headers["Pragma"] = "no-cache"
            response.headers["Expires"] = "0"
        
        # Default: cache for 10 minutes
        else:
            response.headers["Cache-Control"] = "public, max-age=600"
        
        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        
        return response


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
    
    # Mount static files - create directory if it doesn't exist
    static_dir = Path(settings.STATIC_DIR)
    static_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    except RuntimeError as e:
        # Static directory issue - log but don't crash (using Tailwind CDN anyway)
        print(f"Warning: Could not mount static files: {e}")
    
    # Add middleware (order matters!)
    app.add_middleware(CacheHeaderMiddleware)
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
        """Health check endpoint for Railway and monitoring"""
        return {
            "status": "healthy",
            "version": "1.0.0",
            "environment": settings.ENVIRONMENT,
            "debug": settings.DEBUG,
        }
    
    return app


# Create app instance
app = create_app()
