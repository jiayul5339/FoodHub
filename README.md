# FoodHub
## Video Demo:  [FoodHub](https://youtu.be/5iFk4ohBJlU)
## Description:
- > Recipe finder using the Spoonacular API. Built using the Flask framework.

- > Languages used: Python, HTML, CSS

- > Technologies used: Flask, SQL, Jinja, Bootstrap
![FoodHub1](https://user-images.githubusercontent.com/98488999/205149688-93e04628-b128-491e-ae0f-ddff9ed4ead8.JPG)
![FoodHub2](https://user-images.githubusercontent.com/98488999/205149700-748e3c9f-11eb-4900-b0db-f71651a8083b.JPG)
![FoodHub3](https://user-images.githubusercontent.com/98488999/205149708-593a8118-31ef-4611-b59e-93da12ff3b73.JPG)

### Backend:
- **app.py**: Contains code involved in the functionality of the application. This includes starting the Flask session and routes that take users to the different pages.
    - The routes include:
        - **login()**: Verifies username and password by comparing it to database
        - **register()**: Allows users to create an account. Verifies that username hasn't already been taken
        - **index()**: Main page, retrieves "search" input from user and renders index.html to display recipes.
        - **recipe()**: Retrieves a recipe id to make request to Spoonacular API for recipe information
        - **favorite()**: Renders a list of user's favorite recipes in alphabetical order. Can also receive a recipe id through POST method to add a recipe into the database.
        - **delete()**: Deletes recipe from database
        - **logout()**: Clears the user's current session

- **helpers.py**: Contains helper functions that assist app.py
    - Helper functions include:
        - **login_required()**: Checks if user is logged in into a session. Allows for functionality to only be available to logged in users.
        - **lookup(recipe)**: Receives a input parameter from user. The helper makes a request to the Spoonacular API to receive list of recipes
        - **getRecipeInfo(id)**: Receives a recipe id parameter. The helper will use that id to look for information on that recipe.

- **food.db**: Database storing a table of user information and their favorite recipes
    - Tables:
        - **users**: Each row is a user with columns storing their unique id, username, and hashed password
        - **favorites**: Each row is a contains a user's recipe that they favorited. The columns describe the recipe's user id, recipe name, recipe id, recipe image, and recipe url.

### Frontend:
- **layout.html**: Describes the primary layout of the webpage such as the navigation bar. Other html files will be based off of it.
- **login.html**: Main login page. Has input boxes for username and password.
- **register.html**: Allows users to create an account. Page has username, password, and confirmation password input boxes.
- **index.html**: Main page when user logs in. Contains search bar for user to search for recipes. If it receives a search input, it will display a grid of recipes with buttons to view each recipe.
- **recipes.html**: Displays the recipe including its image, name, and ingredients. This page has a button that leads users to the site containing the recipe. It also contains a favorite button which a user can click to save that recipe.
- **favorites.html**: This page shows a list of the user's favorite recipes. Renders the recipe image, recipe name, a link to the recipe, and a delete button.
- **styles.css**: Stylesheet for modifying page layout and aesthetic.
