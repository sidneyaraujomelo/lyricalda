from http import client
from flask import Flask
import lyricsgenius

app = Flask(__name__)

token="Zxn7Q9TdWN2zG7w7i77_nAxnOTEZ9_ZDlPE_rO2xkp2Mu-M0Dyc_BW0FCtZy7Ea4"
genius = lyricsgenius.Genius(token)

artist_id = 32137

@app.route("/members")
def members():
    artist_data = genius.artist(artist_id)['artist']
    artist_albums = genius.artist_albums(artist_id)['albums']
    albums = []
    for artist_album in artist_albums:
        albums.append(
            {
                "id" : artist_album["id"],
                "name" : artist_album["name"],
                "image_url" : artist_album["cover_art_url"]
            }
        )
    return {
        "artist" : {
            "id" : artist_data["id"],
            "name" : artist_data["name"],
            "image_url" : artist_data["image_url"],
            "albums" : albums
        }
    }

if __name__ == "__main__":
    app.run(debug=True)