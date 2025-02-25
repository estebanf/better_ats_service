"""
Process Input Models Module

This module defines the input data models for the document processing API.
It provides Pydantic models for request validation and documentation.
"""

from pydantic import BaseModel, Field
from typing import List

class ProcessInput(BaseModel):
    """
    Input model for the document processing endpoint.
    
    This model defines the structure of the input data expected by the /process endpoint.
    It validates that the job requirements are provided in the correct format.

    Attributes:
        job_requirements (List[str]): A list of job requirements to assess against
            the candidate's documents. Each requirement should be a clear, specific
            statement about a skill, experience, or qualification.

    Example:
        >>> input_data = ProcessInput(
        ...     job_requirements=[
        ...         "5+ years of Python development experience",
        ...         "Experience with AWS cloud services",
        ...         "Strong background in machine learning"
        ...     ]
        ... )
    """
    
    job_requirements: List[str] = Field(
        description="List of job requirements to assess against the candidate's documents",
        min_items=1,
        example=[
            "5+ years of Python development experience",
            "Experience with AWS cloud services",
            "Strong background in machine learning"
        ]
    ) 