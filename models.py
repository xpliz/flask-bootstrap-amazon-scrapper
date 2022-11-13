from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Scrapper(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  title = db.Column(db.String(50))
  price = db.Column(db.String(20))
  reviews = db.Column(db.String(50))
  availability = db.Column(db.String(50))