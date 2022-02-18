from flask import Blueprint, jsonify, session, make_response, render_template
from src.db import execute_sql
from src.Route import Route

sql_create = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        surname TEXT NOT NULL,
        grade INTEGER NOT NULL,
        sex TEXT
    );
"""

sql_drop = "DROP TABLE IF EXISTS users;"

create_blueprint = Blueprint('create', __name__)


class Routes:
    root = Route(
        path="/api/create",
        description="Create routes"
    )
    init = Route(
        path="/api/create/init",
        methods=["CREATE"],
        description="Creating new database"
    )
    reinit = Route(
        path="/api/create/reinit",
        methods=["RECREATE"],
        description="Recreating existing database"
    )

    def as_list(self):
        return [self.init, self.reinit]


@create_blueprint.route(Routes.root.path)
def create():
    return render_template("describe.html", data=Routes().as_list(), title=Routes.root.description)


@create_blueprint.route(Routes.init.path, methods=Routes.init.methods)
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


@create_blueprint.route(Routes.reinit.path, methods=Routes.reinit.methods)
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
