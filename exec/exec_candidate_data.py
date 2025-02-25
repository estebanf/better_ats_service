"""
Candidate Data Extraction Module

This module handles the extraction of structured candidate information from documents
using the Haystack pipeline and LLM processing.
"""

from pipelines import candidate_data_pipeline, get_format_instructions
from models import CandidateData
from haystack import Document
from typing import List

async def exec_candidate_data(documents: List[Document]) -> CandidateData:
    """
    Extract structured candidate data from provided documents.

    This function processes the input documents through a Haystack pipeline to extract
    relevant candidate information such as personal details and work experience.

    Args:
        documents (List[Document]): List of Haystack documents containing the candidate's
            resume or other relevant documents. Each document should have content and
            metadata accessible.

    Returns:
        CandidateData: A structured object containing the extracted candidate information,
            including personal details (name, contact info) and work experiences.

    Example:
        >>> docs = [Document(content="Resume content...")]
        >>> candidate_data = await exec_candidate_data(docs)
        >>> print(f"Candidate name: {candidate_data.first_name} {candidate_data.last_name}")
    """
    results = candidate_data_pipeline.run({
        "documents": documents,
        "format_instructions": get_format_instructions(CandidateData)
    })
    return results["llm_to_model"]["model"]