"""Naive user simulator that simply requests a fixed list of songs."""

from dialoguekit.core.annotated_utterance import AnnotatedUtterance
from dialoguekit.core.utterance import Utterance
from dialoguekit.participant.participant import DialogueParticipant
from dialoguekit.participant.user import User, UserType

_SONGS = [f"song{i} by artist{i}" for i in range(1,6)]
_COMMAND = "/add [song]"


class NaiveUserSimulator(User):
    def __init__(
        self,
        id,
        user_type=UserType.SIMULATOR,
    ) -> None:
        """Initializes the naive user simulator.

        Args:
            id: User ID.
            user_type: User type. Defaults to UserType.SIMULATOR.
        """
        super().__init__(id, user_type)
        self._num_songs = 0

    def _generate_response(self) -> AnnotatedUtterance:
        """Generates a response.

        Returns:
            Annotated utterance.
        """
        if self._num_songs < len(_SONGS):
            self._num_songs += 1
            utterance = _COMMAND.replace("[song]", _SONGS[self._num_songs - 1])
        else:
            utterance = "/quit"     
        return AnnotatedUtterance(utterance,
                                  participant=DialogueParticipant.USER)

    def receive_utterance(self, utterance: Utterance) -> None:
        """Gets called every time there is a new agent utterance.

        Args:
            utterance: Agent utterance.
        """
        response = self._generate_response()
        self._dialogue_connector.register_user_utterance(response)
