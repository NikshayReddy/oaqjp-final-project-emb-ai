# Emotion Detector

An AI-based emotion detection web application built with Flask and IBM Watson Natural Language Understanding.

## Project Structure

- `EmotionDetection/`: Python package containing the emotion detection module.
- `server.py`: Flask web server exposing an emotion detection endpoint.
- `test_emotion_detection.py`: Unit tests for the emotion detection package.
- `requirements.txt`: Python dependencies.
- `setup.py`: Package configuration.

## Usage

1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```

2. Run the web server:
   ```bash
   python server.py
   ```

3. Send a POST request to `http://127.0.0.1:5000/detect` with JSON payload:
   ```json
   {"text": "I am so excited today!"}
   ```

## Notes

- The app attempts to use IBM Watson Natural Language Understanding when `WATSON_NLU_API_KEY` and `WATSON_NLU_URL` are configured.
- When credentials or the library are unavailable, the app uses a fallback rule-based emotion classifier.
