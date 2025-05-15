import sqlite3

def view_bookings():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()

    # Fetch all records from bookings table
    c.execute("SELECT * FROM bookings")
    rows = c.fetchall()

    if rows:
        print("\nAll Bookings:\n")
        for row in rows:
            print(f"ID: {row[0]}")
            print(f"Usernames: {row[1]}")
            print(f"Phone Number: {row[2]}")
            print(f"Movie Name: {row[3]}")
            print(f"Booked Seats: {row[4]}")
            print(f"Theater Name: {row[5]}")
            print("-" * 40)
    else:
        print("No bookings found.")

    conn.close()

if __name__ == '__main__':
    view_bookings()
