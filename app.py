from flask import Flask, request, render_template, redirect, jsonify
import sqlite3

app = Flask(__name__)
TOTAL_SEATS = 100

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    usernames TEXT NOT NULL,
                    phone_number TEXT NOT NULL,
                    movie_name TEXT NOT NULL,
                    booked_seats INTEGER NOT NULL,
                    theater_name TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

def get_bookings():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM bookings")
    bookings = c.fetchall()
    c.execute("SELECT SUM(booked_seats) FROM bookings")
    total_booked = c.fetchone()[0]
    conn.close()
    remaining = TOTAL_SEATS - (total_booked if total_booked else 0)
    return bookings, remaining

@app.route('/')
def index():
    bookings, remaining_seats = get_bookings()
    return render_template('index.html', bookings=bookings, remaining_seats=remaining_seats)

@app.route('/submit', methods=['POST'])
def submit():
    usernames = request.form['usernames']
    phone_number = request.form['phone_number']
    movie_name = request.form['movie_name']
    booked_seats = int(request.form['booked_seats'])
    theater_name = request.form['theater_name']

    bookings, remaining_seats = get_bookings()
    if booked_seats > remaining_seats:
        if request.accept_mimetypes['application/json']:
            return jsonify(success=False, error=f"Only {remaining_seats} seats available. Try booking fewer.")
        return f"Only {remaining_seats} seats available. Try booking fewer."

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (usernames, phone_number, movie_name, booked_seats, theater_name) VALUES (?, ?, ?, ?, ?)",
              (usernames, phone_number, movie_name, booked_seats, theater_name))
    conn.commit()
    conn.close()
    bookings, remaining_seats = get_bookings()
    if request.accept_mimetypes['application/json']:
        return jsonify(success=True, bookings=bookings, remaining_seats=remaining_seats)
    return redirect('/')

@app.route('/delete/<int:booking_id>', methods=['POST'])
def delete_booking(booking_id):
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("DELETE FROM bookings WHERE id=?", (booking_id,))
    conn.commit()
    conn.close()
    bookings, remaining_seats = get_bookings()
    return jsonify(success=True, bookings=bookings, remaining_seats=remaining_seats)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
