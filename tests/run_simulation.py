"""Command line tool to run simulations with the MusicCRS agent."""

import argparse
import logging

from frontend import playlist_agent  # TODO: update accordingly
from tests.advanced_user_simulator import AdvancedUserSimulator
from tests.naive_user_simulator import NaiveUserSimulator
from tests.simulation_platform import SimulationPlatform
from tests.user_profile import UserProfile


def parse_args() -> argparse.Namespace:
    """Parses command-line arguments."""
    parser = argparse.ArgumentParser(description="Simulation.")
    parser.add_argument(
        "--num_simulations",
        type=int,
        default=1,
        help="Number of simulations to run. Defaults to 1.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    platform = SimulationPlatform(
        playlist_agent.PlaylistAgent
    )  # TODO: Update agent name
    logging.info(f"Running {args.num_simulations} simulations")

    User1 = UserProfile(
        id="User1",
        preferences=[
            "Vogue by Madonna",
            "cruel summer by Taylor Swift",
            "Lover by Taylor Swift",
        ],
        prefered_artists=["Madonna", "Taylor Swift"],
        prefered_songs=["Vogue", "Cruel Summer", "Lover"],
        goal=15,
    )

    User2 = UserProfile(
        id="User2",
        preferences=[
            "Let Down by Radiohead",
            "Karma Police by Radiohead",
            "With Or Without You by U2",
            "Africa by TOTO",
        ],
        prefered_artists=["Radiohead", "TOTO", "U2"],
        prefered_songs=["Let Down", "Karma Police", "Africa", "With Or Without You"],
        goal=10,
    )

    User3 = UserProfile(
        id="User3",
        preferences=[
            "Thriller by Michael Jackson",
            "Billie Jean by Micheal Jackson",
            "home by depeche mode",
        ],
        prefered_artists=["Michael Jackson", "depeche mode"],
        prefered_songs=["Thriller", "Billie Jean", "home"],
        goal=7,
    )

    for i in range(1, args.num_simulations + 1):
        # Note: This creates a new agent each time to avoid state issues.
        # Ideally, platform.start() could be called outside the loop, but then # the agent needs to be reset between simulations.
        platform.start()
        print(f"\n--- Staring simulation {i} ---\n")

        platform.connect(f"SimulatedUser{i}", AdvancedUserSimulator, {"profile": User1})

        platform.disconnect(f"SimulatedUser{i}")
        print(f"\n--- Finished simulation {i} ---\n")
    logging.info("All simulations finished")
