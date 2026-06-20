from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import Workout, WorkoutExercises, db, Exercise
from schemas import ExerciseSchema, WorkoutExerciseSchema, WorkoutSchema

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

# Schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
workout_exercises_schema = WorkoutExerciseSchema(many=True)


@app.route("/")
def home():
    return {"message": "Workout API running!"}


# WORKOUT ROUTES
@app.route("/workouts")
def get_all_workouts():
    workouts = Workout.query.all()
    result = workouts_schema.dump(workouts)
    return result, 200


@app.route("/workouts/<int:id>")
def get_workout_by_id(id):
    workout = Workout.query.get_or_404(id)
    result = workout_schema.dump(workout)
    return result, 200


@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    new_workout = Workout(
        date=data.get("date"),
        duration_minutes=data.get("duration_minutes"),
        notes=data.get("notes"),
    )
    db.session.add(new_workout)
    # Commit change to the db
    db.session.commit()

    result = workout_schema.dump(new_workout)
    return result, 201


@app.route("/workouts/<int:id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get_or_404(id)
    db.session.delete(workout)
    db.session.commit()
    return {"message": "Workout deleted"}, 200


# EXERCISE ROUTES
@app.route("/exercises")
def get_all_exercises():
    exercises = Exercise.query.all()
    result = exercises_schema.dump(exercises)
    return result, 200


@app.route("/exercises/<int:id>")
def get_exercise_by_id(id):
    exercise = Exercise.query.get_or_404(id)
    result = exercise_schema.dump(exercise)
    return result, 200


@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()
    new_exercise = Exercise (
        name=data.get("name"),
        category=data.get("category"),
        equipment_needed=data.get("equipment_needed"),
    )
    db.session.add(new_exercise)
    db.session.commit()
    result = exercise_schema.dump(new_exercise)
    return result, 201

@app.route("/exercises/<int:id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get_or_404(id)
    db.session.delete(exercise)
    db.session.commit()
    return {"message": "Exercise deleted"}, 200


# WORKOUT_EXERCISE ROUTES
@app.route(
    "/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises",
    methods=["POST"],
)
def add_exercise_to_workout(workout_id, exercise_id):
    data = request.get_json()
    new_workout_exercise = WorkoutExercises(
        workout_id = workout_id,
        exercise_id = exercise_id,
        reps = data.get("reps"),
        sets = data.get("sets"),
        duration_seconds = data.get("duration_seconds"),
    )
    db.session.add(new_workout_exercise)
    db.session.commit()
    result = workout_exercises_schema.dump(new_workout_exercise)
    return result, 201


@app.route("/workout_exercises/<int:id>", methods=["DELETE"])
def delete_workout_exercise(id):
    workout_exercise = WorkoutExercises.query.get_or_404(id)
    db.session.delete(workout_exercise)
    db.session.commit()
    # This helps the frontend confirm which join‑table row was deleted.
    return {
    "message": f"WorkoutExercise with id {id} has been deleted."
    }, 200



if __name__ == "__main__":
    app.run(debug=True)