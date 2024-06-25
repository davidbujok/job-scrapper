from app import db
from dataclasses import dataclass

@dataclass
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    job = db.Column(db.String(255))
    location = db.Column(db.String(255))

    def __repr__(self) -> str:
        return super().__repr__()

    def serialize(self):
        return {
            "id": self.id,
            "job": self.job,
            "location": self.location,
        }

    @classmethod
    def get_user_jobs(cls, id):
        try:
            user_data = db.session.execute(db.select(User).where(User.id == id)).scalar_one_or_none()
            return user_data.serialize() if user_data else None
        except Exception as e:
            # handle or log the exception, return None or appropriate error response
            print(f'Error: {e}')
            return None

