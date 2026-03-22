import logging
import os
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from app.core.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# Global Supabase client instance
_supabase: Optional[Client] = None

def get_supabase() -> Client:
    """Initialize and retrieve the Supabase client."""
    global _supabase
    if not _supabase:
        try:
            logger.info("Initializing Supabase Client...")
            _supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
            logger.info("✅ Supabase Client Initialized")
        except Exception as e:
            logger.error(f"Failed to connect to Supabase: {e}")
            raise
    return _supabase

def upload_file_to_storage(file_path: str, object_name: str) -> bool:
    """Upload a local file to the Supabase Supabase Storage Bucket."""
    supabase = get_supabase()
    bucket = settings.SUPABASE_BUCKET
    
    try:
        with open(file_path, 'rb') as f:
            # Overwrite if exists
            supabase.storage.from_(bucket).upload(
                path=object_name, 
                file=f,
                file_options={"cache-control": "3600", "upsert": "true"}
            )
        logger.info(f"✅ Uploaded `{object_name}` to Supabase bucket `{bucket}`")
        return True
    except Exception as e:
        logger.error(f"❌ Failed to upload `{object_name}` to Supabase: {e}")
        return False

def get_registry_entry(file_name: str) -> Optional[Dict[str, Any]]:
    """Retrieve file metadata from the fp_file_registry table."""
    supabase = get_supabase()
    try:
        result = supabase.table("fp_file_registry").select("*").eq("file_name", file_name).execute()
        if result.data and len(result.data) > 0:
            return result.data[0]
        return None
    except Exception as e:
        logger.error(f"Supabase GET registry error for `{file_name}`: {e}")
        return None

def upsert_registry_entry(data: Dict[str, Any]) -> bool:
    """Insert or update a record in the fp_file_registry table."""
    supabase = get_supabase()
    try:
        supabase.table("fp_file_registry").upsert(data).execute()
        logger.info(f"✅ Upserted registry entry for `{data.get('file_name')}`")
        return True
    except Exception as e:
        logger.error(f"❌ Supabase UPSERT registry error: {e}")
        return False

def get_all_active_files() -> List[Dict[str, Any]]:
    """Get a list of all active files tracked in the registry."""
    supabase = get_supabase()
    try:
        result = supabase.table("fp_file_registry").select("*").eq("status", "active").execute()
        return result.data
    except Exception as e:
        logger.error(f"❌ Supabase GET all registry error: {e}")
        return []

def mark_file_inactive(file_name: str) -> bool:
    """Soft delete a file from the registry."""
    supabase = get_supabase()
    try:
        supabase.table("fp_file_registry").update({"status": "inactive"}).eq("file_name", file_name).execute()
        logger.info(f"🗑️ Marked `{file_name}` as inactive in Supabase")
        return True
    except Exception as e:
        logger.error(f"❌ Supabase DELETE registry error: {e}")
        return False
