from app.rag.graph import call_llm
print('Calling LLM...')
response = call_llm('You are a helpful assistant.', 'Say hello world in 3 words.')
print('Response:', response)
