import time
import json

from types import SimpleNamespace
from src.settings import ADMIN, style
from flask import Blueprint, request, session, jsonify, make_response

auth_blueprint = Blueprint('auth', __name__)

routes = SimpleNamespace(
    root="/api/auth",
    login="/api/auth/login",
    status="/api/auth/status",
    logout="/api/auth/logout"
)

@auth_blueprint.route(routes.root, methods=["GET"])
def index():
    return f"""
    {style}
    <h2>Authorization</h2>
    <a href="/api">< BACK</a><br><br>
    <table>
        <tr>
            <th>uri</th>
            <th>method</th>
            <th>params</th>
            <th>description</th>
        </tr>
        <tr>
            <td><a href="{routes.login}">{routes.login}</a> </td>
            <td>LOGIN</td>
            <td>[user:str, password:str] </td>
            <td>Login with user and password</td>
        </tr>
        <tr>
            <td><a href="{routes.logout}">{routes.logout}</a> </td>
            <td>GET</td>
            <td>None</td>
            <td>Logout currently authorized user</td>
        </tr>
        <tr>
            <td><a href="{routes.status}">{routes.status}</a></td>
            <td>GET</td>
            <td>None</td>
            <td>Current login status</td>
        </tr>
    </table>
    """


@auth_blueprint.route(routes.login, methods=["OPTIONS", "LOGIN"])
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

        if data is not None and data.get("login") == ADMIN["login"] and data.get("password") == ADMIN["password"]:
            session['authorized'] = True
            response = make_response({"status": "authorized", "session": session}, 200)
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


@auth_blueprint.route(routes.logout, methods=["GET"])
def logout():
    if session.get("authorized"):
        del session["authorized"]
        response = make_response({"status": "logout_ok"}, 201)
        response.delete_cookie("user")
    else:
        response = make_response({"status": "not_authorized"})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


@auth_blueprint.route(routes.status, methods=["HELLO", "GET"])
def status():
    response = make_response({"authorized": session.get("authorized")})
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
