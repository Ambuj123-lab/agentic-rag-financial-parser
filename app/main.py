import os
import logging
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, upload, whatsapp, cron
from app.rag import routes as rag_routes
from app.db.mongodb import connect_to_mongo, close_mongo_connection, ensure_indexes
from app.core.config import get_settings

settings = get_settings()

# Configure simple logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("🚀 Starting up Agentic Financial Parser Backend...")
    await connect_to_mongo()
    await ensure_indexes()
    
    # Initialize Vector DB
    from app.db.pinecone_client import get_pinecone_client
    get_pinecone_client()
    
    # Initialize Supabase client
    try:
        from app.db.supabase_client import get_supabase
        get_supabase()
    except Exception as e:
        logger.warning(f"Supabase init skipped (will retry on first request): {e}")

    yield
    
    # Shutdown actions
    logger.info("🛑 Shutting down...")
    await close_mongo_connection()

app = FastAPI(
    title="Agentic Financial Parser API",
    description="Backend for querying and analyzing complex Indian financial documents via Agentic RAG",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configurations for Frontend (including Vite's 5174 port)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        settings.FRONTEND_URL, 
        "http://localhost:5173", 
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Required for Authlib (Google OAuth state tracking)
from starlette.middleware.sessions import SessionMiddleware
app.add_middleware(SessionMiddleware, secret_key=settings.JWT_SECRET)

# Auth routes at root level (for direct browser navigation: /auth/login, /auth/callback)
app.include_router(auth.router, tags=["Authentication (root)"])

# All API routes under /api prefix (for frontend axios/fetch calls in production)
app.include_router(auth.router, prefix="/api", tags=["Authentication"])
app.include_router(upload.router, prefix="/api", tags=["Upload Security"])
app.include_router(rag_routes.router, prefix="/api", tags=["RAG & Chat"])
app.include_router(whatsapp.router, prefix="/api", tags=["WhatsApp Webhook"])
app.include_router(cron.router, prefix="/api/cron", tags=["Cron Jobs"])

# --- Health Check + Supabase Keep-Alive ---
@app.api_route("/health", methods=["GET", "HEAD"], tags=["System"])
def health_check():
    """Health check for deployment monitoring and Supabase keep-alive."""
    db_status = "unknown"
    
    try:
        from app.db.supabase_client import get_supabase
        client = get_supabase()
        if client:
            # Lightweight query to keep Supabase free tier project active (prevents 7-day pause)
            # UptimeRobot sends HEAD every 5 mins -> keeps Render + Supabase alive
            client.table("fp_file_registry").select("file_name").limit(1).execute()
            db_status = "connected"
        else:
            db_status = "client_not_initialized"
    except Exception as e:
        logger.warning(f"Supabase keep-alive ping failed: {e}")
        db_status = "error"

    return {
        "status": "healthy",
        "database": db_status,
        "agent": "Iron Man Suit Active",
        "timestamp": datetime.now().isoformat()
    }

# --- Uptime Robot Stats ---
import httpx

@app.get("/api/uptime", tags=["System"])
async def get_uptime():
    """Fetches Uptime Robot statistics using read-only API key."""
    api_key = os.environ.get("UPTIMEROBOT_API_KEY") or os.environ.get("UPTIME_ROBOT_API_KEY")
    default_response = {"uptime": "--%", "latency": "--"}
    
    if not api_key:
        return default_response
        
    url = "https://api.uptimerobot.com/v2/getMonitors"
    payload = f"api_key={api_key}&format=json&custom_uptime_ratios=30&response_times=1"
    headers = {
        'cache-control': "no-cache",
        'content-type': "application/x-www-form-urlencoded"
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data=payload, headers=headers, timeout=10.0)
            data = response.json()
            
            if data.get("stat") == "ok" and data.get("monitors"):
                monitor = data["monitors"][0]
                status = monitor.get("status")
                
                # UptimeRobot status: 2 is UP, 8 is SEEMS DOWN, 9 is DOWN
                if status != 2:
                    return default_response
                
                uptime_ratio = float(monitor.get("custom_uptime_ratio", "0"))
                response_times = monitor.get("response_times", [])
                
                latency = "--"
                if response_times:
                    latency = f"{response_times[0].get('value', 0)}ms"
                    
                return {
                    "uptime": f"{uptime_ratio:.2f}%",
                    "latency": latency
                }
    except Exception as e:
        logger.error(f"Error fetching Uptime Robot data: {e}")
        
    return default_response

# --- Root ---
@app.get("/")
async def root():
    # If running in Docker/Production, serve Frontend
    frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
    index_path = os.path.join(frontend_dist, "index.html")
    
    if os.path.exists(index_path):
        with open(index_path, "rb") as f:
            return Response(content=f.read(), media_type="text/html")
    
    # Fallback for local backend-only dev
    return {
        "message": "Agentic Financial Parser API",
        "docs": "/docs",
        "health": "/health"
    }

# --- Serve Frontend (SPA Catch-All for Production/Docker) ---
frontend_dist = os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")
if os.path.exists(frontend_dist):
    # Mount static assets (JS, CSS, Images)
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")
    
    # Mount branding/images if present in public folder copy
    if os.path.exists(os.path.join(frontend_dist, "branding")):
        app.mount("/branding", StaticFiles(directory=os.path.join(frontend_dist, "branding")), name="branding")

    # Serve architecture.html directly (static page, not SPA)
    @app.get("/architecture.html")
    async def serve_architecture():
        arch_path = os.path.join(frontend_dist, "architecture.html")
        if os.path.exists(arch_path):
            with open(arch_path, "rb") as f:
                return Response(content=f.read(), media_type="text/html")
        return Response(status_code=404)

    # Serve index.html for all other routes (SPA React Router)
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api/") or full_path.startswith("auth/") or full_path.startswith("health") or full_path.startswith("docs") or full_path.startswith("openapi.json"):
            return Response(status_code=404)
            
        file_path = os.path.join(frontend_dist, full_path)
        if os.path.isfile(file_path):
            from fastapi.responses import FileResponse
            return FileResponse(file_path)
            
        with open(os.path.join(frontend_dist, "index.html"), "rb") as f:
            return Response(content=f.read(), media_type="text/html")
