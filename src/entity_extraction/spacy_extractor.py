"""
spaCy-based Entity Extractor Module

This module provides entity extraction capabilities using the spaCy NLP library.
"""

import os
import spacy
from typing import Dict, List, Any, Optional, Tuple
import re
import warnings

from .base_extractor import (
    EntityExtractor, Entity, Relationship, EntityCollection,
    EntityFactory, ObservationRecorder, ConfidenceCalculator
)


class SpacyEntityExtractor(EntityExtractor):
    """Entity extractor that uses spaCy for named entity recognition."""
    
    # Mapping of spaCy entity types to our entity types
    DEFAULT_ENTITY_TYPE_MAPPING = {
        "PERSON": "Person",
        "ORG": "Organization",
        "GPE": "Location",
        "LOC": "Location",
        "PRODUCT": "Product",
        "EVENT": "Event",
        "WORK_OF_ART": "CreativeWork",
        "LAW": "Resource",
        "LANGUAGE": "Technology",
        "DATE": "Time",
        "TIME": "Time",
        "MONEY": "Value",
        "QUANTITY": "Value",
        "PERCENT": "Value",
        "CARDINAL": "Value",
        "ORDINAL": "Value",
        # Add more mappings as needed
    }
    
    def __init__(
        self,
        model_name: str = "en_core_web_sm",
        entity_type_mapping: Optional[Dict[str, str]] = None,
        min_confidence: float = 0.5,
        load_model: bool = True
    ):
        """
        Initialize the spaCy-based entity extractor.
        
        Args:
            model_name: Name of the spaCy model to use.
            entity_type_mapping: Mapping from spaCy entity types to our entity types.
            min_confidence: Minimum confidence threshold for entities.
            load_model: Whether to load the model immediately.
        """
        self.model_name = model_name
        self.entity_type_mapping = entity_type_mapping or self.DEFAULT_ENTITY_TYPE_MAPPING
        self.min_confidence = min_confidence
        self.nlp = None
        
        # Load the model if requested
        if load_model:
            self.load_model()
    
    def load_model(self) -> None:
        """Load the spaCy model."""
        try:
            self.nlp = spacy.load(self.model_name)
        except OSError:
            # If the model is not found, try downloading it
            try:
                os.system(f"python -m spacy download {self.model_name}")
                self.nlp = spacy.load(self.model_name)
            except Exception as e:
                warnings.warn(f"Could not load or download spaCy model {self.model_name}: {e}")
                self.nlp = None
    
    def _get_confidence_for_entity(self, ent: spacy.tokens.span.Span) -> float:
        """
        Calculate confidence score for a spaCy entity.
        
        For now, we use a fixed confidence based on the entity type,
        but this could be improved with a more sophisticated approach.
        
        Args:
            ent: spaCy entity span.
            
        Returns:
            Confidence score between 0 and 1.
        """
        # Set base confidence based on entity type
        # This is a simplified approach and could be improved
        base_confidence = {
            "PERSON": 0.85,
            "ORG": 0.8,
            "GPE": 0.85,
            "LOC": 0.75,
            "PRODUCT": 0.7,
            "EVENT": 0.7,
            "WORK_OF_ART": 0.65,
            "LAW": 0.7,
            "LANGUAGE": 0.8,
            "DATE": 0.9,
            "TIME": 0.9,
            "MONEY": 0.9,
            "QUANTITY": 0.85,
            "PERCENT": 0.9,
            "CARDINAL": 0.75,
            "ORDINAL": 0.8,
        }.get(ent.label_, 0.6)  # Default confidence for unknown types
        
        # Adjust confidence based on entity length
        # Very short entities might be less reliable
        length_factor = min(1.0, max(0.7, len(ent.text) / 5.0))
        
        return base_confidence * length_factor
    
    def _get_context(
        self, doc: spacy.tokens.doc.Doc, ent: spacy.tokens.span.Span
    ) -> Tuple[str, str]:
        """
        Get context before and after an entity.
        
        Args:
            doc: spaCy document.
            ent: spaCy entity span.
            
        Returns:
            Tuple of (context_before, context_after).
        """
        # Get context window (up to 10 tokens or 50 characters on each side)
        before_start = max(0, ent.start - 10)
        after_end = min(len(doc), ent.end + 10)
        
        context_before = doc[before_start:ent.start].text
        context_after = doc[ent.end:after_end].text
        
        # Limit context to reasonable length
        if len(context_before) > 50:
            context_before = "..." + context_before[-50:]
        if len(context_after) > 50:
            context_after = context_after[:50] + "..."
        
        return context_before, context_after
    
    def extract_entities(self, text: str, **kwargs) -> EntityCollection:
        """
        Extract entities from text using spaCy.
        
        Args:
            text: The text to extract entities from.
            **kwargs: Additional parameters.
                source_id: Optional source identifier.
                
        Returns:
            A collection of extracted entities and relationships.
        """
        # Check if the model is loaded
        if self.nlp is None:
            self.load_model()
            if self.nlp is None:
                warnings.warn("Could not load spaCy model, returning empty collection")
                return EntityCollection(source_id=kwargs.get("source_id"))
        
        # Process the text with spaCy
        doc = self.nlp(text)
        
        # Create the entity collection
        collection = EntityCollection(source_id=kwargs.get("source_id"))
        
        # Extract entities
        for ent in doc.ents:
            # Map spaCy entity type to our entity type
            if ent.label_ not in self.entity_type_mapping:
                continue  # Skip entities with unmapped types
            
            entity_type = self.entity_type_mapping[ent.label_]
            
            # Calculate confidence
            confidence = self._get_confidence_for_entity(ent)
            
            # Skip entities with low confidence
            if confidence < self.min_confidence:
                continue
            
            # Get context
            context_before, context_after = self._get_context(doc, ent)
            
            # Create the entity
            entity = EntityFactory.create_entity(
                name=ent.text,
                entity_type=entity_type,
                source_text=ent.text,
                start_position=ent.start_char,
                end_position=ent.end_char,
                confidence=confidence,
                metadata={"spacy_type": ent.label_}
            )
            
            # Record the observation
            ObservationRecorder.record_entity_observation(
                entity=entity,
                source=kwargs.get("source_id", "unknown"),
                context_before=context_before,
                context_after=context_after,
                extractor=f"SpacyEntityExtractor({self.model_name})"
            )
            
            # Add the entity to the collection
            collection.add_entity(entity)
        
        # Extract relationships based on syntactic dependencies
        self._extract_relationships(doc, collection, kwargs.get("source_id", "unknown"))
        
        return collection
    
    def _extract_relationships(
        self, doc: spacy.tokens.doc.Doc, collection: EntityCollection, source_id: str
    ) -> None:
        """
        Extract relationships between entities based on syntactic dependencies.
        
        Args:
            doc: spaCy document.
            collection: Entity collection to add relationships to.
            source_id: Source identifier.
        """
        # Create a mapping from token spans to entity IDs
        span_to_entity = {}
        for entity in collection.entities:
            start_token = None
            end_token = None
            
            # Find the token span that corresponds to the entity
            for i, token in enumerate(doc):
                if token.idx == entity.start_position:
                    start_token = i
                if token.idx + len(token.text) == entity.end_position:
                    end_token = i + 1
                    break
            
            if start_token is not None and end_token is not None:
                span_to_entity[(start_token, end_token)] = entity.id
        
        # Look for verb-mediated relationships between entities
        for sent in doc.sents:
            # Find the main verb of the sentence
            main_verb = None
            for token in sent:
                if token.pos_ == "VERB" and token.dep_ in ["ROOT", "xcomp"]:
                    main_verb = token
                    break
            
            if main_verb is None:
                continue
            
            # Find subject and object entities connected to the main verb
            subject_entity = None
            object_entity = None
            
            for token in sent:
                # Check for subject
                if token.dep_ in ["nsubj", "nsubjpass"] and token.head == main_verb:
                    # Find the entity that contains this token
                    for (start, end), entity_id in span_to_entity.items():
                        if start <= token.i < end:
                            subject_entity = entity_id
                            break
                
                # Check for object
                if token.dep_ in ["dobj", "pobj"] and (token.head == main_verb or 
                                                   (token.head.dep_ == "prep" and token.head.head == main_verb)):
                    # Find the entity that contains this token
                    for (start, end), entity_id in span_to_entity.items():
                        if start <= token.i < end:
                            object_entity = entity_id
                            break
            
            # If we found both subject and object entities, create a relationship
            if subject_entity and object_entity:
                # Determine relationship type based on the verb
                relationship_type = "relatesTo"  # Default type
                
                verb_lemma = main_verb.lemma_.lower()
                if verb_lemma in ["use", "utilize", "employ"]:
                    relationship_type = "uses"
                elif verb_lemma in ["work", "collaborate"]:
                    relationship_type = "worksOn"
                elif verb_lemma in ["have", "own", "possess"]:
                    relationship_type = "has"
                elif verb_lemma in ["depend", "rely"]:
                    relationship_type = "dependsOn"
                elif verb_lemma in ["create", "make", "develop", "build"]:
                    relationship_type = "creates"
                
                # Create the relationship
                relationship = EntityFactory.create_relationship(
                    source_entity=subject_entity,
                    target_entity=object_entity,
                    relationship_type=relationship_type,
                    confidence=0.7,  # Base confidence for syntactic relationships
                    metadata={"verb": main_verb.text, "sentence": sent.text}
                )
                
                # Record the observation
                ObservationRecorder.record_relationship_observation(
                    relationship=relationship,
                    source=source_id,
                    context=sent.text,
                    extractor=f"SpacyEntityExtractor({self.model_name})"
                )
                
                # Add the relationship to the collection
                collection.add_relationship(relationship)
