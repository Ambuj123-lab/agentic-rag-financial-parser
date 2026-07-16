import os
import random
import httpx
import json

def fetch_daily_insight():
    """
    1. Selects a random category.
    2. Uses Tavily to search for a unique legal/financial fact.
    3. Uses OpenRouter LLM (or Gemini) to format it into the "Did you know?" HTML structure.
    """
    tavily_key = os.getenv("TAVILY_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not tavily_key or not gemini_key:
        print("Missing API keys for Tavily or Gemini")
        return None

    # Step 1: Select Random Category
    categories = [
        "Fundamental Rights and Articles of the Indian Constitution",
        "Important Amendments in the Indian Constitution",
        "Consumer Rights in India",
        "Traffic and Motor Vehicles Act rules in India",
        "RBI Banking and ATM rules for consumers",
        "Cyber Fraud and IT Act rules in India",
        "Income Tax deductions for individuals in India"
    ]
    selected_category = random.choice(categories)
    
    search_query = f"lesser known but highly useful problem solving law about {selected_category} for common citizens 2026"

    # Step 2: Fetch Data from Tavily
    print(f"Searching Tavily for: {search_query}")
    with httpx.Client(timeout=30.0) as client:
        tavily_response = client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": tavily_key,
                "query": search_query,
                "search_depth": "advanced",
                "include_answer": True,
                "max_results": 3
            }
        )
    
    if tavily_response.status_code != 200:
        print("Tavily search failed:", tavily_response.text)
        return None
        
    tavily_data = tavily_response.json()
    tavily_answer = tavily_data.get("answer", "")
    tavily_results = tavily_data.get("results", [])
    
    sources = [res["url"] for res in tavily_results][:3]
    
    # Step 3: Use LLM to synthesize and format the data
    prompt = f"""
    You are an expert Indian Legal and Financial AI Assistant. 
    Based on the following web search data, extract ONE highly practical and useful law/fact.
    
    Web Search Data:
    {tavily_answer}
    
    Output a JSON object with exactly these 3 keys:
    1. "insight_title": A catchy title starting with "Did you know? - [Topic]"
    2. "insight_explanation": A simple 2-3 sentence explanation of the law in Hinglish or English.
    3. "real_life_scenario": A practical 2-3 sentence scenario showing how this law saves people from trouble.
    
    Do NOT output markdown blocks, just raw valid JSON.
    """
    
    print("Generating AI Insight via Gemini 3.1 Flash Lite...")
    with httpx.Client(timeout=60.0) as client:
        llm_response = client.post(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-lite-preview:generateContent?key={gemini_key}",
            headers={"Content-Type": "application/json"},
            json={
                "contents": [{"parts": [{"text": prompt}]}],
                "generationConfig": {"responseMimeType": "application/json"}
            }
        )
    
    if llm_response.status_code != 200:
        print("LLM generation failed:", llm_response.text)
        return None
        
    try:
        data = llm_response.json()
        content = data["candidates"][0]["content"]["parts"][0]["text"]
        
        parsed_insight = json.loads(content)
        
        return {
            "insight_title": parsed_insight["insight_title"],
            "insight_explanation": parsed_insight["insight_explanation"],
            "real_life_scenario": parsed_insight["real_life_scenario"],
            "sources": sources
        }
    except Exception as e:
        print(f"Failed to parse JSON from LLM: {e}")
        return None

