### prompting
- ```Zero Shot```: The model is given a direct question or task without prior examples.
- ```Few Shot```:  50-60 examples are given to increase the accuracy of responses (upto 50% in some instances)
- ```Few Shot Prompting with Structured output``` :   Allows us to produce easily parsable strucutured output to make it easier to serialize
- ```Chain of Thoughts Prompting```: Provides the multistep resolution of complext problem with each step depending on previous step by providing histomery of messages for continued context
- ```Persona Based Prompting``` : Persona based prompting is useful in making the responses more personalized and aligned to the user's preferences and characteristics.

### Types of memory in llm 

#### Short-Term vs Long-Term Memory Comparison

| Aspect | Short-Term Memory | Long-Term Memory |
|--------|-------------------|------------------|
| **Duration** | Current conversation session | Persists across sessions |
| **Storage** | Model's context window (tokens) | External databases/storage |
| **Capacity** | Limited (4K-128K tokens) | Virtually unlimited |
| **Purpose** | Keep conversation coherent | Preserve knowledge across time |
| **Components** | Conversation history, working memory, attention context | Factual memory, episodic memory, semantic memory |
| **Lifespan** | Lost when conversation ends | Survives indefinitely |
| **Speed** | Immediate access (very fast) | Requires retrieval/lookup |
| **Use Cases** | Multi-turn dialogue, reasoning chains | User preferences, past interactions, domain knowledge |

##### Short-Term Memory Includes:
- **Conversation History** – Recent message turns in order for coherent dialogue
- **Working Memory** – Temporary state such as tool outputs or intermediate calculations
- **Attention Context** – Immediate focus of the assistant (like holding a thought mid-sentence)

##### Long-Term Memory Includes:
- **Factual Memory** – User preferences, account details, and domain facts
- **Episodic Memory** – Summaries of past interactions or completed tasks
- **Semantic Memory** – Relationships between concepts for reasoning and inference

![alt text](image.png)

#### Mem0: Memory Management for AI Agents

**Mem0** is a memory management framework that bridges short-term and long-term memory for AI agents.

##### Mem0's Key Capabilities:

| Feature | Benefit |
|---------|---------|
| **Unified Memory API** | Single interface for managing conversation history, facts, and preferences |
| **Persistent Storage** | Automatically saves conversation context to databases (vector DB, SQL, etc.) |
| **Automatic Retrieval** | Intelligently retrieves relevant past interactions for context |
| **Memory Organization** | Hierarchically organizes facts, preferences, and episodic memories |
| **Smart Summarization** | Condenses long conversations to preserve tokens and context |
| **Multi-user Support** | Maintains separate memory profiles for different users |
| **Memory Graph** | Creates relationships between concepts for semantic understanding |

##### How Mem0 Works with Memory Types:

**Short-Term Memory:**
- Recent conversation turns are kept in the context window
- Mem0 decides what's important enough to save long-term
- Automatically manages token limits

**Long-Term Memory:**
- Stores user facts, preferences, and conversation summaries
- Retrieves relevant history for new conversations
- Learns user patterns over time

##### Integration Example:

```python
from mem0 import Memory

# Initialize Mem0
memory = Memory.from_config({
    "llm": {"provider": "openai", "config": {"model": "gpt-4"}},
    "embedder": {"provider": "openai"},
    "vector_store": {"provider": "pinecone"}
})

# Add to memory
memory.add("User prefers vegetarian food", user_id="user123")

# Search memory
results = memory.search("dietary preferences", user_id="user123")

# Use in LLM context
chat_history = memory.get_history(user_id="user123", limit=5)
```


### Memory Augmentation using Knowledge Graphs

- We can use knowledge graphs like neo4j to give more relationship, hierarchical context along with memory
- Its really heavy to self host so use the free tier cloud instance

## Cypher Query Basics for Neo4j

Cypher is Neo4j's graph query language for querying and manipulating graph data.

### Basic Patterns

```cypher
// Nodes: (variable:Label {property: value})
// Relationships: -[:TYPE]-> or <-[:TYPE]-
// Patterns: (node1)-[:RELATIONSHIP]->(node2)
```

### CRUD Operations

#### CREATE - Add nodes and relationships

```cypher
// Create a node
CREATE (p:Person {name: "Alice", age: 30})

// Create multiple nodes with relationship
CREATE (a:Person {name: "Alice"})-[:KNOWS]->(b:Person {name: "Bob"})

// Create relationship between existing nodes
MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
CREATE (a)-[:WORKS_WITH]->(b)
```

#### MATCH - Find/Query data

```cypher
// Find all persons
MATCH (p:Person) RETURN p

// Find specific person
MATCH (p:Person {name: "Alice"}) RETURN p

// Find relationships
MATCH (a:Person)-[r:KNOWS]->(b:Person)
RETURN a.name, type(r), b.name

// Find with WHERE clause
MATCH (p:Person)
WHERE p.age > 25
RETURN p.name, p.age
```

#### UPDATE - Modify data

```cypher
// Set property
MATCH (p:Person {name: "Alice"})
SET p.age = 31
RETURN p

// Add new property
MATCH (p:Person {name: "Alice"})
SET p.email = "alice@example.com"

// Update multiple properties
MATCH (p:Person {name: "Alice"})
SET p += {city: "NYC", country: "USA"}
```

#### DELETE - Remove data

```cypher
// Delete relationship only
MATCH (a:Person {name: "Alice"})-[r:KNOWS]->(b)
DELETE r

// Delete node (must delete relationships first)
MATCH (p:Person {name: "Alice"})
DETACH DELETE p  // DETACH deletes all relationships too
```

### Common Query Patterns

#### Filtering

```cypher
// Multiple conditions
MATCH (p:Person)
WHERE p.age > 25 AND p.city = "NYC"
RETURN p

// Pattern matching in WHERE
MATCH (p:Person)
WHERE (p)-[:KNOWS]->(:Person {name: "Bob"})
RETURN p.name
```

#### Ordering & Limiting

```cypher
// Sort and limit results
MATCH (p:Person)
RETURN p.name, p.age
ORDER BY p.age DESC
LIMIT 10

// Skip and limit (pagination)
MATCH (p:Person)
RETURN p
ORDER BY p.name
SKIP 20 LIMIT 10
```

#### Aggregation

```cypher
// Count
MATCH (p:Person) RETURN count(p)

// Group by and count
MATCH (p:Person)
RETURN p.city, count(*) as people_count

// Other aggregations
MATCH (p:Person)
RETURN avg(p.age), min(p.age), max(p.age), sum(p.age)
```

#### Path Finding

```cypher
// Shortest path
MATCH path = shortestPath(
  (a:Person {name: "Alice"})-[*]-(b:Person {name: "Charlie"})
)
RETURN path

// Variable-length relationships
MATCH (a:Person {name: "Alice"})-[:KNOWS*1..3]->(friend)
RETURN DISTINCT friend.name

// All paths
MATCH path = (a:Person {name: "Alice"})-[:KNOWS*]-(b:Person)
RETURN path
```

### Advanced Examples

#### Graph Traversal

```cypher
// Friends of friends
MATCH (me:Person {name: "Alice"})-[:KNOWS]->(friend)-[:KNOWS]->(fof)
WHERE NOT (me)-[:KNOWS]->(fof) AND me <> fof
RETURN DISTINCT fof.name

// Recommendation: find books read by similar users
MATCH (me:User {id: 123})-[:READ]->(b:Book)<-[:READ]-(other:User)
MATCH (other)-[:READ]->(rec:Book)
WHERE NOT (me)-[:READ]->(rec)
RETURN rec.title, count(*) as score
ORDER BY score DESC
LIMIT 5
```

#### WITH Clause (Pipeline Queries)

```cypher
// Multi-step query
MATCH (p:Person)
WITH p, size((p)-[:KNOWS]->()) as friend_count
WHERE friend_count > 5
RETURN p.name, friend_count
ORDER BY friend_count DESC
```

#### MERGE (Upsert)

```cypher
// Create if not exists, otherwise match
MERGE (p:Person {email: "alice@example.com"})
ON CREATE SET p.created = timestamp(), p.name = "Alice"
ON MATCH SET p.updated = timestamp()
RETURN p
```

### Python Integration with Neo4j

```python
from neo4j import GraphDatabase

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self.driver.close()
    
    def query(self, cypher_query, parameters=None):
        with self.driver.session() as session:
            result = session.run(cypher_query, parameters)
            return [record.data() for record in result]

# Usage
conn = Neo4jConnection("bolt://localhost:7687", "neo4j", "password")

# Create
conn.query("""
    CREATE (p:Person {name: $name, age: $age})
""", {"name": "Alice", "age": 30})

# Query with parameters
results = conn.query("""
    MATCH (p:Person)
    WHERE p.age > $min_age
    RETURN p.name, p.age
""", {"min_age": 25})

conn.close()
```

**Key Concept:** Cypher uses **patterns** - nodes and relationships form visual patterns that translate directly to queries.








