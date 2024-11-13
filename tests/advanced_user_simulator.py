"""Advanced user simulator that simply requests songs."""

import random

import requests
from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.participant import DialogueParticipant
from dialoguekit.participant.user import User, UserType

from tests.user_profile import UserProfile


class AdvancedUserSimulator(User):
    """Advanced user simulator that simply requests songs.

    Attributes:
        profile: User profile.
        turns: Number of turns.
        max_turns: Maximum number of turns.
        _goal_met: Whether the goal is met.
    """

    def __init__(
        self, id, user_type=UserType.SIMULATOR, profile: UserProfile = None
    ) -> None:
        """Initializes the advanced user simulator.

        Args:
            user_profile: User profile.
            id: User ID.
            user_type: User type. Defaults to UserType.SIMULATOR.
        """
        super().__init__(id, user_type)
        self._num_songs = 0
        self.profile = profile
        self.songs_to_add = self.profile.preferences
        self.turns = 0
        self.max_turns = 20  # stopping criterion
        self.goal_songs_number = self.profile.goal
        self.last_command = ""

    def _generate_response(self) -> AnnotatedUtterance:
        """Generates a response.

        Returns:
            Annotated utterance.
        """

        # Randomly select a command
        utterance = self._choose_command()

        self.turns += 1
        return AnnotatedUtterance(utterance, participant=DialogueParticipant.USER)

    def _choose_command(self) -> str:
        """Chooses a command and a user preference.

        Returns:
            A string witht the command.
        """
        # options = ["/add"]
        options = [
            "/add",
            "/view",
            "/recommend",
            "Q1",
            "Q2",
            "Q3",
        ]

        if self.last_command == "/view":
            options.remove("/view")
        else:
            if "/view" not in options:
                options.append("/view")

        if self.turns >= self.max_turns or self._num_songs == self.goal_songs_number:
            self.last_command = "/exit"
            return "/exit"

        if not self.songs_to_add:
            options.remove("/add")

        choice = random.choice(options)
        self.last_command = choice

        if choice == "/add":
            self.last_command = "/add " + random.choice(self.songs_to_add)
            return self.last_command

        elif choice == "/view":
            return "/view"
        elif choice == "/recommend":
            return "/recommend"
        elif choice == "Q1":
            return f"How many albums has artist {random.choice(self.profile.prefered_artists)} released?"
        elif choice == "Q2":
            return f"Which album features song {random.choice(self.profile.prefered_songs)}?"
        elif choice == "Q3":
            return f"What is the most popular song by artist {random.choice(self.profile.prefered_artists)}?"
        else:
            return "/exit"

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        if self.last_command.startswith("/add"):
            if "Please select one in the suggestions list" in utterance.text:
                # call endpoint
                response = requests.get("http://localhost:5002/move_first_to_playlist")
                print(
                    "***Simulating User choosing one song from the suggestions list***"
                )
                if response.status_code == 200:
                    print("***Song added to playlist***")

            song = self.last_command.split(" ", maxsplit=1)[1]
            if song in self.songs_to_add:
                self.songs_to_add.remove(song)

        elif self.last_command == "/view":
            self._num_songs = len(utterance.text.split("//"))
        elif self.last_command == "/recommend":
            # call endpoint to select 1 song
            response = requests.post(
                "http://localhost:5002/move_recommendation",
                json={"artists": self.profile.prefered_artists},
            )


            if response.status_code == 200:
                songs = response.json().get("songs", "")
                for song in songs:
                    print(
                        "***Simulating User choosing one song from the recommendations list***"
                    )
                    print(
                        f"***Song {song} added to playlist based on user preferences***"
                    )
            else:
                print("***No recommendations available***")

        response = self._generate_response()
        self._dialogue_connector.register_user_utterance(response)
