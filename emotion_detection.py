"""Root-level wrapper for the EmotionDetector application."""

from EmotionDetection.emotion_detection import emotion_detector as _emotion_detector

__all__ = ["emotion_detector"]


def emotion_detector(text_to_analyse: str):
    """Delegates to the EmotionDetection package implementation."""
    return _emotion_detector(text_to_analyse)
