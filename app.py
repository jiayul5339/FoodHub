import os
import datetime
import webbrowser
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import lookup, login_required, getRecipeInfo

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///food.db")

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
    try:
        # Retrieve "search"
        search = lookup(request.args.get("search"))
        # Get recipes what was searched for
        recipes = search["results"]
        return render_template("index.html", recipes=recipes)

    except:
        # Normal index template
        return render_template("index.html")


@app.route("/recipe", methods=["GET", "POST"])
@login_required
def recipe():
    # Get specfic recipe information from recipe id
    recipeInfo = getRecipeInfo(request.args.get("id"))
    # Collect its ingredient and id information
    ingredients = recipeInfo["extendedIngredients"]
    id = recipeInfo["id"]
    # Render the recipe page with recipes displayed
    return render_template("recipes.html", recipeInfo=recipeInfo, ingredients=ingredients, id=id)

@app.route("/favorite", methods=["GET", "POST"])
@login_required
def favorite():
    if request.method == "POST":
        try:
            # Get recipe id to be favorited
            recipeId = request.form.get("id")
            # Retrieve its informationa
            recipeInfo = getRecipeInfo(recipeId)
            # Insert into the favorites database
            db.execute("INSERT INTO favorites (user_id, recipe_id, recipe_name, recipe_image, recipe_url) VALUES (?, ?, ?, ?, ?)", session["user_id"], recipeInfo["id"], recipeInfo["title"], recipeInfo["image"], recipeInfo["sourceUrl"])
            # Return to home page
            return redirect("/")

        except:
            return redirect("/")
    else:
        # Retrieve favorite recipes from favorites database
        favRecipes = db.execute("SELECT recipe_id, recipe_name, recipe_image, recipe_url FROM favorites WHERE user_id = ? ORDER BY recipe_name ASC ", session["user_id"])
        # Render favorite recipes
        return render_template("favorites.html", favRecipes=favRecipes)

@app.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    if request.method == "POST":
        try:
            # Retrieve recipe id of recipe to be deleted
            recipeId = request.form.get("id")
            # Delete recipe from database
            db.execute("DELETE FROM favorites WHERE recipe_id = ? AND user_id = ?", recipeId, session["user_id"])
            return redirect("/favorite")
        except:
            return redirect("/favorite")
            
    else:
        return redirect("/favorite")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        error1 = "Please enter a username and/or password"
        # Ensure username and password was submitted
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("/login.html", error=error1)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        error2 = "Username and/or password was incorrect"
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return render_template("/login.html", error=error2)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    # Register user
    # Check if method is GET or POST
    if request.method == "POST":
        # Get user inputed username and password
        username = request.form.get("username")
        password = request.form.get("password")
        # Hash user's password
        hashPass = generate_password_hash(password)
        # Check if username and password is valid, and if confirm password matches
        error1 = "Please enter a username and/or password"
        error2 = "Your passwords do not match"
        if not username or not request.form.get("password"):
            return render_template("register.html", error=error1)
        if not (password == request.form.get("confirmation")):
            return render_template("register.html", error=error2)

        # Check if username has already been taken
        error3 = "Sorry, username has already been taken"
        rows = db.execute("SELECT * FROM users WHERE username = ?", username, )
        if len(rows) == 0:
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, hashPass)
            return redirect("/")
        else:
            return render_template("register.html", error=error3)
    # If method is GET
    return render_template("register.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
