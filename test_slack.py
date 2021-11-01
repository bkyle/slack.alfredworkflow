import unittest

from slack import *

class TestMessageConstruction(unittest.TestCase):

    def test_base_case(self):
        m = Message("a", "b", "c")
        self.assertEquals(m.sender, "a")
        self.assertEquals(m._timestamp, "b")
        self.assertEquals(m.timestamp, "b")
        self.assertTrue(isinstance(m.body, list))
        self.assertEquals(len(m.body), 1)
        self.assertEquals(m.body[0], "c")

    def test_with_missing_body(self):
        m = Message("x", "x")
        self.assertTrue(isinstance(m.body, list))
        self.assertEquals(len(m.body), 0)

    def test_with_body_list(self):
        m = Message("x", "x", ["c", "d", "e"])
        self.assertEquals(len(m.body), 3)
        self.assertEquals(m.body, ["c", "d", "e"])


class TestMessageOperations(unittest.TestCase):

    def test_append(self):
        m = Message("x", "x")
        self.assertEquals(len(m.body), 0)
        m.append("foo")
        self.assertEquals(len(m.body), 1)
        m.append("bar")
        self.assertEquals(len(m.body), 2)
        self.assertEquals(m.body, ["foo", "bar"])

    def test_continuation_copies_header_fields(self):
        m = Message("a", "b")
        c = Message.continuation(m)
        self.assertEquals(m.sender, c.sender)
        self.assertEquals(m.timestamp, c.timestamp)
        self.assertEquals(m.body, [])

    def test_continuation_overrides(self):
        m = Message("a", "b")
        c = Message.continuation(m, sender="X", timestamp="Y")
        self.assertEquals(c.sender, "X")
        self.assertEquals(c.timestamp, "Y")

    def test_continuation_starts_blank(self):
        c = Message.continuation(None)
        self.assertIsNone(c.sender)
        self.assertIsNone(c.timestamp)


if __name__ == "__main__":
    unittest.main()
