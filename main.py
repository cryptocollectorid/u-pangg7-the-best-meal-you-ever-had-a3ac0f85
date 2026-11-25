#!/usr/bin/env python3
"""The Best Meal You Ever Had — one sentence, at most 200 characters.

Writes the entry to /output/entry.txt with a validation gate matching the
competition's sealed scorer: UTF-8 text of 1 to 200 characters, a single
non-blank line.
"""

import os
import sys

ENTRY = (
    "My grandmother's soto ayam in Jakarta \u2014 turmeric broth, shredded "
    "chicken, a boiled egg at her dawn kitchen table, steam fogging my "
    "glasses before the first spoonful."
)

MAX_CHARS = 200


def validate_entry(text: str) -> str:
    """Enforce the gate: 1-200 chars, one non-blank line, UTF-8 encodable."""
    if not text or not text.strip():
        raise ValueError("entry must not be empty or whitespace only")
    if len(text) != len(text.strip()):
        raise ValueError("entry must not have leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 0x20 and ch not in ("\t",) for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError(
            f"entry is {len(text)} characters, over the {MAX_CHARS} limit"
        )
    text.encode("utf-8")  # raises if not valid UTF-8 text
    return text


def write_entry(text: str, out_path: str = "/output/entry.txt") -> None:
    validated = validate_entry(text)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(validated)
    # Round-trip read-back: the file on disk must hold exactly the entry.
    with open(out_path, "r", encoding="utf-8") as fh:
        if fh.read() != validated:
            raise ValueError("read-back mismatch: file does not hold the entry")
    print(f"Wrote {len(validated)} characters to {out_path}")


def main() -> int:
    try:
        write_entry(ENTRY)
    except ValueError as exc:
        print(f"gate failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
