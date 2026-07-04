import unittest

from EmotionDetection.emotion_detection import emotion_detector


class TestEmotionDetector(unittest.TestCase):

    def test_detects_happiness(self):
        result = emotion_detector("I am so happy and excited today!")
        self.assertEqual(result["status_code"], 200)
        self.assertEqual(result["emotion"], "joy")
        self.assertGreaterEqual(result["confidence"], 0.9)

    def test_detects_sadness(self):
        result = emotion_detector("I am very sad and depressed.")
        self.assertEqual(result["status_code"], 200)
        self.assertEqual(result["emotion"], "sadness")
        self.assertGreaterEqual(result["confidence"], 0.9)

    def test_detects_blank_input(self):
        result = emotion_detector("   ")
        self.assertEqual(result["status_code"], 400)
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Input text cannot be blank.")

    def test_output_format(self):
        result = emotion_detector("I am angry")
        expected_keys = {"status_code", "emotion", "confidence", "scores", "text"}
        self.assertTrue(expected_keys.issubset(set(result.keys())))
        self.assertIsInstance(result["scores"], dict)
        self.assertEqual(result["text"], "I am angry")


if __name__ == "__main__":
    unittest.main()
