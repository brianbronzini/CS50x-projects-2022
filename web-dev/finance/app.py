import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
# datetime added to track current time of purchases and sales of stock
import datetime

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


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

    # Remember session for current user
    id_of_user = session["user_id"]

    # Get all user transactions of purchased shares
    db_user_transact = db.execute("""SELECT symbol,
                                     SUM(shares) AS shares, price
                                     FROM transactions
                                     WHERE user_id = ?
                                     GROUP BY symbol""", id_of_user)

    # Check cash of current user
    db_user_cash = db.execute("""SELECT cash
                                 FROM users
                                 WHERE id = ?""", id_of_user)
    user_cash = db_user_cash[0]["cash"]

    # Display current user's owned stock on homepage
    return render_template("index.html", database=db_user_transact, user_cash=user_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Get user input
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("Number must be integer")

        # Check validity of user input for symbol
        if not symbol:
            return apology("the 'Symbol' input field cannot be blank")

        # Convert stock ticker to uppercase
        stock = lookup(symbol.upper())

        # Check if stock symbol exists
        if stock == None:
            return apology(f"the ticker '{symbol}' does not exist")

        # Check that the number of shares entered is positive
        if shares <= 0:
            return apology("the number of shares must be greater than zero and cannot be blank")

        # Check current stock price
        stock_value = round(stock["price"], 2)

        # Check cost of shares purchased
        transaction = shares * stock_value

        # Remember session for current user
        id_of_user = session["user_id"]

        # Check cash of current user
        db_user_cash = db.execute("""SELECT cash
                                     FROM users
                                     WHERE id = ?""", id_of_user)
        user_cash = db_user_cash[0]["cash"]

        # Check if user can afford to purchase shares
        if user_cash < transaction:
            return apology("not enough funds.")

        # Update user cash after purchase of shares
        update_cash = user_cash - transaction

        # Update the 'users' table with remaining cash
        db.execute(
            """UPDATE users
            SET cash = ?
            WHERE id = ?""", update_cash, id_of_user)
        # UPDATE table_name SET column1 = value1 WHERE condition;

        # Check time and date of purchase
        current_date = datetime.datetime.now()

        # Update 'transactions' table for purchase of shares
        db.execute(
            """INSERT INTO transactions (user_id, symbol, shares, price, date)
            VALUES (?, ?, ?, ?, ?)""", id_of_user, stock["symbol"], shares, stock["price"], current_date)

        # Provide feedback to user upon purchase
        flash(
            f"Congrats! You have purchased {shares} share(s) of {symbol.upper()} at {usd(stock_value)} per share for a total of {usd(transaction)}")

        return redirect("/")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    # Remember session for current use
    id_of_user = session["user_id"]

    # Display history of all transactions by the user
    transactions = db.execute("""SELECT *
                                 FROM transactions
                                 WHERE user_id = ?""", id_of_user)

    return render_template("history.html", transactions=transactions)


@app.route("/add_cash", methods=["GET", "POST"])
@login_required
def add_cash():
    """User can add cash"""
    if request.method == "GET":
        return render_template("add.html")
    else:
        # Get user input
        cash_amount = int(request.form.get("cash_amount"))
        # 'int' converts input string to a number

        # Check validity of user input
        if not cash_amount:
            return apology("cash amount in invalid")

        # Remember session for current user
        id_of_user = session["user_id"]

        # Check cash of current user
        db_user_cash = db.execute("""SELECT cash
                                     FROM users
                                     WHERE id = ?""", id_of_user)
        user_cash = db_user_cash[0]["cash"]

        # Update user cash with new cash amount
        update_cash = user_cash + cash_amount

        # Update the 'users' table with remaining cash
        db.execute("UPDATE users SET cash = ? WHERE id = ?", update_cash, id_of_user)

        flash(f"Success! You have added ${cash_amount} to your account.")

        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("""SELECT *
                             FROM users
                             WHERE username = ?""", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    else:
        # Get user input
        symbol = request.form.get("symbol")

        # Check validity of user input
        if not symbol:
            return apology("must provide valid symbol")

        # Convert stock ticker to uppercase
        stock = lookup(symbol.upper())

        # Check if stock symbol exists
        if stock == None:
            return apology(f"the ticker '{symbol}' does not exist")

        # Pass parameters (name, price, and symbol) from helpers.py into quoted-stock.html
        return render_template("quoted-stock.html", name=stock["name"], price=stock["price"], symbol=stock["symbol"])


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Get user input
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check validity of user input
        if not username:
            return apology("username is invalid")

        if not password:
            return apology("password is invalid")

        if not confirmation:
            return apology("")

        if password != confirmation:
            return apology("passwords do not match")

        # Convert password to hash
        hash_password = generate_password_hash(password)

        # Update database with new user and hash
        try:
            new_user = db.execute("""INSERT INTO users (username, hash)
                                     VALUES (?, ?)""", username, hash_password)

        # Check if username already exists
        except:
            return apology(f"The username {username} already exists")

        # Remember user session
        session["user_id"] = new_user

        flash("You are registered!")

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        # Remember session for current user
        id_of_user = session["user_id"]

        # Get all symbols that the user owns
        owned_symbols = db.execute("""SELECT symbol
                                      FROM transactions
                                      WHERE user_id = ?
                                      GROUP BY symbol
                                      HAVING SUM(shares) > 0""", id_of_user)

        return render_template("sell.html", symbols=[row["symbol"] for row in owned_symbols])
        # For loop iterates and sends the symbol to each row in the 'Symbol' column

    # User reached route via POST (as by submitting a form via POST)
    else:
        # Get user input
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        # 'int' converts input string to a number

        # Check validity of user input
        if not symbol:
            return apology("must provide symbol")

        # Convert stock ticker to uppercase
        stock = lookup(symbol.upper())

        # Check if stock symbol exists
        if stock == None:
            return apology(f"the ticker '{symbol}' does not exist")

        # Check that the number of shares entered is positive
        if shares <= 0:
            return apology("the number of shares must be greater than zero and cannot be blank")

        # Check current stock price
        stock_value = round(stock["price"], 2)

        # Check earnings of shares sold
        transaction = shares * stock_value

        # Remember session for current user
        id_of_user = session["user_id"]

        # Check cash of current user
        db_user_cash = db.execute("""SELECT cash
                                     FROM users
                                     WHERE id = ?""", id_of_user)
        user_cash = db_user_cash[0]["cash"]

        # Check the number of shares the user owns by symbol
        user_shares = db.execute("""SELECT SUM(shares) AS shares
                                    FROM transactions
                                    WHERE user_id = ? AND symbol = ?""", id_of_user, symbol)
        user_shares_actual = user_shares[0]["shares"]

        # Check if user has enough of the specified shares to sell
        if shares > user_shares_actual:
            return apology("insufficient number of shares to sell")

        # Ensure user gets cash from sale
        update_cash = user_cash + transaction

        # Update the 'users' table with remaining cash
        db.execute("""UPDATE users
                      SET cash = ?
                      WHERE id = ?""", update_cash, id_of_user)

        # Check time of sale
        current_date = datetime.datetime.now()

        # Update 'transactions' table for sale of shares
        db.execute("""INSERT INTO transactions (user_id, symbol, shares, price, date)
                      VALUES (?, ?, ?, ?, ?)""", id_of_user, stock["symbol"], (-1)*shares, stock["price"], current_date)

        # Provide feedback to user upon sale
        flash(
            f"Sale Complete! You have sold {shares} share(s) of {symbol} at {usd(stock_value)} per share for a total of {usd(transaction)}")

        return redirect("/")