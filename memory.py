import uuid, datetime
from falkordb import FalkorDB

db = FalkorDB(host="localhost", port=6379)
g = db.select_graph("shared_memory")

def store_memory(text, entities, agent_id, namespace="shared", kind="fact"):
    mid = uuid.uuid4().hex[:8]
    g.query("""
    MERGE (a:Agent {id:$agent})
    CREATE (m:Memory {id:$mid, text:$text, kind:$kind, agent:$agent, namespace:$ns, created_at:$ts})
    MERGE (a)-[:WROTE]->(m)
    WITH m UNWIND $ents AS e
    MERGE (en:Entity {name:e})
    MERGE (m)-[:MENTIONS]->(en)
    """, {'agent': agent_id, 'mid': mid, 'text': text, 'kind': kind, 'ns': namespace,
          'ts': str(datetime.datetime.utcnow()), 'ents': entities})
    return mid

def recall_memory(entities, namespace="shared", limit=8):
    if not entities:
        return []
    r = g.query("""
    MATCH (m:Memory)-[:MENTIONS]->(e:Entity)
    WHERE e.name IN $names AND m.namespace = $ns
    RETURN DISTINCT m.id, m.text, m.agent, m.kind
    ORDER BY m.created_at DESC LIMIT $limit
    """, {'names': entities, 'ns': namespace, 'limit': limit})
    return [{"id": row[0], "text": row[1], "agent": row[2], "kind": row[3]} for row in r.result_set]

def recent_memory(namespace="shared", limit=20):
    r = g.query("""
    MATCH (m:Memory) WHERE m.namespace = $ns
    RETURN m.id, m.text, m.agent, m.kind ORDER BY m.created_at DESC LIMIT $limit
    """, {'ns': namespace, 'limit': limit})
    return [{"id": row[0], "text": row[1], "agent": row[2], "kind": row[3]} for row in r.result_set]