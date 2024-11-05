"""Module performs post-processing for the NLU.

It checks the NLU reply and extracts the intent and entities from the response.
It makes sure the response is in the correct format and returns the extracted
intent and entities to the playlist agent.
"""

import json
import re
from typing import Any, Dict, Union


def extract_json_from_response(response: str) -> Union[Dict[str, Any], None]:
    """Extracts and parses the JSON object from the model response.

    Args:
        response: The response from the NLU model.

    Returns:
        The JSON object extracted from the response.

    Raises:
        json.JSONDecodeError: If the JSON object cannot be decoded.
    """
    try:
        # Use regex to extract the JSON object from the response
        json_text = re.search(r"\{.*\}", response, re.DOTALL)
        if json_text:
            return json.loads(json_text.group())
        else:
            print("No JSON object found in response:", response)
            return None
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None


def clean_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Cleans the fields in the JSON data.

    Args:
        data: The JSON data to clean.

    Returns:
        The cleaned JSON data.
    """
    if not data:
        return {}

    # Remove leading and trailing whitespaces from the fields
    cleanded_data = {}
    for key, value in data.items():
        if isinstance(value, str):
            # Strip extra whitespace
            cleanded_data[key] = value.strip()
        elif isinstance(value, dict):
            # Recursively clean nested dictionaries
            cleanded_data[key] = clean_data(value)
        else:
            cleanded_data[key] = value

    return cleanded_data


def post_process_response(response: str) -> Dict[str, Any]:
    """Full Post-process the NLU response to extract intent and entities.

    Args:
        response: The response from the NLU model.

    Returns:
        The intent and entities extracted from the response.
    """
    # Extract the JSON object from the response
    json_data = extract_json_from_response(response)

    if json_data is None:
        return {}

    # Clean the JSON data
    cleaned_data = clean_data(json_data)

    return cleaned_data
