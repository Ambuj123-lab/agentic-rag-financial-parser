history = [{'content': '''⚠️ **Low Confidence Alert (RAG)**
I couldn't find an exact match in my verified legal/financial documents for this query.

**Action Required:**
Would you like me to switch to **Autonomous Web Search** to find the latest real-time information for you? 
*(Reply with "yes" to proceed)*
***
⚡ *Powered by 9-Node Agentic RAG | Engineered by Ambuj Kumar Tripathi*'''}]

prev_bot_msg = history[-1]['content'].lower()
user_reply = 'yes'
positive_replies = ['yes', 'haan', 'yep', 'sure', 'do it', 'search', 'ok', 'okay', 'kr do', 'kardo', 'han']

match = ('autonomous web search' in prev_bot_msg or 'search the internet for this' in prev_bot_msg)
reply_match = any(user_reply.startswith(pr) or user_reply == pr for pr in positive_replies)

print(f'Match: {match}, Reply Match: {reply_match}')
