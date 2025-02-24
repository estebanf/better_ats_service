from pipelines import candidate_data_pipeline, get_format_instructions
from models import CandidateData
from haystack import Document
from typing import List

def exec_candidate_data(documents: List[Document]):
    results = candidate_data_pipeline.run({
        "documents" : documents,
        "format_instructions" : get_format_instructions(CandidateData)
    })
    return results["llm_to_model"]["model"]