import ollama

response = ollama.chat(
    model="llama3.2",
    messages=[
        {
            "role": "user",
            "content": """Create an intent classifier which classifies the intent with the categories ADD, DELETE, CLEAR.
            Also it should identify the context which is a song title or an artist (or both).
            Example of ADD: 'Please add Cruel Summer by Taylor Swift to the playlist'.
            Your classification should be returned as a JSON object.
            Classify the following message: 'Remove Africa from my list'.
            Do not write Code.
            Only provide the category with the information as JSON.""",
        },
    ],
)
print(response["message"]["content"])
