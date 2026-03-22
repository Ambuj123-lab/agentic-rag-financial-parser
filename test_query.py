import asyncio
import sys
import os

# Ensure app is in python path
sys.path.insert(0, os.path.abspath('.'))

from app.rag.graph import run_query

async def main():
    try:
        res = await run_query('hello', 'dev@test.com', 'Dev User', [])
        print(res)
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    asyncio.run(main())

