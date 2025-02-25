"""
Document Loading Pipeline Module

This module defines a Haystack pipeline for loading and preprocessing documents from various file formats.
The pipeline handles both PDF and DOCX files, converting them into Haystack Document objects for further
processing. It uses a router to direct files to appropriate converters based on their MIME types, and
then joins all processed documents into a single collection.

Components:
    - FileTypeRouter: Routes files based on MIME type
    - PyPDFToDocument: Converts PDF files to Document objects
    - DOCXToDocument: Converts DOCX files to Document objects
    - DocumentJoiner: Combines all processed documents into a single collection
"""

from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.converters.docx import DOCXToDocument
from haystack.components.joiners.document_joiner import DocumentJoiner
from haystack.components.routers import FileTypeRouter

# Initialize the main document loading pipeline
load_documents_pipeline = Pipeline()

# Add router to handle different file types based on MIME types
# Supports PDF (.pdf) and Word (.docx) documents
load_documents_pipeline.add_component(instance=FileTypeRouter(mime_types=[
    "application/pdf",  # PDF files
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"  # DOCX files
]), name="file_type_router")

# Add converter for PDF files
load_documents_pipeline.add_component(instance=PyPDFToDocument(), name="pdf_converter")

# Add converter for DOCX files
load_documents_pipeline.add_component(instance=DOCXToDocument(), name="docx_converter")

# Add joiner to combine all processed documents
load_documents_pipeline.add_component(instance=DocumentJoiner(), name="joiner")

# Connect pipeline components:
# 1. Route PDF files to PDF converter
load_documents_pipeline.connect("file_type_router.application/pdf", "pdf_converter.sources")

# 2. Route DOCX files to DOCX converter
load_documents_pipeline.connect("file_type_router.application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx_converter.sources")

# 3. Connect PDF converter output to joiner
load_documents_pipeline.connect("pdf_converter.documents", "joiner.documents")

# 4. Connect DOCX converter output to joiner
load_documents_pipeline.connect("docx_converter.documents", "joiner.documents")