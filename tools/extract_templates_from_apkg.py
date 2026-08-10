#!/usr/bin/env python3
"""
استخراج القوالب المئة حرفياً من رزمة APKG إلى designs_100.js
المصدر: رزمة_الفرنسية_100_تصميم_كلمة_واحدة_مضبوطة.apkg
"""
import sqlite3, json, re, sys, os

APKG = "/root/Documents/Muhammad/رزمة_الفرنسية_100_تصميم_كلمة_واحدة_مضبوطة.apkg"
OUT = os.path.join(os.path.dirname(__file__), "..", "public", "designs_100.js")

import zipfile, tempfile
with zipfile.ZipFile(APKG) as z:
    with z.open("collection.anki2") as f:
        data = f.read()

tmp = tempfile.NamedTemporaryFile(suffix=".anki2", delete=False)
tmp.write(data); tmp.close()
con = sqlite3.connect(tmp.name)
cur = con.cursor()
models = json.loads(cur.execute("SELECT models FROM col").fetchone()[0])
con.close(); os.unlink(tmp.name)

def num_of(name):
    m = re.search(r"تصميم\s*(\d+)", name)
    return int(m.group(1)) if m else None

by_num = {}
for mid, m in models.items():
    n = num_of(m.get("name", ""))
    if n is None:
        continue
    tmpl = m["tmpls"][0]
    flds = [f["name"] for f in m.get("flds", [])]
    by_num[n] = {
        "name": f"{n:02d}",
        "fields": flds,
        "front": tmpl.get("qfmt", ""),
        "back": tmpl.get("afmt", ""),
        "css": m.get("css", ""),
        "pack": "",
    }

items = [by_num[i] for i in sorted(by_num) if i in by_num]
if len(items) != 100:
    print(f"خطأ: عدد القوالب المستخرجة {len(items)} وليس 100")
    sys.exit(1)

# تحقق أن كل قالب فيه الـ12 حقلاً بالترتيب
EXPECTED = ["French","Arabic","FrSound","ArSound","BothSound","FrFile","ArFile","BothFile","AudioFR","AudioAR","AudioBOTH","ExtraRows"]
for it in items:
    if it["fields"] != EXPECTED:
        print(f"خطأ في حقول القالب {it['name']}: {it['fields']}")
        sys.exit(1)
    if not it["front"] or not it["back"] or not it["css"]:
        print(f"خطأ: قالب {it['name']} فيه جزء فارغ")
        sys.exit(1)

js = "var EMBEDDED_DESIGNS_100 = " + json.dumps(items, ensure_ascii=False, separators=(",", ":")) + ";"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(js)
print(f"تم: {len(items)} قالب -> {os.path.realpath(OUT)} ({os.path.getsize(OUT)} bytes)")
