from flask import jsonify, request
from sqlalchemy import text
from api import api_bp
from extensions import db

def get_all_users():
    sql = text("SELECT id, username, email, role, profile FROM user")
    result = db.session.execute(sql)
    return [dict(row._mapping) for row in result]

def get_user_by_id(user_id):
    sql = text("SELECT id, username, email, role, profile FROM user WHERE id = :user_id")
    result = db.session.execute(sql, {"user_id": user_id}).fetchone()
    return dict(result._mapping) if result else None

@api_bp.get('/users', endpoint='get_users')
@api_bp.get('/user', endpoint='get_user_list')
def api_users():
    users = get_all_users()
    return jsonify(users)

@api_bp.get('/user/<int:user_id>', endpoint='get_user_by_id')
def api_user_detail(user_id):
    user = get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)
