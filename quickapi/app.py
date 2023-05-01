from bonhamtime import BonhamTime
from flask import Flask, redirect
from flask_restful import Api, Resource
from werkzeug.wrappers import Response as WZResponse

app = Flask(__name__)
api = Api(app)


class Hello(Resource):  # type:ignore[misc]
    """Resource to redirect base url to my personal website."""

    def get(self) -> WZResponse:
        return redirect("https://andrewjbonham.com")


api.add_resource(Hello, "/")
api.add_resource(BonhamTime, "/bonhamtime/<int:num>")


if __name__ == "__main__":
    app.run(debug=True)
