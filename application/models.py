from app import db


class Jobs(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    created_date = db.Column(db.DateTime)
    description = db.Column(db.String)
    salary = db.Column(db.Integer)

    def __repr__(self):
        return f'<Job ID: {self.id} Name: {self.name}>'
