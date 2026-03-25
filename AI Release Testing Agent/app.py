"""
app.py - Main entry point for the AI Release Testing Agent
"""

from flask import Flask, request, jsonify
from test_generator import generate_tests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "message": "AI Release Testing Agent is running.",
        "status": "ok"
    })


@app.route("/generate-tests", methods=["POST"])
def generate_tests_route():

    data = request.get_json()

    if not data or "user_story" not in data or "acceptance_criteria" not in data:
        return jsonify({
            "error": "Missing 'user_story' or 'acceptance_criteria'"
        }), 400

    user_story = data["user_story"]
    acceptance_criteria = data["acceptance_criteria"]

    tests = generate_tests(user_story, acceptance_criteria)

    # 🔥 summary calculation
    total = len(tests)
    passed = len([t for t in tests if t.get("status") == "PASS"])
    failed = len([t for t in tests if t.get("status") == "FAIL"])

    return jsonify({
        "user_story": user_story,
        "acceptance_criteria": acceptance_criteria,
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed
        },
        "test_cases": tests
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)