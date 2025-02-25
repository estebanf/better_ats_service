"""
Candidate Data Pipeline Module

This module defines a Haystack pipeline for extracting structured candidate information
from resume documents. It uses OpenAI's LLM to parse and structure the information
into a standardized CandidateData format.
"""

import os
from dotenv import load_dotenv
from haystack import Pipeline
from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage
from haystack.components.generators.chat import OpenAIChatGenerator
from .llm_to_model_component import LLMToModel
from models import CandidateData

# Load environment variables
load_dotenv()

# System prompt defining the AI's role and purpose
candidate_data_template = [
    ChatMessage.from_system(
        "You are a helpful assistant that extracts data from documents received in a job application"
    ),
    ChatMessage.from_user(
        """Your goal is to extract from the documents the information required about the candidate. You should keep the data extracted as written in the documents, so don't summarize it or change it.

        You are expected to extract: First name, Last name, Email, Phone, LinkedIn profile, and all the experiences of the candidate. For each experience, you should extract: Company, Title, Start date, End date, and Description. Do not make up any information, only extract what is written in the documents. Do not attempt to extract any additional information.

        {{format_instructions}}

        The documents where you are going to extract the data from are the following:

        {% for doc in documents %}
        {{doc.meta["file_path"]}}:

        {{doc.content}}

        ---
        {% endfor %}
        """
    ),
]

# Initialize the candidate data extraction pipeline
candidate_data_pipeline = Pipeline()

# Add prompt building component
candidate_data_pipeline.add_component(
    instance=ChatPromptBuilder(template=candidate_data_template),
    name="candidate_prompt"
)

# Add OpenAI chat component with configurable model
candidate_data_pipeline.add_component(
    instance=OpenAIChatGenerator(
        model=os.getenv("CANDIDATE_DATA_MODEL", "gpt-4")
    ),
    name="openai_generator"
)

# Add component to convert LLM output to CandidateData model
candidate_data_pipeline.add_component(
    instance=LLMToModel(model_class=CandidateData),
    name="llm_to_model"
)

# Connect pipeline components
candidate_data_pipeline.connect("candidate_prompt.prompt", "openai_generator.messages")
candidate_data_pipeline.connect("openai_generator.replies", "llm_to_model.replies")
