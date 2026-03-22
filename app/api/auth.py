from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt
from datetime import datetime, timedelta
from app.core.config import get_settings
from app.db.mongodb import get_database

settings = get_settings()
router = APIRouter()

# Mocking Google OAuth logic for local dev/FastAPI until frontend integration
# In a real deployed app, the frontend sends the Google Token to be verified
# Here, we keep it identical to the standard OAuth flow you had.

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm="HS256")
    return encoded_jwt

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def get_current_user(request: Request):
    """FastAPI Dependency to get current user's email from JWT token in header."""
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    
    token = auth_header.split(" ")[1]
    payload = verify_token(token)
    return {"email": payload.get("sub"), "name": payload.get("name")}

@router.get("/me")
async def get_me(user_info: dict = Depends(get_current_user)):
    """ Returns the current logged-in user details to the frontend. """
    db = get_database()
    email = user_info["email"]
    user = await db.users.find_one({"email": email})
    if user:
        return {"email": user["email"], "name": user.get("name", "User")}
    return {"email": email, "name": "User"}

@router.get("/auth/login")
async def login_redirect(request: Request):
    """Redirect to Google OAuth consent screen"""
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    from app.api.oauth import oauth
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/callback")
async def auth_callback(request: Request):
    """Handle Google OAuth callback — issue JWT and redirect to frontend"""
    from authlib.integrations.starlette_client import OAuthError
    from fastapi.responses import RedirectResponse
    try:
        from app.api.oauth import oauth
        token = await oauth.google.authorize_access_token(request)
        user_info = token.get('userinfo')
        if not user_info:
            raise HTTPException(status_code=400, detail="Could not get user info from Google")
            
        access_token = create_access_token({
            "sub": user_info.get("email"),
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
            "is_admin": user_info.get("email") == settings.ADMIN_EMAIL
        })
        
        # Store user locally in MongoDB for tracking history
        db = get_database()
        await db.users.update_one(
            {"email": user_info.get("email")},
            {"$set": {"name": user_info.get("name"), "picture": user_info.get("picture"), "last_login": datetime.utcnow()}},
            upsert=True
        )
        
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/auth-callback?token={access_token}")
        
    except OAuthError as error:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/?error={error}")
    except Exception as e:
        return RedirectResponse(url=f"{settings.FRONTEND_URL}/?error={str(e)}")

@router.post("/auth/logout")
async def logout(request: Request):
    """
    Clear active user status from Redis and trigger cleanup for Temp Vectors.
    Temp vector cleanup will be executed in a background task in the main graph.
    """
    # Simply tell frontend to delete token. Backend is stateless JWT.
        # The actual vector cleanup happens by calling the Pinecone temp filter.
    from app.db.pinecone_client import delete_vectors_by_filter
    
    auth_header = request.headers.get("Authorization")
    if auth_header and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        try:
            payload = verify_token(token)
            email = payload.get("sub")
            # Clear user's temp vectors from Pinecone synchronously
            delete_vectors_by_filter({"user_email": {"$eq": email}, "is_temporary": {"$eq": True}})
        except:
            pass
            
    return {"message": "Logged out successfully"}


@router.post("/auth/dev-login")
async def dev_login():
    """
    Dev-only bypass: Creates a JWT without Google OAuth.
    ONLY works when ENVIRONMENT=development in .env.
    Remove or disable before production deployment.
    """
    if settings.ENVIRONMENT != "development":
        raise HTTPException(status_code=403, detail="Dev login disabled in production")
    
    dev_email = "dev@test.com"
    dev_name = "Dev User"
    
    token = create_access_token({"sub": dev_email, "name": dev_name})
    
    # Store dev user in MongoDB
    db = get_database()
    await db.users.update_one(
        {"email": dev_email},
        {"$set": {"name": dev_name, "last_login": datetime.utcnow()}},
        upsert=True
    )
    
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {"email": dev_email, "name": dev_name}
    }
