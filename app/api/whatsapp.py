import json
import logging
import httpx
from fastapi import APIRouter, Depends, Request, Response, HTTPException
from fastapi.responses import PlainTextResponse

from app.core.config import get_settings
from app.db.mongodb import get_chat_history

logger = logging.getLogger(__name__)
settings = get_settings()

router = APIRouter()

# ---------------------------------------------------------
# META WEBHOOK VERIFICATION (GET)
# ---------------------------------------------------------
@router.get("/whatsapp/webhook")
async def verify_webhook(request: Request):
    """
    Meta uses this endpoint to verify the webhook URL.
    It sends hub.mode, hub.challenge, and hub.verify_token.
    """
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == settings.WHATSAPP_WEBHOOK_VERIFY_TOKEN:
            logger.info("✅ WhatsApp Webhook verified successfully!")
            return PlainTextResponse(content=challenge, status_code=200)
        else:
            logger.warning("❌ WhatsApp Webhook verification failed: Token mismatch")
            raise HTTPException(status_code=403, detail="Verification failed")
    
    raise HTTPException(status_code=400, detail="Bad Request")


# ---------------------------------------------------------
# RECEIVE WHATSAPP MESSAGES (POST)
# ---------------------------------------------------------
from fastapi import APIRouter, Depends, Request, Response, HTTPException, BackgroundTasks

@router.post("/whatsapp/webhook")
async def receive_whatsapp_message(request: Request, background_tasks: BackgroundTasks):
    """
    Receives incoming WhatsApp messages, processes them through LangGraph,
    and sends the response back to the user via WhatsApp API.
    """
    try:
        body = await request.json()
    except Exception:
        return Response(status_code=200)  # Always return 200 to WhatsApp to avoid retries

    if body.get("object") != "whatsapp_business_account":
        return Response(status_code=404)

    try:
        for entry in body.get("entry", []):
            for change in entry.get("changes", []):
                value = change.get("value", {})
                
                # Check if it's a message
                if "messages" in value and value["messages"]:
                    message = value["messages"][0]
                    phone_number_id = value["metadata"]["phone_number_id"]
                    from_number = message["from"]
                    message_id = message["id"]
                    # Extract user profile name if available
                    user_name = "WhatsApp User"
                    if "contacts" in value and len(value["contacts"]) > 0:
                        user_name = value["contacts"][0].get("profile", {}).get("name", "WhatsApp User")
                    
                    # We only process text messages
                    if message["type"] == "text":
                        # Ignore stale messages (older than 5 minutes) from Meta retries
                        timestamp = message.get("timestamp")
                        if timestamp:
                            import time
                            current_time = int(time.time())
                            if current_time - int(timestamp) > 300:
                                logger.warning(f"⏳ Dropping stale WhatsApp message from {from_number} (Age: {current_time - int(timestamp)}s)")
                                continue

                        text_body = message["text"]["body"].strip()
                        logger.info(f"📱 WhatsApp Msg Received from {from_number} ({user_name}): {text_body}")
                        
                        # Process the message asynchronously in the background so we return 200 OK instantly
                        background_tasks.add_task(process_and_reply, from_number, text_body, phone_number_id, message_id, user_name)
                        
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        
    return Response(content="EVENT_RECEIVED", status_code=200)


async def process_and_reply(to_number: str, text: str, phone_number_id: str, message_id: str, user_name: str = "WhatsApp User"):
    """Run LangGraph and send reply via WhatsApp API."""
    from app.rag.graph import run_query
    from app.rag.whatsapp_prompts import WHATSAPP_GREETING_MENU
    
    # Check if it's a greeting to send the exact menu
    lower_text = text.lower().strip()
    if lower_text in ["hi", "hello", "hey", "namaste"]:
        # Send Menu directly without hitting LLM to save latency
        await send_whatsapp_message(to_number, phone_number_id, WHATSAPP_GREETING_MENU)
        return

    # No Thinking indicator, wait for graph processing
    
    # Use phone number as the unique "email" for MongoDB history
    fake_email = f"whatsapp_{to_number}@meta.com"
    history = await get_chat_history(fake_email, limit=6)
    
    try:
        result = await run_query(
            query=text,
            user_email=fake_email,
            user_name=user_name,
            chat_history=history,
            source="whatsapp"  # Critical: tells Graph to use WhatsApp formatting
        )
        
        answer = result.get("answer", "I'm sorry, I couldn't process your request.")
        
        # Append sources if available
        sources = result.get("sources", [])
        if sources:
            answer += "\n\n📚 *Sources:*"
            for i, src in enumerate(sources[:3]):
                # src is a string (filename or "Web Search"), not a dict!
                title = str(src)
                answer += f"\n{i+1}. {title}"
        
        # Convert standard Markdown to WhatsApp-friendly format
        import re
        answer = re.sub(r'\*\*(.*?)\*\*', r'*\1*', answer) # **bold** to *bold*
        answer = re.sub(r'^#+\s+', '', answer, flags=re.MULTILINE) # Remove Headers
        answer = re.sub(r'^\s*-\s+', '• ', answer, flags=re.MULTILINE) # Clean bullets

        # WhatsApp limits text to 4096 chars.
        if len(answer) > 4000:
            answer = answer[:4000] + "...\n(Answer truncated due to WhatsApp limits)"
            
        await send_whatsapp_message(to_number, phone_number_id, answer)
        
        # Save chat to MongoDB
        from app.db.mongodb import save_message
        await save_message(fake_email, "user", text)
        await save_message(fake_email, "assistant", answer, result.get("sources", []))
        
    except Exception as e:
        logger.error(f"WhatsApp graph execution failed: {e}")
        await send_whatsapp_message(to_number, phone_number_id, "I apologize, but I encountered a technical error. Please try again.")


async def send_whatsapp_message(to_number: str, phone_number_id: str, message_body: str):
    """Helper to send HTTP POST back to Meta's Cloud API."""
    token = settings.WHATSAPP_ACCESS_TOKEN
    
    if not token or not phone_number_id:
        logger.error("WhatsApp credentials missing in environment variables.")
        return

    url = f"https://graph.facebook.com/v20.0/{phone_number_id}/messages"
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {
            "preview_url": True,
            "body": message_body
        }
    }
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(url, json=payload, headers=headers)
            if resp.status_code not in (200, 201):
                logger.error(f"Failed to send WhatsApp message: {resp.status_code} - {resp.text}")
            else:
                logger.info(f"✅ Reply sent to {to_number}")
        except Exception as e:
            logger.error(f"Error sending WhatsApp message via HTTP: {e}")
