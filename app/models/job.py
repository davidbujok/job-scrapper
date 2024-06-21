from app import db
from dataclasses import dataclass

@dataclass
class Job(db.Model):
    __tablename__ = "jobs"

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(db.String(255))
    position = db.Column(db.String(255))
    company = db.Column(db.String(255))
    location = db.Column(db.String(255))
    about = db.Column(db.Text, nullable=False)
    url = db.Column(db.String(2000))

    job_id = db.Column(db.String(255), unique=True)
    post_date = db.Column(db.DateTime)
    apply_status = db.Column(db.Boolean, default=False, nullable=False)
    hidden_status = db.Column(db.Boolean, default=False, nullable=False)
    websites_id = db.Column(db.Integer, db.ForeignKey("websites.id"))

    def __repr__(self) -> str:
        return super().__repr__()

    @classmethod
    def get_all_jobs(cls):
        jobs = db.session.execute(db.select(Job)
                                  .where(Job.hidden_status == 'f')
                                  .order_by(Job.post_date.desc())).scalars().all()
        return [job.serialize() for job in jobs]

    @classmethod
    def get_junior_jobs(cls):
        junior_jobs = db.session.execute(db.select(Job)
            .where(Job.level.ilike("%Entry%"))
            .order_by(Job.post_date.desc())) .scalars().all()
        return [job.serialize() for job in junior_jobs]
    
    @classmethod
    def hide_job(cls, id):
        job_to_hide = db.session.query(Job).filter(Job.id == id).scalar()
        if job_to_hide:
            job_to_hide.hidden_status = True
            db.session.commit()

    # @classmethod
    # def hide_job(cls, id):
    #     job_to_hide = db.session.execute(db.select(Job)
    #                    .where(Job.id == id)
    #                    .scalar())
    #     if job_to_hide:
    #         job_to_hide.hidden_status = True
    #         db.session.commit()

        # return [job.serialize() for job in queried_jobs]

    @classmethod
    def query_job(cls, query):
        queried_jobs = db.session.execute(db.select(Job)
                       .where(Job.level.contains(query.capitalize()))
                       .order_by(Job.post_date.desc())).scalars().all()
        return [job.serialize() for job in queried_jobs]

    # @classmethod
    def serialize(self):
        return {
            "id": self.id,
            "title": self.level,
            "position": self.position,
            "company": self.company,
            "location": self.location,
            "about": self.about,
            "url": self.url,
            "job": self.job_id,
            "post_date": self.post_date,
            "apply_status": self.hidden_status,
            "hidden_status": self.hidden_status,
            "websites_id": self.websites_id,
        }
