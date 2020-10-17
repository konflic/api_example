from src.db import execute_sql
from flask import Blueprint, jsonify, make_response, session

delete_blueprint = Blueprint('delete', __name__)


@delete_blueprint.route('/api/delete/<username>')
def delete_user(username):
    if session.get("authorized"):
        execute_sql("DELETE FROM users WHERE name = ?;", (username,))
        return make_response(jsonify({"removed": username, "status": "ok"}), 201)
    else:
        return make_response(jsonify({"status": "error", "description": "not_authorized"}), 403)


@delete_blueprint.route("/api/delete/all")
def delete_all():
    if session.get("authorized"):
        execute_sql("DELETE FROM users WHERE name = ?;", (username,))
        return make_response(jsonify({"removed": username, "status": "ok"}), 201)
    else:
        return make_response(jsonify({"status": "error", "description": "not_authorized"}), 403)