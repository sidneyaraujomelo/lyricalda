from http import client
from flask import Flask
from lda import run_lda
import lyricsgenius

app = Flask(__name__)

token = open("token.txt", "r+").read()
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

@app.route("/album/<id>")
def get_album(id):
    album = genius.album(id)['album']
    tracks = genius.album_tracks(id)['tracks']
    data = {
        "album_name" : album['name'],
        "album_artist" : album['artist']['name'],
        "album_id" : id,
        "album_cover" : album['cover_art_thumbnail_url'],
        "songs" : []
    }
    lyrics = []
    titles = []
    for i, track in enumerate(tracks):
        song_id = track['song']['id']
        song_title = track['song']['title']
        song_lyrics = genius.lyrics(song_id, remove_section_headers=True)
        if song_lyrics is None:
            song_lyrics =  ''
        data["songs"].append({
            'id' : song_id,
            'title' : song_title,
            'lyrics' : song_lyrics
        })
        lyrics.append(song_lyrics)
        titles.append(song_title)
    topic_data = run_lda(titles, lyrics, 3)
    data["topics"] = topic_data[0]
    for i, _ in enumerate(data["topics"]):
        data["topics"][i]["songs"] = []
    print(topic_data[1])
    for inference in topic_data[1]:
        inf_name = list(inference.keys())[0]
        best_topic = inference[inf_name][0][0]
        data["topics"][best_topic]["songs"].append(inf_name)
    return data

if __name__ == "__main__":
    app.run(debug=True)