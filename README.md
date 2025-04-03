# MCP Workflow System

An intelligent workflow system leveraging Model Context Protocol (MCP) for knowledge graph building and contextual understanding in agent-based interactions.

## Project Overview

The MCP Workflow System creates a comprehensive framework for:
- Processing messages and extracting meaningful entities
- Building and maintaining a knowledge graph
- Determining user intent and context
- Generating contextual, knowledge-enhanced responses

This system is designed to serve as a foundation for agent-based AI applications that require persistent memory and contextual understanding.

## Current Status

The project is in active development, with progress in several key areas:

- ✅ **Entity Extraction**: Base framework and initial implementation completed
- 🔄 **Knowledge Graph Schema**: Design completed, implementation in progress
- 🔄 **Architecture Design**: Detailed specification completed, implementation in progress
- 📅 **Intent Determination**: Planned for future implementation
- 📅 **Strategy Execution**: Planned for future implementation
- 📅 **Response Generation**: Planned for future implementation

For a detailed overview of the project's current status, please see [PROJECT_STATUS.md](PROJECT_STATUS.md).

## Core Components

### 1. Entity Extraction
```
ExtractEntities(Named, Technical, Conceptual)
  -> IdentifyNamedEntities(People, Organizations, Technologies)
  -> RecognizeTechnicalTerms(Code, Frameworks, Architecture)
  -> ExtractConceptualElements(Ideas, Goals, Problems)
  -> AssignConfidenceScores(Entities)
  -> DetermineRelationships(EntityPairs)
  -> StructureEntityCollection(Hierarchy)
```

The Entity Extraction module identifies and classifies entities from text. It supports:
- Named Entity Recognition (NER)
- Technical term extraction
- Conceptual element identification
- Relationship extraction
- Confidence scoring

### 2. Knowledge Mapping
```
MapToKnowledge(Entities, Relations)
  -> ResolveEntityIdentities(Matching, Disambiguation)
  -> FindExistingRelations(DirectConnections, PathConnections)
  -> IdentifyKnowledgeGaps(MissingEntities, UncertainRelations)
  -> ScoreRelevance(EntityImportance, RelationStrength)
  -> GenerateKnowledgeQueries(Clarification, Expansion)
  -> CreateKnowledgeUpdatePlan(Additions, Modifications)
```

The Knowledge Mapping component connects extracted entities to the knowledge graph.

### 3. Intent Determination
```
DetermineIntent(Primary, Secondary, Context)
  -> ClassifyIntentType(Query, Command, Statement, Discussion)
  -> ExtractIntentParameters(Entities, Constraints, Preferences)
  -> AssessContextualFactors(History, State, Environment)
  -> PrioritizeIntents(Primary, Secondary, Implied)
  -> FormulateIntentRepresentation(Structured, Actionable)
```

The Intent Determination module identifies the user's intentions from messages.

### 4. Strategy Execution
```
ExecuteStrategy(Actions, Computations, Searches)
  -> PlanExecution(Dependencies, Parallelism, Sequencing)
  -> PerformKnowledgeOperations(Retrieval, Inference, Validation)
  -> ExecuteComputationalTasks(Analysis, Transformation, Generation)
  -> AccessExternalResources(APIs, Files, Databases)
  -> HandleExceptions(Errors, Timeouts, Limitations)
  -> CollectExecutionResults(Outputs, Metrics, Logs)
```

The Strategy Execution component executes operations based on the identified intent.

## Project Structure

```
/
├── docs/                  # Documentation
├── src/                   # Source code
│   ├── core/              # Core workflow components
│   ├── entity_extraction/ # Entity extraction modules
│   ├── knowledge_graph/   # Knowledge graph operations
│   ├── intent/            # Intent determination
│   └── utils/             # Utility functions
├── tests/                 # Test suite
└── examples/              # Example implementations
```

## Getting Started

### Prerequisites

- Python 3.10+
- pip

### Installation

1. Clone the repository
```bash
git clone https://github.com/omar-el-mountassir/mcp-workflow-system.git
cd mcp-workflow-system
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

For the spaCy-based entity extractor, you'll need to download the language model:
```bash
python -m spacy download en_core_web_sm
```

### Running Examples

Try out the entity extraction demo:
```bash
python examples/entity_extraction_demo.py
```

### Running Tests

```bash
pytest
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture Overview](docs/architecture.md)
- [Detailed Architecture](docs/architecture_detailed.md)
- [Knowledge Graph Schema](docs/knowledge_graph_schema.md)
- [Detailed Knowledge Graph Schema](docs/knowledge_graph_schema_detailed.md)
- [Entity Extraction Implementation](docs/entity_extraction_implementation.md)

## Future Development

The project roadmap includes:

1. Completing the entity extraction module with enhanced capabilities
2. Implementing the knowledge graph with database integration
3. Developing the intent determination module
4. Creating the strategy execution framework
5. Building the response generation component
6. Integrating all components into a seamless workflow

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
