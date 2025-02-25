"""
Assessment Pipeline Module

This module defines a Haystack pipeline for assessing job requirements against candidate documents.
It uses OpenAI's LLM to analyze each requirement and determine if it's met by the candidate's
experience, providing clarifying questions when needed.
"""

import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import OpenAIChatGenerator
from .llm_to_model_component import LLMToModel
from models import RequirementAssessment

# Load environment variables
load_dotenv()

# System prompt defining the AI's role and purpose
assessment_template = [
    ChatMessage.from_system(
        "You are a clever assistant that can infer if a candidate meets the a job requirement"
    ),
    ChatMessage.from_user(
        """Your goal is decide if a candidate most likely meets the a requirement for a job. If it does, you just need to confirm that the experience or skill is present int the document. If you are not reasonably sure, then you should formulate a question to the candidate to give them a chance to provide additional information.

        {{format_instructions}}

        This is the requirement you need to assess:
        ```
        {{requirement}}
        ```

        The documents where you are going to review to do your assessment are the following:

        {% for doc in documents %}
        {{doc.meta["file_path"]}}:

        {{doc.content}}

        ---
        {% endfor %}
        """
    ),
]

# Initialize the assessment pipeline
assessment_pipeline = Pipeline()

# Add prompt building component
assessment_pipeline.add_component(
    instance=ChatPromptBuilder(template=assessment_template),
    name="assessment_prompt"
)

# Add OpenAI chat component with configurable model
assessment_pipeline.add_component(
    instance=OpenAIChatGenerator(
        model=os.getenv("ASSESSMENT_MODEL", "gpt-4")
    ),
    name="openai_generator"
)

# Add component to convert LLM output to RequirementAssessment model
assessment_pipeline.add_component(
    instance=LLMToModel(model_class=RequirementAssessment),
    name="llm_to_model"
)

# Connect pipeline components
assessment_pipeline.connect("assessment_prompt.prompt", "openai_generator.messages")
assessment_pipeline.connect("openai_generator.replies", "llm_to_model.replies")

