#!/usr/bin/env python3
import os, json, re, genanki, hashlib
from flask import Flask, request, jsonify, send_file, send_from_directory

app = Flask(__name__, static_folder='public')  # nosec S4502

VOCAB_DATA = None
REPEATED_DATA = None
try:
    with open('parsed_data_full.json') as f:
        VOCAB_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError): pass
try:
    with open('repeated_data.json') as f:
        REPEATED_DATA = json.load(f)
except (FileNotFoundError, json.JSONDecodeError): pass

def get_all_words():
    if not VOCAB_DATA: return []
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
    if not REPEATED_DATA: return []
    r = []
    for cat in ['noms', 'adj', 'verbs']:
        for x in REPEATED_DATA.get(cat, [])[:30]:
            units = x.get('units', [1])
            r.append({'word': x.get('word',''), 'arabe': x.get('arabe',''), 'type': x.get('type',''), 'unit': units[0] if units else 1, 'page': '', 'pluriel': '', 'feminin_s': '', 'feminin_p': '', 'preposition': '', 'auxiliaire': '', 'participe': '', 'synonyme': '', 'contraire': ''})
    return r

def stable_id(s):
    return int(hashlib.md5(s.encode()).hexdigest()[:15], 16)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok', 'words': len(get_all_words())})

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('public', 'index.html')

@app.route('/designs_20.json', methods=['GET'])
def serve_designs():
    return send_from_directory('public', 'designs_20.json')

@app.route('/designs_102.json', methods=['GET'])
def serve_designs_102():
    return send_from_directory('public', 'designs_102.json')

@app.route('/designs_config_102.json', methods=['GET'])
def serve_designs_config():
    return send_from_directory('public', 'designs_config_102.json')

@app.route('/designs_data.js', methods=['GET'])
def serve_designs_data():
    return send_from_directory('public', 'designs_data.js')

@app.route('/designs_premium.js', methods=['GET'])
def serve_designs_premium():
    return send_from_directory('public', 'designs_premium.js')

def generate_multi_design(deck_name, designs):
    """Create a deck where words are distributed round-robin across the selected designs."""
    fields_order = ['word', 'arabe', 'type', 'unit', 'page', 'pluriel', 'feminin_s', 'feminin_p',
                    'preposition', 'auxiliaire', 'participe', 'synonyme', 'contraire']
    all_words = get_all_words() + get_important_words()
    if not all_words:
        return jsonify({'error': 'No word data found'}), 500

    base_css = """@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
.card{font-family:'Noto Sans Arabic',sans-serif;text-align:center;direction:rtl;display:flex;flex-direction:column;align-items:center;justify-content:center;overflow:hidden;position:relative}
@keyframes fadeIn{from{opacity:0}to{opacity:1}}
@keyframes slideUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
"""

    models = []
    deck_id = stable_id('MultiDeck_' + deck_name)
    deck = genanki.Deck(deck_id, deck_name)

    for i, d in enumerate(designs):
        name = d.get('name', 'Design ' + str(i + 1))
        front = d.get('frontHTML', '') or '<div class="french">{{French}}</div>'
        back = d.get('backHTML', '') or front
        css = (d.get('css') or '') + base_css
        mid = stable_id('MultiDesign_' + deck_name + '_' + str(i) + '_' + name)
        model = genanki.Model(
            mid, name,
            fields=[{'name': 'French'}, {'name': 'Arabic'}, {'name': 'WordType'}, {'name': 'Unit'},
                    {'name': 'Page'}, {'name': 'Pluriel'}, {'name': 'FemininS'}, {'name': 'FemininP'},
                    {'name': 'Preposition'}, {'name': 'Auxiliaire'}, {'name': 'Participe'},
                    {'name': 'Synonyme'}, {'name': 'Contraire'}],
            templates=[{'name': 'FR→AR', 'qfmt': front, 'afmt': back}],
            css=css,
            sort_field_index=0)
        models.append(model)

    n = len(models)
    for idx, w in enumerate(all_words):
        note_fields = [str(w.get(f, '')) for f in fields_order]
        model = models[idx % n]
        deck.add_note(genanki.Note(model=model, fields=note_fields))

    safe_name = deck_name.replace('/', '_').replace('\\', '_')
    apkg_path = f'/tmp/{safe_name}_{os.getpid()}.apkg'  # nosec S5443
    genanki.Package(deck).write_to_file(apkg_path)
    print(f"Multi-design deck sent: {len(all_words)} notes across {n} designs")

    response = send_file(apkg_path, as_attachment=True, download_name=f'{safe_name}.apkg',
                    mimetype='application/octet-stream')
    import atexit
    atexit.register(lambda: os.remove(apkg_path) if os.path.exists(apkg_path) else None)
    return response


@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        config = request.get_json()
        if not config: return jsonify({'error': 'No config'}), 400
        print(f"Generating: {config.get('deckName','?')}")

        deck_name = config.get('deckName', 'Français Bac')

        # MULTI-DESIGN: generate a deck where each word gets a different design (round-robin)
        designs = config.get('designs')
        if designs and len(designs) > 0:
            return generate_multi_design(deck_name, designs)

        # Get full card HTML from frontend
        card_front_html = config.get('cardFrontHTML', '')
        card_back_html = config.get('cardBackHTML', '')

        # Anki field placeholders are already in the HTML from renderAnkiTemplate() (frontend)
        # Front: show French word, back: show everything
        def make_front(html):
            # HTML already has field templates from frontend renderAnkiTemplate()
            # Remove sections, meaning, page from front (only word + badges on front)
            import re
            h = re.sub(r'<div data-ve="meaning"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
            h = re.sub(r'<div data-ve="sections"[^>]*>.*?</div>', '', h, flags=re.DOTALL)
            h = re.sub(r'<div data-ve="page"[^>]*>.*?</div>', '', h, flags=re.DOTALL)
            h = re.sub(r'<div data-ve="separator"[^>]*>.*?</div>', '', h, flags=re.DOTALL)
            return h

        def make_back(html):
            # HTML already has all field templates from frontend
            return html

        front = make_front(card_front_html) if card_front_html else '<div class="french">{{French}}</div>\n<span class="unit-badge">Unit {{Unit}}</span>'
        back = make_back(card_back_html) if card_back_html else front

        # CSS: inline styles are in the frontend HTML, we add minimal base CSS
        font_fr = config.get('fontFrench', 'Inter')
        font_ar = config.get('fontArabic', 'Noto Sans Arabic')
        fx = config.get('effect', 'none')
        custom_css = config.get('customCSS', '')
        # Support custom templates
        template_type = config.get('_templateType', 'config')
        custom_front = config.get('_customFront', '')
        custom_back = config.get('_customBack', '')
        custom_css_extra = config.get('_customCSS', '')
        if template_type == 'custom' and custom_front:
            custom_css = custom_css_extra

        effects = {
            'neon': '@keyframes np{0%,100%{text-shadow:0 0 20px currentColor}50%{text-shadow:0 0 40px currentColor,0 0 80px currentColor}}.french{animation:np 2s ease-in-out infinite}',
            'glow': '@keyframes gl{0%,100%{box-shadow:0 0 10px rgba(124,58,237,.3)}50%{box-shadow:0 0 30px rgba(124,58,237,.6)}}.card{animation:gl 3s ease-in-out infinite}',
            'pulse': '@keyframes pl{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}.card{animation:pl 2s ease-in-out infinite}',
            'float': '@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}.card{animation:fl 3s ease-in-out infinite}',
            'sakura': '@keyframes sk{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-2px) rotate(1deg)}}.french{animation:sk 4s ease-in-out infinite}',
            # Professional designs animations are in custom_css_extra
        }
        # No need for custom CSS handling - it's now in the template HTML via renderAnkiTemplate()

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
        apkg_path = f'/tmp/{safe_name}_{os.getpid()}.apkg'  # nosec S5443
        genanki.Package(my_deck).write_to_file(apkg_path)

        print(f"Sent: {len(my_deck.notes)} notes")

        response = send_file(apkg_path, as_attachment=True, download_name=f'{safe_name}.apkg',
                        mimetype='application/octet-stream')
        import atexit
        atexit.register(lambda: os.remove(apkg_path) if os.path.exists(apkg_path) else None)
        return response
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"\nAnki Design Studio (Python)\n  Words: {len(get_all_words())}\n")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
