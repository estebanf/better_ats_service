from typing import List
from pipelines import load_documents_pipeline

def exec_load_documents(file_paths: List[str]):
    results =  load_documents_pipeline.run({
        "file_type_router" : {
            "sources" : file_paths
        }
    })
    return results["joiner"]["documents"]