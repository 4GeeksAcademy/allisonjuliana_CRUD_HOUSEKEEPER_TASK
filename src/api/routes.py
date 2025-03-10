from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, HouseKeeperTask, Room, HouseKeeper
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# CREATE a new HouseKeeperTask
@api.route('/housekeeper_task', methods=['POST'])
def create_housekeeper_task():
    data = request.get_json()
    
    # Validate if all required fields are in the request
    if not data.get('nombre') or not data.get('photo') or not data.get('condition') or not data.get('assignment_date') or not data.get('submission_date'):
        return jsonify({"error": "Missing required data"}), 400

    # Check if room and housekeeper IDs are valid
    room = Room.query.get(data.get('id_room'))
    housekeeper = HouseKeeper.query.get(data.get('id_housekeeper'))

    if not room or not housekeeper:
        return jsonify({"error": "Invalid room or housekeeper ID"}), 404

    # Create new HouseKeeperTask
    new_task = HouseKeeperTask(
        nombre=data['nombre'],
        photo=data['photo'],
        condition=data['condition'],
        assignment_date=data['assignment_date'],
        submission_date=data['submission_date'],
        id_room=data['id_room'],
        id_housekeeper=data['id_housekeeper']
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify(new_task.serialize()), 201

# READ all HouseKeeperTasks
@api.route('/housekeeper_tasks', methods=['GET'])
def get_all_housekeeper_tasks():
    tasks = HouseKeeperTask.query.all()
    return jsonify([task.serialize() for task in tasks]), 200

# READ a single HouseKeeperTask by ID
@api.route('/housekeeper_task/<int:id>', methods=['GET'])
def get_housekeeper_task(id):
    task = HouseKeeperTask.query.get(id)
    
    if task is None:
        return jsonify({"error": "HouseKeeperTask not found"}), 404
    
    return jsonify(task.serialize()), 200

# UPDATE a HouseKeeperTask by ID
@api.route('/housekeeper_task/<int:id>', methods=['PUT'])
def update_housekeeper_task(id):
    task = HouseKeeperTask.query.get(id)

    if task is None:
        return jsonify({"error": "HouseKeeperTask not found"}), 404
    
    data = request.get_json()

    # Update fields if they are provided in the request
    if data.get('nombre'):
        task.nombre = data['nombre']
    if data.get('photo'):
        task.photo = data['photo']
    if data.get('condition'):
        task.condition = data['condition']
    if data.get('assignment_date'):
        task.assignment_date = data['assignment_date']
    if data.get('submission_date'):
        task.submission_date = data['submission_date']
    if data.get('id_room'):
        task.id_room = data['id_room']
    if data.get('id_housekeeper'):
        task.id_housekeeper = data['id_housekeeper']

    db.session.commit()

    return jsonify(task.serialize()), 200

# DELETE a HouseKeeperTask by ID
@api.route('/housekeeper_task/<int:id>', methods=['DELETE'])
def delete_housekeeper_task(id):
    task = HouseKeeperTask.query.get(id)
    
    if task is None:
        return jsonify({"error": "HouseKeeperTask not found"}), 404
    
    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "HouseKeeperTask deleted successfully"}), 200


@api.route('/rooms', methods=['GET'])
def get_all_rooms():
    rooms = Room.query.all()
    return jsonify([room.serialize() for room in rooms]), 200


@api.route('/housekeepers', methods=['GET'])
def get_housekeepers():
    housekeepers = HouseKeeper.query.all()
    return jsonify([housekeeper.serialize() for housekeeper in housekeepers]), 200