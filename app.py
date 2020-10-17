import os
import api

from flask import Flask, jsonify

app = Flask(__name__)

app.register_blueprint(api.read.read_blueprint)
app.register_blueprint(api.info.info_blueprint)
app.register_blueprint(api.create.create_blueprint)
app.register_blueprint(api.update.update_blueprint)
app.register_blueprint(api.auth.auth_blueprint)
app.register_blueprint(api.delete.delete_blueprint)

app.secret_key = "secret"


@app.route('/api')
@app.route('/api/docs')
@app.route('/api/doc')
def index():
    return """
    <h1>API example</h1>
    <a href="/api/doc">Documentation</a> Документация<br>
    <a href="/api/create">Create</a> Создаение данных<br>
    <a href="/api/read">Read</a> Чтение данных<br>
    <a href="/api/info">Info</a> Echo по запросу<br>
    <a href="/api/update">Update</a> Изменение и добавление данных<br>
    <a href="/api/auth">Auth</a> Авторизация<br>
    <a href="/api/delete">Delete</a> Удаление данных<br>
    """


@app.errorhandler(405)
def page_not_found(e):
    return jsonify({"status": "error", "description": "method_not_allowed"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("PORT", 5000), debug=True)
