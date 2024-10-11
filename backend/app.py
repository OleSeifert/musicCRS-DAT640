"""Creates a Flask app that fetches the songs from the playlist file.

The app has a single endpoint that returns the songs from the playlist file and
runs on port 5002.

To run execute the following command:

`python app.py`
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/songs", methods=["GET"])
def get_songs():
    """Fetches the songs from the playlist file."""
    with open("../data/playlist.txt", "r", encoding="utf-8") as file:
        playlist = file.readlines()
        playlist = [song.strip() for song in playlist]
    return jsonify(playlist)


if __name__ == "__main__":
    app.run(port=5002)
