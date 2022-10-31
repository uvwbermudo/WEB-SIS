from flaskr import db 


class Colleges(db.Model):
    __tablename__ = 'colleges'
    college_code = db.Column(db.String(20), primary_key=True, nullable=False)
    college_name = db.Column(db.String(100), nullable=False, unique=True)
    courses = db.relationship('Courses', back_populates ="college")

    def __str__(self):
        return f"{self.college_code} - {self.college_name}"