"""Simplest possible agent that parrots back everything the user says."""

import os
import random
import sqlite3

import requests
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.agent import Agent
from dialoguekit.participant.participant import DialogueParticipant

from backend import parsing
from data.database_manager import DatabaseManager


def connect_db():
    return sqlite3.connect("../data/final_database.db")


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
        db_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/final_database.db")
        )
        self.dbmanager = DatabaseManager(db_path)

        self.commands_not_utilized = [
            "add",
            "delete",
            "view",
            "clear",
            "help",
            "Q1",
            "Q2",
            "Q3",
            "Q4",
            "Q5",
            "Q6",
        ]
        self.counter = 1
        self.command_mappings = {
            "add": "Did you know you can add a song to the playlist by typing '/add <song_name>' or '/add <song_name> by <artist>' or '/add <artist> : <song_name>'?",
            "delete": "Did you know you can delete a song from the playlist by typing '/delete <song_name>'?",
            "view": "Did you know you can view the current playlist by typing '/view'?",
            "clear": "Did you know you can clear the playlist by typing '/clear'?",
            "help": "Did you know you can see all the available commands by typing '/help'?",
            "Q1": "Did you know you can ask me when an album was released by typing 'When was album X released?'?",
            "Q2": "Did you know you can ask me how many albums an artist has released by typing 'How many albums has artist Y released?'?",
            "Q3": "Did you know you can ask me which album features a song by typing 'Which album features song X?'?",
            "Q4": "Did you know you can ask me how many songs an album contains by typing 'How many songs does album X contain?'?",
            "Q5": "Did you know you can ask me how long an album is by typing 'How long is album X?'?",
            "Q6": "Did you know you can ask me the most popular song by an artist by typing 'What is the most popular song by artist Y?'?",
        }

    def find_song_in_db(self, song_title, artist=None):
        """Find a song in the database."""
        conn = connect_db()
        cursor = conn.cursor()

        if artist:
            cursor.execute(
                "SELECT * FROM music WHERE track_name=? AND artists LIKE ?",
                (song_title, f"%{artist}%"),
            )
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
            song_title = command[separator_pos + separator_len :].strip()
        else:
            # Se 'titolo by artista'
            song_title = command[:separator_pos].strip()
            artist = command[separator_pos + separator_len :].strip()

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

    def suggest_command_not_utilized(self):
        """TODO"""
        if self.counter % 5 == 0:
            # Send a suggestion

            pick = random.choice(self.commands_not_utilized)
            suggestion = AnnotatedUtterance(
                self.command_mappings[pick],
                participant=DialogueParticipant.AGENT,
            )
            self._dialogue_connector.register_agent_utterance(suggestion)

    def add_song(self, command) -> None:
        # Estrai il titolo e l'artista dal comando usando la funzione parse_command
        song_title, artist = self.parse_command(command)

        song, equal_songs = self.dbmanager.find_song_by_title_and_artist(
            song_title, artist
        )
        if song:
            song_name = song.track_name
        else:
            song_name = song_title

        if song:
            song_data = song.serialize()

            # Invia la richiesta POST al server Flask
            url = "http://localhost:5002/add_song"
            response = requests.post(url, json=song_data)

            if response.status_code == 401:
                utterance = AnnotatedUtterance(
                    f"The song {song} is already in the playlist",
                    participant=DialogueParticipant.AGENT,
                )
                self._dialogue_connector.register_agent_utterance(utterance)
                return
            elif response.status_code != 201:
                print(f"Error: {response.status_code}")
                return

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

        url = "http://localhost:5002/songs_string"

        # Invia la richiesta GET
        response = requests.get(url)

        utterance = AnnotatedUtterance(
            f"Here is the current playlist: {response.text}",
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(utterance)

    def delete_song(self, song_name: str) -> None:
        # URL dell'endpoint
        url = "http://localhost:5002/delete_song"

        # Crea il payload JSON con il nome della canzone
        delete_data = {"track_name": song_name}

        response = requests.delete(url, json=delete_data)
        if response.status_code == 200:
            utterance = AnnotatedUtterance(
                f"The song {song_name}  has been removed from the playlist",
                participant=DialogueParticipant.AGENT,
            )
        elif response.status_code == 401:
            utterance = AnnotatedUtterance(
                f"The song {song_name} is not in the playlist",
                participant=DialogueParticipant.AGENT,
            )
        self._dialogue_connector.register_agent_utterance(utterance)

    def clear_playlist(self) -> None:
        """Deletes the current playlist."""
        # URL dell'endpoint per cancellare tutte le canzoni
        url = "http://localhost:5002/clear_playlist"

        # Invia la richiesta DELETE per svuotare la playlist
        response = requests.delete(url)

        if response.status_code == 200:
            utterance = AnnotatedUtterance(
                "The playlist is now empty!",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                "Error: The playlist could not be cleared",
                participant=DialogueParticipant.AGENT,
            )
        self._dialogue_connector.register_agent_utterance(utterance)

    # ---- Question handling ----

    def find_album_release_date(self, album_name: str) -> None:
        """Finds the release date of an album.

        Is used for the question "When was album X released?".

        Args:
            album_name: Album name.
        """
        # Get the release date of the album from the db
        release_date = self.dbmanager.find_album_release_date(album_name)

        if release_date:
            # Parse the date
            month, year = parsing.helper_parse_release_date(release_date)

            utterance = AnnotatedUtterance(
                f"The album {album_name} was released in {month} {year}",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                f"Sorry, I couldn't find the album {album_name}",
                participant=DialogueParticipant.AGENT,
            )
        self.dialogue_connector.register_agent_utterance(utterance)

    def find_number_of_albums_by_artist(self, artist_name: str) -> None:
        """Finds the number of albums by an artist.

        Is used for the question "How many albums has artist Y released?".

        Args:
            artist_name: Artist name.
        """
        # Get the number of albums by the artist from the db
        num_albums = self.dbmanager.number_of_albums_by_artist(artist_name)

        if num_albums:
            utterance = AnnotatedUtterance(
                f"{artist_name} has released {num_albums} albums.",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                f"Sorry, I couldn't find any albums by {artist_name}.",
                participant=DialogueParticipant.AGENT,
            )
        self.dialogue_connector.register_agent_utterance(utterance)

    def find_album_for_song(self, song_title: str) -> None:
        """Finds the album which contains a song.

        Is used for the question "Which album features song X?".

        Args:
            song_title: Song title.
        """
        # Get the album from the db
        album_name, artist_name = self.dbmanager.album_for_song(song_title)

        if album_name:
            utterance = AnnotatedUtterance(
                f"The album that features the song {song_title} is {album_name} by {artist_name}",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                f"Sorry, I couldn't find the album for the song {song_title}",
                participant=DialogueParticipant.AGENT,
            )
        self.dialogue_connector.register_agent_utterance(utterance)

    def how_many_songs_on_album(self, album_name: str) -> None:
        """Finds the number of songs on an album.

        Is used for the question "How many songs does album X contain?".

        Args:
            album_name: Album name.
        """
        # Get the number of songs on the album from the db
        num_songs = self.dbmanager.number_of_songs_on_album(album_name)

        if num_songs:
            utterance = AnnotatedUtterance(
                f"The album {album_name} contains {num_songs} songs.",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                f"Sorry, I couldn't find the album {album_name}",
                participant=DialogueParticipant.AGENT,
            )
        self.dialogue_connector.register_agent_utterance(utterance)

    def how_long_is_album(self, album_name: str) -> None:
        """Finds the duration of an album.

        Is used for the question "How long is album X?".

        Args:
            album_name: Album name.
        """
        duration_album = self.dbmanager.duration_of_album(album_name)

        if duration_album:
            utterance = AnnotatedUtterance(
                f"The album {album_name} lasts {parsing.helper_convert_seconds_to_minutes(duration_album)} minutes.",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                f"Sorry, I couldn't find the album {album_name}",
                participant=DialogueParticipant.AGENT,
            )
        self.dialogue_connector.register_agent_utterance(utterance)

    def most_popular_song_by_artist(self, artist_name: str) -> None:
        """Finds the most popular song by an artist.

        Args:
            artist_name: Artist name.
        """
        most_popular_song = self.dbmanager.most_popular_song_by_artist(artist_name)

        if most_popular_song:
            utterance = AnnotatedUtterance(
                f"The most popular song by {artist_name} is {most_popular_song}",
                participant=DialogueParticipant.AGENT,
            )
        else:
            utterance = AnnotatedUtterance(
                f"Sorry, I couldn't find any songs by {artist_name}",
                participant=DialogueParticipant.AGENT,
            )
        self.dialogue_connector.register_agent_utterance(utterance)

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
            self.counter += 1
            if "add" in self.commands_not_utilized:
                self.commands_not_utilized.remove("add")
            if len(self.separate_utterance(utterance.text)) < 2:
                utterance = AnnotatedUtterance(
                    "Please provide the name of the song you want to add",
                    participant=DialogueParticipant.AGENT,
                )
                self._dialogue_connector.register_agent_utterance(utterance)
                self.suggest_command_not_utilized()
                return
            self.add_song(self.separate_utterance(utterance.text)[1])
            self.suggest_command_not_utilized()
            return

        if self.separate_utterance(utterance.text)[0] == "/view":
            self.counter += 1
            if "view" in self.commands_not_utilized:
                self.commands_not_utilized.remove("view")
            self.view_playlist()
            self.suggest_command_not_utilized()
            return

        if self.separate_utterance(utterance.text)[0] == "/clear":
            self.counter += 1
            if "clear" in self.commands_not_utilized:
                self.commands_not_utilized.remove("clear")
            self.clear_playlist()
            self.suggest_command_not_utilized()
            return

        if self.separate_utterance(utterance.text)[0] == "/delete":
            self.counter += 1
            if "delete" in self.commands_not_utilized:
                self.commands_not_utilized.remove("delete")
            if len(self.separate_utterance(utterance.text)) < 2:
                utterance = AnnotatedUtterance(
                    "Please provide the name of the song you want to delete",
                    participant=DialogueParticipant.AGENT,
                )
                self._dialogue_connector.register_agent_utterance(utterance)
                self.suggest_command_not_utilized()
                return
            self.delete_song(self.separate_utterance(utterance.text)[1])
            self.suggest_command_not_utilized()
            return

        if self.separate_utterance(utterance.text)[0] == "/help":
            self.counter += 1
            if "help" in self.commands_not_utilized:
                self.commands_not_utilized.remove("help")
            self.welcome()
            self.suggest_command_not_utilized()
            return

        # ---- Handle questions ----
        if "When was album" in utterance.text:  # A bit hard-coded but works for now
            self.counter += 1
            if "Q1" in self.commands_not_utilized:
                self.commands_not_utilized.remove("Q1")
            album_name = parsing.extract_album_from_question(utterance.text)
            if album_name:
                self.find_album_release_date(album_name)
                self.suggest_command_not_utilized()
                return
            # Tell user album does not exist
            response = AnnotatedUtterance(
                f"Sorry, I couldn't find the album {album_name} in the database",
                participant=DialogueParticipant.AGENT,
            )
            self.dialogue_connector.register_agent_utterance(response)

        if "How many albums has artist" in utterance.text:
            self.counter += 1
            if "Q2" in self.commands_not_utilized:
                self.commands_not_utilized.remove("Q2")
            artist_name = parsing.extract_artist_from_question(utterance.text)
            if artist_name:
                self.find_number_of_albums_by_artist(artist_name)
                self.suggest_command_not_utilized()
                return
            # Tell user artist does not exist
            response = AnnotatedUtterance(
                f"Sorry, I couldn't find any albums by {artist_name}",
                participant=DialogueParticipant.AGENT,
            )
            self.dialogue_connector.register_agent_utterance(response)

        if "Which album features song" in utterance.text:
            self.counter += 1
            if "Q3" in self.commands_not_utilized:
                self.commands_not_utilized.remove("Q3")
            song_name = parsing.extract_song_from_question_for_album(utterance.text)
            if song_name:
                self.find_album_for_song(song_name)
                self.suggest_command_not_utilized()
                return
            # Tell user song does not exist
            response = AnnotatedUtterance(
                f"Sorry, I couldn't find the album for the song {song_name}",
                participant=DialogueParticipant.AGENT,
            )
            self.dialogue_connector.register_agent_utterance(response)

        if "How many songs does album" in utterance.text:
            self.counter += 1
            if "Q4" in self.commands_not_utilized:
                self.commands_not_utilized.remove("Q4")
            album_name = parsing.extract_num_songs_on_album(utterance.text)
            if album_name:
                self.how_many_songs_on_album(album_name)
                self.suggest_command_not_utilized()
                return
            # Tell user album does not exist
            response = AnnotatedUtterance(
                f"Sorry, I couldn't find the album {album_name}",
                participant=DialogueParticipant.AGENT,
            )
            self.dialogue_connector.register_agent_utterance(response)

        if "How long is album" in utterance.text:
            self.counter += 1
            if "Q5" in self.commands_not_utilized:
                self.commands_not_utilized.remove("Q5")
            album_name = parsing.extract_album_name_for_duration(utterance.text)
            if album_name:
                self.how_long_is_album(album_name)
                self.suggest_command_not_utilized()
                return
            # Tell user album does not exist
            response = AnnotatedUtterance(
                f"Sorry, I couldn't find the album {album_name}",
                participant=DialogueParticipant.AGENT,
            )
            self.dialogue_connector.register_agent_utterance(response)

        if "What is the most popular song by" in utterance.text:
            self.counter += 1
            if "Q6" in self.commands_not_utilized:
                self.commands_not_utilized.remove("Q6")
            artist_name = parsing.extract_artist_for_most_popular_song(utterance.text)
            if artist_name:
                self.most_popular_song_by_artist(artist_name)
                self.suggest_command_not_utilized()
                return
            # Tell user artist does not exist
            response = AnnotatedUtterance(
                f"Sorry, I couldn't find any songs by {artist_name}",
                participant=DialogueParticipant.AGENT,
            )
            self.dialogue_connector.register_agent_utterance(response)

        response = AnnotatedUtterance(
            "(Parroting) " + utterance.text,
            participant=DialogueParticipant.AGENT,
        )
        self._dialogue_connector.register_agent_utterance(response)
