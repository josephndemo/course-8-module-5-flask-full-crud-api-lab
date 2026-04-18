from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# CREATE - POST
@app.route("/events", methods=["POST"])
def create_event():
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required"}), 400

    new_id = max(event.id for event in events) + 1 if events else 1
    new_event = Event(new_id, data["title"])
    events.append(new_event)

    return jsonify(new_event.to_dict()), 201


# UPDATE - PATCH
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
    data = request.get_json()

    if not data or "title" not in data:
        return jsonify({"error": "Title is required to update"}), 400

    event = next((e for e in events if e.id == event_id), None)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    event.title = data["title"]

    return jsonify(event.to_dict()), 200


# DELETE - must return 204 with NO BODY
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    global events

    event = next((e for e in events if e.id == event_id), None)

    if not event:
        return jsonify({"error": "Event not found"}), 404

    events = [e for e in events if e.id != event_id]

    return "", 204


if __name__ == "__main__":
    app.run(debug=True)