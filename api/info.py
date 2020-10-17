from types import SimpleNamespace
from src.settings import HTTP_METHODS, style
from flask import Blueprint, request, jsonify, Response

info_blueprint = Blueprint('info', __name__)

routes = SimpleNamespace(
    root="/api/info",
    about="/api/info/about"
)

@info_blueprint.route(routes.root)
def index():
    return f"""
    {style}
    <h2>Examples and info</h2>
    <a href="/api">< BACK</a><br><br>
    <a href="{routes.about}">{routes.about}</a> Returns the request data as response<br>
    <a href="/api/info/response/200">/api/info/response/200</a> - Returns given status response
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
    try:
        response.status_code = int(status)
    except:
        response.status_code = 200
    response.set_data("<p>Response status is: {status}</p>".format(status=status))
    return response
