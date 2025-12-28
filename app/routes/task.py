from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.extensions import db
from app.models.task import Task

task_bp = Blueprint("task", __name__)

@task_bp.route("/", methods=["GET"])
@jwt_required()
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status
        } for t in tasks
    ])

@task_bp.route("/", methods=["POST"])
@jwt_required()
def create_task():
    data = request.json
    task = Task(
        title=data["title"],
        description=data["description"],
        status=data["status"]
    )
    db.session.add(task)
    db.session.commit()
    return jsonify(message="Task created")

@task_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_task(id):
    task = Task.query.get_or_404(id)
    data = request.json

    task.title = data["title"]
    task.description = data["description"]
    task.status = data["status"]

    db.session.commit()
    return jsonify(message="Task updated")

@task_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_task(id):
    task = Task.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify(message="Task deleted")
