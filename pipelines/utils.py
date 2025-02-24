import json
from pydantic import BaseModel

def get_format_instructions(model: BaseModel):
    snippet ="""
        The output should be formatted as a JSON instance that conforms to the JSON schema below.

        As an example, for the schema {"properties": {"foo": {"title": "Foo", "description": "a list of strings", "type": "array", "items": { "type": "string"} }}, "required": ["foo"]}
        the object {"foo": ["bar", "baz"]} is a well-formatted instance of the schema. The object {"properties": {"foo": ["bar", "baz"]}} is not well-formatted.

        Here is the output schema:
        ```json
        """
    # Convert the schema dict to a JSON string
    schema_json = json.dumps(model.model_json_schema(), indent=2)
    snippet += schema_json + "\n"
    snippet += """
        ```        
        Reply with the JSON document only, nothing else. You don't need to add comments before or after the JSON document, neither include the json schema in your response.
    """
    return snippet