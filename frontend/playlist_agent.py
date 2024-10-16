"""Simplest possible agent that parrots back everything the user says."""

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant
import sqlite3
import re

def connect_db():
    return sqlite3.connect('../data/final_database.db')


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

    def find_song_in_db(self, song_title, artist=None):
        """Find a song in the database."""
        conn = connect_db()
        cursor = conn.cursor()

        if artist:
            cursor.execute("SELECT * FROM music WHERE track_name=? AND artists LIKE ?", (song_title, f"%{artist}%"))
        else:
            cursor.execute("SELECT * FROM music WHERE track_name=?", (song_title,))

        result = cursor.fetchall()  # Prende tutte le occorrenze

        conn.close()

        if result:
            return result[0], len(result)  # Per ora prendiamo solo la prima
        else:
            return None, None

    def parse_command(self, command):
        """Parse il comando e separa artista e titolo, utilizzando i separatori ' : ' e ' by '."""
        command = command.strip()

        # Cerca l'ultimo separatore ' by ' o ' : '
        by_pos = command.lower().rfind(" by ")
        colon_pos = command.rfind(" : ")

        if by_pos == -1 and colon_pos == -1:
            # Se non ci sono separatori, considera solo il titolo della canzone
            return command, None

        # Usa il separatore che appare per ultimo
        if by_pos > colon_pos:
            separator_pos = by_pos
            separator_len = 4  # Lunghezza di " by "
            artist_first = False
        else:
            separator_pos = colon_pos
            separator_len = 3  # Lunghezza di " : "
            artist_first = True

        # Dividi la stringa in base al separatore trovato
        if artist_first:
            # Se 'artista : titolo'
            artist = command[:separator_pos].strip()
            song_title = command[separator_pos + separator_len:].strip()
        else:
            # Se 'titolo by artista'
            song_title = command[:separator_pos].strip()
            artist = command[separator_pos + separator_len:].strip()

        return song_title, artist

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


    def add_song(self, command) -> None:
        # Estrai il titolo e l'artista dal comando usando la funzione parse_command
        song_title, artist = self.parse_command(command)

        song, equal_songs = self.find_song_in_db(song_title, artist)
        if(song):
            song_name = song[16]
            artist = song[5]
        else:
            song_name = song_title

        if song:
            with open("../data/playlist.txt", "a", encoding="utf-8") as file:
                file.write(song_name +" by " + artist + "\n")

            if equal_songs > 1:
                utterance = AnnotatedUtterance(
                    f"I found {equal_songs} songs with the name {song_name}, I added my favourite one to the playlist, be more precise if you want one in particular!",
                    participant=DialogueParticipant.AGENT,
                )
            else:
                utterance = AnnotatedUtterance(
                    f"The song {song_title} is added to the playlist",
                    participant=DialogueParticipant.AGENT,
                )
            self._dialogue_connector.register_agent_utterance(utterance)
        else:
            utterance = AnnotatedUtterance(
                f"The song {song_name} is not in our Database",
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
