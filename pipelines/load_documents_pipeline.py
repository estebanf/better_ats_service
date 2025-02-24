from haystack import Pipeline
from haystack.components.converters import PyPDFToDocument
from haystack.components.converters.docx import DOCXToDocument
from haystack.components.joiners.document_joiner import DocumentJoiner
from haystack.components.routers import FileTypeRouter

load_documents_pipeline  = Pipeline()
load_documents_pipeline.add_component(instance=FileTypeRouter(mime_types=[
    "application/pdf", 
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]), 
    name="file_type_router")
load_documents_pipeline.add_component(instance=PyPDFToDocument(),name="pdf_converter")
load_documents_pipeline.add_component(instance=DOCXToDocument(),name="docx_converter")
load_documents_pipeline.add_component(instance=DocumentJoiner(), name="joiner")

load_documents_pipeline.connect("file_type_router.application/pdf", "pdf_converter.sources")
load_documents_pipeline.connect("file_type_router.application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docx_converter.sources")
load_documents_pipeline.connect("pdf_converter.documents", "joiner.documents")
load_documents_pipeline.connect("docx_converter.documents", "joiner.documents")