import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
))

# Load your artist CSV (without IDs)
df = pd.read_csv("data/artists.csv")

# Empty list to store found Spotify IDs
spotify_ids = []

# For each artist, search and get Spotify ID
for artist in df["name"]:
    try:
        result = sp.search(q=artist, type="artist", limit=1)
        artist_id = result["artists"]["items"][0]["id"]
        print(f"✅ Found: {artist} → {artist_id}")
        spotify_ids.append(artist_id)
    except (IndexError, KeyError):
        print(f"❌ Could not find: {artist}")
        spotify_ids.append(None)

# Add new column and save
df["spotify_id"] = spotify_ids
df.to_csv("data/artists_with_ids.csv", index=False)
print("🎉 Saved: data/artists_with_ids.csv")
