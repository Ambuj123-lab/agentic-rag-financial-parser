from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # App Settings
    ENVIRONMENT: str = "development"
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Secret Keys & Auth
    JWT_SECRET: str
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    ADMIN_EMAIL: str = ""  # Only this email can sync/delete/admin
    
    # External APIs
    LLAMA_CLOUD_API_KEY: str
    JINA_API_KEY: str
    OPENROUTER_API_KEY: str
    COHERE_API_KEY: Optional[str] = None
    
    # Vector DB (Pinecone)
    PINECONE_API_KEY: str
    PINECONE_INDEX_NAME: str = "financial-parser-idx"
    
    
    # Structured DB & Storage
    MONGODB_URI: str
    MONGODB_DB_NAME: str = "financial_parser_db"
    
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_BUCKET: str = "financial-parser-pdfs"

    # Performance & Observability
    UPSTASH_REDIS_REST_URL: str = ""
    UPSTASH_REDIS_REST_TOKEN: str = ""
    LANGFUSE_SECRET_KEY: str = ""
    LANGFUSE_PUBLIC_KEY: str = ""
    LANGFUSE_HOST: str = "https://us.cloud.langfuse.com"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

# Global Settings Instance
settings = Settings()

def get_settings() -> Settings:
    return settings
