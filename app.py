
from flask import Flask, render_template, request
from utils import calculate_price
from types import SimpleNamespace

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/calculate", methods=["POST"])
def calculate():

    people = SimpleNamespace()
    print("Request", request.form)
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    people.adult = int(request.form["adult"])
    people.children = int(request.form["children"])
    people.baby = int(request.form["baby"])
    isInsurence = request.form.get("insurance", "off") == "on"

    result = calculate_price(start_date, end_date, people, isInsurence)
    #print(f"Result: {result}")
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
