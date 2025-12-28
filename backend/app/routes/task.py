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
    try:
        data = request.json
        print('CREATE_TASK headers:', dict(request.headers))
        print('CREATE_TASK body:', data)

        task = Task(
            title=data.get("title"),
            description=data.get("description"),
            status=data.get("status")
        )
        db.session.add(task)
        db.session.commit()
        return jsonify(message="Task created")
    except Exception as e:
        print('CREATE_TASK error:', e)
        return jsonify(message="Failed to create task", error=str(e)), 500

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
