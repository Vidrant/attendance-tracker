from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# --------------------------------------------------
# In-memory attendance records
# --------------------------------------------------

attendance = [
    {
        "student_id": 1,
        "student_name": "Sample Student",
        "date": "2026-10-06",
        "status": "Present"
    }
]


# --------------------------------------------------
# Frontend HTML
# --------------------------------------------------

HTML_PAGE = """
<!DOCTYPE html>
<html lang="en">

<head>

    <meta charset="UTF-8">

    <meta name="viewport"
          content="width=device-width, initial-scale=1.0">

    <title>Attendance Tracker</title>

    <style>

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
        }

        body {
            background: #f4f6f8;
            color: #222;
            padding: 30px;
        }

        .container {
            max-width: 950px;
            margin: auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
        }

        header h1 {
            font-size: 32px;
            margin-bottom: 8px;
        }

        .subtitle {
            color: #666;
            margin-bottom: 18px;
        }

        .dashboard-buttons {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
        }

        .dashboard-button {
            display: inline-block;
            padding: 10px 18px;
            border-radius: 7px;
            background: #2563eb;
            color: white;
            text-decoration: none;
            font-size: 14px;
            transition: 0.2s;
        }

        .dashboard-button:hover {
            background: #1d4ed8;
        }

        .monitoring-button {
            background: #475569;
        }

        .monitoring-button:hover {
            background: #334155;
        }

        .card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 3px 12px rgba(0, 0, 0, 0.08);
        }

        .card h2 {
            margin-bottom: 20px;
        }

        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        label {
            font-size: 14px;
            font-weight: bold;
        }

        input,
        select {
            width: 100%;
            padding: 11px;
            border: 1px solid #ccc;
            border-radius: 7px;
            font-size: 14px;
        }

        input:focus,
        select:focus {
            outline: none;
            border-color: #2563eb;
        }

        .submit-button {
            margin-top: 18px;
            padding: 11px 20px;
            border: none;
            border-radius: 7px;
            background: #16a34a;
            color: white;
            cursor: pointer;
            font-size: 14px;
        }

        .submit-button:hover {
            background: #15803d;
        }

        .status-message {
            margin-top: 12px;
            font-size: 14px;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th,
        td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }

        th {
            background: #f1f5f9;
        }

        .present {
            color: #15803d;
            font-weight: bold;
        }

        .absent {
            color: #dc2626;
            font-weight: bold;
        }

        .empty {
            text-align: center;
            color: #777;
            padding: 20px;
        }

        footer {
            text-align: center;
            color: #777;
            font-size: 13px;
            margin-top: 20px;
        }

        @media (max-width: 600px) {

            body {
                padding: 15px;
            }

            .form-grid {
                grid-template-columns: 1fr;
            }

            table {
                font-size: 13px;
            }

            th,
            td {
                padding: 8px;
            }

        }

    </style>

</head>


<body>

<div class="container">

    <!-- Header -->

    <header>

        <h1>Attendance Tracker</h1>

        <p class="subtitle">
            Simple Student Attendance Management System
        </p>

        <div class="dashboard-buttons">

            <a
                href="http://localhost:3000"
                target="_blank"
                class="dashboard-button"
            >
                📊 Grafana Dashboard
            </a>

            <a
                href="http://localhost:9090"
                target="_blank"
                class="dashboard-button monitoring-button"
            >
                📈 Prometheus
            </a>

        </div>

    </header>


    <!-- Add Attendance -->

    <div class="card">

        <h2>Add Attendance</h2>

        <form id="attendanceForm">

            <div class="form-grid">

                <div class="form-group">

                    <label for="student_id">
                        Student ID
                    </label>

                    <input
                        type="number"
                        id="student_id"
                        placeholder="Enter student ID"
                        required
                    >

                </div>


                <div class="form-group">

                    <label for="student_name">
                        Student Name
                    </label>

                    <input
                        type="text"
                        id="student_name"
                        placeholder="Enter student name"
                        required
                    >

                </div>


                <div class="form-group">

                    <label for="date">
                        Date
                    </label>

                    <input
                        type="date"
                        id="date"
                        required
                    >

                </div>


                <div class="form-group">

                    <label for="status">
                        Status
                    </label>

                    <select id="status" required>

                        <option value="Present">
                            Present
                        </option>

                        <option value="Absent">
                            Absent
                        </option>

                    </select>

                </div>

            </div>


            <button
                type="submit"
                class="submit-button"
            >
                Add Attendance
            </button>


            <p
                class="status-message"
                id="message"
            ></p>

        </form>

    </div>


    <!-- Attendance Records -->

    <div class="card">

        <h2>Attendance Records</h2>

        <table>

            <thead>

                <tr>
                    <th>Student ID</th>
                    <th>Name</th>
                    <th>Date</th>
                    <th>Status</th>
                </tr>

            </thead>

            <tbody id="attendanceTable">

            </tbody>

        </table>

    </div>


    <footer>

        Attendance Tracker | Flask REST API

    </footer>

</div>


<script>

    // ----------------------------------------------
    // Load attendance records
    // ----------------------------------------------

    async function loadAttendance() {

        try {

            const response =
                await fetch("/items");

            const data =
                await response.json();

            const table =
                document.getElementById(
                    "attendanceTable"
                );

            table.innerHTML = "";


            if (data.length === 0) {

                table.innerHTML = `
                    <tr>
                        <td
                            colspan="4"
                            class="empty"
                        >
                            No attendance records found.
                        </td>
                    </tr>
                `;

                return;
            }


            data.forEach(record => {

                const row =
                    document.createElement("tr");


                const statusClass =
                    record.status === "Present"
                    ? "present"
                    : "absent";


                row.innerHTML = `

                    <td>
                        ${record.student_id}
                    </td>

                    <td>
                        ${record.student_name}
                    </td>

                    <td>
                        ${record.date}
                    </td>

                    <td class="${statusClass}">
                        ${record.status}
                    </td>

                `;


                table.appendChild(row);

            });

        }

        catch (error) {

            console.error(
                "Error loading attendance:",
                error
            );

        }

    }


    // ----------------------------------------------
    // Add attendance record
    // ----------------------------------------------

    document
        .getElementById("attendanceForm")
        .addEventListener(
            "submit",
            async function(event) {

                event.preventDefault();


                const record = {

                    student_id:
                        Number(
                            document
                                .getElementById(
                                    "student_id"
                                )
                                .value
                        ),

                    student_name:
                        document
                            .getElementById(
                                "student_name"
                            )
                            .value,

                    date:
                        document
                            .getElementById(
                                "date"
                            )
                            .value,

                    status:
                        document
                            .getElementById(
                                "status"
                            )
                            .value
                };


                try {

                    const response =
                        await fetch(
                            "/items",
                            {
                                method: "POST",

                                headers: {
                                    "Content-Type":
                                        "application/json"
                                },

                                body:
                                    JSON.stringify(
                                        record
                                    )
                            }
                        );


                    const result =
                        await response.json();


                    const message =
                        document.getElementById(
                            "message"
                        );


                    if (response.ok) {

                        message.textContent =
                            "Attendance added successfully.";

                        message.style.color =
                            "green";


                        document
                            .getElementById(
                                "attendanceForm"
                            )
                            .reset();


                        loadAttendance();

                    }

                    else {

                        message.textContent =
                            result.error ||
                            "Failed to add attendance.";

                        message.style.color =
                            "red";

                    }

                }

                catch (error) {

                    document
                        .getElementById(
                            "message"
                        )
                        .textContent =
                            "Unable to connect to the server.";

                }

            }
        );


    // Load records when page opens

    loadAttendance();

</script>

</body>

</html>
"""


# --------------------------------------------------
# Frontend
# --------------------------------------------------

@app.route("/", methods=["GET"])
def home():
    """Display the Attendance Tracker frontend."""
    return render_template_string(HTML_PAGE)


# --------------------------------------------------
# GET /items
# --------------------------------------------------

@app.route("/items", methods=["GET"])
def get_items():
    """Return all attendance records."""
    return jsonify(attendance), 200


# --------------------------------------------------
# POST /items
# --------------------------------------------------

@app.route("/items", methods=["POST"])
def add_item():
    """Add a new attendance record."""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body must contain JSON data"
        }), 400


    required_fields = [
        "student_id",
        "student_name",
        "date",
        "status"
    ]


    missing_fields = [
        field
        for field in required_fields
        if field not in data
    ]


    if missing_fields:

        return jsonify({
            "error": "Missing required fields",
            "fields": missing_fields
        }), 400


    if data["status"] not in [
        "Present",
        "Absent"
    ]:

        return jsonify({
            "error":
                "Status must be Present or Absent"
        }), 400


    # Store the attendance record in memory

    attendance.append(data)


    return jsonify({
        "message":
            "Attendance record added successfully",

        "record":
            data
    }), 201


# --------------------------------------------------
# GET /health
# --------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Return application health status."""

    return jsonify({
        "status": "OK"
    }), 200


# --------------------------------------------------
# Run Flask
# --------------------------------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )