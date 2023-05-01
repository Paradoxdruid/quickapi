import datetime

from flask import Response, jsonify
from flask_restful import Resource


class BonhamTime(Resource):  # type:ignore[misc]
    @staticmethod
    def time_to_bonham(num_days: int) -> float:
        BONHAM_LENGTH = datetime.timedelta(days=8)

        user_days = datetime.timedelta(days=num_days)

        return user_days / BONHAM_LENGTH

    def get(self, num: int) -> Response:
        return jsonify({"time_in_bonhams": self.time_to_bonham(num)})
