#!/usr/bin/env python3
"""
استيراد مكتبة صوتية من رزمة APKG فيها أصوات جاهزة:
- يقرأ الحقول AudioFR / AudioAR / AudioBOTH (data URI) أو وسوم [sound:file.mp3]
- ينتج audio_library.json: { كلمة (lowercase) : {fr, ar, both} (base64) }

الاستخدام:
  python3 tools/import_audio_library.py /path/to/deck.apkg
"""
import sys, os, json, re, base64, sqlite3, zipfile, tempfile

AUDIO_FIELDS = ["AudioFR", "AudioAR", "AudioBOTH"]
OUT = os.path.join(os.path.dirname(__file__), "..", "audio_library.json")


def extract_from_apkg(path):
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        media_map = {}
        if "media" in names:
            try:
                media_map = json.loads(z.read("media").decode("utf-8", "replace"))
            except Exception:
                media_map = {}
        with z.open("collection.anki2") as f:
            db = f.read()

    tmp = tempfile.NamedTemporaryFile(suffix=".anki2", delete=False)
    tmp.write(db)
    tmp.close()
    con = sqlite3.connect(tmp.name)
    cur = con.cursor()
    models = json.loads(cur.execute("SELECT models FROM col").fetchone()[0])
    fld_order = {}
    for mid, m in models.items():
        fld_order[mid] = [f["name"] for f in m.get("flds", [])]
    notes = cur.execute("SELECT mid, flds FROM notes").fetchall()
    con.close()
    os.unlink(tmp.name)

    def read_audio(value, z):
        v = (value or "").strip()
        if v.startswith("data:audio"):
            return v
        m = re.search(r"\[sound:([^\]]+)\]", v)
        if m:
            fname = m.group(1)
            num = media_map.get(fname)
            if num is not None:
                data = z.read(str(num))
                return "data:audio/mpeg;base64," + base64.b64encode(data).decode("ascii")
        return ""

    lib = {}
    with zipfile.ZipFile(path) as z:
        for mid, flds_raw in notes:
            fields = flds_raw.split("\x1f")
            names_ = fld_order.get(mid, [])
            d = dict(zip(names_, fields))
            word = (d.get("French") or d.get("word") or "").strip()
            if not word:
                continue
            fr = read_audio(d.get("AudioFR", ""), z)
            ar = read_audio(d.get("AudioAR", ""), z)
            both = read_audio(d.get("AudioBOTH", ""), z)
            if not (fr or ar or both):
                continue
            key = word.lower()
            entry = lib.setdefault(key, {})
            if fr: entry["fr"] = fr
            if ar: entry["ar"] = ar
            if both: entry["both"] = both
    return lib


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("الاستخدام: python3 tools/import_audio_library.py /path/to/deck.apkg")
        sys.exit(1)
    lib = extract_from_apkg(os.path.abspath(sys.argv[1]))
    if not lib:
        print("ما لقينا أصوات في الرزمة")
        sys.exit(1)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(lib, f, ensure_ascii=False)
    print(f"تم: {len(lib)} كلمة -> {os.path.realpath(OUT)}")
