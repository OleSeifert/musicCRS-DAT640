"""Simplest possible agent that parrots back everything the user says."""

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant


class PlaylistAgent(Agent):
    """Represents a playlist agent."""

    def __init__(self, agent_id: str):
        """Playlist agent.

        This agent is used to manage a playlist.
        To end the conversation the user has to say `/exit`.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            """Hello, I'm Playlist agent, I can help you with your music playlist.
             \nYou can add a song to the playlist by typing '/add <song_name>'
               \nYou can view the current playlist by typing '/view'
                 \nYou can clear the playlist by typing '/clear'
                  \nYou can exit the conversation by typing '/exit' """,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def goodbye(self) -> None:
        """Sends the agent's goodbye message."""
        utterance = AnnotatedUtterance(
            "It was nice talking to you. Bye",
            intent=self.stop_intent,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def separate_utterance(self, text: str) -> list[str]:
        """Separates the utterance into command and argument.

        Args:
            text: User utterance.

        Returns:
            List containing the command and argument.
        """
        return text.split(" ", maxsplit=1)

    def add_song(self, song: str) -> None:
        """Adds a song to the playlist.

        Args:
            song: Song to be added to the playlist.
        """
        with open("../data/playlist.txt", "a", encoding="utf-8") as file:
            file.write(song + "\n")

        utterance = AnnotatedUtterance(
            f"The song {song} is now added to the playlist!",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def view_playlist(self) -> None:
        """Shows the current playlist."""
        with open("../data/playlist.txt", "r", encoding="utf-8") as file:
            playlist = file.readlines()
            playlist = [song.strip() for song in playlist]

        utterance = AnnotatedUtterance(
            f"Here is the current playlist: {playlist}",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def delete_playlist(self) -> None:
        """Deletes the current playlist."""
        with open("../data/playlist.txt", "w", encoding="utf-8") as file:
            file.write("")
        utterance = AnnotatedUtterance(
            "The playlist is now empty!",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new user utterance.

        If the received message is "/exit" it will close the conversation.

        Args:
            utterance: User utterance.
        """
        if self.separate_utterance(utterance.text)[0] == "/exit":
            self.goodbye()
            return

        if self.separate_utterance(utterance.text)[0] == "/add":
            self.add_song(self.separate_utterance(utterance.text)[1])
            return

        if self.separate_utterance(utterance.text)[0] == "/view":
            self.view_playlist()
            return

        if self.separate_utterance(utterance.text)[0] == "/clear":
            self.delete_playlist()
            return

        if self.separate_utterance(utterance.text)[0] == "/help":
            self.welcome()
            return

        response = AnnotatedUtterance(
            "(Parroting) " + utterance.text,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)
