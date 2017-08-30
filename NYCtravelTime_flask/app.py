from flask import Flask, url_for, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import taxi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    "Home Session"
    output = []
    loc = []
    dt = []
    if request.method == 'GET':
        return render_template("home.html", output=output, loc=loc, dt=dt)
    else:
        address_orig = request.form['address_orig']
        address_dest = request.form['address_dest']
        day = request.form['day']
        time = request.form['time']
        output = taxi.get_duration(
            address_orig, address_dest, day, time, txt=True)
        loc = [taxi.get_address(address_orig), taxi.get_address(address_dest)]
        dt = taxi.day_time(day, time)
    return render_template('home.html', output=output, loc=loc, dt=dt)


if __name__ == '__main__':
    app.debug = True
    db.create_all()
    app.secret_key = "123"
    app.run(host='0.0.0.0')
