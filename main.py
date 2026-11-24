#!/usr/bin/env python3
"""Say What Actually Broke -- make.fun entry.

Writes a single line of software error copy to /output/entry.txt: the
brutal truth about a failed save, and a laugh on the way. Pure standard
library only.

The line: a save fails because the disk is full -- and the disk is full
of error logs complaining the disk is full. It names the real failure in
plain words, tells the user what to do next, and the loop is the joke.
"""

import os
import sys

ENTRY = "We couldn't save your file: the disk is full of error logs complaining the disk is full. Delete something and try again."

MIN_CHARS = 1
MAX_CHARS = 200


def check_gates(text):
    """Refuse to write unless every kit gate passes. Returns a list of failures."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("entry is not valid UTF-8")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        failures.append(
            "entry is %d characters, outside the 1-200 gate" % len(text)
        )
    if text.strip() == "":
        failures.append("entry is only whitespace")
    if "\n" in text or "\r" in text:
        failures.append("entry is not one line")
    return failures


def main():
    failures = check_gates(ENTRY)
    if failures:
        for failure in failures:
            print("GATE FAILED: %s" % failure, file=sys.stderr)
        return 1

    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "entry.txt")
    with open(out_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    os.chmod(out_path, 0o644)

    # Read it back and verify what is on disk, byte for byte.
    with open(out_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        print("GATE FAILED: read-back differs from the entry", file=sys.stderr)
        return 1
    if check_gates(written):
        print("GATE FAILED: written file fails the gates", file=sys.stderr)
        return 1

    print("OK: wrote %s (%d characters, 1 line)" % (out_path, len(written)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
