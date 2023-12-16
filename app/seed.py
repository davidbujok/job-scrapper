import click
from flask.cli import with_appcontext
from app import db
from app.models.job import Job
from app.models.website import Website
from flask.cli import with_appcontext


@click.command(name='seed')
@with_appcontext
def seed():

    Job.query.delete()
    Website.query.delete()

    web1 = Website()
    web1.website = "www.goodjobs.com"
    db.session.add(web1)
    job1 = Job()
    job1.title = "Junior Developer"
    job1.about = "Great jobs with great people"
    db.session.add(job1)
    db.session.commit()
