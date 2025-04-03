# Knowledge Graph Schema - Detailed Specification

## 1. Overview

The knowledge graph serves as the persistent memory for the MCP Workflow System, storing entities, relationships, and associated metadata extracted from interactions. This document outlines the detailed schema for this knowledge graph.

## 2. Entity Types

### 2.1. Core Entity Types

#### 2.1.1. Person
Represents individuals mentioned in interactions.

**Properties**:
- `name`: String (required) - Full name
- `aliases`: List[String] - Alternative names
- `role`: String - Professional role
- `organization`: String - Associated organization
- `expertise`: List[String] - Areas of expertise
- `contact`: Object - Contact information
- `metadata`: Object - Additional properties

#### 2.1.2. Organization
Represents companies, projects, teams, or other organizational entities.

**Properties**:
- `name`: String (required) - Organization name
- `aliases`: List[String] - Alternative names
- `type`: String - Type of organization (company, project, team)
- `industry`: String - Industry classification
- `description`: String - Brief description
- `metadata`: Object - Additional properties

#### 2.1.3. Technology
Represents programming languages, frameworks, tools, or platforms.

**Properties**:
- `name`: String (required) - Technology name
- `aliases`: List[String] - Alternative names
- `category`: String - Technology category
- `version`: String - Version information
- `description`: String - Brief description
- `url`: String - Reference URL
- `metadata`: Object - Additional properties

#### 2.1.4. Concept
Represents abstract ideas, principles, methodologies, or theories.

**Properties**:
- `name`: String (required) - Concept name
- `aliases`: List[String] - Alternative names
- `category`: String - Concept category
- `description`: String - Brief description
- `related_domains`: List[String] - Related knowledge domains
- `metadata`: Object - Additional properties

#### 2.1.5. Resource
Represents documents, code repositories, APIs, or other resources.

**Properties**:
- `name`: String (required) - Resource name
- `type`: String - Resource type (document, repository, API)
- `location`: String - URL or path
- `description`: String - Brief description
- `owner`: String - Owner (person or organization)
- `access_level`: String - Public, private, etc.
- `metadata`: Object - Additional properties

#### 2.1.6. Task
Represents actions, goals, objectives, or to-do items.

**Properties**:
- `name`: String (required) - Task name
- `description`: String - Detailed description
- `status`: String - Current status
- `priority`: String - Priority level
- `deadline`: DateTime - Due date
- `assignee`: String - Person assigned to the task
- `related_entities`: List[String] - Related entities
- `metadata`: Object - Additional properties

### 2.2. Common Properties for All Entities

All entity types share these common properties:

- `id`: String (required) - Unique identifier
- `type`: String (required) - Entity type
- `created_at`: DateTime - Creation timestamp
- `updated_at`: DateTime - Last update timestamp
- `source`: String - Origin of the entity information
- `confidence`: Float (0-1) - Confidence score
- `observations`: List[Object] - Observed mentions with context
- `embedding`: Vector - Semantic embedding

## 3. Relationship Types

### 3.1. Core Relationship Types

#### 3.1.1. Uses
Indicates that one entity uses another (e.g., a Person uses a Technology).

**Properties**:
- `context`: String - Context of usage
- `proficiency`: String - Level of proficiency
- `frequency`: String - Frequency of usage
- `purpose`: String - Purpose of usage

#### 3.1.2. WorksOn
Indicates that an entity works on another entity (e.g., a Person works on a Project).

**Properties**:
- `role`: String - Role in the work relationship
- `start_date`: DateTime - When the work started
- `end_date`: DateTime - When the work ended (if applicable)
- `contribution`: String - Nature of contribution

#### 3.1.3. Has
Indicates possession or composition (e.g., an Organization has a Technology).

**Properties**:
- `type`: String - Type of possession (owns, contains, etc.)
- `exclusivity`: String - Whether the possession is exclusive
- `since`: DateTime - When the possession began

#### 3.1.4. RelatesTo
A generic relationship indicating that two entities are related.

**Properties**:
- `relation_type`: String - Specific type of relation
- `strength`: Float (0-1) - Strength of the relationship
- `bidirectional`: Boolean - Whether the relationship is bidirectional

#### 3.1.5. DependsOn
Indicates a dependency relationship (e.g., a Technology depends on another Technology).

**Properties**:
- `dependency_type`: String - Type of dependency
- `criticality`: String - How critical the dependency is
- `version_constraint`: String - Version constraints (if applicable)

#### 3.1.6. Creates
Indicates that one entity creates another (e.g., a Person creates a Resource).

**Properties**:
- `creation_date`: DateTime - When the creation occurred
- `contribution_type`: String - Type of contribution
- `attribution`: String - Attribution information

### 3.2. Common Properties for All Relationships

All relationship types share these common properties:

- `id`: String (required) - Unique identifier
- `source_id`: String (required) - Source entity ID
- `target_id`: String (required) - Target entity ID
- `type`: String (required) - Relationship type
- `created_at`: DateTime - Creation timestamp
- `updated_at`: DateTime - Last update timestamp
- `source`: String - Origin of the relationship information
- `confidence`: Float (0-1) - Confidence score
- `observations`: List[Object] - Observed mentions with context

## 4. Metadata Structure

### 4.1. Observation Schema

Each observation represents an instance where an entity or relationship was mentioned or inferred.

```json
{
  "text": "Original text where the entity/relationship was mentioned",
  "source": "Message ID or other source identifier",
  "timestamp": "2025-04-03T12:00:00Z",
  "confidence": 0.95,
  "extractor": "Named entity recognition",
  "context": {
    "before": "Text before the mention",
    "exact": "Exact mention text",
    "after": "Text after the mention"
  },
  "position": {
    "start": 45,
    "end": 58
  }
}
```

### 4.2. Confidence Score Calculation

Confidence scores are calculated based on:

1. The confidence of the extraction method
2. The number of observations (more observations increase confidence)
3. The recency of observations (more recent observations have higher weight)
4. The quality of the source (some sources are more reliable)
5. Consistency across observations

**Formula**:
```
confidence = base_confidence * consistency_factor * recency_factor * source_quality_factor
```

## 5. Storage Implementation

### 5.1. Graph Database Schema

The knowledge graph will be implemented using a graph database (e.g., Neo4j) with the following structure:

#### 5.1.1. Node Labels
- `:Person`
- `:Organization`
- `:Technology`
- `:Concept`
- `:Resource`
- `:Task`

#### 5.1.2. Relationship Types
- `:USES`
- `:WORKS_ON`
- `:HAS`
- `:RELATES_TO`
- `:DEPENDS_ON`
- `:CREATES`

### 5.2. Property Indexing

The following properties will be indexed for efficient queries:

- `id` (unique constraint)
- `name` (index)
- `type` (index)
- `created_at` (index)
- `updated_at` (index)
- `confidence` (index)

### 5.3. Vector Storage

Entity embeddings will be stored in a vector database or as properties in the graph database with vector similarity capabilities.

## 6. Query Patterns

### 6.1. Entity Retrieval Queries

#### 6.1.1. Get Entity by ID
```cypher
MATCH (e {id: $id})
RETURN e
```

#### 6.1.2. Get Entity by Name and Type
```cypher
MATCH (e)
WHERE e.name = $name AND e.type = $type
RETURN e
```

#### 6.1.3. Fuzzy Entity Search
```cypher
MATCH (e)
WHERE e.name =~ $name_pattern
RETURN e
```

### 6.2. Relationship Queries

#### 6.2.1. Get All Relationships for an Entity
```cypher
MATCH (e {id: $id})-[r]-(related)
RETURN r, related
```

#### 6.2.2. Get Specific Relationship Type
```cypher
MATCH (e {id: $id})-[r:RELATIONSHIP_TYPE]-(related)
RETURN r, related
```

#### 6.2.3. Get Path Between Entities
```cypher
MATCH path = shortestPath((e1 {id: $id1})-[*..5]-(e2 {id: $id2}))
RETURN path
```

### 6.3. Knowledge Exploration Queries

#### 6.3.1. Get Knowledge Subgraph
```cypher
MATCH (e {id: $id})-[*1..2]-(related)
RETURN e, related
```

#### 6.3.2. Get Related Entities by Type
```cypher
MATCH (e {id: $id})-[r]-(related:TYPE)
WHERE related.confidence > $min_confidence
RETURN related
ORDER BY related.confidence DESC
```

## 7. Validation Rules

### 7.1. Entity Validation

- Entity IDs must be unique
- Required properties must be present
- Properties must adhere to their defined types
- Confidence scores must be between 0 and 1
- Timestamps must be valid ISO format
- Vectors must have the correct dimensions

### 7.2. Relationship Validation

- Source and target entities must exist
- Relationship type must be valid
- Required properties must be present
- Confidence scores must be between 0 and 1

### 7.3. Semantic Validation

- Entity types must be compatible with relationship types
- Circular dependencies should be flagged
- Contradictory relationships should be detected
- Temporal consistency should be maintained

## 8. Evolution and Maintenance

### 8.1. Schema Versioning

The knowledge graph schema will be versioned to track changes over time.

### 8.2. Migration Strategies

When the schema changes, migration strategies will be applied:

1. **Forward Migration**: Updating existing data to conform to new schema
2. **Backward Compatibility**: Ensuring old data can still be accessed
3. **Schema Coexistence**: Supporting multiple schema versions simultaneously

### 8.3. Cleanup and Maintenance

- Low confidence entities will be periodically reviewed
- Stale information will be flagged for updating
- Orphaned entities will be identified and handled
- Graph consistency checks will be performed regularly

## 9. Integration with MCP Components

### 9.1. Entity Extractor Integration

The Entity Extractor will map extracted entities to this schema, creating new entities and updating existing ones as needed.

### 9.2. Knowledge Mapper Integration

The Knowledge Mapper will use this schema to resolve entities and create relationships between them.

### 9.3. Strategy Executor Integration

The Strategy Executor will query the knowledge graph using the defined query patterns to retrieve information needed for execution.

## 10. Implementation Plan

### 10.1. Phase 1: Core Schema Implementation

- Implement basic entity and relationship types
- Set up graph database structure
- Create validation rules
- Implement basic CRUD operations

### 10.2. Phase 2: Advanced Features

- Add vector embeddings
- Implement more sophisticated confidence scoring
- Create advanced query patterns
- Develop schema evolution mechanisms

### 10.3. Phase 3: Integration and Optimization

- Integrate with other MCP components
- Optimize query performance
- Implement maintenance routines
- Create visualization and exploration tools
