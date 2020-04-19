from flask import Flask, request, Response
from flask_cors import CORS
import copy
import json
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}}, methods=["GET", "POST"])

@app.route("/get_current_volumes", method=["GET", "POST"])
def get_current_volumes():
    pass

@app.route("/set_volume_of_chromecast", methods=["POST"])
def set_volume_of_chromecast():

    data = request.json
    cc_friendly_name = data["cc_friendly_name"]
    volume_set_value = data["volume_set_value"]

    print("Got new volume value ({}) for: {}.".format(volume_set_value, cc_friendly_name))


    return 0

if __name__ == "__main__":
    # get_resources_system()
    app.run(host="0.0.0.0")
