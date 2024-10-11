from dialoguekit.platforms import FlaskSocketPlatform
from playlist_agent import PlaylistAgent

# Just like the backend, we create a FlaskSocketPlatform instance and start it
# with the PlaylistAgent class.
platform = FlaskSocketPlatform(PlaylistAgent)
platform.start()
