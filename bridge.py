from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from memory import store_memory, recent_memory
import uvicorn

app = FastAPI(title="Mnemo Bridge")

# Allow the browser extension to talk to this server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/remember")
async def remember(request: Request):
    data = await request.json()
    mid = store_memory(
        text=data.get("text", ""), 
        entities=data.get("entities", []), 
        agent_id=data.get("agent_id", "browser_web"), 
        kind="fact"
    )
    return {"status": "success", "id": mid}

@app.get("/recall")
async def recall():
    # Grab the 5 most recent memories to inject into the AI
    return recent_memory(limit=5)

if __name__ == "__main__":
    print("Starting Mnemo Bridge on port 8000...")
    uvicorn.run(app, host="127.0.0.1", port=8000)