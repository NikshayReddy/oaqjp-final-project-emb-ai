"""Flask server for the Emotion Detector application."""

from typing import Any

from flask import Flask, jsonify, request

from EmotionDetection import emotion_detector

app = Flask(__name__)


@app.route("/", methods=["GET"])
def health_check() -> Any:
    """Return a simple health check response."""
    return jsonify({"message": "Emotion Detector is running."}), 200


@app.route("/detect", methods=["POST"])
def detect_emotion() -> Any:
    """Analyze text from the request and return emotion detection results."""
    payload = request.get_json(silent=True)
    if not payload or "text" not in payload:
        return jsonify({"status_code": 400, "error": "Request must include a 'text' field."}), 400

    result = emotion_detector(payload.get("text", ""))
    status_code = result.get("status_code", 500)
    return jsonify(result), status_code


if __name__ == "__main__":
    app.run(debug=True)
