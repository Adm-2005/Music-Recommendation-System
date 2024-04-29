import pickle
from flask import Flask, render_template

albums_top50 = pickle.load(open('pickle_files/albums_top50.pkl', 'rb'))
artists_top50 = pickle.load(open('pickle_files/artists_top50.pkl', 'rb'))
tracks_top50 = pickle.load(open('pickle_files/tracks_top50.pkl', 'rb'))
genres_top50 = pickle.load(open('pickle_files/genres_top50.pkl', 'rb'))
similarity_score = pickle.load(open('pickle_files/similarity_score.pkl', 'rb'))
df = pickle.load(open('pickle_files/df.pkl', 'rb'))

def recommend(track_name, similarity_score, df, top_n=5):
    data = []
    track_indices = df[df['track_name'] == track_name].index
    track_idx = track_indices[0] if len(track_indices) > 0 else None
    if track_idx is not None:
        sim_scores = list(enumerate(similarity_score[track_idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        # Here we exclude the track itself, since it will have similarity score of 1 and will be at index 0
        sim_scores = sim_scores[1:top_n+1] 
        track_indices = [x[0] for x in sim_scores]
        for index in track_indices:
            item = [
                df.loc[index, 'track_name'],
                df.loc[index, 'artists'],
                df.loc[index, 'album_name'],
                df.loc[index, 'track_genre']
            ]
            data.append(item)
    return data

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)