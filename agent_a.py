import asyncio, sys, os
from fastmcp import Client
from llm import extract

def get_data(r):
    if hasattr(r, "data") and r.data is not None:
        return r.data
    if hasattr(r, "content") and r.content:
        return r.content[0].text
    return str(r)

async def main():
    msg = " ".join(sys.argv[1:]) or "Alice is building the FalkorDB hackathon project, deadline Oct 18."
    agent_id = os.environ.get("AGENT_ID", "planner")
    print(f"[{agent_id}] user: {msg}")
    data = extract(msg)
    
    async with Client("server.py") as c:
        for m in data["memories"]:
            r = await c.call_tool("remember", {
                "text": m["text"], "entities": m["entities"],
                "agent_id": agent_id, "kind": m["kind"]
            })
            print(f"[{agent_id}] stored: {m['text']} -> {get_data(r)}")

asyncio.run(main())