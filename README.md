# musicCRS - A Music Recommender Sytem

![Static Badge](https://img.shields.io/badge/code_style-black-black)
![Static Badge](https://img.shields.io/badge/python-3.9-blue)

musicCRS is a chat-based music recommender system that can help you build playlists and get recommendations for songs.
We built it as part of the project for the course DAT640 Information Retrieval and Text Mining at Universitetet i Stavanger (UiS) in the autumn semester of 2024.

## Installation

### Dependencies

To install the dependencies use pip and the following command.

```bash
pip install -r requirements.txt
```

Further (development) dependencies can be found in `requirements.dev.txt`.

### Database

The musicCRS system needs a database to function.
We based the database on this [dataset](https://www.kaggle.com/datasets/tonygordonjr/spotify-dataset-2023?select=spotify_data_12_20_2023.csv) from Kaggle.
We will add a way to install the database here in the future.

### LLM

To use the natural language capabilities of the system, a local Llama 3.2 model is needed.
It can be run via [Ollama](https://ollama.com/).

## Usage

To use the musicCRS, run the follwoing steps

  1. Make sure Ollama is running on your system.
  2. Run the bot server with `python -m musicCRS.backend.run_agent` (from the root directory).
  3. Run the backend server with `python -m musicCRS.backend.app` (from the root directory).
  4. Open the `frontend/index.html` file in a browser. Now you can use the bot.

## Contributors

  * [Marco Bologna](https://github.com/MarcoBolo001)
  * [Ole Seifert](https://github.com/OleSeifert)
