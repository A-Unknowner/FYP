from flask import (Flask, render_template, request)
from controller.poe_restaurant_review import acsa_result
import json

app = Flask(__name__)


# testing

@app.route("/")
def index():
    return render_template("index.html")


@app.route('/result', methods=['GET'])
def analyze_review():
    results = acsa_result()
    results_str = results.decode('utf-8')
    results_json = json.loads(results_str)  # Parse string as JSON
    return render_template('result.html', results=results_json)


@app.route("/search_list", methods=["POST"])
def search_list():
    restaurant_name = request.form["restaurant_name"]
    label = f" {restaurant_name}"
    return render_template("search_list.html", content=label)


# User Guide
@app.route("/guide")
def user_guide():
    return render_template("guide.html")


if __name__ == "__main__":
    app.run()
