from app import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(255))
    position = db.Column(db.String(255))
    details = db.Column(db.String(255))
    about = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(255))
    websites_id = db.Column(db.Integer, db.ForeignKey( 'websites.id' ))

    def __repr__(self) -> str:
        return super().__repr__()
