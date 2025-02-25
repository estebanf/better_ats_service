"""
Document Loading Module

This module handles the loading and initial processing of document files (PDFs, etc.)
using Haystack's document processing pipeline. It converts various file formats into
a unified Document representation for further processing.
"""

from typing import List
from pipelines import load_documents_pipeline
from haystack import Document

def exec_load_documents(file_paths: List[str]) -> List[Document]:
    """
    Load and process documents from provided file paths.

    This function takes a list of file paths, processes each file through the appropriate
    document loader (based on file type), and returns a list of Haystack Document objects.
    The pipeline automatically handles different file types and extracts their content.

    Args:
        file_paths (List[str]): List of paths to the documents to be processed. 
            Supports multiple file types (PDF, DOCX, etc.).

    Returns:
        List[Document]: A list of processed Haystack Document objects, each containing
            the content and metadata of the original files.

    Example:
        >>> files = ["/path/to/resume1.pdf", "/path/to/resume2.pdf"]
        >>> documents = exec_load_documents(files)
        >>> print(f"Loaded {len(documents)} documents")
    """
    results = load_documents_pipeline.run({
        "file_type_router": {
            "sources": file_paths
        }
    })
    return results["joiner"]["documents"]