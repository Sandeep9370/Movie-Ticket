import os
import random
from datetime import datetime
from openpyxl import Workbook, load_workbook


# =========================================================
# EXCEL DATABASE FILE
# =========================================================

FILE_NAME = "movie_booking.xlsx"


# =========================================================
# SAMPLE MOVIES
# =========================================================

SAMPLE_MOVIES = [
    [1, "Avengers: Endgame", "Action / Sci-Fi", "3h 02m", 4.8, 180],
    [2, "Avatar: The Way of Water", "Adventure / Sci-Fi", "3h 12m", 4.7, 200],
    [3, "The Batman", "Action / Crime", "2h 56m", 4.6, 150],
    [4, "Spider-Man: No Way Home", "Action / Adventure", "2h 28m", 4.8, 180],
    [5, "Jurassic World", "Adventure / Sci-Fi", "2h 07m", 4.5, 160],
    [6, "Interstellar", "Sci-Fi / Drama", "2h 49m", 4.9, 220]
]


# =========================================================
# CREATE DATABASE
# =========================================================

def initialize_database():

    # -----------------------------------------------------
    # If Excel file does not exist, create it
    # -----------------------------------------------------

    if not os.path.exists(FILE_NAME):

        wb = Workbook()

        # Remove default sheet
        default_sheet = wb.active
        wb.remove(default_sheet)

        create_users_sheet(wb)
        create_movies_sheet(wb)
        create_bookings_sheet(wb)
        create_admins_sheet(wb)

        wb.save(FILE_NAME)

        print("Excel database created successfully.")

    else:

        # Open existing Excel file
        wb = load_workbook(FILE_NAME)

        # Make sure all sheets exist
        if "Users" not in wb.sheetnames:
            create_users_sheet(wb)

        if "Movies" not in wb.sheetnames:
            create_movies_sheet(wb)

        if "Bookings" not in wb.sheetnames:
            create_bookings_sheet(wb)

        if "Admins" not in wb.sheetnames:
            create_admins_sheet(wb)

        # Make sure Movies sheet has sample movies
        ws = wb["Movies"]

        if ws.max_row <= 1:

            for movie in SAMPLE_MOVIES:
                ws.append(movie)

        # Make sure default admin exists
        admin_ws = wb["Admins"]

        admin_exists = False

        for row in admin_ws.iter_rows(
            min_row=2,
            values_only=True
        ):

            if row[1] == "admin":
                admin_exists = True
                break

        if not admin_exists:

            admin_ws.append([
                1,
                "admin",
                "admin123"
            ])

        wb.save(FILE_NAME)

        print("Excel database checked and updated.")

    print(f"Database: {os.path.abspath(FILE_NAME)}")


# =========================================================
# USERS SHEET
# =========================================================

def create_users_sheet(wb):

    ws = wb.create_sheet("Users")

    ws.append([
        "User ID",
        "Name",
        "Email",
        "Password"
    ])


# =========================================================
# MOVIES SHEET
# =========================================================

def create_movies_sheet(wb):

    ws = wb.create_sheet("Movies")

    ws.append([
        "Movie ID",
        "Movie Name",
        "Genre",
        "Duration",
        "Rating",
        "Price"
    ])

    # Add sample movies
    for movie in SAMPLE_MOVIES:
        ws.append(movie)


# =========================================================
# BOOKINGS SHEET
# =========================================================

def create_bookings_sheet(wb):

    ws = wb.create_sheet("Bookings")

    ws.append([
        "Booking ID",
        "User ID",
        "Customer Name",
        "Movie ID",
        "Movie Name",
        "Show Date",
        "Show Time",
        "Seats",
        "Total Amount",
        "Booking Time"
    ])


# =========================================================
# ADMINS SHEET
# =========================================================

def create_admins_sheet(wb):

    ws = wb.create_sheet("Admins")

    ws.append([
        "Admin ID",
        "Username",
        "Password"
    ])

    ws.append([
        1,
        "admin",
        "admin123"
    ])


# =========================================================
# GET WORKBOOK
# =========================================================

def get_workbook():

    initialize_database()

    return load_workbook(FILE_NAME)


# =========================================================
# SAVE WORKBOOK
# =========================================================

def save_database(wb):

    wb.save(FILE_NAME)


# =========================================================
# USER REGISTRATION
# =========================================================

def register_user(name, email, password):

    wb = get_workbook()

    ws = wb["Users"]

    # Check duplicate email
    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[2] and str(row[2]).lower() == email.lower():

            return False, "Email already registered."

    # Generate User ID
    user_id = 1

    if ws.max_row > 1:

        ids = []

        for row in ws.iter_rows(
            min_row=2,
            values_only=True
        ):

            if row[0] is not None:
                ids.append(int(row[0]))

        if ids:
            user_id = max(ids) + 1

    ws.append([
        user_id,
        name,
        email,
        password
    ])

    save_database(wb)

    return True, "Registration successful."


# =========================================================
# USER LOGIN
# =========================================================

def login_user(email, password):

    wb = get_workbook()

    ws = wb["Users"]

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if (
            row[2]
            and str(row[2]).lower() == email.lower()
            and row[3] == password
        ):

            return {
                "id": row[0],
                "name": row[1],
                "email": row[2]
            }

    return None


# =========================================================
# ADMIN LOGIN
# =========================================================

def login_admin(username, password):

    wb = get_workbook()

    ws = wb["Admins"]

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if (
            row[1] == username
            and row[2] == password
        ):

            return {
                "id": row[0],
                "username": row[1]
            }

    return None


# =========================================================
# GET ALL MOVIES
# =========================================================

def get_movies():

    wb = get_workbook()

    ws = wb["Movies"]

    movies = []

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is not None:

            movies.append((
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ))

    return movies


# =========================================================
# GET MOVIE
# =========================================================

def get_movie(movie_id):

    wb = get_workbook()

    ws = wb["Movies"]

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if int(row[0]) == int(movie_id):

            return (
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            )

    return None


# =========================================================
# ADD MOVIE
# =========================================================

def add_movie(
    name,
    genre,
    duration,
    rating,
    price
):

    wb = get_workbook()

    ws = wb["Movies"]

    # Generate next Movie ID
    movie_id = 1

    ids = []

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is not None:

            ids.append(int(row[0]))

    if ids:
        movie_id = max(ids) + 1

    # Add movie to Excel
    ws.append([
        movie_id,
        name,
        genre,
        duration,
        float(rating),
        float(price)
    ])

    save_database(wb)

    print("Movie saved:", name)

    return True


# =========================================================
# UPDATE MOVIE
# =========================================================

def update_movie(
    movie_id,
    name,
    genre,
    duration,
    rating,
    price
):

    wb = get_workbook()

    ws = wb["Movies"]

    for row_number in range(
        2,
        ws.max_row + 1
    ):

        current_id = ws.cell(
            row_number,
            1
        ).value

        if current_id is not None and int(current_id) == int(movie_id):

            ws.cell(
                row_number,
                2
            ).value = name

            ws.cell(
                row_number,
                3
            ).value = genre

            ws.cell(
                row_number,
                4
            ).value = duration

            ws.cell(
                row_number,
                5
            ).value = float(rating)

            ws.cell(
                row_number,
                6
            ).value = float(price)

            save_database(wb)

            return True

    return False


# =========================================================
# DELETE MOVIE
# =========================================================

def delete_movie(movie_id):

    wb = get_workbook()

    ws = wb["Movies"]

    for row_number in range(
        2,
        ws.max_row + 1
    ):

        current_id = ws.cell(
            row_number,
            1
        ).value

        if current_id is not None and int(current_id) == int(movie_id):

            ws.delete_rows(
                row_number,
                1
            )

            save_database(wb)

            return True

    return False


# =========================================================
# GENERATE BOOKING ID
# =========================================================

def generate_booking_id():

    wb = get_workbook()

    ws = wb["Bookings"]

    while True:

        booking_id = "MB" + str(
            random.randint(100000, 999999)
        )

        found = False

        for row in ws.iter_rows(
            min_row=2,
            values_only=True
        ):

            if row[0] == booking_id:

                found = True
                break

        if not found:

            return booking_id


# =========================================================
# GET BOOKED SEATS
# =========================================================

def get_booked_seats(
    movie_id,
    show_date,
    show_time
):

    wb = get_workbook()

    ws = wb["Bookings"]

    booked_seats = []

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        booking_movie_id = row[3]
        booking_date = row[5]
        booking_time = row[6]
        seats = row[7]

        if (
            booking_movie_id is not None
            and int(booking_movie_id) == int(movie_id)
            and str(booking_date) == str(show_date)
            and str(booking_time) == str(show_time)
        ):

            if seats:

                booked_seats.extend(
                    str(seats).split(",")
                )

    return booked_seats


# =========================================================
# CREATE BOOKING
# =========================================================

def create_booking(
    user_id,
    customer_name,
    movie_id,
    show_date,
    show_time,
    seats
):

    if not seats:

        return (
            False,
            "Please select at least one seat."
        )

    movie = get_movie(movie_id)

    if not movie:

        return (
            False,
            "Movie not found."
        )

    movie_name = movie[1]

    ticket_price = float(movie[5])

    # Check booked seats
    booked_seats = get_booked_seats(
        movie_id,
        show_date,
        show_time
    )

    for seat in seats:

        if seat in booked_seats:

            return (
                False,
                f"Seat {seat} is already booked."
            )

    total_amount = (
        ticket_price * len(seats)
    )

    booking_id = generate_booking_id()

    booking_time = datetime.now().strftime(
        "%d-%m-%Y %I:%M %p"
    )

    wb = get_workbook()

    ws = wb["Bookings"]

    ws.append([
        booking_id,
        user_id,
        customer_name,
        movie_id,
        movie_name,
        show_date,
        show_time,
        ",".join(seats),
        total_amount,
        booking_time
    ])

    save_database(wb)

    print("Booking saved:", booking_id)

    return True, {
        "booking_id": booking_id,
        "movie_name": movie_name,
        "show_date": show_date,
        "show_time": show_time,
        "seats": seats,
        "total_amount": total_amount
    }


# =========================================================
# USER BOOKING HISTORY
# =========================================================

def get_user_bookings(user_id):

    wb = get_workbook()

    ws = wb["Bookings"]

    bookings = []

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[1] == user_id:

            bookings.append((
                row[0],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9]
            ))

    return bookings


# =========================================================
# ALL BOOKINGS
# =========================================================

def get_all_bookings():

    wb = get_workbook()

    ws = wb["Bookings"]

    bookings = []

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is not None:

            bookings.append((
                row[0],
                row[2],
                row[4],
                row[5],
                row[6],
                row[7],
                row[8],
                row[9]
            ))

    return bookings


# =========================================================
# CANCEL BOOKING
# =========================================================

def cancel_booking(
    booking_id,
    user_id
):

    wb = get_workbook()

    ws = wb["Bookings"]

    for row_number in range(
        2,
        ws.max_row + 1
    ):

        current_booking = ws.cell(
            row_number,
            1
        ).value

        current_user = ws.cell(
            row_number,
            2
        ).value

        if (
            current_booking == booking_id
            and current_user == user_id
        ):

            ws.delete_rows(
                row_number,
                1
            )

            save_database(wb)

            return (
                True,
                "Booking cancelled successfully."
            )

    return (
        False,
        "Booking not found."
    )


# =========================================================
# SEARCH MOVIES
# =========================================================

def search_movies(keyword):

    wb = get_workbook()

    ws = wb["Movies"]

    movies = []

    keyword = str(keyword).lower()

    for row in ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is None:
            continue

        movie_name = str(row[1]).lower()
        genre = str(row[2]).lower()

        if (
            keyword in movie_name
            or keyword in genre
        ):

            movies.append((
                row[0],
                row[1],
                row[2],
                row[3],
                row[4],
                row[5]
            ))

    return movies


# =========================================================
# STATISTICS
# =========================================================

def get_statistics():

    wb = get_workbook()

    # Movies
    movie_ws = wb["Movies"]

    total_movies = 0

    for row in movie_ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is not None:
            total_movies += 1

    # Users
    user_ws = wb["Users"]

    total_users = 0

    for row in user_ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is not None:
            total_users += 1

    # Bookings
    booking_ws = wb["Bookings"]

    total_bookings = 0
    total_revenue = 0
    total_tickets = 0

    for row in booking_ws.iter_rows(
        min_row=2,
        values_only=True
    ):

        if row[0] is not None:

            total_bookings += 1

            if row[8] is not None:
                total_revenue += float(row[8])

            if row[7]:

                total_tickets += len(
                    str(row[7]).split(",")
                )

    return {
        "total_movies": total_movies,
        "total_users": total_users,
        "total_bookings": total_bookings,
        "total_revenue": total_revenue,
        "total_tickets": total_tickets
    }


# =========================================================
# TEST BACKEND
# =========================================================

if __name__ == "__main__":

    initialize_database()

    print()
    print("========================================")
    print("     MOVIE BOOKING EXCEL BACKEND")
    print("========================================")

    print("\nMovies stored in Excel:")

    movies = get_movies()

    for movie in movies:
        print(
            f"{movie[0]} | "
            f"{movie[1]} | "
            f"{movie[2]} | "
            f"₹{movie[5]}"
        )

    print("\nStatistics:")

    print(get_statistics())

    print("\nAdmin Login:")
    print("Username: admin")
    print("Password: admin123")

    print("\nBackend is working correctly!")
