from marshmallow import Schema, fields, validates_schema, ValidationError

try:
    from .models import Exercise, Workout, WorkoutExercises
except ImportError:
    from models import Exercise, Workout, WorkoutExercises


class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    category = fields.Str(required=True)
    equipment_needed = fields.Bool()

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.DateTime(required=True)
    duration_minutes = fields.Int(required=True)
    notes = fields.Str()

    @validates_schema
    def validate_duration(self, data, **kwargs):
        if data.get("duration_minutes") and data["duration_minutes"] > 300:
            raise ValidationError("Workout duration cannot exceed 300 minutes.")


class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(required=False)
    sets = fields.Int(required=False)
    duration_seconds = fields.Int(required=False)


    @validates_schema
    def validate_reps_sets(self, data, **kwargs):
        if data.get("reps") is None or data.get("sets") is None:
            raise ValidationError("Both reps and sets are required.")
