from flask import jsonify, request
from app import app, db
from app.models import User
from flask_jwt_extended import create_access_token
import datetime
from flask_cors import CORS


CORS(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(username=data['username'], email=data['email'])
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"message": "Missing required fields"}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity={'username': user.username, 'email': user.email}, expires_delta=datetime.timedelta(days=1))
    return jsonify(access_token=access_token), 200
