import tkinter as tk
from tkinter import ttk, messagebox

from backend import (
    initialize_database,
    register_user,
    login_user,
    login_admin,
    get_movies,
    get_movie,
    get_booked_seats,
    create_booking,
    get_user_bookings,
    get_all_bookings,
    cancel_booking,
    get_statistics,
    add_movie,
    update_movie,
    delete_movie,
    search_movies
)


# =========================================================
# COLORS
# =========================================================

BG = "#080D1A"
SIDEBAR = "#101729"
CARD = "#151F35"
CARD2 = "#1D2943"

BLUE = "#287BFF"
BLUE_HOVER = "#4590FF"

WHITE = "#FFFFFF"
TEXT = "#D8DEEA"
MUTED = "#8994A8"

GREEN = "#24D18A"
RED = "#FF5263"
YELLOW = "#FFC857"


# =========================================================
# MAIN APPLICATION
# =========================================================

class MovieBookingApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "MovieBook - Movie Ticket Booking System"
        )

        self.root.geometry("1200x750")
        self.root.minsize(1000, 650)

        self.root.configure(bg=BG)

        # Current logged-in user
        self.current_user = None

        # Selected movie
        self.selected_movie = None

        # Selected seats
        self.selected_seats = []

        # Show details
        self.show_date = "10-09-2026"
        self.show_time = "07:30 PM"

        # Initialize Excel backend
        initialize_database()

        # Start login
        self.show_login()


    # =====================================================
    # CLEAR WINDOW
    # =====================================================

    def clear_window(self):

        for widget in self.root.winfo_children():
            widget.destroy()


    # =====================================================
    # CREATE BUTTON
    # =====================================================

    def create_button(
        self,
        parent,
        text,
        command,
        bg=BLUE,
        width=18
    ):

        button = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=WHITE,
            activebackground=BLUE_HOVER,
            activeforeground=WHITE,
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            cursor="hand2",
            width=width,
            pady=10
        )

        return button


    # =====================================================
    # LOGIN SCREEN
    # =====================================================

    def show_login(self):

        self.clear_window()

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True
        )

        # Left side
        left = tk.Frame(
            main,
            bg=BLUE,
            width=500
        )

        left.pack(
            side="left",
            fill="y"
        )

        left.pack_propagate(False)

        tk.Label(
            left,
            text="🎬",
            font=("Arial", 65),
            bg=BLUE,
            fg=WHITE
        ).pack(
            pady=(130, 10)
        )

        tk.Label(
            left,
            text="MOVIEBOOK",
            font=("Arial", 30, "bold"),
            bg=BLUE,
            fg=WHITE
        ).pack()

        tk.Label(
            left,
            text="Book your movie.\nEnjoy your experience.",
            font=("Arial", 15),
            bg=BLUE,
            fg=WHITE,
            justify="center"
        ).pack(pady=20)

        # Right side
        right = tk.Frame(
            main,
            bg=BG
        )

        right.pack(
            side="right",
            fill="both",
            expand=True
        )

        form = tk.Frame(
            right,
            bg=CARD,
            padx=45,
            pady=35
        )

        form.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            form,
            text="Welcome Back",
            font=("Arial", 25, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(pady=(0, 5))

        tk.Label(
            form,
            text="Login to continue",
            font=("Arial", 11),
            bg=CARD,
            fg=MUTED
        ).pack(pady=(0, 25))

        tk.Label(
            form,
            text="Email",
            font=("Arial", 10, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w")

        self.login_email = tk.Entry(
            form,
            font=("Arial", 12),
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            width=32
        )

        self.login_email.pack(
            pady=(5, 15),
            ipady=9
        )

        tk.Label(
            form,
            text="Password",
            font=("Arial", 10, "bold"),
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w")

        self.login_password = tk.Entry(
            form,
            font=("Arial", 12),
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            show="*",
            relief="flat",
            width=32
        )

        self.login_password.pack(
            pady=(5, 20),
            ipady=9
        )

        self.create_button(
            form,
            "LOGIN",
            self.perform_login
        ).pack(pady=5)

        self.create_button(
            form,
            "CREATE ACCOUNT",
            self.show_register,
            bg=CARD2
        ).pack(pady=8)

        self.create_button(
            form,
            "ADMIN LOGIN",
            self.show_admin_login,
            bg="#553399"
        ).pack(pady=5)


    # =====================================================
    # LOGIN FUNCTION
    # =====================================================

    def perform_login(self):

        email = self.login_email.get().strip()
        password = self.login_password.get().strip()

        if not email or not password:

            messagebox.showwarning(
                "Login",
                "Please enter email and password."
            )

            return

        user = login_user(
            email,
            password
        )

        if user:

            self.current_user = user

            messagebox.showinfo(
                "Login Successful",
                f"Welcome {user['name']}!"
            )

            self.show_home()

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid email or password."
            )


    # =====================================================
    # REGISTER SCREEN
    # =====================================================

    def show_register(self):

        self.clear_window()

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            fill="both",
            expand=True
        )

        form = tk.Frame(
            main,
            bg=CARD,
            padx=50,
            pady=35
        )

        form.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            form,
            text="Create Account",
            font=("Arial", 25, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack()

        tk.Label(
            form,
            text="Register for MovieBook",
            font=("Arial", 11),
            bg=CARD,
            fg=MUTED
        ).pack(pady=(5, 25))

        # Name
        tk.Label(
            form,
            text="Full Name",
            bg=CARD,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.reg_name = tk.Entry(
            form,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12),
            width=32
        )

        self.reg_name.pack(
            pady=(5, 15),
            ipady=9
        )

        # Email
        tk.Label(
            form,
            text="Email",
            bg=CARD,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.reg_email = tk.Entry(
            form,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12),
            width=32
        )

        self.reg_email.pack(
            pady=(5, 15),
            ipady=9
        )

        # Password
        tk.Label(
            form,
            text="Password",
            bg=CARD,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.reg_password = tk.Entry(
            form,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            show="*",
            relief="flat",
            font=("Arial", 12),
            width=32
        )

        self.reg_password.pack(
            pady=(5, 15),
            ipady=9
        )

        # Confirm password
        tk.Label(
            form,
            text="Confirm Password",
            bg=CARD,
            fg=TEXT,
            font=("Arial", 10, "bold")
        ).pack(anchor="w")

        self.reg_confirm = tk.Entry(
            form,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            show="*",
            relief="flat",
            font=("Arial", 12),
            width=32
        )

        self.reg_confirm.pack(
            pady=(5, 20),
            ipady=9
        )

        self.create_button(
            form,
            "REGISTER",
            self.perform_register
        ).pack(pady=5)

        self.create_button(
            form,
            "BACK TO LOGIN",
            self.show_login,
            bg=CARD2
        ).pack(pady=8)


    # =====================================================
    # REGISTER FUNCTION
    # =====================================================

    def perform_register(self):

        name = self.reg_name.get().strip()
        email = self.reg_email.get().strip()
        password = self.reg_password.get().strip()
        confirm = self.reg_confirm.get().strip()

        if not name or not email or not password:

            messagebox.showwarning(
                "Registration",
                "Please fill all fields."
            )

            return

        if password != confirm:

            messagebox.showerror(
                "Registration",
                "Passwords do not match."
            )

            return

        success, message = register_user(
            name,
            email,
            password
        )

        if success:

            messagebox.showinfo(
                "Success",
                message
            )

            self.show_login()

        else:

            messagebox.showerror(
                "Registration",
                message
            )


    # =====================================================
    # USER HOME
    # =====================================================

    def show_home(self):

        self.clear_window()

        self.create_sidebar()

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        # Header
        header = tk.Frame(
            content,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=35,
            pady=25
        )

        tk.Label(
            header,
            text=f"Welcome, {self.current_user['name']} 👋",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(anchor="w")

        tk.Label(
            header,
            text="Book your favourite movie today.",
            font=("Arial", 12),
            bg=BG,
            fg=MUTED
        ).pack(anchor="w", pady=5)

        # Statistics cards
        movies = get_movies()

        self.dashboard_card(
            content,
            "🎬",
            "Available Movies",
            str(len(movies)),
            BLUE,
            0
        )

        self.dashboard_card(
            content,
            "🎟",
            "My Bookings",
            str(len(
                get_user_bookings(
                    self.current_user["id"]
                )
            )),
            GREEN,
            1
        )

        # Movie section
        tk.Label(
            content,
            text="Now Showing",
            font=("Arial", 20, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 15)
        )

        movie_frame = tk.Frame(
            content,
            bg=BG
        )

        movie_frame.pack(
            fill="both",
            expand=True,
            padx=35
        )

        for index, movie in enumerate(movies[:6]):

            self.movie_card(
                movie_frame,
                movie,
                index
            )


    # =====================================================
    # DASHBOARD CARD
    # =====================================================

    def dashboard_card(
        self,
        parent,
        icon,
        title,
        value,
        color,
        column
    ):

        card = tk.Frame(
            parent,
            bg=CARD,
            width=260,
            height=110
        )

        card.pack(
            side="left",
            padx=(35 if column == 0 else 10, 10),
            pady=10
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=icon,
            font=("Arial", 28),
            bg=CARD,
            fg=color
        ).pack(
            side="left",
            padx=20
        )

        text_frame = tk.Frame(
            card,
            bg=CARD
        )

        text_frame.pack(
            side="left",
            pady=20
        )

        tk.Label(
            text_frame,
            text=title,
            font=("Arial", 10),
            bg=CARD,
            fg=MUTED
        ).pack(anchor="w")

        tk.Label(
            text_frame,
            text=value,
            font=("Arial", 22, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(anchor="w")


    # =====================================================
    # SIDEBAR
    # =====================================================

    def create_sidebar(self):

        sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=230
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="🎬",
            font=("Arial", 40),
            bg=SIDEBAR,
            fg=BLUE
        ).pack(pady=(35, 0))

        tk.Label(
            sidebar,
            text="MOVIEBOOK",
            font=("Arial", 18, "bold"),
            bg=SIDEBAR,
            fg=WHITE
        ).pack(pady=(5, 30))

        buttons = [
            ("🏠  Home", self.show_home),
            ("🎬  Movies", self.show_movies),
            ("🎟  My Bookings", self.show_bookings)
        ]

        for text, command in buttons:

            tk.Button(
                sidebar,
                text=text,
                command=command,
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=CARD2,
                activeforeground=WHITE,
                font=("Arial", 11, "bold"),
                relief="flat",
                bd=0,
                anchor="w",
                padx=25,
                cursor="hand2"
            ).pack(
                fill="x",
                pady=3,
                ipady=10
            )

        # Logout
        tk.Button(
            sidebar,
            text="🚪  Logout",
            command=self.logout,
            bg=SIDEBAR,
            fg=RED,
            activebackground=CARD2,
            activeforeground=RED,
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            cursor="hand2"
        ).pack(
            side="bottom",
            fill="x",
            pady=20,
            ipady=10
        )


    # =====================================================
    # MOVIE CARD
    # =====================================================

    def movie_card(
        self,
        parent,
        movie,
        index
    ):

        movie_id = movie[0]
        name = movie[1]
        genre = movie[2]
        duration = movie[3]
        rating = movie[4]
        price = movie[5]

        card = tk.Frame(
            parent,
            bg=CARD,
            width=270,
            height=220
        )

        card.grid(
            row=index // 3,
            column=index % 3,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text="🎬",
            font=("Arial", 40),
            bg=CARD,
            fg=BLUE
        ).pack(pady=(15, 5))

        tk.Label(
            card,
            text=name,
            font=("Arial", 13, "bold"),
            bg=CARD,
            fg=WHITE,
            wraplength=230
        ).pack()

        tk.Label(
            card,
            text=f"{genre}  •  {duration}",
            font=("Arial", 9),
            bg=CARD,
            fg=MUTED
        ).pack(pady=5)

        tk.Label(
            card,
            text=f"⭐ {rating}     ₹{price}",
            font=("Arial", 11, "bold"),
            bg=CARD,
            fg=YELLOW
        ).pack()

        self.create_button(
            card,
            "BOOK NOW",
            lambda m=movie_id: self.start_booking(m),
            width=15
        ).pack(pady=10)


    # =====================================================
    # MOVIES SCREEN
    # =====================================================

    def show_movies(self):

        self.clear_window()

        self.create_sidebar()

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text="All Movies",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 10)
        )

        # Search
        search_frame = tk.Frame(
            content,
            bg=BG
        )

        search_frame.pack(
            fill="x",
            padx=35,
            pady=10
        )

        self.movie_search = tk.Entry(
            search_frame,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12),
            width=40
        )

        self.movie_search.pack(
            side="left",
            ipady=9
        )

        self.create_button(
            search_frame,
            "SEARCH",
            self.perform_movie_search,
            width=12
        ).pack(
            side="left",
            padx=10
        )

        # Scroll area
        movie_frame = tk.Frame(
            content,
            bg=BG
        )

        movie_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        movies = get_movies()

        for index, movie in enumerate(movies):

            self.movie_card(
                movie_frame,
                movie,
                index
            )


    # =====================================================
    # SEARCH MOVIES
    # =====================================================

    def perform_movie_search(self):

        keyword = self.movie_search.get().strip()

        if not keyword:

            self.show_movies()
            return

        movies = search_movies(keyword)

        # Remove movie cards area by rebuilding screen
        self.clear_window()

        self.create_sidebar()

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text=f"Search Results: {keyword}",
            font=("Arial", 23, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=30
        )

        movie_frame = tk.Frame(
            content,
            bg=BG
        )

        movie_frame.pack(
            fill="both",
            expand=True,
            padx=35
        )

        if not movies:

            tk.Label(
                movie_frame,
                text="No movies found.",
                font=("Arial", 15),
                bg=BG,
                fg=MUTED
            ).pack(pady=50)

        else:

            for index, movie in enumerate(movies):

                self.movie_card(
                    movie_frame,
                    movie,
                    index
                )


    # =====================================================
    # START BOOKING
    # =====================================================

    def start_booking(self, movie_id):

        movie = get_movie(movie_id)

        if not movie:
            return

        self.selected_movie = movie

        self.selected_seats = []

        self.show_booking_screen()


    # =====================================================
    # BOOKING SCREEN
    # =====================================================

    def show_booking_screen(self):

        self.clear_window()

        self.create_sidebar()

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        movie = self.selected_movie

        tk.Label(
            content,
            text="Select Your Seats",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=(25, 5)
        )

        tk.Label(
            content,
            text=f"{movie[1]}  •  {movie[2]}  •  ₹{movie[5]} per ticket",
            font=("Arial", 11),
            bg=BG,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=35
        )

        # Main area
        area = tk.Frame(
            content,
            bg=BG
        )

        area.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=20
        )

        # Seat area
        seat_area = tk.Frame(
            area,
            bg=CARD,
            padx=30,
            pady=25
        )

        seat_area.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 15)
        )

        tk.Label(
            seat_area,
            text="SCREEN",
            font=("Arial", 11, "bold"),
            bg=BLUE,
            fg=WHITE,
            width=50,
            pady=8
        ).pack(pady=(0, 25))

        booked = get_booked_seats(
            movie[0],
            self.show_date,
            self.show_time
        )

        rows = ["A", "B", "C", "D", "E", "F"]

        for row in rows:

            row_frame = tk.Frame(
                seat_area,
                bg=CARD
            )

            row_frame.pack(pady=5)

            tk.Label(
                row_frame,
                text=row,
                width=3,
                bg=CARD,
                fg=MUTED,
                font=("Arial", 10, "bold")
            ).pack(side="left")

            for col in range(1, 9):

                seat = f"{row}{col}"

                if seat in booked:

                    color = RED
                    state = "disabled"

                else:

                    color = CARD2
                    state = "normal"

                button = tk.Button(
                    row_frame,
                    text=str(col),
                    width=4,
                    height=1,
                    bg=color,
                    fg=WHITE,
                    activebackground=BLUE,
                    relief="flat",
                    bd=0,
                    state=state,
                    cursor="hand2",
                    command=lambda s=seat:
                    self.toggle_seat(s)
                )

                button.pack(
                    side="left",
                    padx=3
                )

        # Legend
        legend = tk.Frame(
            seat_area,
            bg=CARD
        )

        legend.pack(
            pady=25
        )

        tk.Label(
            legend,
            text="● Available",
            bg=CARD,
            fg=TEXT
        ).pack(side="left", padx=10)

        tk.Label(
            legend,
            text="● Booked",
            bg=CARD,
            fg=RED
        ).pack(side="left", padx=10)

        tk.Label(
            legend,
            text="● Selected",
            bg=CARD,
            fg=GREEN
        ).pack(side="left", padx=10)

        # Booking summary
        summary = tk.Frame(
            area,
            bg=CARD,
            width=300,
            padx=25,
            pady=25
        )

        summary.pack(
            side="right",
            fill="y"
        )

        summary.pack_propagate(False)

        tk.Label(
            summary,
            text="Booking Summary",
            font=("Arial", 18, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack(anchor="w")

        tk.Label(
            summary,
            text=movie[1],
            font=("Arial", 12, "bold"),
            bg=CARD,
            fg=BLUE
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        tk.Label(
            summary,
            text=f"Date: {self.show_date}",
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", pady=3)

        tk.Label(
            summary,
            text=f"Time: {self.show_time}",
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w", pady=3)

        self.selected_label = tk.Label(
            summary,
            text="Seats: None",
            bg=CARD,
            fg=TEXT,
            wraplength=250
        )

        self.selected_label.pack(
            anchor="w",
            pady=15
        )

        self.total_label = tk.Label(
            summary,
            text="Total: ₹0",
            font=("Arial", 18, "bold"),
            bg=CARD,
            fg=GREEN
        )

        self.total_label.pack(
            anchor="w",
            pady=10
        )

        self.create_button(
            summary,
            "CONFIRM BOOKING",
            self.confirm_booking,
            bg=GREEN,
            width=20
        ).pack(
            pady=20
        )


    # =====================================================
    # TOGGLE SEAT
    # =====================================================

    def toggle_seat(self, seat):

        if seat in self.selected_seats:

            self.selected_seats.remove(seat)

        else:

            self.selected_seats.append(seat)

        self.selected_seats.sort()

        movie = self.selected_movie

        total = (
            len(self.selected_seats)
            * float(movie[5])
        )

        seats_text = (
            ", ".join(self.selected_seats)
            if self.selected_seats
            else "None"
        )

        self.selected_label.config(
            text=f"Seats: {seats_text}"
        )

        self.total_label.config(
            text=f"Total: ₹{total:.2f}"
        )


    # =====================================================
    # CONFIRM BOOKING
    # =====================================================

    def confirm_booking(self):

        if not self.selected_seats:

            messagebox.showwarning(
                "Booking",
                "Please select at least one seat."
            )

            return

        movie = self.selected_movie

        success, result = create_booking(
            self.current_user["id"],
            self.current_user["name"],
            movie[0],
            self.show_date,
            self.show_time,
            self.selected_seats
        )

        if success:

            messagebox.showinfo(
                "Booking Successful",
                f"Booking ID: {result['booking_id']}\n\n"
                f"Movie: {result['movie_name']}\n"
                f"Date: {result['show_date']}\n"
                f"Time: {result['show_time']}\n"
                f"Seats: {', '.join(result['seats'])}\n"
                f"Total: ₹{result['total_amount']}"
            )

            self.selected_seats = []

            self.show_bookings()

        else:

            messagebox.showerror(
                "Booking Failed",
                result
            )


    # =====================================================
    # MY BOOKINGS
    # =====================================================

    def show_bookings(self):

        self.clear_window()

        self.create_sidebar()

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text="My Bookings",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=30
        )

        bookings = get_user_bookings(
            self.current_user["id"]
        )

        if not bookings:

            tk.Label(
                content,
                text="You have no bookings yet.",
                font=("Arial", 15),
                bg=BG,
                fg=MUTED
            ).pack(pady=50)

            return

        table_frame = tk.Frame(
            content,
            bg=CARD
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=35,
            pady=10
        )

        columns = (
            "Booking ID",
            "Movie",
            "Date",
            "Time",
            "Seats",
            "Amount",
            "Booking Time"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=120
            )

        for booking in bookings:

            tree.insert(
                "",
                "end",
                values=booking
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Cancel button
        def cancel_selected():

            selected = tree.selection()

            if not selected:

                messagebox.showwarning(
                    "Cancel",
                    "Please select a booking."
                )

                return

            item = tree.item(
                selected[0]
            )

            booking_id = item["values"][0]

            confirm = messagebox.askyesno(
                "Cancel Booking",
                f"Cancel booking {booking_id}?"
            )

            if not confirm:
                return

            success, message = cancel_booking(
                booking_id,
                self.current_user["id"]
            )

            if success:

                messagebox.showinfo(
                    "Cancelled",
                    message
                )

                self.show_bookings()

            else:

                messagebox.showerror(
                    "Error",
                    message
                )

        self.create_button(
            content,
            "CANCEL SELECTED BOOKING",
            cancel_selected,
            bg=RED,
            width=25
        ).pack(
            pady=15
        )


    # =====================================================
    # ADMIN LOGIN
    # =====================================================

    def show_admin_login(self):

        self.clear_window()

        form = tk.Frame(
            self.root,
            bg=CARD,
            padx=50,
            pady=40
        )

        form.place(
            relx=0.5,
            rely=0.5,
            anchor="center"
        )

        tk.Label(
            form,
            text="👨‍💼",
            font=("Arial", 45),
            bg=CARD,
            fg=BLUE
        ).pack()

        tk.Label(
            form,
            text="Admin Login",
            font=("Arial", 25, "bold"),
            bg=CARD,
            fg=WHITE
        ).pack()

        tk.Label(
            form,
            text="Administrator Access",
            font=("Arial", 11),
            bg=CARD,
            fg=MUTED
        ).pack(
            pady=(5, 25)
        )

        tk.Label(
            form,
            text="Username",
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w")

        self.admin_username = tk.Entry(
            form,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            relief="flat",
            font=("Arial", 12),
            width=30
        )

        self.admin_username.pack(
            pady=(5, 15),
            ipady=9
        )

        tk.Label(
            form,
            text="Password",
            bg=CARD,
            fg=TEXT
        ).pack(anchor="w")

        self.admin_password = tk.Entry(
            form,
            bg=CARD2,
            fg=WHITE,
            insertbackground=WHITE,
            show="*",
            relief="flat",
            font=("Arial", 12),
            width=30
        )

        self.admin_password.pack(
            pady=(5, 20),
            ipady=9
        )

        self.create_button(
            form,
            "ADMIN LOGIN",
            self.perform_admin_login,
            bg="#553399"
        ).pack(pady=5)

        self.create_button(
            form,
            "BACK",
            self.show_login,
            bg=CARD2
        ).pack(pady=8)

        tk.Label(
            form,
            text="Default: admin / admin123",
            font=("Arial", 9),
            bg=CARD,
            fg=MUTED
        ).pack(pady=10)


    # =====================================================
    # ADMIN LOGIN FUNCTION
    # =====================================================

    def perform_admin_login(self):

        username = self.admin_username.get().strip()
        password = self.admin_password.get().strip()

        admin = login_admin(
            username,
            password
        )

        if admin:

            self.show_admin_dashboard()

        else:

            messagebox.showerror(
                "Admin Login",
                "Invalid admin username or password."
            )


    # =====================================================
    # ADMIN DASHBOARD
    # =====================================================

    def show_admin_dashboard(self):

        self.clear_window()

        # Sidebar
        sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=230
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="👨‍💼",
            font=("Arial", 40),
            bg=SIDEBAR,
            fg=BLUE
        ).pack(pady=(35, 5))

        tk.Label(
            sidebar,
            text="ADMIN PANEL",
            font=("Arial", 18, "bold"),
            bg=SIDEBAR,
            fg=WHITE
        ).pack(pady=(0, 30))

        admin_buttons = [
            ("📊 Dashboard", self.show_admin_dashboard),
            ("🎬 Manage Movies", self.admin_movies),
            ("🎟 All Bookings", self.admin_bookings)
        ]

        for text, command in admin_buttons:

            tk.Button(
                sidebar,
                text=text,
                command=command,
                bg=SIDEBAR,
                fg=TEXT,
                activebackground=CARD2,
                activeforeground=WHITE,
                font=("Arial", 11, "bold"),
                relief="flat",
                bd=0,
                anchor="w",
                padx=25,
                cursor="hand2"
            ).pack(
                fill="x",
                pady=3,
                ipady=10
            )

        tk.Button(
            sidebar,
            text="🚪 Logout",
            command=self.show_login,
            bg=SIDEBAR,
            fg=RED,
            activebackground=CARD2,
            activeforeground=RED,
            font=("Arial", 11, "bold"),
            relief="flat",
            bd=0,
            anchor="w",
            padx=25,
            cursor="hand2"
        ).pack(
            side="bottom",
            fill="x",
            pady=20,
            ipady=10
        )

        # Content
        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text="Admin Dashboard",
            font=("Arial", 27, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=35,
            pady=(30, 5)
        )

        tk.Label(
            content,
            text="Manage your MovieBook system",
            font=("Arial", 11),
            bg=BG,
            fg=MUTED
        ).pack(
            anchor="w",
            padx=35
        )

        stats = get_statistics()

        # Cards
        card_data = [
            (
                "🎬",
                "Total Movies",
                stats["total_movies"],
                BLUE
            ),
            (
                "👤",
                "Total Users",
                stats["total_users"],
                GREEN
            ),
            (
                "🎟",
                "Total Bookings",
                stats["total_bookings"],
                YELLOW
            ),
            (
                "₹",
                "Total Revenue",
                f"₹{stats['total_revenue']:.2f}",
                RED
            )
        ]

        cards_frame = tk.Frame(
            content,
            bg=BG
        )

        cards_frame.pack(
            fill="x",
            padx=25,
            pady=30
        )

        for icon, title, value, color in card_data:

            card = tk.Frame(
                cards_frame,
                bg=CARD,
                width=210,
                height=130
            )

            card.pack(
                side="left",
                padx=10
            )

            card.pack_propagate(False)

            tk.Label(
                card,
                text=icon,
                font=("Arial", 30),
                bg=CARD,
                fg=color
            ).pack(pady=(15, 0))

            tk.Label(
                card,
                text=str(value),
                font=("Arial", 22, "bold"),
                bg=CARD,
                fg=WHITE
            ).pack()

            tk.Label(
                card,
                text=title,
                font=("Arial", 9),
                bg=CARD,
                fg=MUTED
            ).pack()


        tk.Label(
            content,
            text=f"Total Tickets Sold: {stats['total_tickets']}",
            font=("Arial", 16, "bold"),
            bg=BG,
            fg=GREEN
        ).pack(
            anchor="w",
            padx=35,
            pady=20
        )


    # =====================================================
    # ADMIN MOVIES
    # =====================================================

    def admin_movies(self):

        self.clear_window()

        # Sidebar
        sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=230
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="👨‍💼",
            font=("Arial", 40),
            bg=SIDEBAR,
            fg=BLUE
        ).pack(pady=(35, 5))

        tk.Label(
            sidebar,
            text="ADMIN PANEL",
            font=("Arial", 18, "bold"),
            bg=SIDEBAR,
            fg=WHITE
        ).pack(pady=(0, 30))

        tk.Button(
            sidebar,
            text="📊 Dashboard",
            command=self.show_admin_dashboard,
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            fill="x",
            ipady=10
        )

        tk.Button(
            sidebar,
            text="🎬 Manage Movies",
            command=self.admin_movies,
            bg=CARD2,
            fg=WHITE,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            fill="x",
            ipady=10
        )

        tk.Button(
            sidebar,
            text="🎟 All Bookings",
            command=self.admin_bookings,
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            fill="x",
            ipady=10
        )

        tk.Button(
            sidebar,
            text="🚪 Logout",
            command=self.show_login,
            bg=SIDEBAR,
            fg=RED,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            side="bottom",
            fill="x",
            pady=20,
            ipady=10
        )

        # Content
        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text="Manage Movies",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=30,
            pady=25
        )

        # Form
        form = tk.Frame(
            content,
            bg=CARD,
            padx=20,
            pady=15
        )

        form.pack(
            fill="x",
            padx=30
        )

        entries = []

        labels = [
            "Movie Name",
            "Genre",
            "Duration",
            "Rating",
            "Price"
        ]

        for i, label in enumerate(labels):

            frame = tk.Frame(
                form,
                bg=CARD
            )

            frame.grid(
                row=0,
                column=i,
                padx=7
            )

            tk.Label(
                frame,
                text=label,
                bg=CARD,
                fg=MUTED,
                font=("Arial", 9)
            ).pack()

            entry = tk.Entry(
                frame,
                bg=CARD2,
                fg=WHITE,
                insertbackground=WHITE,
                relief="flat",
                width=17
            )

            entry.pack(
                ipady=7,
                pady=5
            )

            entries.append(entry)

        self.admin_movie_name = entries[0]
        self.admin_movie_genre = entries[1]
        self.admin_movie_duration = entries[2]
        self.admin_movie_rating = entries[3]
        self.admin_movie_price = entries[4]

        self.edit_movie_id = None

        buttons = tk.Frame(
            content,
            bg=BG
        )

        buttons.pack(
            fill="x",
            padx=30,
            pady=12
        )

        self.create_button(
            buttons,
            "ADD MOVIE",
            self.admin_add_movie,
            bg=GREEN,
            width=15
        ).pack(side="left", padx=5)

        self.create_button(
            buttons,
            "UPDATE MOVIE",
            self.admin_update_movie,
            bg=BLUE,
            width=15
        ).pack(side="left", padx=5)

        self.create_button(
            buttons,
            "DELETE MOVIE",
            self.admin_delete_movie,
            bg=RED,
            width=15
        ).pack(side="left", padx=5)

        self.create_button(
            buttons,
            "CLEAR",
            self.clear_movie_form,
            bg=CARD2,
            width=12
        ).pack(side="left", padx=5)

        # Table
        table_frame = tk.Frame(
            content,
            bg=CARD
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        columns = (
            "ID",
            "Movie",
            "Genre",
            "Duration",
            "Rating",
            "Price"
        )

        self.movie_tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            self.movie_tree.heading(
                column,
                text=column
            )

            self.movie_tree.column(
                column,
                width=120
            )

        self.movie_tree.pack(
            fill="both",
            expand=True
        )

        self.movie_tree.bind(
            "<ButtonRelease-1>",
            self.select_admin_movie
        )

        self.refresh_admin_movies()


    # =====================================================
    # REFRESH ADMIN MOVIES
    # =====================================================

    def refresh_admin_movies(self):

        for item in self.movie_tree.get_children():

            self.movie_tree.delete(item)

        for movie in get_movies():

            self.movie_tree.insert(
                "",
                "end",
                values=movie
            )


    # =====================================================
    # SELECT ADMIN MOVIE
    # =====================================================

    def select_admin_movie(self, event):

        selected = self.movie_tree.selection()

        if not selected:
            return

        values = self.movie_tree.item(
            selected[0]
        )["values"]

        self.edit_movie_id = int(values[0])

        self.admin_movie_name.delete(0, "end")
        self.admin_movie_name.insert(0, values[1])

        self.admin_movie_genre.delete(0, "end")
        self.admin_movie_genre.insert(0, values[2])

        self.admin_movie_duration.delete(0, "end")
        self.admin_movie_duration.insert(0, values[3])

        self.admin_movie_rating.delete(0, "end")
        self.admin_movie_rating.insert(0, values[4])

        self.admin_movie_price.delete(0, "end")
        self.admin_movie_price.insert(0, values[5])


    # =====================================================
    # ADD MOVIE
    # =====================================================

    def admin_add_movie(self):

        name = self.admin_movie_name.get().strip()
        genre = self.admin_movie_genre.get().strip()
        duration = self.admin_movie_duration.get().strip()
        rating = self.admin_movie_rating.get().strip()
        price = self.admin_movie_price.get().strip()

        if not all([
            name,
            genre,
            duration,
            rating,
            price
        ]):

            messagebox.showwarning(
                "Movie",
                "Please fill all movie fields."
            )

            return

        try:

            rating = float(rating)
            price = float(price)

        except ValueError:

            messagebox.showerror(
                "Movie",
                "Rating and price must be numbers."
            )

            return

        add_movie(
            name,
            genre,
            duration,
            rating,
            price
        )

        messagebox.showinfo(
            "Success",
            "Movie added successfully."
        )

        self.clear_movie_form()
        self.refresh_admin_movies()


    # =====================================================
    # UPDATE MOVIE
    # =====================================================

    def admin_update_movie(self):

        if not self.edit_movie_id:

            messagebox.showwarning(
                "Movie",
                "Select a movie first."
            )

            return

        name = self.admin_movie_name.get().strip()
        genre = self.admin_movie_genre.get().strip()
        duration = self.admin_movie_duration.get().strip()
        rating = self.admin_movie_rating.get().strip()
        price = self.admin_movie_price.get().strip()

        try:

            rating = float(rating)
            price = float(price)

        except ValueError:

            messagebox.showerror(
                "Movie",
                "Rating and price must be numbers."
            )

            return

        update_movie(
            self.edit_movie_id,
            name,
            genre,
            duration,
            rating,
            price
        )

        messagebox.showinfo(
            "Success",
            "Movie updated successfully."
        )

        self.clear_movie_form()
        self.refresh_admin_movies()


    # =====================================================
    # DELETE MOVIE
    # =====================================================

    def admin_delete_movie(self):

        if not self.edit_movie_id:

            messagebox.showwarning(
                "Movie",
                "Select a movie first."
            )

            return

        confirm = messagebox.askyesno(
            "Delete Movie",
            "Are you sure you want to delete this movie?"
        )

        if not confirm:
            return

        delete_movie(
            self.edit_movie_id
        )

        messagebox.showinfo(
            "Success",
            "Movie deleted successfully."
        )

        self.clear_movie_form()
        self.refresh_admin_movies()


    # =====================================================
    # CLEAR MOVIE FORM
    # =====================================================

    def clear_movie_form(self):

        for entry in [
            self.admin_movie_name,
            self.admin_movie_genre,
            self.admin_movie_duration,
            self.admin_movie_rating,
            self.admin_movie_price
        ]:

            entry.delete(
                0,
                "end"
            )

        self.edit_movie_id = None


    # =====================================================
    # ADMIN BOOKINGS
    # =====================================================

    def admin_bookings(self):

        self.clear_window()

        sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=230
        )

        sidebar.pack(
            side="left",
            fill="y"
        )

        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="👨‍💼",
            font=("Arial", 40),
            bg=SIDEBAR,
            fg=BLUE
        ).pack(pady=(35, 5))

        tk.Label(
            sidebar,
            text="ADMIN PANEL",
            font=("Arial", 18, "bold"),
            bg=SIDEBAR,
            fg=WHITE
        ).pack(pady=(0, 30))

        tk.Button(
            sidebar,
            text="📊 Dashboard",
            command=self.show_admin_dashboard,
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            fill="x",
            ipady=10
        )

        tk.Button(
            sidebar,
            text="🎬 Manage Movies",
            command=self.admin_movies,
            bg=SIDEBAR,
            fg=TEXT,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            fill="x",
            ipady=10
        )

        tk.Button(
            sidebar,
            text="🎟 All Bookings",
            command=self.admin_bookings,
            bg=CARD2,
            fg=WHITE,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            fill="x",
            ipady=10
        )

        tk.Button(
            sidebar,
            text="🚪 Logout",
            command=self.show_login,
            bg=SIDEBAR,
            fg=RED,
            activebackground=CARD2,
            relief="flat",
            bd=0,
            anchor="w",
            padx=25
        ).pack(
            side="bottom",
            fill="x",
            pady=20,
            ipady=10
        )

        content = tk.Frame(
            self.root,
            bg=BG
        )

        content.pack(
            side="right",
            fill="both",
            expand=True
        )

        tk.Label(
            content,
            text="All Customer Bookings",
            font=("Arial", 25, "bold"),
            bg=BG,
            fg=WHITE
        ).pack(
            anchor="w",
            padx=30,
            pady=25
        )

        bookings = get_all_bookings()

        table_frame = tk.Frame(
            content,
            bg=CARD
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=10
        )

        columns = (
            "Booking ID",
            "Customer",
            "Movie",
            "Date",
            "Time",
            "Seats",
            "Amount",
            "Booking Time"
        )

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column in columns:

            tree.heading(
                column,
                text=column
            )

            tree.column(
                column,
                width=115
            )

        for booking in bookings:

            tree.insert(
                "",
                "end",
                values=booking
            )

        tree.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


    # =====================================================
    # LOGOUT
    # =====================================================

    def logout(self):

        self.current_user = None
        self.selected_movie = None
        self.selected_seats = []

        self.show_login()


# =========================================================
# APPLICATION START
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = MovieBookingApp(root)

    root.mainloop()
