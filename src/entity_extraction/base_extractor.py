"""
Base Entity Extractor Module

This module provides the foundational classes and functions for entity extraction
in the MCP Workflow System.
"""

from typing import Dict, List, Optional, Union, Any
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
import json
import uuid
from datetime import datetime


@dataclass
class Entity:
    """Represents an extracted entity."""
    
    id: str
    name: str
    type: str
    source_text: str
    start_position: int
    end_position: int
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the entity to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "source_text": self.source_text,
            "start_position": self.start_position,
            "end_position": self.end_position,
            "confidence": self.confidence,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Entity':
        """Create an entity from a dictionary."""
        return cls(
            id=data["id"],
            name=data["name"],
            type=data["type"],
            source_text=data["source_text"],
            start_position=data["start_position"],
            end_position=data["end_position"],
            confidence=data["confidence"],
            metadata=data.get("metadata", {})
        )
    
    def to_json(self) -> str:
        """Convert the entity to a JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class Relationship:
    """Represents a relationship between entities."""
    
    id: str
    source_entity: str  # Entity ID
    target_entity: str  # Entity ID
    type: str
    confidence: float
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the relationship to a dictionary."""
        return {
            "id": self.id,
            "source_entity": self.source_entity,
            "target_entity": self.target_entity,
            "type": self.type,
            "confidence": self.confidence,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Relationship':
        """Create a relationship from a dictionary."""
        return cls(
            id=data["id"],
            source_entity=data["source_entity"],
            target_entity=data["target_entity"],
            type=data["type"],
            confidence=data["confidence"],
            metadata=data.get("metadata", {})
        )
    
    def to_json(self) -> str:
        """Convert the relationship to a JSON string."""
        return json.dumps(self.to_dict())


@dataclass
class EntityCollection:
    """A collection of entities and relationships."""
    
    entities: List[Entity] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    source_id: Optional[str] = None
    
    def add_entity(self, entity: Entity) -> None:
        """Add an entity to the collection."""
        self.entities.append(entity)
    
    def add_relationship(self, relationship: Relationship) -> None:
        """Add a relationship to the collection."""
        self.relationships.append(relationship)
    
    def get_entity_by_id(self, entity_id: str) -> Optional[Entity]:
        """Get an entity by its ID."""
        for entity in self.entities:
            if entity.id == entity_id:
                return entity
        return None
    
    def get_entities_by_type(self, entity_type: str) -> List[Entity]:
        """Get all entities of a specific type."""
        return [entity for entity in self.entities if entity.type == entity_type]
    
    def get_relationships_by_type(self, relationship_type: str) -> List[Relationship]:
        """Get all relationships of a specific type."""
        return [rel for rel in self.relationships if rel.type == relationship_type]
    
    def get_relationships_for_entity(self, entity_id: str) -> List[Relationship]:
        """Get all relationships involving a specific entity."""
        return [
            rel for rel in self.relationships 
            if rel.source_entity == entity_id or rel.target_entity == entity_id
        ]
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the collection to a dictionary."""
        return {
            "entities": [entity.to_dict() for entity in self.entities],
            "relationships": [rel.to_dict() for rel in self.relationships],
            "source_id": self.source_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'EntityCollection':
        """Create a collection from a dictionary."""
        collection = cls(source_id=data.get("source_id"))
        for entity_data in data.get("entities", []):
            collection.add_entity(Entity.from_dict(entity_data))
        for rel_data in data.get("relationships", []):
            collection.add_relationship(Relationship.from_dict(rel_data))
        return collection
    
    def to_json(self) -> str:
        """Convert the collection to a JSON string."""
        return json.dumps(self.to_dict())


class EntityExtractor(ABC):
    """Base class for entity extractors."""
    
    @abstractmethod
    def extract_entities(self, text: str, **kwargs) -> EntityCollection:
        """
        Extract entities from the given text.
        
        Args:
            text: The text to extract entities from.
            **kwargs: Additional extractor-specific parameters.
            
        Returns:
            A collection of extracted entities and relationships.
        """
        pass


class CompositeEntityExtractor(EntityExtractor):
    """An entity extractor that combines multiple extractors."""
    
    def __init__(self, extractors: List[EntityExtractor]):
        """
        Initialize the composite extractor.
        
        Args:
            extractors: A list of entity extractors to use.
        """
        self.extractors = extractors
    
    def extract_entities(self, text: str, **kwargs) -> EntityCollection:
        """
        Extract entities using all configured extractors.
        
        Args:
            text: The text to extract entities from.
            **kwargs: Additional parameters passed to each extractor.
            
        Returns:
            A combined collection of entities and relationships.
        """
        # Create an empty collection for the result
        result_collection = EntityCollection()
        
        # Extract entities using each extractor
        for extractor in self.extractors:
            collection = extractor.extract_entities(text, **kwargs)
            
            # Add entities and relationships to the result collection
            for entity in collection.entities:
                # Check for duplicate entities (simplified approach)
                duplicate = False
                for existing_entity in result_collection.entities:
                    if (
                        existing_entity.name == entity.name and 
                        existing_entity.type == entity.type
                    ):
                        # If we find a duplicate, keep the one with higher confidence
                        if entity.confidence > existing_entity.confidence:
                            existing_entity.confidence = entity.confidence
                            existing_entity.metadata.update(entity.metadata)
                        duplicate = True
                        break
                
                if not duplicate:
                    result_collection.add_entity(entity)
            
            # Add all relationships
            for relationship in collection.relationships:
                result_collection.add_relationship(relationship)
        
        return result_collection


class ConfidenceCalculator:
    """Utility class for calculating confidence scores."""
    
    @staticmethod
    def calculate_entity_confidence(
        base_score: float,
        context_factor: float = 1.0,
        frequency_factor: float = 0.0,
        method_agreement: float = 0.0
    ) -> float:
        """
        Calculate the confidence score for an entity.
        
        Args:
            base_score: Base confidence from the extraction model (0-1)
            context_factor: Factor based on context clarity (0-1)
            frequency_factor: Factor based on frequency of occurrence (0+)
            method_agreement: Factor based on agreement between methods (0-1)
            
        Returns:
            Final confidence score between 0 and 1
        """
        confidence = base_score * context_factor * (1 + 0.2 * frequency_factor)
        confidence = confidence * (0.8 + 0.2 * method_agreement)
        return min(1.0, max(0.0, confidence))
    
    @staticmethod
    def calculate_relationship_confidence(
        source_confidence: float,
        target_confidence: float,
        relation_strength: float,
        context_support: float = 1.0
    ) -> float:
        """
        Calculate the confidence score for a relationship.
        
        Args:
            source_confidence: Confidence in the source entity (0-1)
            target_confidence: Confidence in the target entity (0-1)
            relation_strength: Strength of the relationship evidence (0-1)
            context_support: Support from the context (0-1)
            
        Returns:
            Final confidence score between 0 and 1
        """
        # The relationship confidence is limited by the confidence in its entities
        entity_confidence = min(source_confidence, target_confidence)
        
        # Calculate final confidence based on relation strength and context
        confidence = entity_confidence * relation_strength * context_support
        
        return min(1.0, max(0.0, confidence))


class EntityFactory:
    """Factory class for creating entities and relationships."""
    
    @staticmethod
    def create_entity(
        name: str,
        entity_type: str,
        source_text: str,
        start_position: int,
        end_position: int,
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Entity:
        """
        Create a new entity with a unique ID.
        
        Args:
            name: The name of the entity.
            entity_type: The type of the entity.
            source_text: The source text from which the entity was extracted.
            start_position: The start position of the entity in the source text.
            end_position: The end position of the entity in the source text.
            confidence: The confidence score for the entity.
            metadata: Additional metadata for the entity.
            
        Returns:
            A new Entity instance.
        """
        entity_id = str(uuid.uuid4())
        
        if metadata is None:
            metadata = {}
        
        # Add creation timestamp to metadata
        if "created_at" not in metadata:
            metadata["created_at"] = datetime.now().isoformat()
        
        return Entity(
            id=entity_id,
            name=name,
            type=entity_type,
            source_text=source_text,
            start_position=start_position,
            end_position=end_position,
            confidence=confidence,
            metadata=metadata
        )
    
    @staticmethod
    def create_relationship(
        source_entity: str,
        target_entity: str,
        relationship_type: str,
        confidence: float,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Relationship:
        """
        Create a new relationship with a unique ID.
        
        Args:
            source_entity: The ID of the source entity.
            target_entity: The ID of the target entity.
            relationship_type: The type of the relationship.
            confidence: The confidence score for the relationship.
            metadata: Additional metadata for the relationship.
            
        Returns:
            A new Relationship instance.
        """
        relationship_id = str(uuid.uuid4())
        
        if metadata is None:
            metadata = {}
        
        # Add creation timestamp to metadata
        if "created_at" not in metadata:
            metadata["created_at"] = datetime.now().isoformat()
        
        return Relationship(
            id=relationship_id,
            source_entity=source_entity,
            target_entity=target_entity,
            type=relationship_type,
            confidence=confidence,
            metadata=metadata
        )


class ObservationRecorder:
    """Utility class for recording observations about entities and relationships."""
    
    @staticmethod
    def record_entity_observation(
        entity: Entity,
        source: str,
        context_before: str = "",
        context_after: str = "",
        extractor: str = "unknown"
    ) -> None:
        """
        Record an observation of an entity.
        
        Args:
            entity: The entity that was observed.
            source: The source of the observation (e.g., message ID).
            context_before: Text before the entity mention.
            context_after: Text after the entity mention.
            extractor: The extractor that identified the entity.
        """
        # Initialize observations list if it doesn't exist
        if "observations" not in entity.metadata:
            entity.metadata["observations"] = []
        
        # Create the observation
        observation = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "extractor": extractor,
            "context": {
                "before": context_before,
                "exact": entity.source_text,
                "after": context_after
            },
            "position": {
                "start": entity.start_position,
                "end": entity.end_position
            },
            "confidence": entity.confidence
        }
        
        # Add the observation
        entity.metadata["observations"].append(observation)
    
    @staticmethod
    def record_relationship_observation(
        relationship: Relationship,
        source: str,
        context: str = "",
        extractor: str = "unknown"
    ) -> None:
        """
        Record an observation of a relationship.
        
        Args:
            relationship: The relationship that was observed.
            source: The source of the observation (e.g., message ID).
            context: The context in which the relationship was observed.
            extractor: The extractor that identified the relationship.
        """
        # Initialize observations list if it doesn't exist
        if "observations" not in relationship.metadata:
            relationship.metadata["observations"] = []
        
        # Create the observation
        observation = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "extractor": extractor,
            "context": context,
            "confidence": relationship.confidence
        }
        
        # Add the observation
        relationship.metadata["observations"].append(observation)


# Sample implementation of a simple rule-based extractor
class SimpleRuleBasedExtractor(EntityExtractor):
    """A simple rule-based entity extractor for demonstration."""
    
    def __init__(self, entity_patterns: Dict[str, List[str]]):
        """
        Initialize the extractor with entity patterns.
        
        Args:
            entity_patterns: A dictionary mapping entity types to lists of patterns.
        """
        self.entity_patterns = entity_patterns
    
    def extract_entities(self, text: str, **kwargs) -> EntityCollection:
        """
        Extract entities using simple pattern matching.
        
        Args:
            text: The text to extract entities from.
            **kwargs: Additional parameters.
            
        Returns:
            A collection of extracted entities.
        """
        collection = EntityCollection()
        source_id = kwargs.get("source_id", None)
        collection.source_id = source_id
        
        # Simple implementation for demonstration
        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                start_idx = 0
                while True:
                    # Find the pattern in the text
                    idx = text.find(pattern, start_idx)
                    if idx == -1:
                        break
                    
                    # Create an entity
                    entity = EntityFactory.create_entity(
                        name=pattern,
                        entity_type=entity_type,
                        source_text=pattern,
                        start_position=idx,
                        end_position=idx + len(pattern),
                        confidence=0.8,  # Fixed confidence for demonstration
                        metadata={"extractor": "SimpleRuleBasedExtractor"}
                    )
                    
                    # Record an observation
                    context_before = text[max(0, idx-50):idx]
                    context_after = text[idx+len(pattern):min(len(text), idx+len(pattern)+50)]
                    ObservationRecorder.record_entity_observation(
                        entity=entity,
                        source=source_id or "unknown",
                        context_before=context_before,
                        context_after=context_after,
                        extractor="SimpleRuleBasedExtractor"
                    )
                    
                    # Add the entity to the collection
                    collection.add_entity(entity)
                    
                    # Move to the next occurrence
                    start_idx = idx + len(pattern)
        
        # For demonstration, we'll create relationships between entities of the same type
        entities_by_type = {}
        for entity in collection.entities:
            if entity.type not in entities_by_type:
                entities_by_type[entity.type] = []
            entities_by_type[entity.type].append(entity)
        
        # Create "relatesTo" relationships between entities of the same type
        for entity_type, entities in entities_by_type.items():
            for i in range(len(entities) - 1):
                for j in range(i + 1, len(entities)):
                    relationship = EntityFactory.create_relationship(
                        source_entity=entities[i].id,
                        target_entity=entities[j].id,
                        relationship_type="relatesTo",
                        confidence=0.7,  # Fixed confidence for demonstration
                        metadata={"extractor": "SimpleRuleBasedExtractor"}
                    )
                    
                    # Record an observation
                    ObservationRecorder.record_relationship_observation(
                        relationship=relationship,
                        source=source_id or "unknown",
                        context=f"Both entities are of type {entity_type}",
                        extractor="SimpleRuleBasedExtractor"
                    )
                    
                    # Add the relationship to the collection
                    collection.add_relationship(relationship)
        
        return collection
