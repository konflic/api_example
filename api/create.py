from src.settings import style
from types import SimpleNamespace
from flask import Blueprint, jsonify, session, make_response
from src.db import execute_sql

sql_create = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        surname TEXT NOT NULL,
        grade INTEGER NOT NULL
    );
"""

sql_drop = "DROP TABLE IF EXISTS users;"

create_blueprint = Blueprint('create', __name__)

routes = SimpleNamespace(
    root="/api/create",
    init="/api/create/init",
    reinit="/api/create/reinit"
)


@create_blueprint.route(routes.root)
def create():
    return f"""
    {style}
    <h2>Create endpoint</h2>
    <a href="/api">< BACK</a><br><br>
    <table>
        <tr>
            <th>uri</th>
            <th>method</th>
            <th>params</th>
            <th>description</th>
        </tr>
        <tr>
            <td><a href="{routes.init}">{routes.init}</a></td>
            <td>CREATE</td>
            <td>None</td>
            <td>Creating database if exists</td>
        </tr>
        <tr>
            <td><a href="{routes.reinit}">{routes.reinit}</a></td>
            <td>CREATE</td>
            <td>None</td>
            <td>Remove and create new database</td>
        </tr>
    </table>
    """


@create_blueprint.route('/api/create/init', methods=["CREATE"])
def init():
    if session.get("authorized"):
        try:
            execute_sql(sql_create)
        except Exception as e:
            return make_response(jsonify({"status": "error", "error": str(e)}), 400)
        else:
            return make_response(jsonify({"status": "created"}), 201)
    else:
        return make_response(jsonify({"status": "error", "description": "authorization_required"}), 403)


@create_blueprint.route('/api/create/reinit', methods=["CREATE"])
def reinit():
    if session.get("authorized"):
        try:
            execute_sql(sql_drop)
            execute_sql(sql_create)
        except Exception as e:
            return jsonify({"status": "error", "error": str(e)})
        else:
            return jsonify({"status": "table dropped and created"})
    else:
        return make_response(jsonify({"status": "error", "description": "authorization_required"}), 403)
