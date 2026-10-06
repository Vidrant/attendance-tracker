from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory attendance records
attendance = [
    {
        "student_id": 1,
        "student_name": "Sample Student",
        "date": "2026-10-06",
        "status": "Present"
    }
]


@app.route("/items", methods=["GET"])
def get_items():
    """Return all attendance records."""
    return jsonify(attendance), 200


@app.route("/items", methods=["POST"])
def add_item():
    """Add a new attendance record."""
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Request body must contain JSON data"}), 400

    required_fields = ["student_id", "student_name", "date", "status"]

    missing_fields = [
        field for field in required_fields
        if field not in data
    ]

    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400

    attendance.append(data)

    return jsonify({
        "message": "Attendance record added successfully",
        "record": data
    }), 201


@app.route("/health", methods=["GET"])
def health():
    """Return application health status."""
    return jsonify({"status": "OK"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
