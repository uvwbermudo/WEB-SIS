from flaskr import db 


class Courses(db.Model):
    __tablename__ = 'courses'
    course_code = db.Column(db.String(20), primary_key=True, nullable=False)
    course_name = db.Column(db.String(100), nullable=False, unique=True)
    college_code = db.Column(
        db.String(25), 
        db.ForeignKey('colleges.college_code', onupdate="CASCADE"), 
        nullable=True, 
        )

    college = db.relationship('Colleges', back_populates="courses")
    students = db.relationship('Students', back_populates ="course")

    def __repr__(self):
        return f"{self.course_code} - {self.course_name}"