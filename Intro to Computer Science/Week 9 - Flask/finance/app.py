import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime, timezone

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    stocks = db.execute("""
        SELECT symbol, price,
           SUM(CASE WHEN type = 0 THEN shares ELSE 0 END) -
           SUM(CASE WHEN type = 1 THEN shares ELSE 0 END) AS shares
        FROM transactions
        WHERE user_id = ?
        GROUP BY symbol
    """, session["user_id"])

    stocks = [stock for stock in stocks if stock["shares"] and stock["shares"] > 0]

    grand_total = 0
    for stock in stocks:
        stock["currentPrice"] = lookup(stock["symbol"])["price"]
        stock["total"] = stock["shares"] * stock["currentPrice"]
        grand_total += stock["total"]

    cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
    grand_total += cash

    stocks = [stock for stock in stocks if stock["shares"] > 0]

    return render_template("index.html", stocks=stocks, cash=cash, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    buy = 0

    if request.method == "POST":

        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except (TypeError, ValueError):
            return apology("must enter an integer number of shares", 400)

        if not symbol:
            return apology("must enter a symbol", 400)

        elif not shares:
            return apology("must enter a number of shares", 400)

        elif shares <= 0:
            return apology("must enter a positive number of shares", 400)

        elif lookup(symbol) is None:
            return apology("invalid symbol", 400)

        usersAvailableCash = db.execute(
            "SELECT cash FROM users WHERE id = ?", session["user_id"])[0]["cash"]
        price = lookup(symbol)["price"]
        netPrice = price * shares
        timestamp = datetime.now(timezone.utc).isoformat()

        if usersAvailableCash < netPrice:
            return apology("balance exceeded with request", 400)

        else:
            db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp, type) VALUES (?, ?, ?, ?, ?, ?)",
                       session["user_id"], symbol, shares, price, timestamp, buy
                       )
            db.execute("UPDATE users SET cash = cash - ? WHERE id = ?",
                       netPrice, session["user_id"])

            return redirect("/")

    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    stocks = db.execute(
        "SELECT symbol, shares, price, timestamp, type FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", stocks=stocks)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 400)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":

        if not request.form.get("symbol"):
            return apology("must enter a symbol", 400)

        quote = lookup(request.form.get("symbol"))
        if quote is None:
            return apology("invalid symbol", 400)

        return render_template("quoted.html", **quote)
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        if not request.form.get("username"):
            return apology("must provide username", 400)

        elif db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username")):
            return apology("username already exists", 400)

        elif not request.form.get("password"):
            return apology("must provide password", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("password must be the same as confirmation", 400)

        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", request.form.get(
            "username"), generate_password_hash(request.form.get("password")))

        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    sell = 1

    if request.method == "POST":

        symbol = request.form.get("symbol")

        try:
            shares = int(request.form.get("shares"))
        except (ValueError, TypeError):
            return apology("Invalid number of shares", 400)

        if not symbol:
            return apology("no stock selected", 400)

        if int(shares) < 1:
            return apology("must enter a positive integer amount of shares", 400)

        row = db.execute("""
            SELECT
                SUM(CASE WHEN type = 0 THEN shares ELSE 0 END) AS total_bought,
                SUM(CASE WHEN type = 1 THEN shares ELSE 0 END) AS total_sold
            FROM transactions
            WHERE user_id = ? AND symbol = ?
        """, session["user_id"], symbol)[0]

        total_bought = row["total_bought"] or 0
        total_sold = row["total_sold"] or 0

        available_shares = total_bought - total_sold

        if available_shares <= 0:
            return apology("no shares of that stock", 400)

        if available_shares < shares:
            return apology("not enough shares of that stock", 400)

        price = lookup(symbol)["price"]
        netPrice = price * shares
        timestamp = datetime.now(timezone.utc).isoformat()

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, timestamp, type) VALUES (?, ?, ?, ?, ?, ?)",
                   session["user_id"], symbol, shares, price, timestamp, sell
                   )

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", netPrice, session["user_id"])

        return redirect("/")

    else:

        rows = db.execute("""
            SELECT symbol,
                SUM(CASE WHEN type = 0 THEN shares ELSE 0 END) AS total_bought,
                SUM(CASE WHEN type = 1 THEN shares ELSE 0 END) AS total_sold
            FROM transactions
            WHERE user_id = ?
            GROUP BY symbol
            HAVING (total_bought - total_sold) > 0
        """, session["user_id"])

        return render_template("sell.html", symbols=rows)


@app.route("/add_balance", methods=["GET", "POST"])
@login_required
def addBalance():
    """Add additional cash to account"""

    add = 2

    if request.method == "POST":
        if "cardNumber" in request.form:
            cardNumber = request.form.get("cardNumber")
            expiryDate = request.form.get("expiryDate")
            securityCode = request.form.get("securityCode")

            if not cardNumber or len(cardNumber) != 16 or not cardNumber.isdigit():
                return apology("Invalid card number", 400)

            if not expiryDate:
                return apology("Enter expiry date", 400)

            if not securityCode or len(securityCode) != 3 or not securityCode.isdigit():
                return apology("Invalid security code", 400)

            paymentDetails = generate_password_hash(cardNumber + expiryDate + securityCode)
            db.execute("UPDATE users SET paymentMethod = ? WHERE id = ?",
                       paymentDetails, session["user_id"])

            return redirect("/add_balance")

        amount = request.form.get("amount")
        timestamp = datetime.now(timezone.utc).isoformat()

        if not amount or not amount.isdigit() or int(amount) <= 0:
            return apology("Enter a valid amount", 400)

        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?", int(amount), session["user_id"])
        db.execute("INSERT INTO transactions (user_id, price, timestamp, type) VALUES (?, ?, ?, ?)",
                   session["user_id"], int(amount), timestamp, add)

        return redirect("/")

    result = db.execute("SELECT paymentMethod FROM users WHERE id = ?", session["user_id"])
    if not result or not result[0]["paymentMethod"]:
        return render_template("registerPaymentDetails.html")
    else:
        return render_template("addBalance.html")


@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change():
    """Change account password"""

    if request.method == "POST":

        oldPassword = request.form.get("oldPassword")
        newPassword = request.form.get("newPassword")
        confirmation = request.form.get("confirmation")

        if not oldPassword:
            return apology("must enter old password", 400)

        hash = db.execute("SELECT hash FROM users WHERE id = ?", session["user_id"])

        if generate_password_hash(oldPassword) != hash:
            return apology("must enter correct old password", 400)

        elif not newPassword:
            return apology("must enter new password", 400)

        elif newPassword != confirmation:
            return apology("new password must be the same as confirmation", 400)

        db.execute("UPDATE users SET hash = ? WHERE id = ?",
                   generate_password_hash(newPassword), session["user_id"])
        return redirect("/")

    else:
        return render_template("changePassword.html")
