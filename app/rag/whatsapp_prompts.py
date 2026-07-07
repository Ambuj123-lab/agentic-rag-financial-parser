"""
WhatsApp-specific Prompts and Formatting Logic.
Handles greeting menus, disclaimers, and WhatsApp-friendly formatting rules.
"""

WHATSAPP_GREETING_MENU = """👋 Welcome to *Ambuj Kumar Tripathi's Adaptive Agentic AI*.

Designed & Engineered by *Ambuj Kumar Tripathi*.

I'm an advanced AI Assistant powered by a *production-grade 9-Node Adaptive Agentic RAG Architecture*.

I can help you with:

⚖️ Indian Constitution, Laws & Legal Research
💰 Taxation & Financial Regulations
💻 Programming, AI & Technical Queries
🌐 Live Web Search *(when additional information is required)*

✨ Features:
✅ Adaptive Retrieval
✅ Human-in-the-Loop (HITL)
✅ Confidence-Aware Routing
✅ Multi-turn Conversations
✅ Context-Aware Responses

⚠️ *Note:* WhatsApp does NOT support file/PDF uploads. Please use my Web Interface at https://agentic-financial-parser.onrender.com for Document Analysis (Max 10MB / 30 Pages).

💡 Example Questions:
• Explain Article 21 of the Constitution.
• What are the latest RBI KYC guidelines?
• Show a FastAPI Semantic Cache example.

🚀 How can I assist you today?
"""

WHATSAPP_DISCLAIMER = "\n\n_⚠️ Disclaimer: This AI queries documents for training and learning purposes only. It is not a substitute for professional advice. For critical matters, please consult a qualified CA, advocate, or relevant expert._"

# This instruction is appended to the LLM system prompt when source="whatsapp"
WHATSAPP_SYSTEM_INSTRUCTION = """
CRITICAL WHATSAPP FORMATTING RULES:
You are interacting with a user via WhatsApp. You MUST follow these rules strictly:
1. DO NOT use Markdown tables. Tables render terribly on WhatsApp. Use bullet points instead.
2. DO NOT use Markdown headers like `#` or `##`. Use bold text `*Heading*` instead.
3. Use WhatsApp-specific markdown for bold (`*text*`) and italics (`_text_`).
4. Keep answers relatively short and concise (under 3000 characters). Break complex ideas into easy-to-read bullet points.
5. If the user greets you (hi, hello, hey), casually remind them that you are created by Ambuj Tripathi, but do not sound robotic.
6. Remember that you are fully capable of answering in Hindi, English, Hinglish, and Devanagari. Match the user's language and tone exactly.
"""
