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
        self,
        profile: UserProfile,
        id,
        user_type=UserType.SIMULATOR,
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
        self.turns = 0
        self.max_turns = 10  # stopping criterion
        self._goal_met = False

    def _generate_response(self) -> AnnotatedUtterance:
        """Generates a response.

        Returns:
            Annotated utterance.
        """
        if self._goal_met or self.turns > = self.max_turns:
            return AnnotatedUtterance("/exit", participant=DialogueParticipant.USER)

        # Randomly select a command
        command = self._choose_command()

        self.turns += 1
        return AnnotatedUtterance(command, participant=DialogueParticipant.USER)

    def _choose_command(self) -> str:
        options = ["/add", "/view", "/recommend"] # TODO: Add questions

        choice = random.choice(options)

        if choice == "/add":
            pass
        elif choice == "/view":
            pass
        elif choice == "/recommend":
            pass
        # TODO: Add questions also here

        return "/exit"

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        # TODO: Check if it is answering to the view
        # * count number of songs
        # * save it somewhere
        # ? How can we detect if playlist is in line with the goal??
        # TODO: Detect if multiple songs are recommended

        pass
