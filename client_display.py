# display 서버

import flask
from flask import request
import time

app = flask.Flask(__name__)

@app.route("/api/displayEmptySeats", methods=["POST"])
def match():
    num_empty_seats = int(request.values["num_empty_seats"])
    print("빈 좌석 수: {}".format(num_empty_seats))
    return "OK"

app.run("0.0.0.0", port=8899, threaded=True)