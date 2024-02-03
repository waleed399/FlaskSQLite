from database import db


class Anime(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=False, nullable=False)
    description = db.Column(db.String(1000), unique=False, nullable=False)
    author = db.Column(db.String(20), unique=False, nullable=False)
    actors = db.Column(db.String, unique=False, nullable=False)
    release_year = db.Column(db.Integer, unique=False, nullable=False)
    image = db.Column(db.String, unique=False, nullable=False)
    reviews = db.relationship('Review', backref='anime', lazy=True)
