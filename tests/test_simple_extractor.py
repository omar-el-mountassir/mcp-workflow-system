"""Tests for the simple rule-based entity extractor."""

import sys
import os
import pytest
from typing import Dict, List

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.entity_extraction.base_extractor import SimpleRuleBasedExtractor, EntityCollection


def test_simple_rule_based_extractor():
    """Test the SimpleRuleBasedExtractor with basic patterns."""
    # Define some test patterns
    patterns = {
        "Person": ["Omar", "John", "Alice"],
        "Organization": ["Google", "Microsoft", "LifeSync"],
        "Technology": ["Python", "JavaScript", "React", "Node.js"]
    }
    
    # Create the extractor
    extractor = SimpleRuleBasedExtractor(patterns)
    
    # Test text that contains some of the patterns
    test_text = """
    Omar is working on a project called LifeSync, which uses Python and JavaScript.
    John from Microsoft is also interested in the project, and Alice might join later.
    The team is considering using React and Node.js for the frontend.
    """
    
    # Extract entities
    result = extractor.extract_entities(test_text, source_id="test_message_1")
    
    # Verify the results
    assert isinstance(result, EntityCollection)
    
    # Check if we found all the expected entities
    expected_entities = [
        ("Omar", "Person"),
        ("LifeSync", "Organization"),
        ("Python", "Technology"),
        ("JavaScript", "Technology"),
        ("John", "Person"),
        ("Microsoft", "Organization"),
        ("Alice", "Person"),
        ("React", "Technology"),
        ("Node.js", "Technology")
    ]
    
    # Create a dictionary to count found entities by name and type
    found_entities: Dict[str, List[str]] = {}
    for entity in result.entities:
        key = f"{entity.name}:{entity.type}"
        if key not in found_entities:
            found_entities[key] = []
        found_entities[key].append(entity.id)
    
    # Check if all expected entities were found
    for name, entity_type in expected_entities:
        key = f"{name}:{entity_type}"
        assert key in found_entities, f"Entity {name} of type {entity_type} not found"
    
    # Verify that relationships were created
    assert len(result.relationships) > 0, "No relationships were created"
    
    # Check if we have the correct number of relationships
    # For each entity type, we should have n*(n-1)/2 relationships
    expected_relationship_count = 0
    entity_counts = {}
    for _, entity_type in expected_entities:
        if entity_type not in entity_counts:
            entity_counts[entity_type] = 0
        entity_counts[entity_type] += 1
    
    for entity_type, count in entity_counts.items():
        expected_relationship_count += (count * (count - 1)) // 2
    
    assert len(result.relationships) == expected_relationship_count, \
        f"Expected {expected_relationship_count} relationships, got {len(result.relationships)}"
    
    # Verify that all relationships have the correct type
    for relationship in result.relationships:
        assert relationship.type == "relatesTo", \
            f"Expected relationship type 'relatesTo', got '{relationship.type}'"
    
    # Verify that relationships connect entities of the same type
    for relationship in result.relationships:
        source_entity = result.get_entity_by_id(relationship.source_entity)
        target_entity = result.get_entity_by_id(relationship.target_entity)
        
        assert source_entity is not None, f"Source entity {relationship.source_entity} not found"
        assert target_entity is not None, f"Target entity {relationship.target_entity} not found"
        
        assert source_entity.type == target_entity.type, \
            f"Relationship connects entities of different types: {source_entity.type} and {target_entity.type}"


def test_entity_collection_methods():
    """Test the methods of the EntityCollection class."""
    # Create an extractor with some patterns
    patterns = {
        "Person": ["Omar", "John", "Alice"],
        "Organization": ["Google", "Microsoft", "LifeSync"],
    }
    
    extractor = SimpleRuleBasedExtractor(patterns)
    
    # Test text with some of the patterns
    test_text = """
    Omar works at Google. John and Alice work at Microsoft. LifeSync is a new startup.
    """
    
    # Extract entities
    collection = extractor.extract_entities(test_text, source_id="test_message_2")
    
    # Test get_entity_by_id
    first_entity = collection.entities[0]
    retrieved_entity = collection.get_entity_by_id(first_entity.id)
    assert retrieved_entity is not None
    assert retrieved_entity.id == first_entity.id
    
    # Test get_entities_by_type
    person_entities = collection.get_entities_by_type("Person")
    assert len(person_entities) == 3  # Omar, John, Alice
    
    organization_entities = collection.get_entities_by_type("Organization")
    assert len(organization_entities) == 3  # Google, Microsoft, LifeSync
    
    # Test get_relationships_by_type
    relates_to_relationships = collection.get_relationships_by_type("relatesTo")
    assert len(relates_to_relationships) == len(collection.relationships)
    
    # Test get_relationships_for_entity
    omar_entity = next((e for e in collection.entities if e.name == "Omar"), None)
    assert omar_entity is not None
    
    omar_relationships = collection.get_relationships_for_entity(omar_entity.id)
    assert len(omar_relationships) == 2  # Relationships with John and Alice
    
    # Test serialization and deserialization
    collection_dict = collection.to_dict()
    reconstructed_collection = EntityCollection.from_dict(collection_dict)
    
    assert len(reconstructed_collection.entities) == len(collection.entities)
    assert len(reconstructed_collection.relationships) == len(collection.relationships)
    
    # Check if entity IDs match
    original_ids = {entity.id for entity in collection.entities}
    reconstructed_ids = {entity.id for entity in reconstructed_collection.entities}
    assert original_ids == reconstructed_ids


if __name__ == "__main__":
    # Run the tests
    test_simple_rule_based_extractor()
    test_entity_collection_methods()
    print("All tests passed!")
