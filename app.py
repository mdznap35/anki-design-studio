#!/usr/bin/env python3
import os, json, re, genanki, hashlib, shutil, threading, uuid
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request, jsonify, send_file, send_from_directory
import tts

app = Flask(__name__, static_folder='public')  # nosec S4502

@app.after_request
def add_cors_headers(response):  # nosec SXXX
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response

@app.after_request
def maybe_gzip(response):  # nosec SXXX
    # ضغط الملفات الكبيرة (JS/JSON/HTML) لتسريع التحميل على الجوال
    try:
        pth = request.path or ''
        if request.method != 'GET' or response.status_code >= 400:
            return response
        if not (pth.endswith('.js') or pth.endswith('.json') or pth.endswith('.html')):
            return response
        if 'gzip' not in (request.headers.get('Accept-Encoding') or '').lower():
            return response
        if response.direct_passthrough:
            response.direct_passthrough = False
        body = response.get_data()
        if len(body) < 2048:
            return response
        comp = __import__('gzip').compress(body, 6)
        if len(comp) >= len(body):
            return response
        import hashlib
        response.set_data(comp)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(comp))
        response.headers['Vary'] = 'Accept-Encoding'
        response.headers['ETag'] = '"' + hashlib.md5(comp).hexdigest()[:16] + '-gz"'
    except Exception:
        pass
    return response

@app.route('/api/generate', methods=['OPTIONS'])
def generate_preflight():
    return '', 204

VOCAB_DATA = None
REPEATED_DATA = None
WORDS_FINAL = None
try:
    with open('parsed_data_full.json') as f:
        VOCAB_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    pass
try:
    with open('repeated_data.json') as f:
        REPEATED_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    pass
try:
    with open('words_final.json') as f:
        WORDS_FINAL = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    pass


def get_all_words():
    # المصدر الأساسي: الرزمة النهائية النظيفة (4511 كلمة)
    if WORDS_FINAL:
        return WORDS_FINAL
    if not VOCAB_DATA:
        return []
    w = []
    for uk in VOCAB_DATA:
        un = int(uk.split('_')[1])
        for x in VOCAB_DATA[uk].get('noms', []):
            w.append({'word': x.get('singulier',''), 'arabe': x.get('arabe',''), 'type': 'Nom', 'unit': un, 'page': x.get('page',''), 'pluriel': x.get('pluriel',''), 'feminin_s': '', 'feminin_p': '', 'preposition': '', 'auxiliaire': '', 'participe': '', 'synonyme': x.get('synonyme',''), 'contraire': x.get('contraire','')})
        for x in VOCAB_DATA[uk].get('adj', []):
            w.append({'word': x.get('masculin_s',''), 'arabe': x.get('arabe',''), 'type': 'Adjectif', 'unit': un, 'page': x.get('page',''), 'pluriel': '', 'feminin_s': x.get('feminin_s',''), 'feminin_p': x.get('feminin_p',''), 'preposition': '', 'auxiliaire': '', 'participe': '', 'synonyme': x.get('synonyme',''), 'contraire': x.get('contraire','')})
        for x in VOCAB_DATA[uk].get('verbs', []):
            w.append({'word': x.get('verbe',''), 'arabe': x.get('arabe',''), 'type': 'Verbe', 'unit': un, 'page': x.get('page',''), 'pluriel': '', 'feminin_s': '', 'feminin_p': '', 'preposition': x.get('preposition',''), 'auxiliaire': '', 'participe': x.get('participe',''), 'synonyme': x.get('synonyme',''), 'contraire': ''})
    return w


def get_important_words():
    # الكلمات المهمة موجودة داخل words_final.json
    if WORDS_FINAL:
        return []
    if not REPEATED_DATA:
        return []
    r = []
    for cat in ['noms', 'adj', 'verbs']:
        for x in REPEATED_DATA.get(cat, [])[:30]:
            units = x.get('units', [1])
            r.append({'word': x.get('word',''), 'arabe': x.get('arabe',''), 'type': x.get('type',''), 'unit': units[0] if units else 1, 'page': '', 'pluriel': '', 'feminin_s': '', 'feminin_p': '', 'preposition': '', 'auxiliaire': '', 'participe': '', 'synonyme': '', 'contraire': ''})
    return r


def stable_id(s):
    return int(hashlib.md5(s.encode()).hexdigest()[:15], 16)


def extra_rows(w):
    rows = []
    for label, key in [('الوحدة', 'unit'), ('النوع', 'type'), ('الجمع', 'pluriel'),
                       ('المرادف', 'synonyme'), ('الضد', 'contraire'), ('الصفحة', 'page')]:
        v = (w.get(key) or '').strip()
        if v:
            rows.append('<b>' + label + ':</b> ' + v)
    return '<br>'.join(rows)


@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'words': len(get_all_words())})


AUDIO_MAX_WORDS = 250  # حد توليد الصوت التلقائي (بدون مكتبة) — الرزمة الكاملة تحتاج المكتبة


@app.route('/api/audio_status', methods=['GET'])
def audio_status():
    tts.load_library()
    return jsonify({
        'total_words': len(get_all_words()) + len(get_important_words()),
        'library_words': len(tts._lib),
        'audio_enabled_default': len(tts._lib) > 0,
        'max_generate_words': AUDIO_MAX_WORDS,
    })


@app.route('/api/tts_voices', methods=['GET'])
def tts_voices():
    return jsonify(tts.voice_list())


@app.route('/api/tts_preview', methods=['POST'])
def tts_preview():
    try:
        data = request.get_json() or {}
        cfg = data.get('ttsConfig') or {}
        if not isinstance(cfg, dict):
            cfg = {}
        fr_a, ar_a, both_a = tts.preview(cfg, data.get('fr') or 'Bonjour',
                                         data.get('ar') or 'مرحبا')
        return jsonify({'fr': fr_a, 'ar': ar_a, 'both': both_a})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def index():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/designs_20.json', methods=['GET'])
def serve_designs():
    return send_from_directory(app.static_folder, 'designs_20.json')


@app.route('/designs_102.json', methods=['GET'])
def serve_designs_102():
    return send_from_directory(app.static_folder, 'designs_102.json')


@app.route('/designs_config_102.json', methods=['GET'])
def serve_designs_config():
    return send_from_directory(app.static_folder, 'designs_config_102.json')


@app.route('/designs_data.js', methods=['GET'])
def serve_designs_data():
    return send_from_directory(app.static_folder, 'designs_data.js')


@app.route('/designs_premium.js', methods=['GET'])
def serve_designs_premium():
    return send_from_directory(app.static_folder, 'designs_premium.js')


@app.route('/designs_100.js', methods=['GET'])
def serve_designs_100():
    return send_from_directory(app.static_folder, 'designs_100.js')


def _build_note_fields(fields, w, tts_cfg, include_audio):
    return tts.note_fields_for(fields, w.get('word', ''), w.get('arabe', ''),
                               tts_cfg, extra_rows(w), include_audio)


def _write_deck(deck, safe_name):
    apkg_path = f'/tmp/{safe_name}_{os.getpid()}.apkg'  # nosec S5443
    genanki.Package(deck).write_to_file(apkg_path)
    response = send_file(apkg_path, as_attachment=True, download_name=f'{safe_name}.apkg',
                         mimetype='application/octet-stream')
    import atexit
    atexit.register(lambda: os.remove(apkg_path) if os.path.exists(apkg_path) else None)
    return response


def _audio_guard(all_words, include_audio):
    """(محجوزة) الرزم الكبيرة أصبحت تُدار عبر نظام المهام الخلفية"""
    return None


# ===== نظام الرزم الكبيرة: كاش + مهام خلفية (Jobs) =====
DECK_CACHE_DIR = '/tmp/anki_deck_cache'  # nosec S5443
os.makedirs(DECK_CACHE_DIR, exist_ok=True)
JOBS = {}
JOBS_LOCK = threading.Lock()
JOB_SEM = threading.Semaphore(2)


def _settings_hash(config):
    key = {
        'deck': config.get('deckName', ''),
        'designs': config.get('designs'),
        'tts': config.get('ttsConfig'),
        'audio': config.get('includeAudio', True),
        'custom': [config.get('_templateType'), config.get('_customFront'),
                   config.get('_customBack'), config.get('_customCSS'),
                   config.get('_customFields'), config.get('_templateName')],
        'words': len(get_all_words()) + len(get_important_words()),
    }
    return hashlib.md5(json.dumps(key, sort_keys=True, ensure_ascii=False).encode('utf-8')).hexdigest()


def _cache_get(h):
    p = os.path.join(DECK_CACHE_DIR, h + '.apkg')
    return p if os.path.exists(p) else None


def _cache_put(h, path):
    try:
        dest = os.path.join(DECK_CACHE_DIR, h + '.apkg')
        shutil.copyfile(path, dest)
        _trim_cache(3)  # إبقاء آخر 3 رزم محفوظة فقط
        return dest
    except Exception:
        return path


def _trim_cache(keep):
    try:
        files = [f for f in os.listdir(DECK_CACHE_DIR) if f.endswith('.apkg')]
        files.sort(key=lambda f: os.path.getmtime(os.path.join(DECK_CACHE_DIR, f)), reverse=True)
        for f in files[keep:]:
            try:
                os.remove(os.path.join(DECK_CACHE_DIR, f))
            except OSError:
                pass
    except Exception:
        pass


def _build_deck_apkg(deck_name, designs, tts_cfg, include_audio, progress=None):
    """يبني الرزمة (توزيع عادل للكلمات على التصاميم) ويعيد مسار ملف apkg"""
    all_words = get_all_words() + get_important_words()
    if not all_words:
        raise ValueError('No word data found')
    deck = genanki.Deck(stable_id('MultiDeck_' + deck_name), deck_name)
    models = []
    for i, d in enumerate(designs):
        name = d.get('name') or f'{i + 1:02d}'
        fields = d.get('fields') or tts.DEFAULT_FIELDS
        front = d.get('frontHTML', '') or '<div class="french">{{French}}</div>'
        back = d.get('backHTML', '') or front
        css = d.get('css') or ''
        mid = stable_id('MultiDesign_' + deck_name + '_' + str(i) + '_' + name)
        model = genanki.Model(
            mid, name,
            fields=[{'name': f} for f in fields],
            templates=[{'name': 'بطاقة', 'qfmt': front, 'afmt': back}],
            css=css,
            sort_field_index=0)
        models.append((model, fields))

    n = len(models)
    done = [0]
    done_lock = threading.Lock()

    def make_fields(idx):
        model, fields = models[idx % n]
        r = (model, _build_note_fields(fields, all_words[idx], tts_cfg, include_audio))
        with done_lock:
            done[0] += 1
            if progress:
                progress(done[0])
        return r

    if include_audio:
        with ThreadPoolExecutor(max_workers=6) as ex:
            results = list(ex.map(make_fields, range(len(all_words))))
    else:
        results = [make_fields(i) for i in range(len(all_words))]

    for model, nf in results:
        deck.add_note(genanki.Note(model=model, fields=nf))

    safe_name = deck_name.replace('/', '_').replace('\\', '_')
    apkg_path = os.path.join('/tmp', f'{safe_name}_{os.getpid()}_{uuid.uuid4().hex[:6]}.apkg')  # nosec S5443
    genanki.Package(deck).write_to_file(apkg_path)
    print(f"Deck built: {len(all_words)} notes across {n} designs (audio={include_audio})")
    return apkg_path


def _should_job(tts_cfg, include_audio):
    """هل تحتاج الرزمة توليد صوت بالخلفية (كبيرة أو إعدادات غير افتراضية)؟"""
    if not include_audio:
        return False
    all_words = get_all_words() + get_important_words()
    if len(all_words) <= AUDIO_MAX_WORDS:
        return False  # رزمة صغيرة: توليد فوري
    tts.load_library()
    gaps = any(int(tts_cfg.get(k, 0) or 0) > 0
               for k in ('frGapBefore', 'frGapAfter', 'arGapBefore', 'arGapAfter'))
    if tts._lib:
        missing = [w for w in all_words if not tts.library_lookup(w.get('word', ''))]
        if not missing and not gaps and not tts.needs_regen(tts_cfg, True):
            return False  # مكتبة كاملة + إعدادات افتراضية: تضمين فوري
    return True


def _job_progress(jid, n):
    with JOBS_LOCK:
        if jid in JOBS:
            JOBS[jid]['done'] = n


def _start_job(jid, h, deck_name, designs, tts_cfg, include_audio):
    all_words = get_all_words() + get_important_words()
    with JOBS_LOCK:
        JOBS[jid] = {'status': 'queued', 'done': 0, 'total': len(all_words),
                     'error': '', 'path': '', 'deck_name': deck_name}

    def run():
        with JOBS_LOCK:
            if jid in JOBS:
                JOBS[jid]['status'] = 'running'
        with JOB_SEM:
            try:
                path = _build_deck_apkg(deck_name, designs, tts_cfg, include_audio,
                                        progress=lambda n: _job_progress(jid, n))
                cached = _cache_put(h, path)
                with JOBS_LOCK:
                    if jid in JOBS:
                        JOBS[jid]['status'] = 'done'
                        JOBS[jid]['path'] = cached
                        JOBS[jid]['done'] = JOBS[jid]['total']
            except Exception as e:
                print(f"Job {jid} error: {e}")
                with JOBS_LOCK:
                    if jid in JOBS:
                        JOBS[jid]['status'] = 'error'
                        JOBS[jid]['error'] = str(e)

    threading.Thread(target=run, daemon=True).start()


def _send_apkg(path, deck_name):
    safe = deck_name.replace('/', '_').replace('\\', '_') + '.apkg'
    return send_file(path, as_attachment=True, download_name=safe, mimetype='application/octet-stream')


@app.route('/api/job/<jid>', methods=['GET'])
def job_status(jid):
    with JOBS_LOCK:
        j = dict(JOBS.get(jid) or {})
    if not j:
        return jsonify({'status': 'notfound'}), 404
    return jsonify({'status': j.get('status'), 'done': j.get('done', 0),
                    'total': j.get('total', 0), 'error': j.get('error', '')})


@app.route('/api/download/<jid>', methods=['GET'])
def job_download(jid):
    with JOBS_LOCK:
        j = dict(JOBS.get(jid) or {})
    if not j or j.get('status') != 'done' or not j.get('path') or not os.path.exists(j.get('path')):
        return jsonify({'error': 'غير جاهز بعد'}), 404
    return _send_apkg(j['path'], j.get('deck_name', 'deck'))


@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        config = request.get_json()
        if not config:
            return jsonify({'error': 'No config'}), 400
        print(f"Generating: {config.get('deckName','?')}")

        deck_name = config.get('deckName', 'Français Bac')
        include_audio = config.get('includeAudio', True)
        tts_cfg = config.get('ttsConfig') or {}
        if not isinstance(tts_cfg, dict):
            tts_cfg = {}
        tts_cfg.setdefault('speed', config.get('ttsSpeed') or 1)
        tts_cfg.setdefault('pitch', config.get('ttsPitch') or 1)
        tts_cfg.setdefault('frVoice', tts.DEFAULT_VOICES['fr'])
        tts_cfg.setdefault('arVoice', tts.DEFAULT_VOICES['ar'])
        tts_cfg.setdefault('frGapBefore', 0)
        tts_cfg.setdefault('frGapAfter', 0)
        tts_cfg.setdefault('arGapBefore', 0)
        tts_cfg.setdefault('arGapAfter', 0)

        # تحضير قائمة التصاميم (متعددة أو قالب مخصص)
        designs = config.get('designs')
        template_type = config.get('_templateType', 'config')
        if (not designs or not len(designs)) and template_type == 'custom' and config.get('_customFront'):
            designs = [{
                'name': config.get('_templateName') or 'تصميم',
                'fields': config.get('_customFields') or tts.DEFAULT_FIELDS,
                'frontHTML': config.get('_customFront', ''),
                'backHTML': config.get('_customBack', '') or config.get('_customFront', ''),
                'css': config.get('_customCSS', ''),
            }]

        if designs and len(designs) > 0:
            h = _settings_hash(config)
            cached = _cache_get(h)
            if cached:
                print(f"Serving cached deck: {deck_name}")
                return _send_apkg(cached, deck_name)
            if _should_job(tts_cfg, include_audio):
                jid = uuid.uuid4().hex[:10]
                _start_job(jid, h, deck_name, designs, tts_cfg, include_audio)
                return jsonify({'job': jid, 'status': 'started'}), 202
            path = _build_deck_apkg(deck_name, designs, tts_cfg, include_audio)
            cached = _cache_put(h, path)
            return _send_apkg(cached, deck_name)

        # ===== المحرر (config): المسار القديم بدون تغيير =====
        card_front_html = config.get('cardFrontHTML', '')
        card_back_html = config.get('cardBackHTML', '')

        def make_front(html):
            import re
            h = re.sub(r'<div data-ve="meaning"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
            h = re.sub(r'<div data-ve="sections"[^>]*>.*?</div>', '', h, flags=re.DOTALL)
            h = re.sub(r'<div data-ve="page"[^>]*>.*?</div>', '', h, flags=re.DOTALL)
            h = re.sub(r'<div data-ve="separator"[^>]*>.*?</div>', '', h, flags=re.DOTALL)
            return h

        def make_back(html):
            return html

        front = make_front(card_front_html) if card_front_html else '<div class="french">{{French}}</div>\n<span class="unit-badge">Unit {{Unit}}</span>'
        back = make_back(card_back_html) if card_back_html else front

        font_fr = config.get('fontFrench', 'Inter')
        font_ar = config.get('fontArabic', 'Noto Sans Arabic')
        fx = config.get('effect', 'none')
        custom_css = config.get('customCSS', '')

        effects = {
            'neon': '@keyframes np{0%,100%{text-shadow:0 0 20px currentColor}50%{text-shadow:0 0 40px currentColor,0 0 80px currentColor}}.french{animation:np 2s ease-in-out infinite}',
            'glow': '@keyframes gl{0%,100%{box-shadow:0 0 10px rgba(124,58,237,.3)}50%{box-shadow:0 0 30px rgba(124,58,237,.6)}}.card{animation:gl 3s ease-in-out infinite}',
            'pulse': '@keyframes pl{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}.card{animation:pl 2s ease-in-out infinite}',
            'float': '@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}.card{animation:fl 3s ease-in-out infinite}',
            'sakura': '@keyframes sk{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-2px) rotate(1deg)}}.french{animation:sk 4s ease-in-out infinite}',
        }

        css = f"""@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
.card{{font-family:{font_ar};text-align:center;direction:rtl;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;position:relative}}
.french{{direction:ltr;unicode-bidi:embed}}
.meaning{{direction:rtl}}
.section{{text-align:center}}
.section-label{{font-size:.6em;text-transform:uppercase;letter-spacing:2px;margin-bottom:3px}}
.section-value{{font-size:.9em;font-weight:700;direction:ltr;unicode-bidi:embed}}
.sep{{border:none;border-top:1px solid #e2e8f0;margin:4px 20px}}
.unit-badge{{display:inline-block;font-size:.68em;font-weight:700;padding:3px 12px;border-radius:20px;direction:ltr;margin:2px}}
.badge{{display:inline-block;font-size:.72em;font-weight:700;padding:4px 14px;border-radius:20px;direction:ltr;margin:2px}}
.badge-nom{{background:#dbeafe;color:#1e40af}}
.badge-adj{{background:#fef3c7;color:#92400e}}
.badge-verb{{background:#d1fae5;color:#065f46}}
.page-ref{{font-size:.6em;margin-top:4px}}
{custom_css}
{effects.get(fx, '')}
@keyframes fadeIn{{from{{opacity:0}}to{{opacity:1}}}}
@keyframes slideUp{{from{{opacity:0;transform:translateY(20px)}}to{{opacity:1;transform:translateY(0)}}}}
@keyframes bounce{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.1)}}}}
"""

        model_id = stable_id('FrancaisBac2021')
        deck_id = stable_id(deck_name)

        my_model = genanki.Model(model_id, 'FrancaisBac2021',
            fields=[{'name': 'French'}, {'name': 'Arabic'}, {'name': 'WordType'}, {'name': 'Unit'}, {'name': 'Page'}, {'name': 'Pluriel'}, {'name': 'FemininS'}, {'name': 'FemininP'}, {'name': 'Preposition'}, {'name': 'Auxiliaire'}, {'name': 'Participe'}, {'name': 'Synonyme'}, {'name': 'Contraire'}],
            templates=[{'name': 'FR→AR', 'qfmt': front, 'afmt': back}, {'name': 'AR→FR', 'qfmt': front.replace('{{French}}', '{{Arabic}}'), 'afmt': back}],
            css=css)

        my_deck = genanki.Deck(deck_id, deck_name)

        fields_order = ['word', 'arabe', 'type', 'unit', 'page', 'pluriel', 'feminin_s', 'feminin_p', 'preposition', 'auxiliaire', 'participe', 'synonyme', 'contraire']

        all_words = get_all_words() + get_important_words()
        for w in all_words:
            note_fields = [str(w.get(f, '')) for f in fields_order]
            my_deck.add_note(genanki.Note(model=my_model, fields=note_fields))

        safe_name = deck_name.replace('/', '_').replace('\\', '_')
        genanki.Package(my_deck).write_to_file(f'/tmp/{safe_name}_{os.getpid()}.apkg')  # nosec S5443
        print(f"Sent: {len(my_deck.notes)} notes")
        return _write_deck(my_deck, safe_name)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print(f"\nAnki Design Studio (Python)\n  Words: {len(get_all_words())}\n")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
