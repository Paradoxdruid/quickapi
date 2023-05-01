from flask import Response, jsonify
from flask_restful import Resource, reqparse

# Request url should look like:
# https://bonh.am/buffer?buffer_conc_inital=1&buffer_conc_final=0.1&pka=4.76&volume=1&hcl=6&naoh=6&initial_ph=4.5&final_ph=5.2


def buffer_solver(
    _buffer_conc_initial: str,
    _buffer_conc_final: str,
    _buffer_pKa: str,
    _total_volume: str,
    _HCl_stock_conc: str,
    _NaOH_stock_conc: str,
    _initial_pH: str,
    _final_pH: str,
) -> str:
    # Sanitize input and catch unusable input
    try:
        buffer_conc_initial = float(_buffer_conc_initial)
        buffer_conc_final = float(_buffer_conc_final)
        buffer_pKa = float(_buffer_pKa)
        total_volume = float(_total_volume)
        HCl_stock_conc = float(_HCl_stock_conc)
        NaOH_stock_conc = float(_NaOH_stock_conc)
        initial_pH = float(_initial_pH)
        final_pH = float(_final_pH)
    except ValueError:
        return "Invalid input values, try again"

    # Remove common nonsense conditions
    if not (0.0 < buffer_conc_initial <= 100.0):
        return "Invalid initial buffer concentration"
    if not (0.0 < buffer_conc_final <= 100.0):
        return "Invalid final buffer concentration"
    if not (0.0 < HCl_stock_conc <= 100.0):
        return "Invalid HCl concentration"
    if not (0.0 < NaOH_stock_conc <= 100.0):
        return "Invalid NaOH concentration"
    if buffer_conc_final > buffer_conc_initial:
        return "Can't increase concentration through dilution"
    if not (0.0 < buffer_pKa <= 100.0):
        return "Invalid pKa value"
    if not (0.0 < initial_pH <= 20.0):
        return "Invalid initial pH"
    if not (0.0 < final_pH <= 20.0):
        return "Invalid final pH"

    # First find moles of buffer and volume of buffer:
    buffer_volume = (buffer_conc_final * total_volume) / buffer_conc_initial
    moles_of_buffer = buffer_volume * buffer_conc_initial

    # Then, find initial conditions:
    initial_ratio = 10 ** (initial_pH - buffer_pKa)
    initial_HA = moles_of_buffer / (1 + initial_ratio)

    # Then, final conditions:
    final_ratio = 10 ** (final_pH - buffer_pKa)
    final_HA = moles_of_buffer / (1 + final_ratio)

    # Then, solve for titrant:
    difference = final_HA - initial_HA

    # Set titrant
    if difference < 0:
        titrant = "NaOH"
        difference = abs(difference)
        volume_titrant = difference / NaOH_stock_conc
    else:
        titrant = "HCl"
        volume_titrant = difference / HCl_stock_conc

    # Solve for volume of water
    volume_water = total_volume - (volume_titrant + buffer_volume)

    return (
        "add {} liters stock buffer, " "{} liters of stock {}, and {} liters of water."
    ).format(
        round(buffer_volume, 4),
        round(volume_titrant, 4),
        titrant,
        round(volume_water, 4),
    )


class Buffer(Resource):  # type:ignore[misc]
    def get(self) -> Response:
        parser = reqparse.RequestParser(bundle_errors=True)
        parser.add_argument(
            "buffer_conc_inital",
            type=float,
            help="Initial Buffer concentration",
            location="args",
            required=True,
        )
        parser.add_argument(
            "buffer_conc_final",
            type=float,
            help="Final Buffer concentration",
            location="args",
            required=True,
        )
        parser.add_argument(
            "pka",
            type=float,
            help="Buffer pKa",
            location="args",
            required=True,
        )
        parser.add_argument(
            "volume",
            type=float,
            help="Volume",
            location="args",
            required=True,
        )
        parser.add_argument(
            "hcl",
            type=float,
            help="HCl stock concentration",
            location="args",
            required=True,
        )
        parser.add_argument(
            "naoh",
            type=float,
            help="NaOH stock concentration",
            location="args",
            required=True,
        )
        parser.add_argument(
            "initial_ph",
            type=float,
            help="Initial pH",
            location="args",
            required=True,
        )
        parser.add_argument(
            "final_ph",
            type=float,
            help="Final pH",
            location="args",
            required=True,
        )

        args = parser.parse_args()

        result = buffer_solver(
            args["buffer_conc_inital"],
            args["buffer_conc_final"],
            args["pka"],
            args["volume"],
            args["hcl"],
            args["naoh"],
            args["initial_ph"],
            args["final_ph"],
        )

        return jsonify({"recipe": result})
