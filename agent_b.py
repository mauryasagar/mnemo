import asyncio, sys, json
from fastmcp import Client
from llm import answer

async def main():
    q = " ".join(sys.argv[1:]) or "What do you know about the hackathon project?"
    print(f"[reviewer] question: {q}")
    
    async with Client("server.py") as c:
        print("[reviewer] connecting to shared memory...")
        r = await c.call_tool("recent", {"limit": 20})
        
        # The result is now a clean JSON string
        mems = json.loads(r.content[0].text)

        print(f"[reviewer] recalled {len(mems)} memories from shared graph")
        for m in mems:
            print(f"  [{m['id']}] ({m['agent']}, {m['kind']}) {m['text']}")
            
        print(f"\n[reviewer] asking Gemma to answer based on these memories...")
        ans = answer(q, mems)
        print(f"\n[reviewer] answer:\n{ans}")

asyncio.run(main())