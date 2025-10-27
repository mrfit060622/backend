from flask import Blueprint

bp_ping = Blueprint("ping", __name__)
@bp_ping.route("/acorda", methods=["GET"])
def ping():
    return {"status": "ok"}, 200