from django.test import TestCase

class SanityCheckTests(TestCase):
    def test_is_true(self):
        self.assertIs(True, True)
