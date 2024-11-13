"""Advanced user simulator that simply requests songs."""

import random

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
        self._goal_met = False
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
        options = ["/add"]
        # options = ["/add", "/view", "/recommend"]  # TODO: Add questions

        if self.turns >= self.max_turns or self._num_songs == 10:
            return "/exit"

        if not self.songs_to_add:
            options.remove("/add")

        choice = random.choice(options)
        self.last_command = choice

        if choice == "/add":
            self.last_command = "/add " + random.choice(self.songs_to_add)
            return "/add " + random.choice(self.songs_to_add)

        elif choice == "/view":
            return "/view"
        elif choice == "/recommend":
            return "/recommend"
        # TODO: Add questions also here

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        if self.last_command.startswith("/add"):
            if "Please select one in the suggestions list" in utterance.text:
                # call endpoint
                pass
            else:
                song = self.last_command.split(" ", maxsplit=1)[1]
                print(song)
                print(self.songs_to_add)
                if song in self.songs_to_add:
                    self.songs_to_add.remove(song)
                    print(self.songs_to_add)
        elif self.last_command == "/view":
            self._num_songs = len(utterance.text.split("//"))
        elif self.last_command == "/recommend":
            # call endpoint to select 1 song
            pass

        # ? How can we detect if playlist is in line with the goal??
        # TODO: Detect if multiple songs are recommended

        response = self._generate_response()
        self._dialogue_connector.register_user_utterance(response)
