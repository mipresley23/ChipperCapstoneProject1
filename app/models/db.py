from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), nullable=False, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    hashed_password = db.Column(db.String(255), nullable=False)
    profile_pic = db.Column(db.String(2000), nullable=True)

    chirps = db.relationship("Chirp", back_populates="user")
    comments = db.relationship("Comment", back_populates="user")

    @property
    def password(self):
        return self.hashed_password

    @password.setter
    def password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'profile_pic': self.profile_pic
        }


class Chirp(db.Model):
  __tablename__ = 'chirps'

  id = db.Column(db.Integer, primary_key=True)
  media = db.Column(db.String(2000), nullable=True)
  body = db.Column(db.String(300), nullable=True)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

  user = db.relationship("User", back_populates='chirps')
  comments = db.relationship("Comment", back_populates='chirps', cascade='all, delete')


  def to_dict(self):
    return{
      "id": self.id,
      "media": self.media,
      "body": self.body,
      "user": self.user.to_dict()
    }

class Comment(db.Model):
  __tablename__ = 'comments'

  id = db.Column(db.Integer, primary_key=True)
  media = db.Column(db.String(2000), nullable=True)
  body = db.Column(db.String(300), nullable=True)
  userId = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
  chirpId = db.Column(db.Integer, db.ForeignKey('chirps.id'), nullable=False)

  user = db.relationship("User", back_populates='comments')
  chirps = db.relationship("Chirp", back_populates='comments')

  def to_dict(self):
    return{
      "id": self.id,
      "media": self.media,
      "body": self.body,
      "user": self.user.to_dict(),
      "chirpId": self.chirpId
    }
