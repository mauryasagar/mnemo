import json
from mcp.server.fastmcp import FastMCP
from memory import store_memory, recall_memory, recent_memory

mcp = FastMCP("Mnemo")

@mcp.tool()
def remember(text: str, entities: list[str] = [], agent_id: str = "default",
             namespace: str = "shared", kind: str = "fact") -> str:
    """Store a durable memory (fact, preference, task, decision)."""
    return f"Stored memory {store_memory(text, entities, agent_id, namespace, kind)}"

@mcp.tool()
def recall(entities: list[str], namespace: str = "shared", limit: int = 8) -> str:
    """Retrieve memories linked to these entities."""
    return json.dumps(recall_memory(entities, namespace, limit))

@mcp.tool()
def recent(namespace: str = "shared", limit: int = 20) -> str:
    """Get the most recent memories in a namespace."""
    return json.dumps(recent_memory(namespace, limit))

if __name__ == "__main__":
    mcp.run(transport="stdio")