import datetime

from flask import Response, make_response
from flask_restful import Resource


class BonhamTime(Resource):  # type:ignore[misc]
    @staticmethod
    def time_to_bonham(num_days: int) -> float:
        BONHAM_LENGTH = datetime.timedelta(days=8)

        user_days = datetime.timedelta(days=num_days)

        return user_days / BONHAM_LENGTH

    def get(self, num: int) -> Response:
        bonham_time = self.time_to_bonham(num)

        headers = {"Content-Type": "text/html"}

        template = f"""<!doctype html>
        <title>Bonham Time: {bonham_time}</title>
        <h1>Bonham Time: {bonham_time}</h1>"""

        return make_response(template, 200, headers)
