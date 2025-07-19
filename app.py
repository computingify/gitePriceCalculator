
from flask import Flask, render_template, request
from utils import calculate_price

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    people = int(request.form["people"])

    result = calculate_price(start_date, end_date, people)
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
