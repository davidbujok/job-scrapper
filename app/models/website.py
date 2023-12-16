from app import db

class Website(db.Model):

    __tablename__ = 'websites'

    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255), unique=True, nullable=False)
