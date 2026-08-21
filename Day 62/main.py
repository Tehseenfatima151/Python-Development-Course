import csv
import os
from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
from forms import CafeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = "8BYkEfBA6O6donzWlSihBXox7C0sKR6b"  # use a real secret in production (env var)
Bootstrap5(app)

CSV_FILE = "cafe-data.csv"


@app.route("/")
def home():
    return render_template("cafes.html", cafes=read_cafes())


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        # Write a new row to the CSV file
        file_exists = os.path.isfile(CSV_FILE)
        with open(CSV_FILE, mode="a", newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            if not file_exists:
                writer.writerow(["Cafe Name", "Location", "Open", "Close",
                                  "Coffee Rating", "Wifi Rating", "Power Rating"])
            writer.writerow([
                form.cafe.data,
                form.location.data,
                form.open_time.data,
                form.close_time.data,
                form.coffee_rating.data,
                form.wifi_rating.data,
                form.power_rating.data
            ])
        return redirect(url_for('home'))
    return render_template('add.html', form=form)


def read_cafes():
    if not os.path.isfile(CSV_FILE):
        return []
    with open(CSV_FILE, newline='', encoding='utf-8') as csv_file:
        return list(csv.reader(csv_file))[1:]  # skip header row


if __name__ == '__main__':
    app.run(debug=True)