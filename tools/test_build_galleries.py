#!/usr/bin/env python3
"""Regression tests for gallery builds; never deploy or modify protected pages."""
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SAMPLES = {
    "en9": ("Student", "طالب"),
    "enlit": ("Novel", "رواية"),
    "ensci": ("Atom", "ذرة"),
    "fr9": ("Leçon", "درس"),
}
PROTECTED = ("index.html", "bac12.html", "out/bac12.html")
ANKI_RESERVED = {
    "FrontSide", "Tags", "Type", "Deck", "Subdeck", "Card",
    "c1", "c2", "c3", "c4", "c5", "c6",
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def embedded_designs(html):
    marker = "var EMBEDDED_DESIGNS_100 = "
    pos = html.find(marker)
    if pos < 0:
        raise AssertionError("EMBEDDED_DESIGNS_100 is missing")
    start = html.find("[", pos)
    if start < 0:
        raise AssertionError("Design catalog array opener is missing")
    depth = 0
    in_string = escaped = False
    for i in range(start, len(html)):
        ch = html[i]
        if in_string:
            if escaped:
                escaped = False
            elif ch == "\\":
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


def sample_binding(html, sample):
    expected = "var pwf='%s',pwa='%s';" % sample
    if expected not in html:
        raise AssertionError("Preview binding is incorrect; expected %s" % expected)


def main():
    protected_before = {
        name: digest(ROOT / name)
        for name in PROTECTED
        if (ROOT / name).is_file()
    }

    render = (ROOT / "render.yaml").read_text(encoding="utf-8")
    match = re.search(r"^\s*buildCommand:\s*(.+)$", render, re.MULTILINE)
    if not match:
        raise AssertionError("render.yaml buildCommand is missing")
    command = match.group(1)
    if "cp out/*.html" in command:
        raise AssertionError("Unsafe wildcard copy could overwrite a protected gallery")
    for deck in EXPECTED_SAMPLES:
        if "out/%s.html" % deck not in command:
            raise AssertionError("Render command must publish %s.html explicitly" % deck)
    if "out/bac12.html" in command:
        raise AssertionError("Render command must not copy the protected bac12 gallery")

    subprocess.run(
        [sys.executable, str(ROOT / "tools" / "build_galleries.py")],
        cwd=ROOT,
        check=True,
    )

    for deck, sample in EXPECTED_SAMPLES.items():
        out_path = ROOT / "out" / (deck + ".html")
        if not out_path.is_file():
            raise AssertionError("Missing output: " + str(out_path))
        html = out_path.read_text(encoding="utf-8")
        designs = embedded_designs(html)
        if len(designs) != 100:
            raise AssertionError("%s has %d designs; expected exactly 100" % (deck, len(designs)))
        sample_binding(html, sample)

        model_path = ROOT / "tools" / "decks" / deck / "templates.json"
        model_data = json.loads(model_path.read_text(encoding="utf-8"))
        models = model_data.get("models")
        if not isinstance(models, list) or not models:
            raise AssertionError("%s has no valid model schema" % deck)
        expected_fields = models[0].get("fields")
        if not isinstance(expected_fields, list) or not expected_fields:
            raise AssertionError("%s has no non-empty model fields" % deck)
        expected_set = set(expected_fields)
        for model in models[1:]:
            if set(model.get("fields", [])) != expected_set:
                raise AssertionError("%s model variants have incompatible field sets" % deck)

        for number, design in enumerate(designs, 1):
            if not isinstance(design.get("fields"), list) or design["fields"] != expected_fields:
                raise AssertionError("%s design %02d has an incorrect deck field schema" % (deck, number))
            if design.get("pack") != deck:
                raise AssertionError("%s design %02d retains the wrong pack ID" % (deck, number))
            for side in ("front", "back"):
                template = design.get(side)
                if not isinstance(template, str):
                    raise AssertionError("%s design %02d has no %s HTML" % (deck, number, side))
                fields = {
                    field_name.strip()
                    for _, field_name in re.findall(r"\{\{([#\^/]?)([^{}]+)\}\}", template)
                }
                unknown = sorted(fields - expected_set - ANKI_RESERVED)
                if unknown:
                    raise AssertionError("%s design %02d %s contains unmapped fields: %s" %
                                         (deck, number, side, ", ".join(unknown)))

    protected_after = {
        name: digest(ROOT / name)
        for name in protected_before
    }
    if protected_before != protected_after:
        raise AssertionError("A protected source/output file changed during the build")

    print("PASS: all four galleries contain 100 mapped designs; sample bindings, pack IDs,")
    print("      field schemas, and protected-file hashes are valid.")


if __name__ == "__main__":
    main()
