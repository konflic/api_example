import os
import api

from flask import Flask, jsonify, make_response

app = Flask(__name__)

app.register_blueprint(api.read.read_blueprint)
app.register_blueprint(api.info.info_blueprint)
app.register_blueprint(api.create.create_blueprint)
app.register_blueprint(api.update.update_blueprint)
app.register_blueprint(api.auth.auth_blueprint)
app.register_blueprint(api.delete.delete_blueprint)

app.secret_key = "secret"


@app.route("/")
def index():
    return """
    <p><b>Welcome to test API app!</b></p>
    <a href="/api">Start here</a>
    """


@app.route('/api')
def api():
    return """
    <h1>API example: v1.0.0</h1>
    <a href="/api/create">Create</a> Создаение данных<br>
    <a href="/api/read">Read</a> Чтение данных<br>
    <a href="/api/info">Info</a> Echo по запросу<br>
    <a href="/api/update">Update</a> Изменение и добавление данных<br>
    <a href="/api/auth">Auth</a> Авторизация<br>
    <a href="/api/delete">Delete</a> Удаление данных<br>
    """


@app.route('/favicon.ico')
def favicon():
    return make_response(200)


# Example of wrong status response
@app.errorhandler(404)
def page_not_found(e):
    return make_response(
        jsonify({"status": "error", "description": "hello, i am here with wrong status!", "error": str(e)}), 502)

@app.errorhandler(405)
def method_not_allowed(e):
    return make_response(
        jsonify({"status": "error", "description": "this method should not be here"}), 405)


if __name__ == "__main__":
    print("==> ADMIN: ", os.getenv("ADMIN"))
    print("==> PASSWORD: ", os.getenv("PASSWORD"))

    app.run(
        host="0.0.0.0",
        port=os.getenv("PORT", 5000),
        debug=True
    )
