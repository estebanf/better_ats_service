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
):
    # Parse the process_input JSON string into our Pydantic model
    process_input_data = ProcessInput(**json.loads(process_input))
    
    # Ensure /tmp directory exists
    tmp_dir = Path("/tmp")
    tmp_dir.mkdir(exist_ok=True)
    
    # Process and store the uploaded files
    file_contents = []
    uploaded_files = []
    
    for file in files:
        # Get original file extension
        original_extension = Path(file.filename).suffix
        # Generate unique filename with original extension
        unique_filename = f"{uuid.uuid4()}{original_extension}"
        file_path = tmp_dir / unique_filename
        absolute_path = file_path.absolute()
        
        # Read and save the file
        content = await file.read()
        with open(file_path, "wb") as f:
            f.write(content)
            
        file_contents.append({
            "original_filename": file.filename,
            "saved_filename": unique_filename,
            "path": str(absolute_path)
        })
        uploaded_files.append(str(absolute_path))
    
    documents = exec_load_documents(uploaded_files)
    
    # Execute candidate data extraction and requirements assessment in parallel
    candidate_data, assessments = await asyncio.gather(
        exec_candidate_data(documents),
        exec_assessment(documents, process_input_data.job_requirements)
    )

    results = ProcessOutput(
        candidate_data=candidate_data,
        requirements_assessment=assessments
    )
    
    return results 