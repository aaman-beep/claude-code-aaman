#!/usr/bin/env python3
"""Resolve EmailBison spintax into one plain readable email.

Spintax blocks look like {option A|option B|option C} and may nest. Merge tags use the
same braces but contain no pipe ({FIRST_NAME}, {COMPANY}) — those must survive untouched.
Resolution is deterministic (first option) so re-runs render the same email.
"""
import re

MERGE_RX = re.compile(r"^\{[^{}|]*\}$")


def resolve(text, pick=0):
    """Collapse every spintax block to one option. Innermost blocks resolve first."""
    if not text:
        return text
    rx = re.compile(r"\{([^{}]*)\}")
    prev = None
    while prev != text:
        prev = text

        def repl(m):
            inner = m.group(1)
            if "|" not in inner:                       # merge tag — keep, but shield the
                return "\0" + inner + "\1"             # braces so the loop terminates
            opts = inner.split("|")
            return opts[pick if pick < len(opts) else 0]

        text = rx.sub(repl, text)
    return text.replace("\0", "{").replace("\1", "}")


def strip_html(html):
    """EmailBison bodies are HTML; render as the plain text a reader would see."""
    if not html:
        return html
    text = re.sub(r"<br\s*/?>", "\n", html, flags=re.I)
    text = re.sub(r"</p>\s*<p[^>]*>", "\n\n", text, flags=re.I)
    text = re.sub(r"</?(p|div)[^>]*>", "\n", text, flags=re.I)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<") \
               .replace("&gt;", ">").replace("&#39;", "'").replace("&quot;", '"')
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


if __name__ == "__main__":
    tests = [
        ("{Hi|Hey} {FIRST_NAME}, {we {love|like} it|it's fine}", "Hi {FIRST_NAME}, we love it"),
        ("{COMPANY} plain", "{COMPANY} plain"),
        ("no braces at all", "no braces at all"),
    ]
    for src, want in tests:
        got = resolve(src)
        assert got == want, f"{src!r} -> {got!r} (wanted {want!r})"
    print("spintax.py self-test OK")
