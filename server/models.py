from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from datetime import datetime

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = 'exercises'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    category = db.Column(db.String)
    equipment_needed = db.Column(db.Boolean)

    workout_exercises = db.relationship('WorkoutExercises', back_populates = 'exercise', cascade="all, delete-orphan")

    # Exercise validators
    @validates('name')
    def validate_name(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Name cannot be empty")
        return value

    @validates('category')        
    def validate_category(self, key, value):
        if not value or value.strip() == "":
            raise ValueError("Category cannot be empty")
        return value


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Integer)
    notes = db.Column(db.Text)

    workout_exercises = db.relationship('WorkoutExercises', back_populates = 'workout', cascade="all, delete-orphan")

    # Workout validators
    @validates('duration_minutes')
    def validate_duration_minutes(self, key, value):
        if value < 0:
            raise ValueError("duration_minutes must be greater than 0")
        return value
    
    @validates('date')
    def validate_date(self, key, value):
        if not value:
            raise ValueError("Date cannot be empty")
        if not isinstance(value, datetime):
            raise ValueError("Invalid date format")
        return value

# Join Table
class WorkoutExercises (db.Model):
    __tablename__ = 'workout_exercises' 

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id")) 
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id")) 
    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = db.relationship("Workout", back_populates="workout_exercises")
    exercise = db.relationship("Exercise", back_populates="workout_exercises")

    # WorkoutExercises validators

    @validates('reps')
    def validate_reps(self, key, value):
        if value < 0:
            raise ValueError("Must be greater than 0")
        return value
    
    @validates('sets')
    def validate_sets(self, key, value):
        if value < 0:
            raise ValueError("Must be greater than 0")
        return value
    
    __table_args__ = (
    CheckConstraint('reps > 0', name='check_reps_positive'),
    CheckConstraint('sets > 0', name='check_sets_positive'),
)


