# urls of form:
# https://bonh.am/electrode?voltage=200&input=AgClSat&output=NHE&pretty=1

from flask import Response, jsonify, make_response, render_template
from flask_restful import Resource, reqparse


class RefElectrode(Resource):  # type:ignore[misc]
    REFERENCE = {
        "NHE": 0,
        "SHE": 0,
        "SCE": 244,
        "CalSat": 244,
        "Cal1M": 280,
        "Cal0p1M": 336,
        "CalNaCl": 236,
        "AgClSat": 199,
        "AgCl0p1M": 288,
        "AgClNaCl": 197,
    }

    VALUES = {
        "NHE": "Normal Hydrogen Electrode",
        "SHE": "Standard Hydrogen Electrode",
        "SCE": "Saturated KCl",
        "CalSat": "Saturated Calomel",
        "Cal1M": "Calomel 1M KCl",
        "Cal0p1M": "Calomel 0.1M KCl",
        "CalNaCl": "Calomel Saturated NaCl",
        "AgClSat": "Ag/AgCL Saturated KCl",
        "AgCl0p1M": "Ag/AgCl 0.1M KCl",
        "AgClNaCl": "Ag/AgCL Saturated NaCl",
    }

    VALUE_LIST = ",".join([f"{key}:{value}" for key, value in VALUES.items()])

    @staticmethod
    def electrode_calc(voltage: float, input: str, output: str) -> float:
        return (
            voltage
            + RefElectrode.REFERENCE.get(input, 0)
            - RefElectrode.REFERENCE.get(output, 0)
        )

    def get(self) -> Response:
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            "voltage",
            type=float,
            help="Provide input voltage in mV",
            location="args",
            required=True,
        )
        parser.add_argument(
            "input",
            type=str,
            help=f"Type of input reference electrode, from: {RefElectrode.VALUE_LIST}",
            location="args",
            required=True,
        )
        parser.add_argument(
            "output",
            type=str,
            help=f"Type of input reference electrode, from: {RefElectrode.VALUE_LIST}",
            location="args",
            required=True,
        )
        parser.add_argument(
            "pretty",
            type=int,
            help="Print pretty html",
            location="args",
            default=0,
        )

        args = parser.parse_args()

        result = self.electrode_calc(
            args["voltage"],
            args["input"],
            args["output"],
        )

        if args["pretty"] == 1:
            headers = {"Content-Type": "text/html"}

            return make_response(
                render_template(
                    "ref_electrode.html",
                    voltage=args["voltage"],
                    input=args["input"],
                    output=args["output"],
                    result=result,
                    values=RefElectrode.VALUES,
                ),
                200,
                headers,
            )

        else:
            return jsonify({"output": result})
