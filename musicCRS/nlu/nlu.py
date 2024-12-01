"""Module contains the NLU.

It has the prompt, which is sent to the model to get the user intent and
entities.

Under the hood Ollama is used to query a LLAMA 3.2 model and get the response.
"""

from typing import Any, Dict, Union

import ollama

from . import post_processing


def get_nlu_response(user_input: str) -> str:
    """Provides the natural language understanding response.

    Args:
        user_input: The user input to process.

    Returns:
        A JSON formatted response from the model containing the intent and
        entities.
    """
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
                        - "recommend": Get a song recommendation
                        - "create": Create a new playlist based on the user's preferences
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
                        - `description`: A description of the playlist that the user wants to create, or an empty string if not mentioned

                        ### Entity Requirements by Intent:
                        Each intent should include only the specified entities, but always return all entities:
                        - `add`: Populate `song` (mandatory) and `artist` (if provided, otherwise leave him as empty strings). If you are not able to find a song title, probably the right intent is 'recommend'.
                        - `delete`: Populate `song` or `position` if specified; otherwise, leave them as empty strings.
                        - `clear`: No entities are needed, but all entities should still be included as empty strings.
                        - `recommend`: No entities are needed, but all entities should still be included as empty strings.
                        - `create`: Populate `description`.
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
                        5. **Description Entity**: The `description` entity is not empty only in a create intent. It should be a string with the description of the playlist that the user wants to create.

                        ### Examples:
                        - User: "add bohemian rhapsody by Queen to my playlist"
                        Output:
                        {{
                            "intent": "add",
                            "entities": {{
                                "song": "bohemian rhapsody",
                                "artist": "Queen",
                                "album": "",
                                "position": "",
                                "description": ""
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
                                "position": "",
                                "description": ""
                            }}
                        }}
                        - User: "Suggest me some songs"
                        Output:
                        {{
                            "intent": "recommend",
                            "entities": {{
                                "song": "",
                                "artist": "",
                                "album": "",
                                "position": "",
                                "description": ""
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
                                "position": "",
                                "description": ""
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
                                "position": "[4,1]",
                                "description": ""
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
                                "position": "",
                                "description": ""
                            }}
                        }}
                        - User: "Create a playlist with sad love songs"
                        Output:
                        {{
                            "intent": "create",
                            "entities": {{
                                "song": "",
                                "artist": "",
                                "album": "",
                                "position": ""
                                "description": "sad love songs"
                            }}
                        }}

                        REMEMBER TO DO NOT PROVIDE AN ARTIST IF IT'S NOT PROVIDED BY THE USER.
                        User command: '{user_input}'
                        """,
            },
        ],
    )
    return response["message"]["content"]


def get_playlist_songs(user_input: str) -> str:
    """Queries the model to get parameters for playlist songs.

    Args:
        user_input: The user input to process.

    Returns:
        The JSON formatted response from the model.
    """
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": f"""
                    You are a playlist creation assistant. Given a description of the playlist a user wants to create, you will analyze the mood, style, and intended vibe of the playlist and output a structured JSON response. Include fields only if they are important for accurately capturing the user's intent.

                    ### Field Descriptions:
                    Use these descriptions to interpret the user’s playlist request and assign values accurately. Pay close attention to mood-related keywords (e.g., "melancholic," "chill," "romantic," "soft," "calm," "winter"), as these often indicate a lower energy level.

                    - **genre**: A list of genres that fit the playlist description (e.g., ["pop", "rock", "jazz"]). If relevant, include multiple genres that might align with the description to capture the user’s intended atmosphere.

                    - **danceability**: Describes how suitable a track is for dancing, based on musical elements like tempo, beat, and rhythm. Use "low" for less danceable tracks, "mid" for moderately danceable, and "high" for highly danceable.

                    - **energy**: Represents the intensity and activity level of a track. High-energy tracks are fast, loud, and intense, while low-energy tracks are calm and relaxing. For descriptions like "calm," "chill," "romantic," "melancholic," "winter," or "soft," choose "low" energy. For balanced or neutral energy, use "mid." For upbeat, active, or intense music, use "high."

                    - **tempo**: The speed or pace of a track in beats per minute (BPM). Choose "low" for slow tracks, "mid" for moderate tempo, and "high" for fast-paced tracks. Generally, tracks below 100 BPM are "low," between 100 and 140 BPM are "mid," and above 140 BPM are "high."

                    - **valence**: Indicates the positivity of a track. Use "low" for sad or somber music, "mid" for neutral mood, and "high" for happy or upbeat tracks.

                    - **min**: This is an estimated playlist length in minutes, based on the description or activity implied in the user request. If the description suggests an activity with a typical duration (e.g., "gym session," "focus music"), use an appropriate time, such as 60 minutes for a gym session. If no specific activity is implied, set a minimum playlist length of at least 20 minutes to create a meaningful listening experience.

                    ### Instructions:
                    1. Interpret the description to infer the genre and characteristics of the music the user is looking for.
                    2. Populate only the fields most relevant to the description:
                        - **genre**: List of genres (e.g., ["pop", "rock"]). If appropriate, include multiple genres.
                        - **danceability, energy, tempo, valence**: Each a string ("low", "mid", or "high") to represent the music characteristics as described above.
                        - **min**: Estimated playlist duration in minutes, based on the activity or general context of the playlist request.
                    3. Pay close attention to keywords in the description to interpret energy accurately, especially for mood-specific requests like "melancholic," "chill," or "calm."
                    4. Provide data for each relevant field based on the theme of the playlist description.

                    ### Output Format:
                    Respond only with a JSON object in this format:

                    {{
                        "genre": ["genre_1", "genre_2"],
                        "danceability": "low | mid | high",
                        "energy": "low | mid | high",
                        "tempo": "low | mid | high",
                        "valence": "low | mid | high",
                        "min": estimated_minutes
                    }}

                    Include only the fields you consider important for the given playlist description.

                    ### Examples

                    #### Example 1
                    **User Description:** “I want a playlist of upbeat pop songs for working out.”

                    **Expected Output:**

                    {{
                        "genre": ["pop"],
                        "danceability": "high",
                        "energy": "high",
                        "tempo": "high",
                        "valence": "high",
                        "min": 60
                    }}

                    #### Example 2

                    **User Description:** “Create a calm and relaxing playlist with acoustic music.”

                    **Expected Output:**

                    {{
                        "genre": ["acoustic", "folk"],
                        "energy": "low",
                        "tempo": "low",
                        "valence": "mid",
                        "min": 25
                    }}

                    #### Example 3

                    **User Description:** “I want a playlist with instrumental music.”

                    **Expected Output:**

                    {{
                        "genre": ["instrumental"],
                        "speechiness": "low",
                        "min": 35
                    }}

                    #### Example 4
                    **User Description:** “Melancholic winter songs.”

                    **Expected Output:**

                    {{
                        "genre": ["ambient", "folk", "indie"],
                        "energy": "low",
                        "tempo": "low",
                        "valence": "low",
                        "min": 30
                    }}

                    Respond only with the JSON output in the specified format.

                    **User Description**: '{user_input}'
                    """,
            }
        ],
    )

    return response["message"]["content"]


def interact_with_playlist_agent(user_preferences: str) -> str:
    """Queries the model to get a correct input for the playlist agent

    Args:
        user_preferences: The user input to process.

    Returns:
        The JSON formatted response from the model.
    """
    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": f"""
                    You are a simulation agent interacting with the Music Recommender System to create a playlist based on user preferences and goals. The system supports commands and queries for managing and querying playlists, which you should use strategically to meet the user’s goal.

                    ### Instructions

                    1. **Commands**: Use these to add, delete, clear, view, or get help with the playlist.
                        - **/add <song>**: Add a song to the playlist.
                        - **/delete <song>**: Delete a song from the playlist.
                        - **/clear**: Clear the current playlist.
                        - **/view**: Show the current playlist.
                        - **/help**: Show help message.
                        - **/exit**: Exit the conversation.

                    2. **Queries**: You can also ask questions about songs and albums in the system’s database:
                        - "When was album X released?"
                        - "How many albums has artist Y released?"
                        - "Which album features song X?"
                        - "How many songs does album X contain?"
                        - "How long is album X?"
                        - "What is the most popular song by artist X?"

                    3. **User Profile**:
                        Use the provided user profile to inform your actions. Prioritize their preferred genres and liked artists, avoid disliked artists, and work towards achieving the user’s specified goal.

                    REMEMBER TO
                    ### Example User Profile:
                    UserProfile(id='1', preferences=['rock', 'pop', 'jazz'], liked_artists=['Taylor Swift', 'Ariana Grande'], disliked_artists=['Justin Bieber'], goal='Create a playlist')

                    ---

                    ### Examples of Interactions

                    **Example 1**

                    **User Profile**:
                    UserProfile(id='1', preferences=['rock', 'pop', 'jazz'], liked_artists=['Taylor Swift', 'Ariana Grande'], disliked_artists=['Justin Bieber'], goal='Create a playlist')

                    **System Command**: /add Shake It Off by Taylor Swift

                    ---

                    **Example 2**

                    **User Profile**:
                    UserProfile(id='2', preferences=['jazz', 'classical'], liked_artists=['John Coltrane'], disliked_artists=['Justin Bieber'], goal='Create a playlist')

                    **System Command**: /add A Love Supreme by John Coltrane

                    ---

                    **Example 3**

                    **User Profile**:
                    UserProfile(id='1', preferences=['rock', 'pop'], liked_artists=['Ariana Grande'], disliked_artists=['Justin Bieber'], goal='Create a playlist')

                    **System Command**: /add 7 rings by Ariana Grande

                    ---

                    ### Task

                    Based on the following user profile and the system commands and queries, respond with the most suitable command or query to help build the playlist. Respond with only the command or query without explanations.

                    **User Profile**:
                    {user_preferences}

                    """,
            }
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

    def generate_playlist(self, user_input: str) -> Union[Dict[str, Any], None]:
        """Queries the model to get parameters for playlist songs.

        It is used for the `recommend` intent to get the playlist parameters,
        which are then used to query the database for the playlist songs.

        Args:
            user_input: The user input to process.

        Returns:
            The playlist parameters extracted from the user input.
        """
        # Call the model with the user input
        response = get_playlist_songs(user_input)

        # Parse the json response
        json_data = post_processing.post_process_response(response)
        print(json_data)

        return json_data


# TODO: Remove the following code
if __name__ == "__main__":

    response_test = get_playlist_songs(
        "melancholic songs for a quick stroll around the park"
    )
    print(response_test)
