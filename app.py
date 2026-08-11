#!/usr/bin/env python3
import os, json, re, genanki, hashlib
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
    """يرجع رسالة خطأ إذا كان التوليد التلقائي غير عملي، أو None للسماح."""
    if not include_audio:
        return None
    tts.load_library()
    if tts._lib:
        return None  # المكتبة جاهزة: تضمين مباشر بدون توليد
    unique = len({(w.get('word') or '').strip().lower() for w in all_words if (w.get('word') or '').strip()})
    if unique > AUDIO_MAX_WORDS:
        return ('الرزمة كبيرة جداً للتوليد التلقائي للصوت (أكثر من %d كلمة). '
                'أرسل مكتبتك الصوتية الجاهزة ليتم تضمينها، أو فعّل الصوت لرزمة أصغر.') % AUDIO_MAX_WORDS
    return None


def generate_multi_design(deck_name, designs, tts_cfg, include_audio):
    """رزمة واحدة: توزيع عادل للكلمات على التصاميم المختارة (round-robin)."""
    all_words = get_all_words() + get_important_words()
    if not all_words:
        return jsonify({'error': 'No word data found'}), 500
    guard = _audio_guard(all_words, include_audio)
    if guard:
        return jsonify({'error': guard}), 400

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

    def make_fields(idx):
        model, fields = models[idx % n]
        return model, _build_note_fields(fields, all_words[idx], tts_cfg, include_audio)

    if include_audio:
        with ThreadPoolExecutor(max_workers=6) as ex:
            results = list(ex.map(make_fields, range(len(all_words))))
    else:
        results = [make_fields(i) for i in range(len(all_words))]

    for model, nf in results:
        deck.add_note(genanki.Note(model=model, fields=nf))

    safe_name = deck_name.replace('/', '_').replace('\\', '_')
    print(f"Multi-design deck sent: {len(all_words)} notes across {n} designs (audio={include_audio})")
    return _write_deck(deck, safe_name)


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

        # MULTI-DESIGN: توزيع عادل على التصاميم المختارة
        designs = config.get('designs')
        if designs and len(designs) > 0:
            return generate_multi_design(deck_name, designs, tts_cfg, include_audio)

        # ===== القوالب الجاهزة (custom): HTML/CSS حرفياً من الرزمة =====
        template_type = config.get('_templateType', 'config')
        custom_front = config.get('_customFront', '')
        custom_back = config.get('_customBack', '')
        custom_css_extra = config.get('_customCSS', '')
        custom_fields = config.get('_customFields') or tts.DEFAULT_FIELDS
        custom_name = config.get('_templateName') or 'تصميم'

        if template_type == 'custom' and custom_front:
            all_words = get_all_words() + get_important_words()
            if not all_words:
                return jsonify({'error': 'No word data found'}), 500
            guard = _audio_guard(all_words, include_audio)
            if guard:
                return jsonify({'error': guard}), 400
            model = genanki.Model(
                stable_id('Custom_' + custom_name + '_' + deck_name), custom_name,
                fields=[{'name': f} for f in custom_fields],
                templates=[{'name': 'بطاقة', 'qfmt': custom_front, 'afmt': custom_back or custom_front}],
                css=custom_css_extra)
            deck = genanki.Deck(stable_id('Deck_' + deck_name), deck_name)

            def make_fields(idx):
                return _build_note_fields(custom_fields, all_words[idx], tts_cfg, include_audio)

            if include_audio:
                with ThreadPoolExecutor(max_workers=6) as ex:
                    results = list(ex.map(make_fields, range(len(all_words))))
            else:
                results = [make_fields(i) for i in range(len(all_words))]
            for nf in results:
                deck.add_note(genanki.Note(model=model, fields=nf))
            safe_name = deck_name.replace('/', '_').replace('\\', '_')
            print(f"Custom deck sent: {len(all_words)} notes (audio={include_audio})")
            return _write_deck(deck, safe_name)

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
