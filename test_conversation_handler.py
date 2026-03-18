import unittest

from conversation_handler import ConversationHandler


class ConversationHandlerCapabilitiesTests(unittest.TestCase):
    def setUp(self):
        self.handler = ConversationHandler()

    def test_detects_repo_functionality_question_as_capabilities(self):
        question = "can you see my github repo and work on it or fix it can you do it?"
        self.assertEqual(self.handler.detect_intent(question), "capabilities")

    def test_capabilities_response_mentions_repo_help(self):
        response = self.handler.get_response("capabilities")
        self.assertIn("repository", response.lower())
        self.assertIn("fix", response.lower())


if __name__ == "__main__":
    unittest.main()
