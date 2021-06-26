from flask import Flask, redirect, url_for, render_template, request, flash
import requests
import base64
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recommended_albums.db'
db = SQLAlchemy(app)


class albums(db.Model):
    album_id = db.Column('id', db.Integer, primary_key=True)
    album_artist = db.Column('artist', db.Text())
    album_name = db.Column('name', db.Text())

    def __str__(self):
        return str(self.album_id) + '. ' + self.album_artist + "    by " + self.album_name


def getting_songs(name):
    url = "https://accounts.spotify.com/api/token"
    headers = {}
    data = {}

    clientSecret = "099bf37c94cf4fb489a04e881cfdf16a"
    clientId = "24b461a974084b09949f1b6312c40cbb"

    message = f"{clientId}:{clientSecret}"
    messageBytes = message.encode('ascii')
    base64Bytes = base64.b64encode(messageBytes)
    base64Message = base64Bytes.decode('ascii')

    headers['Authorization'] = f"Basic {base64Message}"
    data['grant_type'] = "client_credentials"
    r = requests.post(url, headers=headers, data=data)
    token = r.json()['access_token']

    search_url = f"https://api.spotify.com/v1/search?q={name}&type=track&limit=10"
    headers = {
        "Authorization": "Bearer " + token
    }

    res = requests.get(url=search_url, headers=headers)
    result = res.json()

    all_rows = []

    for track in result['tracks']['items']:
        row = (track['name'], track['album']['release_date'])
        all_rows.append(row)
    return all_rows


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/recommended')
def reccomend():
    all_albums = albums.query.all()
    flash("Top 50 best indie albums according to pitchfork")
    return render_template('recommended.html', all_albums=all_albums)

@app.route('/recommended/page=2')
def second_page():
    all_albums = albums.query.all()
    flash("Top 50 best indie albums according to pitchfork")
    return render_template('secondpage.html', all_albums=all_albums)

@app.route('/recommended/page=3')
def third_page():
    all_albums = albums.query.all()
    flash("Top 50 best indie albums according to pitchfork")
    return render_template('thirdpage.html', all_albums=all_albums)


@app.route('/about')
@app.route('/aboutus')
def about():
    return render_template('aboutpage.html')


@app.route('/success/<artist_name>', methods=['GET', 'POST'])
def success(artist_name):
    results = getting_songs(artist_name)
    flash("Top 10 most famous songs by " + artist_name + " right now.")
    return render_template('successful.html', results=results, artist_name=artist_name)


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        artist = request.form['artist']
        return redirect(url_for('success', artist_name=artist))
    return render_template('searchpage.html')


if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
