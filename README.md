# Mnemo

### Universal, Graph-Backed Memory Layer for AI Agents

Mnemo is a persistent memory infrastructure that allows distinct AI agents to share context, recall facts autonomously, and maintain provenance across different platforms.

**[Explore the Architecture](#architecture-overview) · [View Features](#core-features) · [Quick Start](#setup--installation)**

---

## 🚨 The Problem

Modern AI interactions suffer from a fundamental flaw: **amnesia**.

1. **Session Isolation:** Terminal agents, such as Cursor agents and local scripts, forget everything when their processes end.
2. **Walled Gardens:** Web-based AI assistants like ChatGPT, Claude, and Gemini operate in silos. Information shared with one assistant is not automatically available to another.
3. **The Vector Database Trap:** Many AI memory solutions rely on flat vector databases and semantic search, making it difficult to trace why an AI knows something or understand relationships between entities.

## 💡 The Solution: Mnemo

**Mnemo** acts as a universal memory layer that decouples AI memory from the AI model itself.

Instead of requiring an AI to remember everything internally, Mnemo provides tools to store and retrieve information from an external memory graph.

By combining the **Model Context Protocol (MCP)** with **FalkorDB**, Mnemo allows compatible AI agents to:

- **Save** facts and session data to a unified graph.
- **Recall** context across different platforms.
- **Trace** provenance by identifying which agent stored a memory and when.

A memory saved by one connected agent can be retrieved by another, including local scripts and browser-based AI interfaces, through the shared memory infrastructure.

---

## 🏗️ Architecture Overview

Mnemo uses a decoupled architecture that connects local AI processes with web-based AI interfaces through a shared graph database.

```text
       [ Local Terminal ]                   [ Web Browser ]
       ├── agent_a.py (Writer)               ├── ChatGPT
       └── agent_b.py (Reader)               ├── Gemini
                 │                           └── Chrome Extension
                 │ MCP                                │ HTTP
                 ▼                                    ▼
  ┌──────────────────────────────────────────────────────────┐
  │                    Mnemo Core (Local)                    │
  │                                                          │
  │   [ server.py ] (MCP Server) ◄────► [ bridge.py ]        │
  │                                            (FastAPI)     │
  └──────────────────────┬───────────────────┬──────────────┘
                         │                   │
                         │ Cypher Queries    │ Cypher Queries
                         ▼                   ▼
              ┌────────────────────────────────────┐
              │           FalkorDB (Graph)         │
              │                                    │
              │  (Agent) ──[:WROTE]──► (Memory)    │
              │  (Memory) ─[:MENTIONS]► (Entity)   │
              └────────────────────────────────────┘
```

### How It Works

1. An AI agent stores information through Mnemo's MCP server or HTTP bridge.
2. Mnemo records the memory and associates it with the agent that created it.
3. Entities mentioned in the memory are linked to graph nodes.
4. Other connected agents retrieve relevant memories by traversing the graph.

---

## ✨ Core Features

- **Standard MCP Integration:** A native Model Context Protocol server enables compatible clients, including Claude Desktop, Cursor, and custom Python agents, to access memory tools.
- **Cross-Platform Memory Bridge:** A FastAPI bridge and Chrome extension connect browser-based AI interfaces to the same memory graph used by local agents.
- **Provenance and Traceability:** Memories are linked to the agents that created them, preserving information about their origin.
- **Relational Multi-Hop Reasoning:** Graph traversal follows entity relationships instead of relying exclusively on semantic similarity.
- **Local-First Privacy:** The intended architecture runs the memory database and local language model on your machine, reducing reliance on third-party AI APIs for memory processing.

---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Database | [FalkorDB](https://www.falkordb.com/) | Graph database for storing memories and entity relationships using Cypher queries. |
| Protocol | [Model Context Protocol](https://modelcontextprotocol.io/) | Standard interface for AI agents to interact with memory tools. |
| Backend Bridge | [FastAPI](https://fastapi.tiangolo.com/) and [Uvicorn](https://www.uvicorn.org/) | Handles HTTP requests from the browser extension. |
| AI Engine | [Ollama](https://ollama.com/) with `gemma4:e2b` | Local language model for extracting entities and generating answers from recalled context. |
| Browser Extension | Chrome Manifest V3 | Connects supported web-based AI interfaces to Mnemo. |
| Language | Python 3.10+ and Vanilla JavaScript | Backend services and browser extension logic. |

---

## 🕸️ The Graph Model

Mnemo uses a property graph to represent memories and their relationships. Rather than storing only isolated text, it connects each memory to the agent that created it and the entities it mentions.

```cypher
(:Agent {id})
    │
    └──[:WROTE]──► (:Memory {
                        id,
                        text,
                        kind,
                        created_at
                    })
                        │
                        └──[:MENTIONS]──► (:Entity {name})
```

### Core Cypher Queries

The following queries illustrate the graph operations used by the memory layer. Adapt them to your actual database schema and application code as needed.

#### 1. Storing a Memory and Extracting Entities

Create a memory, associate it with the authoring agent, and link the memory to extracted entities.

```cypher
MERGE (a:Agent {id: $agent})
CREATE (m:Memory {
    id: $mid,
    text: $text,
    kind: $kind,
    agent: $agent,
    created_at: $ts
})
MERGE (a)-[:WROTE]->(m)
WITH m
UNWIND $ents AS e
MERGE (en:Entity {name: e})
MERGE (m)-[:MENTIONS]->(en)
```

#### 2. Recalling Memories Through Graph Traversal

Find memories connected to entities mentioned in a query.

```cypher
MATCH (m:Memory)-[:MENTIONS]->(e:Entity)
WHERE e.name IN $names
RETURN DISTINCT
    m.id,
    m.text,
    m.agent,
    m.kind,
    m.created_at
ORDER BY m.created_at DESC
LIMIT $limit
```

**Note:** These examples assume that the relevant parameters are supplied by the application. Verify compatibility with your FalkorDB client and Cypher implementation before using them.

---

## 📸 Screenshots

Add screenshots of your running project to demonstrate its functionality.

### 1. Terminal Agents Sharing Memory Through MCP

![Terminal agents sharing memory](https://via.placeholder.com/800x400?text=Replace+with+Terminal+Screenshot)

### 2. FalkorDB Graph Visualization

![FalkorDB graph visualization](https://via.placeholder.com/800x400?text=Replace+with+FalkorDB+Graph+Screenshot)

### 3. Browser Extension Integration

![Browser extension integration](https://via.placeholder.com/800x400?text=Replace+with+Browser+Extension+Screenshot)

> **Before publishing:** Replace these placeholder images with actual screenshots. You can store your images in a `screenshots/` directory and reference them using relative paths, such as `![Terminal output](screenshots/terminal.png)`.

---

## 🚀 Setup & Installation

Follow these steps to run Mnemo locally.

### Prerequisites

Make sure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Python 3.10 or later](https://www.python.org/downloads/)
- [Ollama](https://ollama.com/)
- Git, if you are cloning the repository

### 1. Start FalkorDB

Start the graph database using Docker.

**Windows:**

```powershell
docker.exe run -d --name mnemo-falkordb -p 6379:6379 -p 3000:3000 falkordb/falkordb:latest
```

**macOS/Linux:**

```bash
docker run -d --name mnemo-falkordb -p 6379:6379 -p 3000:3000 falkordb/falkordb:latest
```

The database is exposed on port `6379`, and the web interface is exposed on port `3000`, according to the configuration above.

Open the dashboard at:

**http://localhost:3000**

If you already have a container named `mnemo-falkordb`, reuse it or remove it before creating another container with the same name.

### 2. Install Python Dependencies

Optionally, create and activate a virtual environment.

**Windows PowerShell:**

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install the required packages:

```bash
pip install fastmcp==3.4.9 falkordb ollama fastapi uvicorn
```

### 3. Configure Ollama

Ensure Ollama is installed and running. Pull the model used by this project:

```bash
ollama pull gemma4:e2b
```

Confirm that the model is available:

```bash
ollama list
```

### 4. Run the Terminal Agents

Use two separate terminal processes to test memory sharing through MCP.

**Terminal 1 — Store a memory:**

```bash
python agent_a.py "Alice is building the FalkorDB hackathon project. Deadline is Oct 18."
```

**Terminal 2 — Recall the memory:**

```bash
python agent_b.py "What do you know about Alice and the deadline?"
```

The second agent should retrieve relevant information saved by the first agent, provided both scripts are configured to use the same Mnemo server and graph database.

### 5. Start the HTTP Bridge

Start the FastAPI bridge so the browser extension can communicate with Mnemo.

```bash
python bridge.py
```

Keep the terminal running. The bridge is expected to listen at:

**http://127.0.0.1:8000**

If your application uses a different host or port, update the extension configuration accordingly.

### 6. Load the Chrome Extension

1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode**.
4. Click **Load unpacked**.
5. Select the `extension/` directory in the Mnemo repository.
6. Open a supported AI interface, such as ChatGPT, Claude, or Gemini.
7. Use the extension's memory controls, if implemented, to save a session or inject recalled memories.

The extension should be configured to communicate with the local bridge at `http://127.0.0.1:8000`.

---

## 🔒 Privacy

Mnemo is designed to keep its memory infrastructure local by using a local graph database and a local language model.

Actual privacy guarantees depend on the configuration of the browser extension, connected AI services, and any external APIs used by your application. Review those integrations before storing sensitive information.

---

## 📄 License

Add your chosen license here, along with a link to the repository's `LICENSE` file if one exists.