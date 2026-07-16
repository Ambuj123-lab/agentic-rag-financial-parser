from fastapi import APIRouter, Query, HTTPException
from app.rag.daily_insight_agent import fetch_daily_insight
from app.utils.email_sender import send_daily_insight_email
import os

router = APIRouter()

# This is the list of emails that will receive the daily AI insights
SUBSCRIBERS = [
    "ambujonly761@gmail.com",
    "tripathi.anku@outlook.com",
]

def background_email_task():
    print("Starting background email task...")
    insight_data = fetch_daily_insight()
    
    if not insight_data:
        print("Failed to fetch insight data.")
        return
        
    success = send_daily_insight_email(
        to_emails=SUBSCRIBERS,
        subject=insight_data["insight_title"],
        insight_title=insight_data["insight_title"],
        insight_explanation=insight_data["insight_explanation"],
        real_life_scenario=insight_data["real_life_scenario"],
        sources=insight_data["sources"]
    )
    
    if success:
        print("Successfully distributed daily insights.")
    else:
        print("Failed to distribute daily insights.")

@router.get("/send-daily-fact")
async def trigger_daily_email(
    token: str = Query(..., description="Secret token to trigger the cron job")
):
    """
    Triggers the autonomous AI agent to fetch a fact and email it.
    Can only be triggered if the correct secret token is provided.
    """
    secret_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "AmbujLegalBot2026")
    
    if token != secret_token:
        raise HTTPException(status_code=403, detail="Unauthorized cron trigger")
        
    try:
        print("Starting synchronous email task...")
        insight_data = fetch_daily_insight()
        
        if not insight_data:
            return {"status": "error", "message": "Failed to fetch insight data from LLM or Web."}
            
        success = send_daily_insight_email(
            to_emails=SUBSCRIBERS,
            subject=insight_data["insight_title"],
            insight_title=insight_data["insight_title"],
            insight_explanation=insight_data["insight_explanation"],
            real_life_scenario=insight_data["real_life_scenario"],
            sources=insight_data["sources"]
        )
        
        if success:
            return {"status": "success", "message": "Successfully generated and sent daily insight!"}
        else:
            return {"status": "error", "message": "Failed to send email via SMTP."}
    except Exception as e:
        return {"status": "error", "message": f"Server error: {str(e)}"}
