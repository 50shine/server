from flask import Flask, jsonify, request, render_template
import uuid

app = Flask(__name__)

connected_instances = {}
server_version = "1.0"


def generate_unique_id():
    return str(uuid.uuid4())


@app.route("/")
def index():
    return render_template("index.html", instances=connected_instances.values())


@app.route("/api/change_version", methods=["POST"])
def change_version():
    global server_version

    data = request.json
    new_version = data.get("version")

    if new_version:
        server_version = new_version
        return jsonify({"message": "Server version changed"})
    else:
        return jsonify({"message": "Invalid version"}), 400


@app.route("/api/kick_instance", methods=["POST"])
def kick_instance():
    data = request.json
    instance_id = data.get("instance_id")

    if instance_id in connected_instances:
        connected_instances.pop(instance_id)
        return jsonify({"message": "Instance kicked"})
    else:
        return jsonify({"message": "Instance not found"}), 404


@app.route("/api/instances", methods=["GET"])
def list_instances():
    instances = list(connected_instances.values())
    return jsonify({"instances": instances})


@app.route("/api/connect", methods=["POST"])
def connect_instance():
    instance_id = generate_unique_id()
    connected_instances[instance_id] = {
        "id": instance_id,
        "message_count": 0
    }
    return jsonify({"instance_id": instance_id})


@app.route("/api/validate", methods=["GET"])
def validate_connection():
    data = request.headers
    client_version = data.get("X-Version")

    if client_version == server_version:
        return jsonify({"message": "Connection validated"})
    else:
        return jsonify({"message": "Version mismatch"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=443)
