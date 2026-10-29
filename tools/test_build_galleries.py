#!/usr/bin/env python3
"""Regression checks for the four gallery build outputs."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED = {
    "en9": ("Student", "طالب"),
    "enlit": ("Novel", "رواية"),
    "ensci": ("Atom", "ذرة"),
    "fr9": ("Leçon", "درس"),
}
PROTECTED = ("index.html", "bac12.html", "out/bac12.html")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedded_designs(html):
    marker = "var EMBEDDED_DESIGNS_100 = "
    pos = html.find(marker)
    if pos < 0:
        raise AssertionError("EMBEDDED_DESIGNS_100 is missing")
    start = html.find("[", pos)
    depth = 0
    in_string = escaped = False
    for i in range(start, len(html)):
        ch = html[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\\\":
                escaped = True
            elif ch == '"':
                in_string = False
        elif ch == '"':
            in_string = True
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                return json.loads(html[start:i + 1])
    raise AssertionError("Design catalog JSON is incomplete")


def main():
    protected_before = {name: digest(ROOT / name) for name in PROTECTED if (ROOT / name).exists()}
    render = (ROOT / "render.yaml").read_text(encoding="utf-8")
    match = re.search(r"^\\s*buildCommand:\\s*(.+)$", render, re.MULTILINE)
    if not match:
        raise AssertionError("render.yaml buildCommand is missing")
    command = match.group(1)
    if "cp out/*.html" in command:
        raise AssertionError("Unsafe wildcard copy may overwrite a protected gallery")
    for deck in EXPECTED:
        if "out/%s.html" % deck not in command:
            raise AssertionError("Render buildCommand does not publish %s.html explicitly" % deck)
    if "out/bac12.html" in command:
        raise AssertionError("Render buildCommand must not publish the protected bac12 gallery")

    subprocess.run([sys.executable, str(ROOT / "tools" / "build_galleries.py")], cwd=ROOT, check=True)
    for deck, sample in EXPECTED.items():
        path = ROOT / "out" / (deck + ".html")
        if not path.is_file():
            raise AssertionError("Missing output: " + str(path))
        html = path.read_text(encoding="utf-8")
        designs = embedded_designs(html)
        if len(designs) != 100:
            raise AssertionError("%s contains %d designs, expected 100" % (deck, len(designs)))
        if sample[0] not in html or sample[1] not in html:
            raise AssertionError("%s sample word is missing: %r" % (deck, sample))
        for design in designs:
            if not isinstance(design.get("fields"), list) or not design["fields"]:
                raise AssertionError("%s has a design without the deck field schema" % deck)
    protected_after = {name: digest(ROOT / name) for name in protected_before}
    if protected_before != protected_after:
        raise AssertionError("A protected file changed during gallery build")
    print("PASS: 4 galleries, 100 designs each, sample words, schemas, and protected-file hashes")


if __name__ == "__main__":
    main()
