from flask import (Flask, redirect, render_template, request)
app = Flask(__name__)


#I'm Jon
#im gat
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search_list", methods=["POST"])
def search_list():
    restaurant_name = request.form["restaurant_name"]
    label = f" {restaurant_name}"
    return render_template("search_list.html", content = label)


if __name__ == "__main__":
    app.run()
