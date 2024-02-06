from database import db


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    review_text = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    anime_id = db.Column(db.Integer, db.ForeignKey('anime.id', ondelete='CASCADE'), nullable=False)


def __repr__(self):
    return f"Review(id={self.id}, text={self.text})"
