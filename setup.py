from setuptools import find_packages, setup

setup(
    name="EmotionDetection",
    version="0.1.0",
    description="Emotion detection web app using Watson NLP",
    packages=find_packages(include=["EmotionDetection", "EmotionDetection.*"]),
    install_requires=["Flask>=2.0", "ibm-watson>=6.0"],
    python_requires=">=3.8",
    author="Emotion Detector",
    author_email="noreply@example.com",
)
