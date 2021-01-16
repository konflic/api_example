import time
import json

from src.settings import ADMIN
from src.Route import Route
from flask import Blueprint, request, session, make_response, render_template

auth_blueprint = Blueprint('auth', __name__)


class Routes:
    root = Route(
        path="/api/auth",
        description="Authorization"
    )
    login = Route(
        path="/api/auth/login",
        methods=["OPTIONS", "LOGIN"],
        params="{'login': 'login', 'password': 'password'}",
        description="Authorization handler"
    )
    status = Route(
        path="/api/auth/status",
        methods=["HELLO", "GET"],
        description="Check status of current authorization"
    )
    logout = Route(
        path="/api/auth/logout",
        methods=["DELETE"],
        description="Finish session of currently authorized user"
    )

    def as_list(self):
        return [self.login, self.status, self.logout]


@auth_blueprint.route(Routes.root.path, methods=Routes.root.methods)
def index():
    return render_template("describe.html", data=Routes().as_list(), title=Routes.root.description)


@auth_blueprint.route(Routes.login.path, methods=Routes.login.methods)
def login():
    if request.method == "OPTIONS":
        response = make_response({"status": "ok"}, 200)
        response.headers["Access-Control-Allow-Methods"] = "LOGIN, OPTIONS"
    else:

        data = request.get_json()

        if data is None:
            try:
                data = json.loads(request.get_data())
            except json.decoder.JSONDecodeError:
                data = {"login": "NONE", "password": "NONE"}

        if data is not None and data.get("login") == ADMIN.get("login") and data.get("password") == ADMIN.get("password"):
            session['authorized'] = True
            response = make_response({"status": f"authorized as {ADMIN.get('login')}", "session": str(session)}, 200)
            time.sleep(2)  # Imitating long response
        else:
            # This is an example of wrong code given to auth error
            # 402 is a Payment required status
            response = make_response({
                "error": "wrong credentials",
                "credentials": str(data)
            }, 402)

    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Server"] = "WTF? 1.01 server"
    return response


@auth_blueprint.route(Routes.logout.path, methods=Routes.logout.methods)
def logout():
    if session.get("authorized"):
        del session["authorized"]
        response = make_response({"status": "logout_ok"}, 201)
        response.delete_cookie("user")
    else:
        response = make_response({"status": "not_authorized"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@auth_blueprint.route(Routes.status.path, methods=Routes.status.methods)
def status():
    response = make_response({"authorized": session.get("authorized")})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
