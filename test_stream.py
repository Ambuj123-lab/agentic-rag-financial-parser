import httpx
import json

def test():
    with httpx.stream("POST", "http://127.0.0.1:8000/chat/stream", json={
        "email": "test@test.com",
        "name": "Test",
        "question": "What are the new tax slabs in Budget 2026?"
    }, params={"token": "mock-token-for-depends"}, timeout=60.0) as r:
        for line in r.iter_lines():
            if line:
                print(line)

if __name__ == "__main__":
    test()
