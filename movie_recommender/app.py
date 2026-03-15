from flask import Flask, render_template, request
from recommender import recommend

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def home():

    movies = []
    searched_movie = ""
    matched_movie = ""

    if request.method == "POST":

        searched_movie = request.form["movie"]

        movies, matched_movie = recommend(searched_movie)

    return render_template(
        "index.html",
        movies=movies,
        searched_movie=searched_movie,
        matched_movie=matched_movie
    )


if __name__ == "__main__":
    app.run(debug=True)