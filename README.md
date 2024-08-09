# Spotify statistics generator.
_See how your taste in music has changed over the years through graphs!_

Based on the following parameters:
- Popularity
- Danceability
- Energy
- Key
- Loudness
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Valence
- Tempo
- Duration (Milliseconds)

### How to use:

1) First, star and clone this repository (Please 🥹):

```
git clone https://github.com/willnaoosmith/Spotify-statistics-generator.git
```

2) Install the requirements:

```
cd Spotify-statistics-generator && pip install -r requirements.txt
```

3) Set up your spotify integration (You can see more about it on the [Spotify docs](https://developer.spotify.com/documentation/web-api)):

```python
spotifyClient = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
    client_id="Your client ID here",
    client_secret="Your client secret here",
    redirect_uri="Your redirect URI here",
    scope="Your app scope here"
  )
)
```


4) Run the script and follow the instructions provided:

```
python main.py
```
