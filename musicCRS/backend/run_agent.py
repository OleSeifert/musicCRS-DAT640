"""Module contains the code to start the server for the playlist agent."""

from dialoguekit.platforms import FlaskSocketPlatform

from musicCRS.backend.playlist_agent import PlaylistAgent

if __name__ == "__main__":
    # Just like the backend, we create a FlaskSocketPlatform instance and start it
    # with the PlaylistAgent class.
    platform = FlaskSocketPlatform(PlaylistAgent)
    platform.start()
