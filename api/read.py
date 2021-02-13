import sqlite3

from src.Route import Route
from src.db import get_sql_result
from flask import Blueprint, jsonify, make_response, render_template

read_blueprint = Blueprint('read', __name__)


class Routes:
    root = Route(
        path="/api/read",
        description="Read"
    )
    read_all = Route(
        path="/api/read/all",
        methods=["GET"],
        description="Returns all user records in database"
    )
    read_name = Route(
        path="/api/read/<name>",
        methods=["GET"],
        params="/<name>",
        description="Returns record for a given name"
    )

    def as_list(self):
        return [self.read_all, self.read_name]


@read_blueprint.route(Routes.root.path)
def index():
    return render_template("describe.html", data=Routes().as_list(), title=Routes.root.description)


@read_blueprint.route(Routes.read_all.path)
def all():
    try:
        data = get_sql_result("SELECT * FROM users;")
        return jsonify(data)
    except sqlite3.OperationalError:
        return make_response({"error": "database not created"})


@read_blueprint.route(Routes.read_name.path)
def user(name):
    try:
        data = get_sql_result("SELECT * FROM users WHERE name = ?;", (name,))
        return jsonify(data)
    except sqlite3.OperationalError:
        return make_response({"error": "database not created"})
