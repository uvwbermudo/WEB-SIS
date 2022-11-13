from flaskr import db 


class Students(db.Model):
    __tablename__ = 'students'
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    profile_pic = db.Column(db.String(240), nullable=True)
    course_code = db.Column(
        db.String(20),
        db.ForeignKey('courses.course_code', onupdate="CASCADE"), 
        nullable=True,
        )

    course = db.relationship('Courses', back_populates="students")

    def __repr__(self):
        return f"{self.id} - {self.last_name} {self.first_name}"
