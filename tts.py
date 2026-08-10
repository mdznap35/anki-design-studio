#!/usr/bin/env python3
"""
توليد الصوت للرزم:
1) مكتبة صوتية جاهزة (audio_library.json): كلمة -> {fr, ar, both} (base64)
2) مكمّل عبر Edge-TTS (أصوات رجالية) مع تحكم بالسرعة والنغمة + كاش
"""
import os, json, base64, threading

LIBRARY_PATH = os.path.join(os.path.dirname(__file__), "audio_library.json")
VOICES = {"fr": "fr-FR-HenriNeural", "ar": "ar-SA-HamedNeural"}
DEFAULT_FIELDS = ["French", "Arabic", "FrSound", "ArSound", "BothSound",
                  "FrFile", "ArFile", "BothFile", "AudioFR", "AudioAR",
                  "AudioBOTH", "ExtraRows"]

_lib = {}
_lib_loaded = False
_lib_lock = threading.Lock()
_cache = {}
_cache_lock = threading.Lock()


def _norm(w):
    return (w or "").strip().lower()


def load_library():
    global _lib, _lib_loaded
    if _lib_loaded:
        return _lib
    with _lib_lock:
        if _lib_loaded:
            return _lib
        if os.path.exists(LIBRARY_PATH):
            try:
                with open(LIBRARY_PATH, encoding="utf-8") as f:
                    _lib = json.load(f)
            except Exception:
                _lib = {}
        _lib_loaded = True
    return _lib


def library_lookup(word):
    load_library()
    return _lib.get(_norm(word))


def _edge_synth(text, lang, rate_pct, pitch_hz):
    import asyncio
    import edge_tts

    async def _run():
        com = edge_tts.Communicate(text, VOICES.get(lang, VOICES["fr"]),
                                   rate=f"{rate_pct:+d}%", pitch=f"{pitch_hz:+d}Hz")
        buf = b""
        async for chunk in com.stream():
            if chunk["type"] == "audio":
                buf += chunk["data"]
        return buf

    return asyncio.run(_run())


def _synth_base64(text, lang, rate_pct, pitch_hz):
    if not text:
        return ""
    key = (text, lang, rate_pct, pitch_hz)
    with _cache_lock:
        if key in _cache:
            return _cache[key]
    try:
        mp3 = _edge_synth(text, lang, rate_pct, pitch_hz)
        if not mp3:
            return ""
        b64 = base64.b64encode(mp3).decode("ascii")
        b64 = "data:audio/mpeg;base64," + b64
    except Exception:
        return ""
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


def ensure_word_audio(word, arabic, speed=1.0, pitch=1.0):
    """يرجع (fr_b64, ar_b64, both_b64) أو ('','','') عند الفشل"""
    word = (word or "").strip()
    arabic = (arabic or "").strip()
    if not word:
        return ("", "", "")
    lib = library_lookup(word)
    if lib:
        return (lib.get("fr", ""), lib.get("ar", ""), lib.get("both", ""))
    rate_pct, pitch_hz = speed_pitch_to_params(speed, pitch)
    fr_a = _synth_base64(word, "fr", rate_pct, pitch_hz)
    ar_a = _synth_base64(arabic, "ar", rate_pct, pitch_hz) if arabic else ""
    both_a = ""
    if fr_a and ar_a:
        # دمج FR + AR في مقطع واحد (نفس ترميز mp3) -> زر "الاثنان معاً"
        try:
            fr_raw = base64.b64decode(fr_a.split(",", 1)[1])
            ar_raw = base64.b64decode(ar_a.split(",", 1)[1])
            both_raw = fr_raw + ar_raw
            both_a = "data:audio/mpeg;base64," + base64.b64encode(both_raw).decode("ascii")
        except Exception:
            both_a = ""
    return (fr_a, ar_a, both_a)


def note_fields_for(fields, word, arabic, speed=1.0, pitch=1.0, extra="", include_audio=True):
    """يبني صف الحقول بالترتيب المطلوب من القالب"""
    fr_a = ar_a = both_a = ""
    if include_audio:
        try:
            fr_a, ar_a, both_a = ensure_word_audio(word, arabic, speed, pitch)
        except Exception:
            fr_a = ar_a = both_a = ""
    mapping = {
        "French": word, "Arabic": arabic,
        "FrSound": "", "ArSound": "", "BothSound": "",
        "FrFile": "", "ArFile": "", "BothFile": "",
        "AudioFR": fr_a, "AudioAR": ar_a, "AudioBOTH": both_a,
        "ExtraRows": extra,
    }
    return [str(mapping.get(f, "")) for f in fields]
