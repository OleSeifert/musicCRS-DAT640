"""Contains mappings for the playlist recommendation system.

The mappings are used to convert the user's preferences into a format that can
be used to query the database.
"""

DANCEABILITY_MAPPING = {"low": [0, 0.33], "mid": [0.33, 0.66], "high": [0.66, 1]}

ENERGY_MAPPING = {"low": [0, 0.33], "mid": [0.33, 0.66], "high": [0.66, 1]}

VALENCE_MAPPING = {"low": [0, 0.33], "mid": [0.33, 0.66], "high": [0.66, 1]}

TEMPO_MAPPING = {"low": [0, 100], "mid": [100, 140], "high": [140, 200]}
