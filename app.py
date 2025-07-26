
from flask import Flask, render_template, request
from utils import calculate_price
from types import SimpleNamespace
import calendar_ical

app = Flask(__name__)

@app.route("/")
def index():
    #f"https://www.airbnb.fr/calendar/ical/{AIRBNB_ID}.ics?s={AIRBNB_TOKEN}"
    cal = calendar_ical.CalendarIcal("https://www.airbnb.fr/calendar/ical/1398287456607254737.ics?s=f7fa0dbdb6ae6606d5d25ad8c12e320c")
    reserved_dates = cal.get_reserved_dates()
    return render_template("index.html", reserved_dates=reserved_dates)

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
    isExtraAccess = request.form.get("extraAccess", "off") == "on"

    result = calculate_price(start_date, end_date, people, isInsurence, isExtraAccess)
    #print(f"Result: {result}")
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
