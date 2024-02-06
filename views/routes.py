# routes.py

from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

from database import app, db
from models.Anime import Anime
from models.Review import Review
from models.User import User


def setup_routes():
    @app.route("/")
    def homepage():

        anime_list = Anime.query.all()
        user_is_active = session.get('user_is_active', False)
        if user_is_active:
            username = User.query.filter_by(is_active=True).first().username
            return render_template("homepage.html", anime_list=anime_list, user_is_active=user_is_active, username=username)

        return render_template("homepage.html", anime_list=anime_list, user_is_active=user_is_active)


@app.route("/series_display/<int:anime_id>/<int:user_is_active>")
def series_display(anime_id, user_is_active):
    anime = Anime.query.filter_by(id=anime_id).first()
    reviews = Review.query.filter_by(anime_id=anime_id).all()
    return render_template("anime_details.html", anime=anime, user_is_active=user_is_active, reviews=reviews)


@app.route('/show_login')
def show_login():
    return render_template('login.html')


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        # Process the form data here
        usernames = [user.username for user in User.query.all()]
        username = request.form['username']
        password = request.form['password']
        confirmed_pass = request.form['confirm_password']
        # Perform registration logic, e.g., save to the database
        if len(password) < 8:
            flash('Password must be more than 8 characters', 'error')
            return redirect(url_for('register'))
        if username not in usernames and confirmed_pass == password:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            curr_user = User(username=username, password=hashed_password)
            db.session.add(curr_user)
            db.session.commit()
            # Redirect to a different page after successful registration
            return redirect(url_for('login'))
        else:
            flash('Username already exists. Please choose a different one.', 'error')
            return redirect(url_for('register'))

    # If the request is GET, simply render the registration form
    return render_template('register.html')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
                # Successful login, redirect to the homepage
            user.is_active = True
            db.session.commit()
            session['user_is_active'] = user.is_active
            return redirect(url_for('homepage'))
        else:
             # Invalid credentials, display an error message
            error_message = "Invalid username or password. Please try again."
            flash(error_message, 'error')
            return render_template("login.html", error_message=error_message)

        # Render the login form for GET requests
    return render_template("login.html", error_message=None)


@app.route("/logout", methods=['GET'])
def logout():
    user = User.query.filter_by(is_active=True).first()

    user.is_active = False
    db.session.commit()
    session['user_is_active'] = False

    # Redirect to the homepage or login page
    return redirect(url_for('homepage'))


@app.route("/add_review/<int:anime_id>", methods=['GET', 'POST'])
def add_review(anime_id):
    if request.method == 'POST':
        review_text = request.form.get('review_text')
        user = User.query.filter_by(is_active=True).first()

        if user:
            # Assuming you have the User ID and Anime ID
            user_id = user.id
            anime = Anime.query.get(anime_id)
            if anime:
                review = Review(review_text=review_text, user_id=user_id, anime_id=anime_id)
                db.session.add(review)
                db.session.commit()
    # Redirect to the anime details page
    reviews = Review.query.filter_by(anime_id = anime_id).all()
    anime_list = Anime.query.all()
    return render_template("anime_details.html", anime=anime_list[anime_id-1], user_is_active=user.is_active, reviews=reviews)


@app.route('/add_anime', methods=['GET', 'POST'])
def add_anime():
    if request.method == 'POST':
        # Get data from the form
        name = request.form.get('name')
        description = request.form.get('description')
        author = request.form.get('author')
        actors = request.form.get('actors')
        release_year = request.form.get('release_year')
        image = request.form.get('image')

        # Create a new Anime instance
        new_anime = Anime(name=name, description=description, author=author, actors=actors, release_year=release_year, image=image)

        # Add the new anime to the database
        db.session.add(new_anime)
        db.session.commit()

        return redirect(url_for('homepage'))  # Redirect to the home page after adding the anime

    return render_template('add_anime.html')


@app.route('/delete_anime/<int:anime_id>', methods=['POST'])
def delete_anime(anime_id):

    anime = Anime.query.get(anime_id)

    # Check if the anime exists
    if anime:
        # Delete the anime from the database
        db.session.delete(anime)
        db.session.commit()

    # Redirect to the anime list page
    return redirect(url_for('homepage'))
