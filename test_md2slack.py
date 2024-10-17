# pylint: disable=missing-class-docstring, missing-function-docstring, missing-module-docstring

import unittest
from md2slack import md2slack

class TestMd2Slack(unittest.TestCase):

    def test_noop(self):
        expected = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        text = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

    def test_italics(self):
        expected = 'Lorem ipsum dolor _sit amet_, consectetur adipiscing elit.'

        text = 'Lorem ipsum dolor *sit amet*, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor _sit amet_, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

    def test_bold(self):
        expected = 'Lorem ipsum dolor *sit amet*, consectetur adipiscing elit.'

        text = 'Lorem ipsum dolor **sit amet**, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor __sit amet__, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

    def test_bold_italics(self):
        expected = 'Lorem ipsum dolor *_sit amet_*, consectetur adipiscing elit.'

        text = 'Lorem ipsum dolor ***sit amet***, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor **_sit amet_**, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor _**sit amet**_, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor __*sit amet*__, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor *__sit amet__*, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

        text = 'Lorem ipsum dolor ___sit amet___, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))

    def test_internal_underscores(self):
        expected = 'Lorem ipsum dolor *_sit_amet_*, consectetur adipiscing elit.'

        text = 'Lorem ipsum dolor ***sit_amet***, consectetur adipiscing elit.'
        self.assertEqual(expected, md2slack(text))
