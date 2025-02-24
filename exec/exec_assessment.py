"""
Assessment Execution Module

This module handles the parallel processing of job requirements against candidate documents.
It uses a ThreadPoolExecutor to process multiple requirements concurrently while respecting
a configurable maximum number of worker threads.
"""

from pipelines import assessment_pipeline, get_format_instructions
from models import RequirementAssessment
from typing import List
from haystack import Document
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from dotenv import load_dotenv

# Load environment variables at module initialization
load_dotenv()

def process_requirement(documents: List[Document], requirement: str, format_instructions: str) -> RequirementAssessment:
    """
    Process a single job requirement against the provided documents.
    
    Args:
        documents (List[Document]): List of Haystack documents containing candidate information
        requirement (str): The job requirement to assess
        format_instructions (str): Instructions for formatting the assessment output
    
    Returns:
        RequirementAssessment: Assessment result for the given requirement
    """
    requirement_result = assessment_pipeline.run({
        "documents": documents,
        "requirement": requirement,
        "format_instructions": format_instructions
    })
    return requirement_result["llm_to_model"]["model"]

async def exec_assessment(documents: List[Document], requirements: List[str]) -> List[RequirementAssessment]:
    """
    Execute assessment of multiple job requirements in parallel.
    
    This function processes multiple job requirements concurrently using a thread pool,
    with the maximum number of concurrent operations controlled by the MAX_WORKERS
    environment variable.
    
    Args:
        documents (List[Document]): List of Haystack documents containing candidate information
        requirements (List[str]): List of job requirements to assess
    
    Returns:
        List[RequirementAssessment]: List of assessment results for each requirement
    
    Raises:
        Exception: If any requirement processing fails, with details about which requirement caused the error
    """
    # Get formatting instructions for the RequirementAssessment model
    format_instructions = get_format_instructions(RequirementAssessment)
    results = []
    
    # Get max_workers from environment variable, default to 4 if not set
    max_workers = int(os.getenv("MAX_WORKERS", "4"))
    
    # Using ThreadPoolExecutor with configured max_workers
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all requirements for processing
        future_to_requirement = {
            executor.submit(
                process_requirement, 
                documents, 
                requirement, 
                format_instructions
            ): requirement for requirement in requirements
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_requirement):
            requirement = future_to_requirement[future]
            try:
                result = future.result()
                results.append(result)
            except Exception as e:
                raise Exception(f'Error processing requirement "{requirement}": {str(e)}')

    return results
