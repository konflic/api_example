import json

from flask import Blueprint, request, make_response
from src.Route import Route

sql_drop = "DROP TABLE IF EXISTS users;"
config_blueprint = Blueprint('config', __name__)


class Routes:
    root = Route(
        path="/api/config",
        description="Remote config wrapper"
    )
    update = Route(
        path="/api/config/update",
        methods=["POST"],
        description="Creating new database"
    )

    def as_list(self):
        return [self.root, self.update]


@config_blueprint.route(Routes.root.path)
def create():
    response = ""
    with open("example.json", "r") as f:
        data = json.load(f)
        for k, v in data.items():
            value = f"'{str(v)}'" if " " in str(v) else str(v)
            response += k.upper() + "=" + value + "\n"
    return make_response(response, 200)



@config_blueprint.route(Routes.update.path, methods=Routes.update.methods)
def update():
    data = request.json
    with open("example.json", "w+") as f:
        f.write(json.dumps(data))
    return make_response({"status": "ok"}, 200)
