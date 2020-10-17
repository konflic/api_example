from types import SimpleNamespace
from src.db import execute_sql
from src.settings import style
from flask import Blueprint, jsonify, make_response, session

delete_blueprint = Blueprint('delete', __name__)

routes = SimpleNamespace(
    root="/api/delete",
    all="/api/delete/all",
    name="/api/delete/name"
)

@delete_blueprint.route(routes.root, methods=["GET"])
def index():
    return f"""
    {style}
    <h2>Delete data</h2>
    <a href="/api">< BACK</a><br><br>
        <table>
        <tr>
            <th>uri</th>
            <th>method</th>
            <th>params</th>
            <th>description</th>
        </tr>
        <tr>
            <td><a href="{routes.all}">{routes.all}</a></td>
            <td>DELETE</td>
            <td>None</td>
            <td>Delete all users from table</td>
        </tr>
        <tr>
            <td><a href="{routes.name}">{routes.name}</a></td>
            <td>DELETE</td>
            <td>None</td>
            <td>Delete user with given name from table</td>
        </tr>
    </table>
    """

@delete_blueprint.route('/api/delete/<name>', methods=["DELETE"])
def delete_user(name):
    if session.get("authorized"):
        execute_sql("DELETE FROM users WHERE name = ?;", (name,))
        return make_response(jsonify({"removed": name, "status": "ok"}), 201)
    else:
        return make_response(jsonify({"status": "error", "description": "not_authorized"}), 403)


@delete_blueprint.route(routes.all, methods=["DELETE"])
def delete_all():
    if session.get("authorized"):
        execute_sql("DELETE FROM users;")
        return make_response({"removed": "everything", "status": "ok"}, 201)
    else:
        return make_response({"status": "error", "description": "not_authorized"}, 403)
