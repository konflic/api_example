import sqlite3

from src.db import get_sql_result
from src.settings import style
from flask import Blueprint, jsonify, make_response

read_blueprint = Blueprint('read', __name__)

root = "/api/read"

@read_blueprint.route(root)
def index():
    return f"""
    {style}
    <h2>Read</h2>
    <a href="/api">< BACK</a><br><br>
    <table>
        <tr>
            <th>uri</th>
            <th>method</th>
            <th>params</th>
            <th>description</th>
        </tr>
        <tr>
            <td><a href="/api/read/all">/api/read/all</a</td>
            <td>GET</td>
            <td>None</td>
            <td>Show all users in database</td>
        </tr>
        <tr>
            <td><a href="/api/read/name">/api/read/name</a></td>
            <td>GET</td>
            <td>None</td>
            <td>Show data for given name</td>
        </tr>
    </table>
    """


@read_blueprint.route(f"{root}/all")
def all():
    try:
        data = get_sql_result("SELECT * FROM users;")
        return jsonify(data)
    except sqlite3.OperationalError:
        return make_response({"error": "database not created"})


@read_blueprint.route(f'{root}/<name>')
def user(name):
    try:
        data = get_sql_result("SELECT * FROM users WHERE name = ?;", (name,))
        return jsonify(data)
    except sqlite3.OperationalError:
        return make_response({"error": "database not created"})
