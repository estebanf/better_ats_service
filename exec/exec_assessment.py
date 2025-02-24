from pipelines import assessment_pipeline, get_format_instructions
from models import RequirementAssessment
from typing import List
from haystack import Document

def exec_assessment(documents: List[Document], requirements: List[str]):
    format_instructions = get_format_instructions(RequirementAssessment)
    assessments = []

    for requirement in requirements:
        requirement_assessment = assessment_pipeline.run(
            {
                "assessment_prompt": {
                    "format_instructions": format_instructions,
                    "requirement": requirement,
                    "documents":documents
                }
            }
        )
        assessments.append(requirement_assessment["llm_to_model"]["model"])

    return assessments
