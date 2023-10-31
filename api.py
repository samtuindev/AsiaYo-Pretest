from decimal import Decimal, ROUND_HALF_UP
from flask import Flask, request, jsonify
import re
app = Flask(__name__)

currencies = {
    "TWD": {
        "TWD": 1,
        "JPY": 3.669,
        "USD": 0.03281
    },
    "JPY": {
        "TWD": 0.26956,
        "JPY": 1,
        "USD": 0.00885
    },
    "USD": {
        "TWD": 30.444,
        "JPY": 111.801,
        "USD": 1
    }
}


@app.route("/api/exchange", methods=["GET"])
def get_exchange():
    source = request.args.get("source", type=str)
    target = request.args.get("target", type=str)
    amount = request.args.get("amount", type=str)
    try:
        pattern = r"^\$\d{1,3}(,\d{3})*$"
        if not re.match(pattern, amount):
            raise ValueError
        amount = float(amount.lstrip("$").replace(",", ""))
        amount_after_exchange = rounding(amount * currencies[source][target])
        return jsonify({
            "msg": "success",
            "amount": amount_after_exchange
        }), 200

    except ValueError:
        error_msg = "Invalid format for amount."
        status_code = 400
    except KeyError:
        error_msg = "Invalid currency code."
        status_code = 400
    except Exception as e:
        error_msg = str(e)
        status_code = 500

    return jsonify({
        "msg": "bad",
        "amount": None,
        "error_msg": error_msg
    }), status_code


def rounding(num: float) -> str:
    res = Decimal(str(num)).quantize(Decimal("0.01"),
                                     rounding=ROUND_HALF_UP)
    return f"${res:,.2f}"


if __name__ == "__main__":
    app.debug = False
    app.run()
