from dialoguekit.platforms import FlaskSocketPlatform
from sample_agents.parrot_agent import ParrotAgent
from playlist_agent import PlaylistAgent

platform = FlaskSocketPlatform(PlaylistAgent)
platform.start()
