#!/usr/bin/env python
# -*- coding: utf-8 -*-

# slack.py is a pretty printer for copy/pasted slack transcripts.
#
# Typical usage of this script is in a pipeline that takes the pastboard
# contents as input as follows:
#
#   pbpaste | slack.py | pbcopy
#
# NOTE: that this script expects the input to be plain text. Unfortunately the
# plain text version of the chat history is lower fidelity than the HTML. On
# macOS, the pasteboard contents are HTML and are converted to plain text when
# pasted into a target application. By default, ``pbpaste`` will ask for the
# plain text version of the clipboard content. Below is a snippet that will
# return the contents of the pasteboard as HTML.
#
#   osascript -e 'the clipboard as «class HTML»' | \
#     perl -ne 'print chr foreach unpack("C*",pack("H*",substr($_,11,-3)))'
#
# https://stackoverflow.com/questions/17217450/how-to-get-html-data-out-of-of-the-os-x-pasteboard-clipboard

from __future__ import print_function

import sys
import re
import cStringIO as StringIO

class Message:
    def __init__(self, sender, timestamp, body=None):
        self._sender = sender
        self._timestamp = timestamp

        if body is None:
            self._body = []
        elif isinstance(body, list):
            self._body = body
        else:
            self._body = [body]

    @property
    def sender(self):
        return self._sender

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def body(self):
        return self._body

    def append(self, s):
        self._body.append(s)

    @staticmethod
    def continuation(message, sender=None, timestamp=None, body=None):
        """Copies the passed message and then overrides fields with the non-None passed values.  If the
        passed message is ``None`` a new empty ``Message`` is used."""

        if sender is None and message is not None:
            sender = message.sender
        if timestamp is None and message is not None:
            timestamp = message.timestamp

        return Message(sender, timestamp)


class Parser:
    def parse(self, text, ostream = None):
        """
        Args:
          text: (StringIO) The input text to be parsed as a file-like object.

          ostream: (StringIO) The output stream/file to write the processed output to.
                   If ``None`` then an instance of ``StringIO`` will be created.

        Returns:
          An instance of ``StringIO`` with the output.  This will be the value of ``ostream``
          if one was provided.
        """
        pass

class TextParser(Parser):

    def _strip_emoji(self, text):
        """Strip emoji characters in the form of :emoji: from the passed string. The
        cleansed string is returned.

        Args:
          text: (str) A string that contains emoji characters to be removed.

        Returns:
          The passed string with emoji characters removed.
        """
        return re.sub(r":[^:]+:", "", text)

    def _parse_first_line(self, text):
        """Parses the first line of a message into a tuple of (name, date). Both
        ``name`` and ``date`` are unparsed strings.

        Args:
          text: (str) A string that represents the first line in a sequence of lines
            that make up a message or a set of messages from an individual. This string
            is expected to include the user's name and the date.

        Returns:
          A tuple containing the sender's name and the time the message was sent, both
          as strings.
        """
        matches = re.findall(r"(.*) (\d+:\d+ (AM|PM))", text)
        if matches:
            name, time, _ = matches[0]
            return name.strip(), time.strip()
        else:
            return None, None

    def parse(self, text, ostream = None):
        if isinstance(text, str):
            text = text.splitlines()

        if ostream is None:
            ostream = StringIO()


        messages = []
        message = None
        for line in text:
            line = line.strip()
            line = self._strip_emoji(line)

            if re.match(r"^.* \d+:\d+ (AM|PM)$", line):
                sender, time = self._parse_first_line(line)
                message = Message(sender, time)
                messages.append(message)
            elif re.match(r"^\d+:\d+$", line):
                sender = None
                if message:
                    sender = message["sender"]
                time = line
                message = Message.continuation(message, timestamp=time)
                messages.append(message)
            else:
                if message is None:
                    continue
                if line != "":
                    message.append(line)

        for i, message in enumerate(messages):
            ostream.write("> *%s* %s\n" % (message.sender, message.timestamp))
            for j, line in enumerate(message.body):
                ostream.write("> %s\n" % line)
                if j < len(message.body) - 1:
                    ostream.write("> \n")
            if i < len(messages) - 1:
                ostream.write("\n")

class Renderer:
    def render(self, message, is_continuation=False):
        """Renders the passed message.

        Args:
          message: (Message) the message to be rendered.
          is_continuation: (bool) flag indicating whether the message is a continuation
            of a previous message.  e.g. the message is part of a flow from an individual.

        Returns:
          Nothing
        """
        pass

class MarkdownRenderer(Renderer):
    def render(self, message, is_continuation=False):
        pass

class SlackdownRenderer(Renderer):
    def render(self, message, is_continuation=False):
        pass

def main():
    try:
        text = sys.stdin.read()
        TextParser().parse(text, sys.stdout)
    except KeyboardInterrupt as e:
        sys.exit(0)

if __name__ == "__main__":
    main()
