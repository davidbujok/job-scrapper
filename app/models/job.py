from app import db

class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    about = db.Column(db.Text)
    websites_id = db.Column(db.Integer, db.ForeignKey( 'websites.id' ))

    def __repr__(self) -> str:
        return super().__repr__()
