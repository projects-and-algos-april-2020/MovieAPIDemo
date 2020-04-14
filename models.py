from app import db
from sqlalchemy.sql import func

# some_user.posts => [Post, Post]
class User(db.Model):	
    __tablename__ = "users"    # optional		
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())

    reviews = db.relationship("Review", back_populates="author", cascade="all, delete, delete-orphan")

    def __repr__(self):
        return f"<User: {self.email}>"

class Review(db.Model):
    __tablename__ = "reviews"    # optional
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255))
    movie_api_id = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship('User', foreign_keys=[author_id])
    created_at = db.Column(db.DateTime, server_default=func.now())    # notice the extra import statement above
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())