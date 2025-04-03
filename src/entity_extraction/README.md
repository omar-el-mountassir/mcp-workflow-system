# Entity Extraction Module

This module provides the functionality to extract entities and relationships from text within the MCP Workflow System.

## Overview

The entity extraction module identifies named entities, technical terms, and conceptual elements from text, and determines the relationships between them. This information is used to build and maintain the knowledge graph.

## Components

### Base Extractor

The `base_extractor.py` file contains the core classes and interfaces:

- `Entity`: Represents an extracted entity with properties like name, type, and confidence score.
- `Relationship`: Represents a relationship between two entities.
- `EntityCollection`: A collection of entities and relationships.
- `EntityExtractor`: Base class for all entity extractors.
- `CompositeEntityExtractor`: Combines multiple extractors into one.
- `ConfidenceCalculator`: Utility for calculating confidence scores.
- `EntityFactory`: Factory for creating entities and relationships.
- `ObservationRecorder`: Utility for recording observations about entities and relationships.
- `SimpleRuleBasedExtractor`: A simple pattern-matching extractor for demonstration.

### spaCy Extractor

The `spacy_extractor.py` file provides a more sophisticated entity extractor using the spaCy NLP library:

- `SpacyEntityExtractor`: Uses spaCy's named entity recognition for extraction.
- It also implements relationship extraction based on syntactic dependencies.

## Usage

### Simple Example

```python
from entity_extraction.base_extractor import SimpleRuleBasedExtractor

# Define patterns for the extractor
patterns = {
    "Person": ["Omar", "John", "Alice"],
    "Organization": ["Google", "Microsoft", "LifeSync"],
    "Technology": ["Python", "JavaScript", "React"]
}

# Create the extractor
extractor = SimpleRuleBasedExtractor(patterns)

# Extract entities from a text
text = "Omar is working on LifeSync using Python."
collection = extractor.extract_entities(text, source_id="example")

# Use the extracted entities
for entity in collection.entities:
    print(f"{entity.name} ({entity.type}): {entity.confidence}")

for rel in collection.relationships:
    source = collection.get_entity_by_id(rel.source_entity)
    target = collection.get_entity_by_id(rel.target_entity)
    print(f"{source.name} --[{rel.type}]--> {target.name}")
```

### Using spaCy Extractor

```python
from entity_extraction.spacy_extractor import SpacyEntityExtractor

# Create the extractor
extractor = SpacyEntityExtractor(model_name="en_core_web_sm")

# Extract entities
text = "Apple is planning to build a new headquarters in Austin, Texas."
collection = extractor.extract_entities(text, source_id="example")

# Use the extracted entities
for entity in collection.entities:
    print(f"{entity.name} ({entity.type}): {entity.confidence}")
```

### Composite Extractor

```python
from entity_extraction.base_extractor import SimpleRuleBasedExtractor, CompositeEntityExtractor
from entity_extraction.spacy_extractor import SpacyEntityExtractor

# Create individual extractors
simple_extractor = SimpleRuleBasedExtractor({
    "Technology": ["Python", "JavaScript", "React"]
})
spacy_extractor = SpacyEntityExtractor()

# Create a composite extractor
composite = CompositeEntityExtractor([simple_extractor, spacy_extractor])

# Extract entities
text = "Google is using Python for machine learning projects."
collection = composite.extract_entities(text, source_id="example")
```

## Extension

To create a custom entity extractor, extend the `EntityExtractor` base class:

```python
from entity_extraction.base_extractor import EntityExtractor, EntityCollection

class MyCustomExtractor(EntityExtractor):
    def extract_entities(self, text, **kwargs):
        collection = EntityCollection(source_id=kwargs.get("source_id"))
        
        # Implement your extraction logic here
        
        return collection
```

## Dependencies

- Python 3.10+
- For spaCy extractor: spaCy library and language models

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

## Future Improvements

1. Enhanced technical term extraction
2. More sophisticated relationship extraction
3. Domain-specific entity extractors
4. Integration with transformers models for improved accuracy
5. Multilingual support
