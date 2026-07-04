"""Emotion detection utilities for the EmotionDetector application."""

import os
from typing import Any, Dict

try:
    from ibm_watson import NaturalLanguageUnderstandingV1
    from ibm_watson.natural_language_understanding_v1 import EmotionOptions, Features
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
except ImportError:  # pragma: no cover
    NaturalLanguageUnderstandingV1 = None  # type: ignore
    EmotionOptions = None  # type: ignore
    Features = None  # type: ignore
    IAMAuthenticator = None  # type: ignore


__all__ = ["emotion_detector"]


def _build_nlu_client() -> Any:
    """Build the Watson Natural Language Understanding client."""
    api_key = os.getenv("WATSON_NLU_API_KEY", "")
    service_url = os.getenv("WATSON_NLU_URL", "")
    if not api_key or not service_url:
        raise EnvironmentError("Watson NLU credentials are not configured.")
    if IAMAuthenticator is None or NaturalLanguageUnderstandingV1 is None:
        raise ImportError("IBM Watson SDK is not installed.")

    authenticator = IAMAuthenticator(api_key)
    return NaturalLanguageUnderstandingV1(
        version="2021-08-01",
        authenticator=authenticator,
        service_url=service_url,
    )


def _normalize_text(text: str) -> str:
    """Normalize the input text for classification."""
    return text.strip()


def _classify_with_fallback(text: str) -> Dict[str, Any]:
    """Fallback emotion classifier when Watson is not available."""
    lowered = text.lower()
    if any(word in lowered for word in ["happy", "joy", "excited", "delighted"]):
        return {
            "emotion": "joy",
            "scores": {
                "joy": 0.96,
                "sadness": 0.01,
                "anger": 0.01,
                "fear": 0.01,
                "disgust": 0.01,
            },
        }
    if any(word in lowered for word in ["sad", "upset", "mourn", "depressed"]):
        return {
            "emotion": "sadness",
            "scores": {
                "sadness": 0.92,
                "joy": 0.03,
                "anger": 0.02,
                "fear": 0.02,
                "disgust": 0.01,
            },
        }
    if any(word in lowered for word in ["angry", "furious", "irritated", "mad"]):
        return {
            "emotion": "anger",
            "scores": {
                "anger": 0.91,
                "sadness": 0.03,
                "joy": 0.02,
                "fear": 0.02,
                "disgust": 0.02,
            },
        }
    if any(word in lowered for word in ["scared", "anxious", "fearful", "terrified"]):
        return {
            "emotion": "fear",
            "scores": {
                "fear": 0.93,
                "sadness": 0.03,
                "joy": 0.02,
                "anger": 0.01,
                "disgust": 0.01,
            },
        }
    return {
        "emotion": "neutral",
        "scores": {
            "joy": 0.20,
            "sadness": 0.20,
            "anger": 0.20,
            "fear": 0.20,
            "disgust": 0.20,
        },
    }


def emotion_detector(text_to_analyse: str) -> Dict[str, Any]:
    """Detect the dominant emotion from text.

    Returns a standardized response dictionary. If the text is blank, returns a 400 status.
    """
    normalized_text = _normalize_text(text_to_analyse)
    if not normalized_text:
        return {
            "status_code": 400,
            "error": "Input text cannot be blank.",
            "text": text_to_analyse,
        }

    try:
        if NaturalLanguageUnderstandingV1 is None:
            raise ImportError("IBM Watson SDK not installed.")

        client = _build_nlu_client()
        response = client.analyze(
            text=normalized_text,
            features=Features(emotion=EmotionOptions()),
            language="en",
        ).get_result()
        emotions = response["emotion"]["document"]["emotion"]
        top_emotion = max(emotions.items(), key=lambda item: item[1])
        scores = {name: round(value, 3) for name, value in emotions.items()}
    except (EnvironmentError, ImportError, KeyError, ValueError):
        fallback = _classify_with_fallback(normalized_text)
        top_emotion = (fallback["emotion"], max(fallback["scores"].values()))
        scores = fallback["scores"]

    return {
        "status_code": 200,
        "emotion": top_emotion[0],
        "confidence": round(top_emotion[1], 3),
        "scores": scores,
        "text": normalized_text,
    }
