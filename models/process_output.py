from pydantic import BaseModel, Field
from typing import List
from .candidate import CandidateData
from .assessment import RequirementAssessment

class ProcessOutput(BaseModel):
    """Model to represent the output of processing a candidate's documents against job requirements"""
    candidate_data: CandidateData = Field(description="The extracted candidate data from the documents")
    requirements_assessment: List[RequirementAssessment] = Field(description="The assessment of each job requirement against the candidate's documents") 