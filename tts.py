#!/usr/bin/env python3
"""
توليد الصوت للرزم:
1) مكتبة صوتية جاهزة (audio_library.json): كلمة -> {fr, ar, both} (base64)
2) مكمّل عبر Edge-TTS (أصوات رجالية/نسائية/لهجات عربية وفرنسية)
   مع تحكم بالسرعة والنغمة والفاصل الزمني بين الكلمات + كاش
"""
import os, json, base64, threading, subprocess, tempfile, shutil

LIBRARY_PATH = os.path.join(os.path.dirname(__file__), "audio_library.json")
DEFAULT_FIELDS = ["French", "Arabic", "FrSound", "ArSound", "BothSound",
                  "FrFile", "ArFile", "BothFile", "AudioFR", "AudioAR",
                  "AudioBOTH", "ExtraRows"]

# ===== بنك الأصوات (edge-tts) — فرنسية: رجال/نساء، عربية: لهجات كاملة =====
FR_VOICES = [
    {"id": "fr-FR-HenriNeural",            "label": "فرنسي (فرنسا) — هنري",    "gender": "male"},
    {"id": "fr-FR-RemyMultilingualNeural", "label": "فرنسي (فرنسا) — ريمي",    "gender": "male"},
    {"id": "fr-CA-AntoineNeural",          "label": "فرنسي (كندا) — أنطوان",   "gender": "male"},
    {"id": "fr-CA-JeanNeural",             "label": "فرنسي (كندا) — جان",      "gender": "male"},
    {"id": "fr-CA-ThierryNeural",          "label": "فرنسي (كندا) — تييري",    "gender": "male"},
    {"id": "fr-BE-GerardNeural",           "label": "فرنسي (بلجيكا) — جيرار",  "gender": "male"},
    {"id": "fr-CH-FabriceNeural",          "label": "فرنسي (سويسرا) — فابريس", "gender": "male"},
    {"id": "fr-FR-DeniseNeural",           "label": "فرنسي (فرنسا) — دينيس",   "gender": "female"},
    {"id": "fr-FR-EloiseNeural",           "label": "فرنسي (فرنسا) — إلويز",   "gender": "female"},
    {"id": "fr-FR-VivienneMultilingualNeural", "label": "فرنسي (فرنسا) — فيفيان", "gender": "female"},
    {"id": "fr-CA-SylvieNeural",           "label": "فرنسي (كندا) — سيلفي",    "gender": "female"},
    {"id": "fr-BE-CharlineNeural",         "label": "فرنسي (بلجيكا) — شارلين", "gender": "female"},
    {"id": "fr-CH-ArianeNeural",           "label": "فرنسي (سويسرا) — أريان",  "gender": "female"},
]

AR_VOICES = [
    {"id": "ar-SA-HamedNeural",    "label": "عربي (السعودية) — حامد",   "gender": "male"},
    {"id": "ar-SA-ZariyahNeural",  "label": "عربي (السعودية) — زريا",   "gender": "female"},
    {"id": "ar-AE-HamdanNeural",   "label": "عربي (الإمارات) — حمدان",  "gender": "male"},
    {"id": "ar-AE-FatimaNeural",   "label": "عربي (الإمارات) — فاطمة",  "gender": "female"},
    {"id": "ar-BH-AliNeural",      "label": "عربي (البحرين) — علي",     "gender": "male"},
    {"id": "ar-BH-LailaNeural",    "label": "عربي (البحرين) — ليلى",    "gender": "female"},
    {"id": "ar-DZ-IsmaelNeural",   "label": "عربي (الجزائر) — إسماعيل", "gender": "male"},
    {"id": "ar-DZ-AminaNeural",    "label": "عربي (الجزائر) — أمينة",   "gender": "female"},
    {"id": "ar-EG-ShakirNeural",   "label": "عربي (مصر) — شاكر",        "gender": "male"},
    {"id": "ar-EG-SalmaNeural",    "label": "عربي (مصر) — سلمى",        "gender": "female"},
    {"id": "ar-IQ-BasselNeural",   "label": "عربي (العراق) — باسل",     "gender": "male"},
    {"id": "ar-IQ-RanaNeural",     "label": "عربي (العراق) — رنا",      "gender": "female"},
    {"id": "ar-JO-TaimNeural",     "label": "عربي (الأردن) — تيم",      "gender": "male"},
    {"id": "ar-JO-SanaNeural",     "label": "عربي (الأردن) — سناء",     "gender": "female"},
    {"id": "ar-KW-FahedNeural",    "label": "عربي (الكويت) — فهد",      "gender": "male"},
    {"id": "ar-KW-NouraNeural",    "label": "عربي (الكويت) — نورة",     "gender": "female"},
    {"id": "ar-LB-RamiNeural",     "label": "عربي (لبنان) — رامي",      "gender": "male"},
    {"id": "ar-LB-LaylaNeural",    "label": "عربي (لبنان) — ليلى",      "gender": "female"},
    {"id": "ar-LY-OmarNeural",     "label": "عربي (ليبيا) — عمر",       "gender": "male"},
    {"id": "ar-LY-ImanNeural",     "label": "عربي (ليبيا) — إيمان",     "gender": "female"},
    {"id": "ar-MA-JamalNeural",    "label": "عربي (المغرب) — جمال",     "gender": "male"},
    {"id": "ar-MA-MounaNeural",    "label": "عربي (المغرب) — منى",      "gender": "female"},
    {"id": "ar-OM-AbdullahNeural", "label": "عربي (عُمان) — عبدالله",   "gender": "male"},
    {"id": "ar-OM-AyshaNeural",    "label": "عربي (عُمان) — عائشة",     "gender": "female"},
    {"id": "ar-QA-MoazNeural",     "label": "عربي (قطر) — معاذ",        "gender": "male"},
    {"id": "ar-QA-AmalNeural",     "label": "عربي (قطر) — أمل",         "gender": "female"},
    {"id": "ar-SY-LaithNeural",    "label": "عربي (سوريا) — ليث",       "gender": "male"},
    {"id": "ar-SY-AmanyNeural",    "label": "عربي (سوريا) — أماني",     "gender": "female"},
    {"id": "ar-TN-HediNeural",     "label": "عربي (تونس) — هادي",       "gender": "male"},
    {"id": "ar-TN-ReemNeural",     "label": "عربي (تونس) — ريم",        "gender": "female"},
    {"id": "ar-YE-SalehNeural",    "label": "عربي (اليمن) — صالح",      "gender": "male"},
    {"id": "ar-YE-MaryamNeural",   "label": "عربي (اليمن) — مريم",      "gender": "female"},
]

VOICE_POOL = {"fr": FR_VOICES, "ar": AR_VOICES}
DEFAULT_VOICES = {"fr": "fr-FR-HenriNeural", "ar": "ar-SA-HamedNeural"}

_lib = {}
_lib_loaded = False
_lib_lock = threading.Lock()
_cache = {}
_cache_lock = threading.Lock()
_sil_cache = {}
_sil_lock = threading.Lock()
_FFMPEG = shutil.which("ffmpeg")

WORD_CACHE_DIR = os.path.join(tempfile.gettempdir(), "anki_word_cache")  # nosec S5443
WORD_CACHE_MAX_BYTES = 600 * 1024 * 1024  # سقف حجم الكاش (~600MB)
os.makedirs(WORD_CACHE_DIR, exist_ok=True)


def _word_cache_path(text, lang, rate_pct, pitch_hz, voice):
    import hashlib
    h = hashlib.md5(("%s|%s|%d|%d|%s" % (text, lang, rate_pct, pitch_hz, voice)).encode("utf-8")).hexdigest()
    return os.path.join(WORD_CACHE_DIR, h + ".txt")


def _word_cache_read(text, lang, rate_pct, pitch_hz, voice):
    try:
        with open(_word_cache_path(text, lang, rate_pct, pitch_hz, voice), encoding="utf-8") as f:
            return f.read().strip() or ""
    except Exception:
        return ""


_trim_counter = [0]


def _word_cache_write(text, lang, rate_pct, pitch_hz, voice, b64):
    try:
        p = _word_cache_path(text, lang, rate_pct, pitch_hz, voice)
        with open(p, "w", encoding="utf-8") as f:
            f.write(b64)
        _trim_counter[0] += 1
        if _trim_counter[0] % 25 == 0:
            _trim_word_cache()
    except Exception:
        pass


def _trim_word_cache():
    try:
        files = []
        total = 0
        for fn in os.listdir(WORD_CACHE_DIR):
            if not fn.endswith(".txt"):
                continue
            fp = os.path.join(WORD_CACHE_DIR, fn)
            try:
                sz = os.path.getsize(fp)
            except OSError:
                continue
            files.append((os.path.getmtime(fp), fp, sz))
            total += sz
        if total <= WORD_CACHE_MAX_BYTES:
            return
        files.sort()
        for _, fp, sz in files:
            if total <= WORD_CACHE_MAX_BYTES:
                break
            try:
                os.remove(fp)
                total -= sz
            except OSError:
                pass
    except Exception:
        pass


def word_cached(word, arabic="", cfg=None):
    """هل صوت الفرنسي والعربي لهذه الكلمة مولّد ومحفوظ من قبل (بنفس الإعدادات)؟"""
    cfg = cfg or {}
    try:
        rate_pct, pitch_hz = speed_pitch_to_params(cfg.get("speed", 1.0), cfg.get("pitch", 1.0))
        fr_voice = resolve_voice("fr", cfg.get("frVoice"))
        ar_voice = resolve_voice("ar", cfg.get("arVoice"))
        w = (word or "").strip()
        a = (arabic or "").strip()
        if not w:
            return False
        if not bool(_word_cache_read(w, "fr", rate_pct, pitch_hz, fr_voice)):
            return False
        if a and not bool(_word_cache_read(a, "ar", rate_pct, pitch_hz, ar_voice)):
            return False
        return True
    except Exception:
        return False


def _norm(w):
    return (w or "").strip().lower()


def load_library():
    global _lib, _lib_loaded
    if _lib_loaded:
        return _lib
    with _lib_lock:
        if _lib_loaded:
            return _lib
        merged = {}
        base = os.path.dirname(os.path.abspath(__file__))
        try:
            files = sorted(f for f in os.listdir(base)
                           if f.startswith('audio_library') and f.endswith('.json'))
        except Exception:
            files = []
        for fn in files:
            try:
                with open(os.path.join(base, fn), encoding='utf-8') as f:
                    data = json.load(f)
                if isinstance(data, dict):
                    merged.update(data)
            except Exception:
                pass
        _lib = merged
        _lib_loaded = True
    return _lib


def library_lookup(word):
    load_library()
    return _lib.get(_norm(word))


def voice_list():
    """قائمة الأصوات الكاملة للواجهة (فرنسي + عربي)"""
    return {"fr": FR_VOICES, "ar": AR_VOICES}


def resolve_voice(lang, vid):
    """تأكيد أن الصوت المطلوب موجود فعلاً، وإلا الرجوع للافتراضي"""
    pool = VOICE_POOL.get(lang, [])
    if vid:
        for v in pool:
            if v["id"] == vid:
                return vid
    return DEFAULT_VOICES.get(lang, "fr-FR-HenriNeural")


def needs_regen(cfg, has_lib):
    """هل يجب إعادة توليد الصوت عبر edge-tts (تغيير صوت/سرعة/نغمة) أم تكفي المكتبة؟"""
    if not has_lib:
        return True
    try:
        if float(cfg.get("speed", 1.0) or 1.0) != 1.0:
            return True
        if float(cfg.get("pitch", 1.0) or 1.0) != 1.0:
            return True
    except (TypeError, ValueError):
        return True
    if cfg.get("frVoice") and cfg.get("frVoice") != DEFAULT_VOICES["fr"]:
        return True
    if cfg.get("arVoice") and cfg.get("arVoice") != DEFAULT_VOICES["ar"]:
        return True
    return False


def _edge_synth(text, lang, rate_pct, pitch_hz, voice):
    import asyncio
    import edge_tts

    async def _run():
        com = edge_tts.Communicate(text, voice,
                                   rate="%+d%%" % rate_pct, pitch="%+dHz" % pitch_hz)
        buf = b""
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                buf += chunk["data"]
        return buf

    return asyncio.run(_run())


def _synth_base64(text, lang, rate_pct, pitch_hz, voice, _tries=3):
    if not text:
        return ""
    key = (text, lang, rate_pct, pitch_hz, voice)
    with _cache_lock:
        if key in _cache:
            return _cache[key]
    disk = _word_cache_read(text, lang, rate_pct, pitch_hz, voice)
    if disk:
        with _cache_lock:
            _cache[key] = disk
        return disk
    import time
    b64 = ""
    for i in range(_tries):
        try:
            mp3 = _edge_synth(text, lang, rate_pct, pitch_hz, voice)
            if mp3:
                b64 = "data:audio/mpeg;base64," + base64.b64encode(mp3).decode("ascii")
                break
        except Exception:
            pass
        if i < _tries - 1:
            time.sleep(0.8 * (i + 1))
    if not b64:
        return ""
    _word_cache_write(text, lang, rate_pct, pitch_hz, voice, b64)
    with _cache_lock:
        _cache[key] = b64
    return b64


def speed_pitch_to_params(speed, pitch):
    """speed/pitch من الواجهة (0.5..2) -> rate% / pitchHz"""
    try:
        speed = float(speed)
    except (TypeError, ValueError):
        speed = 1.0
    try:
        pitch = float(pitch)
    except (TypeError, ValueError):
        pitch = 1.0
    rate_pct = max(-50, min(100, int(round((speed - 1) * 100))))
    pitch_hz = max(-20, min(20, int(round((pitch - 1) * 30))))
    return rate_pct, pitch_hz


def _silence(ms):
    """مقطع mp3 صامت (24000Hz mono) بالطول المطلوب — يُولَّد مرة واحدة ويُخزَّن"""
    if not _FFMPEG or not ms:
        return b""
    ms = int(ms)
    if ms <= 0:
        return b""
    with _sil_lock:
        if ms in _sil_cache:
            return _sil_cache[ms]
    tmp = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp.close()
    try:
        subprocess.run([_FFMPEG, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                        "-t", "%.3f" % (ms / 1000.0), "-q:a", "9", tmp.name],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=20)
        with open(tmp.name, "rb") as f:
            data = f.read()
    except Exception:
        data = b""
    finally:
        try:
            os.remove(tmp.name)
        except OSError:
            pass
    if data:
        with _sil_lock:
            _sil_cache[ms] = data
    return data


def _concat_mp3(parts):
    """دمج مقاطع mp3 متطابقة الخصائص عبر ffmpeg (نسخ مباشر بدون إعادة ترميز)"""
    parts = [p for p in parts if p]
    if not parts:
        return b""
    if len(parts) == 1:
        return parts[0]
    if not _FFMPEG:
        return b"".join(parts)
    try:
        with tempfile.TemporaryDirectory() as td:
            list_path = os.path.join(td, "list.txt")
            with open(list_path, "w", encoding="utf-8") as lf:
                for i, p in enumerate(parts):
                    fp = os.path.join(td, "p%d.mp3" % i)
                    with open(fp, "wb") as f:
                        f.write(p)
                    lf.write("file '%s'\n" % fp)
            out = os.path.join(td, "out.mp3")
            r = subprocess.run([_FFMPEG, "-y", "-f", "concat", "-safe", "0",
                                "-i", list_path, "-c", "copy", out],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                               timeout=30)
            if r.returncode == 0 and os.path.exists(out):
                with open(out, "rb") as f:
                    return f.read()
    except Exception:
        pass
    return b"".join(parts)


def _b64_mp3(raw):
    return "data:audio/mpeg;base64," + base64.b64encode(raw).decode("ascii") if raw else ""


def _build_clips(fr_raw, ar_raw, cfg):
    """تطبيق الفواصل الزمنية ويرجع (fr_b64, ar_b64, both_b64)
    - قبل الفرنسي / بعد الفرنسي (= الفاصل بين الكلمتين في المقطع المدمج)
    - قبل العربي / بعد العربي
    """
    fr_before = _silence(cfg.get("frGapBefore", 0))
    fr_after = _silence(cfg.get("frGapAfter", 0))
    ar_before = _silence(cfg.get("arGapBefore", 0))
    ar_after = _silence(cfg.get("arGapAfter", 0))

    fr_clip = _concat_mp3([fr_before, fr_raw, fr_after]) if fr_raw else b""
    ar_clip = _concat_mp3([ar_before, ar_raw, ar_after]) if ar_raw else b""
    if fr_raw and ar_raw:
        both_raw = _concat_mp3([fr_before, fr_raw, fr_after, ar_raw, ar_after])
    elif fr_raw:
        both_raw = fr_clip
    else:
        both_raw = b""
    return _b64_mp3(fr_clip), _b64_mp3(ar_clip), _b64_mp3(both_raw)


def _gaps_active(cfg):
    for k in ("frGapBefore", "frGapAfter", "arGapBefore", "arGapAfter"):
        try:
            if int(cfg.get(k, 0) or 0) > 0:
                return True
        except (TypeError, ValueError):
            pass
    return False


def _raw_from_b64(b64):
    if not b64:
        return b""
    try:
        return base64.b64decode(str(b64).split(",", 1)[1])
    except Exception:
        return b""


def ensure_word_audio(word, arabic, cfg=None):
    """يرجع (fr_b64, ar_b64, both_b64) حسب الإعدادات (أصوات + فاصل + سرعة + نغمة)"""
    cfg = cfg or {}
    word = (word or "").strip()
    arabic = (arabic or "").strip()
    if not word:
        return ("", "", "")

    lib = library_lookup(word)
    has_gaps = _gaps_active(cfg)
    regen = needs_regen(cfg, bool(lib))

    # مكتبة جاهزة + إعدادات افتراضية بدون فواصل: مسار سريع (تضمين مباشر)
    if lib and not has_gaps and not regen:
        fr_a = lib.get("fr", "")
        ar_a = lib.get("ar", "")
        both_a = lib.get("both", "")
        if not both_a and fr_a and ar_a:
            both_a = _b64_mp3(_raw_from_b64(fr_a) + _raw_from_b64(ar_a))
        return (fr_a, ar_a, both_a)

    # مكتبة جاهزة + إعدادات افتراضية مع فواصل: نبني المقاطع من المكتبة مع الصمت
    if lib and has_gaps and not regen:
        fr_raw = _raw_from_b64(lib.get("fr", ""))
        ar_raw = _raw_from_b64(lib.get("ar", ""))
        return _build_clips(fr_raw, ar_raw, cfg)

    # توليد عبر edge-tts بالصوت المحدد لكل لغة
    rate_pct, pitch_hz = speed_pitch_to_params(cfg.get("speed", 1.0), cfg.get("pitch", 1.0))
    fr_voice = resolve_voice("fr", cfg.get("frVoice"))
    ar_voice = resolve_voice("ar", cfg.get("arVoice"))
    fr_b64 = _synth_base64(word, "fr", rate_pct, pitch_hz, fr_voice)
    ar_b64 = _synth_base64(arabic, "ar", rate_pct, pitch_hz, ar_voice) if arabic else ""
    if not fr_b64 and not ar_b64:
        return ("", "", "")
    fr_raw = _raw_from_b64(fr_b64)
    ar_raw = _raw_from_b64(ar_b64)
    return _build_clips(fr_raw, ar_raw, cfg)


def preview(cfg=None, fr_text="Bonjour", ar_text="مرحبا"):
    """معاينة سريعة بإعدادات المستخدم الحالية"""
    cfg = dict(cfg or {})
    return ensure_word_audio(fr_text, ar_text, cfg)


def note_fields_for(fields, w, cfg=None, extra="", include_audio=True):
    """يبني صف الحقول بالترتيب المطلوب من القالب (يدعم الحقول الدلالية + الصوت)"""
    if isinstance(w, dict):
        word = w.get('word', '') or ''
        arabic = w.get('arabe', '') or ''
    else:
        word = w or ''
        arabic = ''
    fr_a = ar_a = both_a = ""
    if include_audio:
        try:
            fr_a, ar_a, both_a = ensure_word_audio(word, arabic, cfg)
        except Exception:
            fr_a = ar_a = both_a = ""
    if isinstance(w, dict):
        g = lambda k: str(w.get(k, '') or '')
    else:
        g = lambda k: ''
    mapping = {
        "French": word, "Arabic": arabic,
        "FrSound": "", "ArSound": "", "BothSound": "",
        "FrFile": "", "ArFile": "", "BothFile": "",
        "AudioFR": fr_a, "AudioAR": ar_a, "AudioBOTH": both_a,
        "ExtraRows": extra, "Extras": extra,
        "Plural": g('pluriel'), "Synonym": g('synonyme'), "Antonym": g('contraire'),
        "Unit": g('unit'), "Type": g('type'), "Page": g('page'), "Extra": g('extra'),
    }
    return [str(mapping.get(f, "")) for f in fields]
