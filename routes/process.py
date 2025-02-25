"""
Process Route Module

This module provides the main processing endpoint for the ATS service. It handles document uploads,
candidate data extraction, and job requirement assessments using Haystack pipelines.

The module processes multiple document formats (PDF, DOCX) and returns structured data about
the candidate and assessment of their qualifications against job requirements.
"""

import os
import uuid
import json
import asyncio
from fastapi import APIRouter, UploadFile, File, Form
from models.process_input import ProcessInput
from pathlib import Path
from typing import List
from exec import exec_load_documents, exec_candidate_data, exec_assessment
from models.process_output import ProcessOutput

router = APIRouter()

@router.post("/process", response_model=ProcessOutput)
async def process_documents(
    process_input: str = Form(...),
    files: List[UploadFile] = File(...)
) -> ProcessOutput:
    """
    Process uploaded documents to extract candidate data and assess job requirements.

    This endpoint handles the complete processing pipeline:
    1. Receives and stores uploaded documents
    2. Extracts structured candidate information
    3. Assesses candidate qualifications against job requirements

    Args:
        process_input (str): JSON string containing job requirements and processing parameters
        files (List[UploadFile]): List of document files (PDF/DOCX) to process

    Returns:
        ProcessOutput: Structured output containing candidate data and requirement assessments

    Raises:
        HTTPException: If file processing fails or temporary directory is not accessible
    """
    # Parse the process_input JSON string into our Pydantic model
    process_input_data = ProcessInput(**json.loads(process_input))
    
    # Get temporary directory from environment variable with fallback to /tmp
    tmp_dir = Path(os.getenv("UPLOAD_TMP_DIR", "/tmp"))
    tmp_dir.mkdir(exist_ok=True)
    
    # Process and store the uploaded files
    file_contents = []  # Store metadata about processed files
    uploaded_files = []  # Store paths to uploaded files for pipeline processing
    
    for file in files:
        # Get original file extension
        original_extension = Path(file.filename).suffix
        # Generate unique filename with original extension to prevent collisions
        unique_filename = f"{uuid.uuid4()}{original_extension}"
        file_path = tmp_dir / unique_filename
        absolute_path = file_path.absolute()
        
        # Read and save the file to temporary storage
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
            
        # Track file metadata and path for processing
        file_contents.append({
            "original_filename": file.filename,
            "saved_filename": unique_filename,
            "path": str(absolute_path)
        })
        uploaded_files.append(str(absolute_path))
    
    # Convert uploaded files to Haystack documents
    documents = exec_load_documents(uploaded_files)
    
    # Execute candidate data extraction and requirements assessment in parallel
    # This improves performance by running independent tasks concurrently
    candidate_data, assessments = await asyncio.gather(
        exec_candidate_data(documents),
        exec_assessment(documents, process_input_data.job_requirements)
    )

    # Combine results into final output structure
    results = ProcessOutput(
        candidate_data=candidate_data,
        requirements_assessment=assessments
    )
    
    return results 