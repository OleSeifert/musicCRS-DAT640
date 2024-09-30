"""Simplest possible agent that parrots back everything the user says."""

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant


class PlaylistAgent(Agent):
    def __init__(self, agent_id: str):
        """Parrot agent.

        This agent parrots back what the user utters.
        To end the conversation the user has to say `EXIT`.

        Args:
            agent_id: Agent id.
        """
        super().__init__(agent_id)

    def welcome(self) -> None:
        """Sends the agent's welcome message."""
        utterance = AnnotatedUtterance(
            '''Hello, I'm Playlist agent, I can help you with your music playlist. 
             \nYou can add a song to the playlist by typing '/add <song_name>'
               \nYou can view the current playlist by typing '/view'
                 \nYou can clear the playlist by typing '/clear' 
                  \nYou can exit the conversation by typing '/exit' ''',
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

    def separate_utterance(self, text):
        return text.split(" ", maxsplit=1)

    def add_song(self, song):
        with open("playlist.txt", "a") as file:
            file.write(song + "\n")

        utterance = AnnotatedUtterance(
            f"The song {song} is now added to the playlist!",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def view_playlist(self):
        with open("playlist.txt", "r") as file:
            playlist = file.readlines()
            playlist = [song.strip() for song in playlist]

        utterance = AnnotatedUtterance(
            f"Here is the current playlist: {playlist}",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def delete_playlist(self):
        with open("playlist.txt", "w") as file:
            file.write("")
        utterance = AnnotatedUtterance(
            f"The playlist is now empty!",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called each time there is a new user utterance.

        If the received message is "EXIT" it will close the conversation.

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
