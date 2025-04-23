from flask import Flask, render_template, request, redirect
from datetime import datetime, timedelta
import sqlite3, csv

app = Flask(__name__)


def load_vegetables():
    veggies = []
    with open('veg.csv') as f:
        reader = csv.DictReader(f)
        for row in reader:
            veggies.append(row)
    return veggies


@app.route('/')
def index():
    veggies = load_vegetables()
    return render_template('index.html', veggies=veggies)


@app.route('/plant', methods=['POST'])
def plant():
    veg = request.form['vegetable']
    variety = request.form['variety']
    planting_date = datetime.strptime(request.form['planting_date'], '%Y-%m-%d')

    min_days = int(request.form['min_days'])
    max_days = int(request.form['max_days'])
    min_h = planting_date + timedelta(days=min_days)
    max_h = planting_date + timedelta(days=max_days)

    # Save to DB
    conn = sqlite3.connect('.venv/gardening.db')
    c = conn.cursor()
    c.execute('''INSERT INTO plantings (vegetable, variety, planting_date, min_harvest_date, max_harvest_date)
                 VALUES (?, ?, ?, ?, ?)''',
              (veg, variety, planting_date.date(), min_h.date(), max_h.date()))
    conn.commit()
    conn.close()

    return redirect('/plantings')


@app.route('/plantings')
def plantings():
    conn = sqlite3.connect('.venv/gardening.db')
    c = conn.cursor()
    c.execute("SELECT * FROM plantings")
    rows = c.fetchall()
    conn.close()
    return render_template('plantings.html', plantings=rows)


if __name__ == '__main__':
    app.run(debug=True)