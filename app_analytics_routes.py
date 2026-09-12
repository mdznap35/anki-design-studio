# ============================================================
# تحليلات Anki Design Studio — أضف هاد البلوك لـ app.py (Flask)
# ============================================================
# 1) تأكد إنك موجود عندك في أعلى app.py:  import json, os
#    وإذا ما في، ضيفهم. كمان تأكد إنك معرّف `app = Flask(__name__)`.
# 2) اضبط المتغير OWNER_KEY من Environment على Render (مفتاح قوي بتبتدعه إنت).
# 3) الصفحة (index.html) بتبعت لنفس الرابط (/api/track, /api/stats) فما في حاجة تعدّل بالواجهة.
# ------------------------------------------------------------

import json, os

ANALYTICS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'analytics.json')
OWNER_KEY = os.environ.get('OWNER_KEY', 'owner-secret-change-me')
ANALYTICS_MAX_EVENTS = 200000


def _analytics_load():
    try:
        with open(ANALYTICS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return []


def _analytics_save(events):
    try:
        if len(events) > ANALYTICS_MAX_EVENTS:
            events = events[-ANALYTICS_MAX_EVENTS:]
        with open(ANALYTICS_FILE, 'w', encoding='utf-8') as f:
            json.dump(events, f)
    except Exception:
        pass


@app.route('/api/track', methods=['POST', 'OPTIONS'])
def api_track():
    if request.method == 'OPTIONS':
        return ('', 204)
    try:
        ev = request.get_json(force=True, silent=True) or {}
        if ev.get('type'):
            events = _analytics_load()
            events.append(ev)
            _analytics_save(events)
    except Exception:
        pass
    return jsonify({'ok': True})


@app.route('/api/stats', methods=['GET'])
def api_stats():
    key = request.args.get('key', '')
    if key != OWNER_KEY:
        return jsonify({'error': 'unauthorized'}), 403
    events = _analytics_load()
    visitors = set()
    downloaders = set()
    visits = 0
    downloads = 0
    for e in events:
        if not e:
            continue
        if e.get('deviceId'):
            visitors.add(e['deviceId'])
        if e.get('type') == 'visit':
            visits += 1
        if e.get('type') == 'download':
            downloads += 1
            if e.get('deviceId'):
                downloaders.add(e['deviceId'])
    return jsonify({
        'visits': visits,
        'uniqueVisitors': len(visitors),
        'downloads': downloads,
        'uniqueDownloaders': len(downloaders)
    })
# ============================================================
# نهاية بلوك التحليلات
# ============================================================
