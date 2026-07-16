from fastapi import APIRouter, Query, HTTPException, BackgroundTasks
from app.rag.daily_insight_agent import fetch_daily_insight
from app.utils.email_sender import send_daily_insight_email
import os

router = APIRouter()

# This is the list of emails that will receive the daily AI insights
SUBSCRIBERS = [
    "ambujonly761@gmail.com",
    # Add your friends' emails here:
    # "friend1@gmail.com",
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
    background_tasks: BackgroundTasks,
    token: str = Query(..., description="Secret token to trigger the cron job")
):
    """
    Triggers the autonomous AI agent to fetch a fact and email it.
    Can only be triggered if the correct secret token is provided.
    """
    secret_token = os.getenv("WHATSAPP_WEBHOOK_VERIFY_TOKEN", "AmbujLegalBot2026")
    
    if token != secret_token:
        raise HTTPException(status_code=403, detail="Unauthorized cron trigger")
        
    # Run the heavy LLM/Tavily search and email sending in the background
    # so the cron-job.org HTTP request doesn't timeout.
    background_tasks.add_task(background_email_task)
    
    return {"status": "success", "message": "Daily AI Insight generation started in the background."}
