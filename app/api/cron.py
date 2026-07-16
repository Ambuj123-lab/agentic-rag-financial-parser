from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from app.rag.daily_insight_agent import fetch_daily_insight
from app.utils.email_sender import send_daily_insight_email
import os
import logging
import traceback

router = APIRouter()
logger = logging.getLogger(__name__)

# This is the list of emails that will receive the daily AI insights
SUBSCRIBERS = [
    "ambujonly761@gmail.com",
    "tripathi.anku@outlook.com",
]

def background_email_task():
    """
    Runs in background after HTTP response is sent.
    Full try/except with detailed logging so we can see EXACTLY where it fails in Render logs.
    """
    try:
        logger.info("📧 [CRON] Step 1/3: Starting Tavily web search for daily insight...")
        print("📧 [CRON] Step 1/3: Starting Tavily web search for daily insight...")
        
        insight_data = fetch_daily_insight()
        
        if not insight_data:
            logger.error("❌ [CRON] Step 1 FAILED: fetch_daily_insight() returned None. Check Tavily/Gemini API keys.")
            print("❌ [CRON] Step 1 FAILED: fetch_daily_insight() returned None.")
            return
            
        logger.info(f"✅ [CRON] Step 1/3 DONE: Got insight → {insight_data['insight_title'][:60]}...")
        print(f"✅ [CRON] Step 1/3 DONE: Got insight → {insight_data['insight_title'][:60]}...")
        
        logger.info(f"📧 [CRON] Step 2/3: Sending email to {len(SUBSCRIBERS)} subscribers via SMTP...")
        print(f"📧 [CRON] Step 2/3: Sending email to {len(SUBSCRIBERS)} subscribers via SMTP...")
        
        success = send_daily_insight_email(
            to_emails=SUBSCRIBERS,
            subject=insight_data["insight_title"],
            insight_title=insight_data["insight_title"],
            insight_explanation=insight_data["insight_explanation"],
            real_life_scenario=insight_data["real_life_scenario"],
            sources=insight_data["sources"]
        )
        
        if success:
            logger.info("✅ [CRON] Step 3/3 DONE: Email sent successfully to all subscribers!")
            print("✅ [CRON] Step 3/3 DONE: Email sent successfully!")
        else:
            logger.error("❌ [CRON] Step 2 FAILED: send_daily_insight_email() returned False. Check SENDER_EMAIL and SENDER_APP_PASSWORD env vars.")
            print("❌ [CRON] Step 2 FAILED: Email sending failed.")
            
    except Exception as e:
        logger.error(f"❌ [CRON] CRASHED with exception: {str(e)}")
        logger.error(f"❌ [CRON] Full traceback:\n{traceback.format_exc()}")
        print(f"❌ [CRON] CRASHED: {str(e)}")
        print(traceback.format_exc())


@router.get("/send-daily-fact")
async def trigger_daily_email(
    background_tasks: BackgroundTasks,
    token: str = Query(..., description="Secret token to trigger the cron job")
):
    """
    Triggers the autonomous AI agent to fetch a fact and email it.
    Uses BackgroundTasks because Render free tier has 30s HTTP timeout,
    but the full pipeline (Tavily + Gemini + SMTP) takes ~60s.
    """
    secret_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "AmbujLegalBot2026")
    
    if token != secret_token:
        raise HTTPException(status_code=403, detail="Unauthorized cron trigger")
    
    # Verify critical env vars BEFORE starting background task
    missing_vars = []
    if not os.getenv("TAVILY_API_KEY"):
        missing_vars.append("TAVILY_API_KEY")
    if not os.getenv("GEMINI_API_KEY"):
        missing_vars.append("GEMINI_API_KEY")
    if not os.getenv("SENDER_EMAIL"):
        missing_vars.append("SENDER_EMAIL")
    if not os.getenv("SENDER_APP_PASSWORD"):
        missing_vars.append("SENDER_APP_PASSWORD")
    
    if missing_vars:
        return {
            "status": "error",
            "message": f"Missing environment variables: {', '.join(missing_vars)}. Set them in Render dashboard."
        }
    
    logger.info("📧 [CRON] Cron triggered! Queuing background email task...")
    print("📧 [CRON] Cron triggered! Queuing background email task...")
    
    background_tasks.add_task(background_email_task)
    
    return {
        "status": "accepted",
        "message": "Daily insight generation started. Check Render logs for progress (Steps 1/3 → 2/3 → 3/3)."
    }


@router.get("/test-smtp")
async def test_smtp_connection(
    token: str = Query(..., description="Secret token")
):
    """
    Quick SMTP test — sends a simple test email to verify credentials work.
    This is lightweight and finishes within 30s timeout.
    """
    secret_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "AmbujLegalBot2026")
    if token != secret_token:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_APP_PASSWORD")
    
    if not sender_email or not sender_password:
        return {"status": "error", "message": f"SENDER_EMAIL={bool(sender_email)}, SENDER_APP_PASSWORD={bool(sender_password)}"}
    
    try:
        import httpx
        gas_url = "https://script.google.com/macros/s/AKfycbxD1xUuye063G_z7SzLzNxZU7ljb3d7sZln7c9dMd8YNIeW0iQufN78IYE7Lcn-lcTbgg/exec"
        
        payload = {
            "to_emails": [SUBSCRIBERS[0]],
            "subject": "🧪 API Test - Agentic Financial Parser",
            "html_content": "<h3>✅ API Test from Agentic Financial Parser - Cron system is working via GAS!</h3>"
        }
        
        with httpx.Client(timeout=30.0) as client:
            response = client.post(gas_url, json=payload)
            
        if response.status_code == 200:
            return {"status": "success", "message": f"Test email sent to {SUBSCRIBERS[0]} via Google Apps Script!"}
        else:
            return {"status": "error", "message": f"GAS failed with status {response.status_code}"}
    except Exception as e:
        return {"status": "error", "message": f"HTTP failed: {str(e)}"}
