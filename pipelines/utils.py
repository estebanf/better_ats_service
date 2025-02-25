"""
Pipeline Utilities Module

This module provides utility functions for working with Haystack pipelines,
particularly focused on handling Pydantic models and formatting instructions
for LLM interactions.
"""

import json
from typing import Type
from pydantic import BaseModel

def get_format_instructions(model_class: Type[BaseModel]) -> str:
    """
    Generate format instructions for LLM based on a Pydantic model.

    This function creates a structured format guide that helps the LLM understand
    how to format its response to match the expected Pydantic model structure.

    Args:
        model_class (Type[BaseModel]): The Pydantic model class to generate
            instructions for. Must be a subclass of BaseModel.

    Returns:
        str: A formatted string containing JSON structure instructions based
            on the model's schema, including field descriptions and examples.

    Example:
        >>> from models import CandidateData
        >>> instructions = get_format_instructions(CandidateData)
        >>> print(instructions)
        'Format the response as a JSON object with the following structure:
         {
             "first_name": "string",  // The candidate's first name
             "last_name": "string",   // The candidate's last name
             ...
         }'
    """
    # Get the model's JSON schema
    schema = model_class.model_json_schema()
    
    # Extract relevant information from the schema
    properties = schema.get("properties", {})
    required = schema.get("required", [])
    
    # Build the format instructions
    instructions = ["Format the response as a JSON object with the following structure:"]
    instructions.append("{")
    
    # Add each field with its description
    for field_name, field_info in properties.items():
        description = field_info.get("description", "")
        field_type = field_info.get("type", "any")
        required_mark = "*" if field_name in required else ""
        
        instructions.append(f'    "{field_name}"{required_mark}: {field_type}  // {description}')
    
    instructions.append("}")
    
    return "\n".join(instructions)