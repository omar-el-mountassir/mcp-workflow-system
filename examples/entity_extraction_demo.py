#!/usr/bin/env python3
"""
Entity Extraction Demo

This script demonstrates how to use the entity extraction components
of the MCP Workflow System.
"""

import sys
import os
import json
from typing import Dict, List, Any

# Add the src directory to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.entity_extraction.base_extractor import SimpleRuleBasedExtractor, CompositeEntityExtractor
from src.entity_extraction.spacy_extractor import SpacyEntityExtractor


def print_entity_collection(collection, indent=0):
    """Pretty print an entity collection."""
    ind = " " * indent
    print(f"{ind}Entities ({len(collection.entities)}):")
    for entity in collection.entities:
        print(f"{ind}  - {entity.name} (Type: {entity.type}, Confidence: {entity.confidence:.2f})")
        if "observations" in entity.metadata:
            print(f"{ind}    Observations: {len(entity.metadata['observations'])}")
    
    print(f"\n{ind}Relationships ({len(collection.relationships)}):")
    for rel in collection.relationships:
        source_entity = next((e for e in collection.entities if e.id == rel.source_entity), None)
        target_entity = next((e for e in collection.entities if e.id == rel.target_entity), None)
        
        if source_entity and target_entity:
            print(f"{ind}  - {source_entity.name} --[{rel.type}]--> {target_entity.name} (Confidence: {rel.confidence:.2f})")


def extract_with_simple_extractor(text):
    """Extract entities using the simple rule-based extractor."""
    print("\n=== Simple Rule-Based Extractor ===\n")
    
    # Define patterns for the extractor
    patterns = {
        "Person": ["Omar", "John", "Alice", "Bob", "Claude"],
        "Organization": ["Google", "Microsoft", "LifeSync", "OpenAI", "Anthropic"],
        "Technology": ["Python", "JavaScript", "React", "Node.js", "LLM", "AI", "spaCy"]
    }
    
    # Create the extractor
    extractor = SimpleRuleBasedExtractor(patterns)
    
    # Extract entities
    collection = extractor.extract_entities(text, source_id="demo_1")
    
    # Print the results
    print_entity_collection(collection)
    
    return collection


def extract_with_spacy_extractor(text):
    """Extract entities using the spaCy-based extractor."""
    print("\n=== spaCy-Based Extractor ===\n")
    
    # Create the extractor
    try:
        extractor = SpacyEntityExtractor(model_name="en_core_web_sm")
    except Exception as e:
        print(f"Error initializing spaCy extractor: {e}")
        print("Make sure you have spaCy installed: pip install spacy")
        print("And the required model: python -m spacy download en_core_web_sm")
        return None
    
    # Extract entities
    collection = extractor.extract_entities(text, source_id="demo_2")
    
    # Print the results
    print_entity_collection(collection)
    
    return collection


def extract_with_composite_extractor(text):
    """Extract entities using a composite extractor."""
    print("\n=== Composite Extractor ===\n")
    
    # Create the simple rule-based extractor
    patterns = {
        "Person": ["Omar", "John", "Alice", "Bob", "Claude"],
        "Organization": ["Google", "Microsoft", "LifeSync", "OpenAI", "Anthropic"],
        "Technology": ["Python", "JavaScript", "React", "Node.js", "LLM", "AI", "spaCy"]
    }
    simple_extractor = SimpleRuleBasedExtractor(patterns)
    
    # Create the spaCy-based extractor
    try:
        spacy_extractor = SpacyEntityExtractor(model_name="en_core_web_sm")
    except Exception as e:
        print(f"Error initializing spaCy extractor: {e}")
        print("Using only the simple rule-based extractor.")
        spacy_extractor = None
    
    # Create the composite extractor
    extractors = [simple_extractor]
    if spacy_extractor:
        extractors.append(spacy_extractor)
    
    composite_extractor = CompositeEntityExtractor(extractors)
    
    # Extract entities
    collection = composite_extractor.extract_entities(text, source_id="demo_3")
    
    # Print the results
    print_entity_collection(collection)
    
    return collection


def save_collection_to_json(collection, filename):
    """Save an entity collection to a JSON file."""
    with open(filename, "w") as f:
        json.dump(collection.to_dict(), f, indent=2)
    print(f"\nSaved collection to {filename}")


def main():
    """Run the entity extraction demo."""
    print("=== MCP Workflow System - Entity Extraction Demo ===\n")
    
    # Sample text for entity extraction
    text = """
    Omar is working on a project called LifeSync, which uses Python and spaCy for natural language processing.
    The project team includes John from Google and Alice from Microsoft. Bob is also interested in joining the team.
    
    LifeSync aims to create an intelligent workflow system that leverages LLM technology and AI for knowledge graph building.
    The frontend will be built with React and Node.js.
    
    Claude from Anthropic has provided valuable insights into the project architecture.
    """
    
    print("Sample Text:")
    print("-" * 80)
    print(text)
    print("-" * 80)
    
    # Extract entities using different extractors
    simple_collection = extract_with_simple_extractor(text)
    spacy_collection = extract_with_spacy_extractor(text)
    composite_collection = extract_with_composite_extractor(text)
    
    # Save the results to JSON files
    if simple_collection:
        save_collection_to_json(simple_collection, "simple_extraction.json")
    
    if spacy_collection:
        save_collection_to_json(spacy_collection, "spacy_extraction.json")
    
    if composite_collection:
        save_collection_to_json(composite_collection, "composite_extraction.json")


if __name__ == "__main__":
    main()
