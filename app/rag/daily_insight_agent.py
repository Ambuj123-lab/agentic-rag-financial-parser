import os
import random
import httpx
import json
from collections import deque

# In-memory tracker to prevent repeating categories within the same server lifecycle.
# With 50+ categories and maxlen=40, topics won't repeat for ~5 days even at 8 emails/day.
RECENT_CATEGORIES = deque(maxlen=40)

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

    # Step 1: Select Random Category (50+ topics for maximum variety)
    categories = [
        # ── Constitutional & Rights ──
        "Fundamental Rights and Articles of the Indian Constitution",
        "Important Amendments in the Indian Constitution",
        "Consumer Rights in India",
        "RTI (Right to Information) filing process and citizen power in India",
        "PIL (Public Interest Litigation) how common citizens can file in India",
        "Directive Principles of State Policy and their real-world impact in India",
        
        # ── Financial & Tax ──
        "New vs Old Income Tax Regime rules and deductions effective from April 1, 2026 in India",
        "RBI Banking and ATM rules for consumers",
        "SEBI rules and Mutual Fund regulations for retail investors",
        "Credit Score (CIBIL) and Loan rights for borrowers in India",
        "IRDAI rules and Health/Term Insurance claim rights for citizens",
        "GST rules and input tax credit for small businesses in India",
        "HRA, LTA and salary tax exemptions for salaried employees in India",
        "Capital gains tax on property, gold and mutual funds in India",
        "Startup India tax benefits under Section 80-IAC and angel tax rules",
        "EPF and PPF withdrawal rules and tax implications in India",
        "NPS (National Pension System) tax benefits under Section 80CCD in India",
        "TDS rules on freelance income and professional services in India",
        "Sukanya Samriddhi Yojana and girl child savings scheme rules in India",
        
        # ── Digital & Cyber ──
        "Cyber Fraud, Data Privacy, and IT Act rules in India",
        "Digital Personal Data Protection Act (DPDP) 2023 citizen rights in India",
        "UPI fraud prevention and RBI refund rules for digital payments in India",
        "Right to be forgotten and data erasure under Indian law",
        "OTT and social media content regulation rules in India",
        
        # ── Safety & Legal ──
        "Women's safety rights and POSH Act (Prevention of Sexual Harassment) in India",
        "Child protection laws and POCSO Act awareness in India",
        "Citizen rights during police arrest, FIR filing, and bail in India",
        "Traffic and Motor Vehicles Act rules in India",
        "Tenant and Landlord legal rights and rent control in India",
        "Domestic violence laws and protective rights for women in India",
        "BNS (Bharatiya Nyaya Sanhita) basic citizen safety sections and rules",
        "Anti-ragging laws and UGC regulations in Indian colleges",
        "Senior citizen rights and Maintenance and Welfare Act protections in India",
        "Disability rights and RPWD Act benefits in India",
        "Noise pollution and environment protection citizen rights in India",
        
        # ── Property & Real Estate ──
        "RERA Act rights for homebuyers against builders in India",
        "Property registration and stamp duty rules across Indian states",
        "Inheritance and succession laws for ancestral property in India",
        "Will drafting and probate process in India",
        
        # ── Employment & Labour ──
        "Employee rights under new Labour Codes 2025 in India",
        "Gratuity and severance pay calculation rules in India",
        "Maternity and paternity leave entitlements in India",
        "Wrongful termination and notice period laws in India",
        "Gig worker and freelancer legal protections in India",
        
        # ── Healthcare ──
        "Ayushman Bharat scheme eligibility and hospital rights in India",
        "Medical negligence and patient rights in Indian hospitals",
        "Organ donation laws and living will (advance directive) in India",
        "Food safety and FSSAI consumer complaint rights in India",
        
        # ── Everyday Legal ──
        "Cheque bounce penalties and process under Section 138 NI Act in India",
        "Defamation laws (civil vs criminal) in India",
        "Election laws and Model Code of Conduct awareness in India",
    ]
    
    # Filter out categories that were sent recently to avoid repeats
    available_categories = [c for c in categories if c not in RECENT_CATEGORIES]
    if not available_categories:
        available_categories = categories # Fallback if tracker fills up
        
    selected_category = random.choice(available_categories)
    RECENT_CATEGORIES.append(selected_category)
    
    # Add randomness to the search angle to prevent LLM fatigue
    search_angles = [
        "most essential and basic fundamental law or right about",
        "recent changes, penalties or rules regarding",
        "common misconceptions and practical legal truth about",
        "step-by-step rights and legal protection for citizens regarding"
    ]
    selected_angle = random.choice(search_angles)
    
    search_query = f"{selected_angle} {selected_category} that every common citizen of India must know 2026"

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
    2. "insight_explanation": A simple 2-3 sentence explanation of the law in Hinglish or English. YOU MUST INCLUDE THE EXACT SECTION, ARTICLE, OR RULE NUMBER IF AVAILABLE.
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

