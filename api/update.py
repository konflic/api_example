from types import SimpleNamespace
from src.settings import style
from src.db import execute_sql
from flask import Blueprint, request, jsonify, session, make_response

update_blueprint = Blueprint('update', __name__)

routes = SimpleNamespace(
    root="/api/update",
    add="/api/update/add",
    change_grade="/api/update/grade"
)


@update_blueprint.route(routes.root, methods=['GET'])
def index():
    return f"""
    {style}
    <h2>Update data</h2>
    <a href="/api">< BACK</a><br><br>
    <table>
        <tr>
            <th>uri</th>
            <th>method</th>
            <th>params</th>
            <th>description</th>
        </tr>
        <tr>
            <td><a href="{routes.add}">{routes.add}</a</td>
            <td>POST</td>
            <td>name:str surname:str sex:str grade:int</td>
            <td>Add user with given data to database</td>
        </tr>
        <tr>
            <td><a href="{routes.change_grade}">{routes.change_grade}</a</td>
            <td>POST</td>
            <td>name:str grade:int</td>
            <td>Updates grade for given user</td>
        </tr>
    </table>
    """


@update_blueprint.route(routes.add, methods=['POST'])
def add():
    if session.get("authorized"):
        data = request.json
        try:
            execute_sql("INSERT INTO users (name, surname, grade, sex) VALUES (?, ? ,?, ?)",
                        (data['name'], data['surname'], data['grade'], data['sex']))
        except Exception as e:
            return make_response({"status": "error", "description": str(e)}, 400)
        return make_response({"status": "ok", "data": data}, 201)
    else:
        return make_response({"status": "error", "description": "authorization_required"}, 403)


@update_blueprint.route(routes.change_grade, methods=['POST'])
def change_grade():
    if session.get("authorized"):
        data = request.json
        try:
            execute_sql("UPDATE users SET grade = ? WHERE name = ?;", (data['grade'], data['name']))
        except Exception as e:
            return make_response({"status": "error", "description": str(e)}, 400)
        return make_response({"status": "ok", "data": data}, 201)
    else:
        return make_response({"status": "error", "description": "authorization_required"}, 403)
