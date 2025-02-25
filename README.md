# Better ATS Service

A FastAPI-based microservice that processes resumes against job requirements using AI. The service extracts candidate information from uploaded documents and assesses each job requirement against the candidate's experience.

## Features

- Extract structured candidate data from resumes (PDF format)
- Assess job requirements against candidate experience
- Generate clarifying questions for requirements that can't be verified
- Parallel processing of requirements
- RESTful API interface

## Project Structure

```
better-ats-service/
├── models/              # Pydantic models for data validation
│   ├── experience.py    # Experience data model
│   ├── candidate.py     # Candidate data model
│   ├── assessment.py    # Requirement assessment model
│   └── process_input.py # API input/output models
├── routes/              # FastAPI route handlers
│   └── process.py       # Main processing endpoint
├── pipelines/           # Haystack pipeline definitions
│   ├── assessment_pipeline.py    # Job requirement assessment
│   └── candidate_data_pipeline.py # Candidate data extraction
├── exec/                # Pipeline execution modules
│   ├── exec_assessment.py     # Parallel requirement processing
│   └── exec_candidate_data.py # Candidate data extraction
└── main.py             # FastAPI application entry point
```

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```bash
# Server Configuration
HOST=0.0.0.0            # Server host
PORT=8000               # Server port

# OpenAI Configuration
OPENAI_API_KEY=your_key # Your OpenAI API key

# Model Configuration
CANDIDATE_DATA_MODEL=gpt-4  # Model for candidate data extraction
ASSESSMENT_MODEL=gpt-4      # Model for requirement assessment

# Performance Configuration
MAX_WORKERS=4           # Maximum concurrent requirement assessments

# File Storage Configuration
UPLOAD_TMP_DIR=/tmp    # Temporary directory for file uploads
```

## API Interface

### POST /process

Process resumes against job requirements.

#### Request

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: multipart/form-data" \
  -F "files=@/path/to/resume1.pdf" \
  -F "files=@/path/to/resume2.pdf" \
  -F 'process_input={
    "job_requirements": [
      "5+ years of Python development experience",
      "Experience with AWS cloud services",
      "Strong background in machine learning"
    ]
  }'
```

#### Response

```json
{
  "candidate_data": {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@email.com",
    "phone": "+1 (555) 123-4567",
    "linkedin": "linkedin.com/in/johndoe",
    "experiences": [
      {
        "company": "Tech Corp",
        "title": "Senior Python Developer",
        "start_date": "01/2020",
        "end_date": "Present",
        "description": "Led development of cloud-based applications..."
      }
    ]
  },
  "requirements_assessment": [
    {
      "requirement": "5+ years of Python development experience",
      "present_in_documents": true,
      "inquiry": null
    },
    {
      "requirement": "Experience with AWS cloud services",
      "present_in_documents": true,
      "inquiry": null
    },
    {
      "requirement": "Strong background in machine learning",
      "present_in_documents": false,
      "inquiry": "Could you describe any specific machine learning projects you've worked on?"
    }
  ]
}
```

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/better-ats-service.git
cd better-ats-service
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. Run the service:
```bash
uvicorn main:app --reload
```

The API documentation will be available at `http://localhost:8000/docs`

## Dependencies

- FastAPI: Web framework
- Haystack: Document processing and LLM pipelines
- PyPDF: PDF processing
- OpenAI: LLM provider
- python-multipart: File upload handling
- python-dotenv: Environment variable management

## Development

The service uses several key components:

- **Models**: Pydantic models for data validation and serialization
- **Routes**: FastAPI route handlers for API endpoints
- **Pipelines**: [#Haystack](https://github.com/deepset-ai/haystack) pipelines for document processing and LLM interactions
- **Exec**: Execution modules for parallel processing and pipeline orchestration

### Adding New Features

1. Define new models in `models/`
2. Create new pipelines in `pipelines/`
3. Add execution logic in `exec/`
4. Define routes in `routes/`

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
