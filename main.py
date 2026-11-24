#!/usr/bin/env python3
"""Place the judged Two-Sentence Horror text at /output/entry.txt, atomically.

The grader reads only the artifact.  This program's whole job is to put the exact
intended bytes there: UTF-8, 1..400 characters, no trailing newline, in one atomic
rename, with a byte-for-byte read-back check.  Standard library only (python3.13).
"""

from __future__ import annotations

import hashlib
import os
import tempfile

# Single source of truth for the entry. Exactly two sentences:
#   1) an ordinary school call; 2) the reveal that makes sentence 1 horrid.
STORY = (
    "The school called to say my son had been picked up by his father. "
    "I've never told them he doesn't have one."
)

OUTPUT_PATH = "/output/entry.txt"
MAX_CHARS = 400
# Only these end a sentence in this text; "doesn't" is not a terminator.
TERMINATORS = ".!?"


def encode_and_validate(story: str) -> bytes:
    """Fail loudly rather than let an invalid entry reach the gate."""
    if not (1 <= len(story) <= MAX_CHARS):
        raise ValueError("entry must be 1 to 400 characters")
    if not story.strip():
        raise ValueError("entry must not be only whitespace")
    if any(c in story for c in "\r\n"):
        raise ValueError("entry must contain no newline characters")
    if sum(story.count(c) for c in TERMINATORS) != 2 or not story.endswith("."):
        raise ValueError("entry must be exactly two sentences")
    data = story.encode("utf-8")
    # Decode check catches anything the encoder or a future edit could break.
    if data.decode("utf-8") != story:
        raise ValueError("entry is not valid UTF-8")
    return data


def write_entry() -> bytes:
    """Write to a temp file in the same directory, fsync, then os.replace."""
    data = encode_and_validate(STORY)
    directory = os.path.dirname(OUTPUT_PATH) or "."
    os.makedirs(directory, exist_ok=True)

    fd, temp_path = tempfile.mkstemp(prefix=".entry-", suffix=".tmp", dir=directory)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_path, OUTPUT_PATH)
        # Make the rename itself durable where the filesystem supports it.
        try:
            dir_fd = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(dir_fd)
            finally:
                os.close(dir_fd)
        except OSError:
            pass
    except BaseException:
        try:
            os.unlink(temp_path)
        except OSError:
            pass
        raise

    with open(OUTPUT_PATH, "rb") as handle:
        written = handle.read()
    if written != data:
        raise IOError("entry.txt did not match the intended bytes after write")
    return written


if __name__ == "__main__":
    result = write_entry()
    print(
        "wrote /output/entry.txt: "
        f"{len(result)} bytes, {len(result.decode('utf-8'))} chars, "
        f"sha256 {hashlib.sha256(result).hexdigest()}"
    )
