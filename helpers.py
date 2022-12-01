import os
import requests
import urllib.parse

from flask import redirect, session
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup(recipe):
    """Look up recipe information."""
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.spoonacular.com/recipes/complexSearch?query={recipe}&number=100&apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        results = response.json()
        return {
            "results": results["results"]
        }
    except (KeyError, TypeError, ValueError):
        return None

def getRecipeInfo(id):
    # Contact API
    try:
        api_key = os.environ.get("API_KEY")
        url = f"https://api.spoonacular.com/recipes/{id}/information?apiKey={api_key}"
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        results = response.json()
        return {
            "id": results["id"],
            "title": results["title"],
            "image": results["image"],
            "sourceUrl": results["sourceUrl"],
            "extendedIngredients": results["extendedIngredients"]
        }
    except (KeyError, TypeError, ValueError):
        return None
