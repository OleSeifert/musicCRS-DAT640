"""Module contains the NLU.

It has the prompt, which is sent to the model to get the user intent and
entities.

Under the hood Ollama is used to query a LLAMA 3.2 model and get the response.
"""

from typing import Any, Dict, Union

import ollama

from . import post_processing


def get_nlu_response(user_input: str) -> str:
    """Query the model with the user input and return the result."""
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": f"""
You are an assistant specializing in intent detection. Identify the user's intent and extract all relevant entities, filling in any entities not mentioned with an empty string. Maintain the exact case (uppercase or lowercase) as given by the user.

### Intent Options:
Choose the appropriate intent based on the user's command:
- "add": Add a song to the playlist
- "delete": Delete a song from the playlist
- "clear": Clear the playlist
- Questions about songs and albums:
  - "Q1": When was album X released?
  - "Q2": How many albums has artist Y released?
  - "Q3": Which album features song X?
  - "Q4": How many songs does album X contain?
  - "Q5": How long is album X?
  - "Q6": What is the most popular song by artist X?

### Entity Extraction:
Always provide the following entities in the JSON response, filling in any entities not mentioned with an empty string:
- `song`: The title of a song, or an empty string if not mentioned
- `artist`: The name of an artist, or an empty string if not mentioned
- `album`: The title of an album, or an empty string if not mentioned
- `position`: Position in the playlist (e.g., "first", "last"), or an empty string if not mentioned

### Entity Requirements by Intent:
Each intent should include only the specified entities, but always return all entities:
- `add`: Populate `song` and `artist` if provided; otherwise, leave them as empty strings.
- `delete`: Populate `song` or `position` if specified; otherwise, leave them as empty strings.
- `clear`: No entities are needed, but all entities should still be included as empty strings.
- `Q1` to `Q6`: Include only the listed entity, but return all entities as empty strings if they are not mentioned:
  - `Q1`: `album`
  - `Q2`: `artist`
  - `Q3`: `song`
  - `Q4`: `album`
  - `Q5`: `album`
  - `Q6`: `artist`

### Important:
1. **Case Sensitivity**: Maintain the user’s input case (uppercase or lowercase) in the output.
2. **Include All Entities**: Always return `song`, `artist`, `album`, and `position` as fields in the JSON response, filling with an empty string if not provided.
3. **Return JSON Only**: Provide only the JSON output, and do not include any extra text or comments.
4. **Position Entity**: The `position` entity is not empty only in a delete intent. It should be an array of integers e.g. [1] if the user wants to delete the second song, or [0,1,2] if the user wants to delete the first three songs.

### Examples:
- User: "add bohemian rhapsody by Queen to my playlist"
  Output:
  {{
      "intent": "add",
      "entities": {{
          "song": "bohemian rhapsody",
          "artist": "Queen",
          "album": "",
          "position": ""
      }}
  }}
- User: "Add thriller to my playlist"
  Output:
  {{
      "intent": "add",
      "entities": {{
          "song": "thriller",
          "artist": "",
          "album": "",
          "position": ""
      }}
  }}
- User: "delete bohemian rhapsody from my playlist"
  Output:
  {{
      "intent": "delete",
      "entities": {{
          "song": "bohemian rhapsody",
          "artist": "",
          "album": "",
          "position": ""
      }}
  }}
  - User: "delete song number five and two"
  Output:
  {{
      "intent": "delete",
      "entities": {{
          "song": "",
          "artist": "",
          "album": "",
          "position": "[4,1]"
      }}
  }}
- User: "When was 1989 released?"
  Output:
  {{
      "intent": "Q1",
      "entities": {{
          "song": "",
          "artist": "",
          "album": "1989",
          "position": ""
      }}
  }}

REMEMBER TO DO NOT PROVIDE AN ARTIST IF IT'S NOT PROVIDED BY THE USER.
User command: '{user_input}'
""",
            },
        ],
    )
    return response["message"]["content"]


class NLUProcessor:
    """
    Class to process the NLU.

    It takes care of the communication with the model and extracts the intent
    and entities from the response. It is called by the playlist agent to
    understand the user's command.
    """

    def __init__(self, model_name: str = "llama3.2") -> None:
        """Initialize the NLUProcessor with a specific model.

        Args:
            model_name: The name of the model to use for the NLU.
        """
        self.model_name = model_name

    def process_input(self, user_input: str) -> Union[Dict[str, Any], None]:
        """Process the user input and return the intent and entities.

        It calls the model with the user input and extracts the intent and
        entities from the response.

        Args:
            user_input: The user input to process.

        Returns:
            The intent and entities extracted from the user input.
        """
        # Call the model with the user input
        response = get_nlu_response(user_input)

        # Parse the json response
        json_data = post_processing.post_process_response(response)

        return json_data


# TODO: Remove the following code
if __name__ == "__main__":
    processor = NLUProcessor()
    res = processor.process_input("Delte the first two songs from the playlist")
    print(res)
    print(type(res))
