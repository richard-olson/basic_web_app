from basic_web_app import db


class Job(db.Model):
    __tablename__ = "jobs"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=False, nullable=False)
    created_date = db.Column(db.DateTime, unique=False, nullable=False)
    description = db.Column(db.String(320), unique=False, nullable=False)
    salary = db.Column(db.Integer, unique=False, nullable=False)
    employer = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return f"<Job ID: {self.id} Name: {self.name}>"
