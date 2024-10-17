#!/usr/bin/env python3

import re
import sys


def md2slack(text):
    """Convert text written with markdown formatting into slack formatting."""
    # Bold-Italics
    text = re.sub(r'\*\*\*(.*?)\*\*\*', r'*_\1_*', text)
    text = re.sub(r'\*\*_(.*?)_\*\*', r'*_\1_*', text)
    text = re.sub(r'_\*\*(.*?)\*\*_', r'*_\1_*', text)
    text = re.sub(r'__\*(.*?)\*__', r'*_\1_*', text)
    text = re.sub(r'\*__(.*?)__\*', r'*_\1_*', text)
    text = re.sub(r'___(.*?)___', r'*_\1_*', text)
    
    # Italic
    text = re.sub(r'\*(?!_)(.*?)(?<!_)\*', r'_\1_', text)
    text = re.sub(r'(?<!\*)_(.*?)_(?!\*)', r'_\1_', text)

    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'*\1*', text)
    text = re.sub(r'__(.*?)__', r'*\1*', text)

    return text


def main():
    try:
        text = sys.stdin.read()
        converted = md2slack(text)
        print(converted)
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    main()
