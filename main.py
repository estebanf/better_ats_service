"""
Better ATS Service - Main Application

This module initializes and configures the FastAPI application for the Better ATS Service.
It sets up CORS, logging, and includes the necessary routers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from routes.process import router as process_router
import logging

# Configure logging to suppress pypdf warnings
logging.getLogger('pypdf').setLevel(logging.ERROR)

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI application with metadata
app = FastAPI(
    title="Better ATS Service",
    description="API for Better ATS Service - Processes resumes and evaluates them against job requirements",
    version="1.0.0"
)

# Configure CORS middleware to handle cross-origin requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with their tags for API documentation
app.include_router(process_router, tags=["Process"])

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify the service is running.
    
    Returns:
        dict: A simple status message indicating the service is healthy
    """
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    
    # Get host and port from environment variables with defaults
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    
    # Run the application using uvicorn
    uvicorn.run(app, host=host, port=port)
