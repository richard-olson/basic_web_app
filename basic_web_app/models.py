from . import db


class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    created_date = db.Column(db.DateTime)
    description = db.Column(db.String(160))
    salary = db.Column(db.Integer)
    employer = db.Column(db.String(64))

    def __repr__(self):
        return f'<Job ID: {self.id} Name: {self.name}>'
