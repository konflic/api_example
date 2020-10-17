from types import SimpleNamespace
from src.settings import HTTP_METHODS
from flask import Blueprint, request, jsonify, Response

info_blueprint = Blueprint('info', __name__)

routes = SimpleNamespace(
    root="/api/info",
    about="/api/info/about"
)

@info_blueprint.route(routes.root)
def index():
    return f"""
    <a href="{routes.about}">{routes.about}</a> - Возвращает информацию о запросе<br>
    <a href="/info/response">/info/response/<status></a> - Возвращает запрос нужного статуса
    """


@info_blueprint.route('/api/info/about', methods=HTTP_METHODS)
def about():
    return jsonify({
        "scheme": request.scheme,
        "path": request.path,
        "user_agent": str(request.user_agent),
        "cookies": {k: v for k, v in request.cookies.items()},
        "args": {k: v for k, v in request.args.items()},
        "content_md5": request.content_md5,
        "get_json": request.get_json(),
        "headers": {k: v for k, v in request.headers.items()},
        "is_json": request.is_json,
        "referrer": request.referrer,
        "method": request.method,
        "mimetype_params": dict(request.mimetype_params)
    })


@info_blueprint.route('/api/info/response', methods=HTTP_METHODS)
@info_blueprint.route('/api/info/response/<status>', methods=HTTP_METHODS)
def response(status=200):
    response = Response()
    response.status_code = int(status)
    response.set_data("<h1>Response status is: {status}</h1>".format(status=status))
    return response
