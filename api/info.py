from src.Route import Route
from flask import Blueprint, request, jsonify, Response, make_response, render_template

info_blueprint = Blueprint('info', __name__)


class Routes:
    root = Route(
        path="/api/info",
        params="Any",
        description="Info"
    )
    about = Route(
        path="/api/info/about",
        description="Returns echo of the given request"
    )
    response = Route(
        path="/api/info/response",
        params="/<status>",
        description="Returns a given status code"
    )
    data = Route(
        path="/api/info/data",
        description="Returns json data"
    )

    def as_list(self):
        return [self.about, self.response, self.data]


@info_blueprint.route(Routes.root.path)
def index():
    return render_template("describe.html", data=Routes().as_list(), title=Routes.root.description)


@info_blueprint.route(Routes.about.path, methods=Routes.about.methods)
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


@info_blueprint.route(Routes.response.path, methods=Routes.response.methods)
@info_blueprint.route(f'{Routes.response.path}/<status>', methods=Routes.response.methods)
def response(status=200):
    response = Response()
    try:
        response.status_code = int(status)
    except:
        # Default value
        response.status_code = 200
    response.set_data("<p>Response status is: {status}</p>".format(status=status))
    return response


@info_blueprint.route(Routes.data.path, methods=Routes.data.methods)
def data():
    response = make_response(jsonify({
        "tag": "BUTTON",
        "classes": "btn btn-primary target",
        "text": "Loaded with Ajax",
        "display": "inline"
    }), 200)
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
