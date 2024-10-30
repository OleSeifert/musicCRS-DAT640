import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": """
            You are an intent detection assistant. Identify the user's intent from the following options:
    - Add a song to the playlist (intent: "add")
    - Delete a song from the playlist (intent: "delete")
    - Clear the playlist (intent: "clear")
    - Answer questions about songs and albums with these questions:
      - "When was album X released?" (intent: "Q1")
      - "How many albums has artist Y released?" (intent: "Q2")
      - "Which album features song X?" (intent: "Q3")
      - "How many songs does album X contain?" (intent: "Q4")
      - "How long is album X?" (intent: "Q5")
      - "What is the most popular song by artist X?" (intent: "Q6")


    For each command, also extract entities if available:
    - `artist`, `album`, `song`, `position`
    Please only provide entities that are relevant to the user's intent. E.G.
    if there is no song mentioned, don't provide a song entity!!

    The position entity is only relevant if the user mentions a specific position ('first', 'third', ...) in the playlist.
    You have to add that only for the delete intet and for questions about songs.
    If the 'last song' is mentioned, the position should be 'last'.
    If a range of positions is described, provide the indices of the first and last song to be deleted.

    Please use indexing starting from 0!

    For the following intents provide only the listed entities:
    - add: song, artist (artist only if provided)
    - delete: song
    - clear: no entities needed
    - Q1: album
    - Q2: artist
    - Q3: song
    - Q4: album
    - Q5: album
    - Q6: artist

    Negative words like 'hate' 'dislike' prompt to delete a song from the playlist.


    The following are examples of user queries, the queries can look different.
    The output for the query 'Put Bohemian Rhapsody by Queen in my playlist' would be:
    {
        "intent": "add",
        "entities": {
            "song": "Bohemian Rhapsody",
            "artist": "Queen"
        }
    }
    The output for the query 'Add Thriller to my playlist' would be:
    {
        "intent": "add",
        "entities": {
            "song": "Thriller"
        }
    }
    The output for the query 'remove Bohemian Rhapsody from my playlist' would be:
    {
        "intent": "delete",
        "entities": {
            "song": "Bohemian Rhapsody"
        }
    }
    The output for the query 'Delete the second song from the playlist' would be:
    {
        "intent": "delete",
        "entities": {
            "position": 1
        }
    }
    The output for the query 'delete the playlist' woud be:
    {
        "intent": "clear"
    }
    The output for the query 'When was 1989 released?' would be:
    {
        "intent": "Q1",
        "entities": {
            "album": "1989"
        }
    }
    The output for the query 'How many albums does Taylor Swift have?' would be:
    {
        "intent": "Q2",
        "entities": {
            "artist": "Taylor Swift"
        }
    }
    The ouptut for the query 'Which album features Shake it Off?' would be:
    {
        "intent": "Q3",
        "entities": {
            "song": "Shake it Off"
        }
    }
    The output for the query 'How many songs are on Abbey Road?' would be:
    {
        "intent": "Q4",
        "entities": {
            "album": "Abbey Road"
        }
    }
    The output for the query 'How long does it take to listen to Thriller?' would be:
    {
        "intent": "Q5",
        "entities": {
            "album": "Thriller"
        }
    }
    The output for the query 'What is Michael Jackson most famous for?' would be:
    {
        "intent": "Q6",
        "entities": {
            "artist": "Michael Jackson"
        }
    }
    Do not write anything else, than the JSON output.

    User command: 'delete from the ninth to the last'
    """,
        },
    ],
)
print(response["message"]["content"])
