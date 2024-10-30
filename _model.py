import ollama
import json


def query_intent(prompt, model="llama3.2"):
    # Send the structured prompt to Ollama and print the response for debugging
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])

    # Check if 'choices' is in the response and extract content if present
    if 'choices' in response:
        response_text = "".join(choice.get("content", "") for choice in response['choices'])
    else:
        print("Unexpected response format:", response)
        return None

    return response_text


# Example usage
if __name__ == "__main__":
    user_input = "Add Bohemian Rhapsody to my playlist"

    # Structured prompt for intent detection
    prompt = f"""
    You are an intent detection assistant. Identify the user's intent from the following options:
    - Add a song to the playlist (intent: "add")
    - Delete a song from the playlist (intent: "delete")
    - Clear the playlist (intent: "clear")
    - Answer questions about songs and albums with these questions:
      - "When was album X released?"
      - "How many albums has artist Y released?"
      - "Which album features song X?"
      - "How many songs does album X contain?"
      - "How long is album X?"
      - "What is the most popular song by artist X?"

    For each command, also extract entities if available:
    - `artist`, `album`, `song`

    Provide the output in JSON format like this example:
    {{
        "intent": "add",
        "entities": {{
            "song": "Bohemian Rhapsody",
            "artist": "Queen"
        }}
    }}

    User command: '{user_input}'
    """

    # Query the model and print the result
    result = query_intent(prompt)
    if result:
        print("Model response:", result)

        # Attempt to parse JSON if the response is in the correct format
        try:
            result_json = json.loads(result)
            print("Parsed JSON:", result_json)
        except json.JSONDecodeError:
            print("Response is not in JSON format:", result)
    else:
        print("No valid response received.")
