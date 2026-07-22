#!/usr/bin/env python3
import os, json, genanki, hashlib
from flask import Flask, request, jsonify, send_file, send_from_directory

app = Flask(__name__, static_folder='public')

VOCAB_DATA = None
REPEATED_DATA = None
try:
    with open('parsed_data_full.json') as f:
        VOCAB_DATA = json.load(f)
except: pass
try:
    with open('repeated_data.json') as f:
        REPEATED_DATA = json.load(f)
except: pass

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
            w.append({'word': x.get('verbe',''), 'arabe': x.get('arabe',''), 'type': 'Verbe', 'unit': un, 'page': x.get('page',''), 'pluriel': '', 'feminin_s': '', 'feminin_p': '', 'preposition': x.get('preposition',''), 'auxiliaire': x.get('auxiliaire',''), 'participe': x.get('participe',''), 'synonyme': x.get('synonyme',''), 'contraire': ''})
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

@app.route('/api/health')
def health():
    return jsonify({'status': 'ok', 'words': len(get_all_words())})

@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

@app.route('/api/generate', methods=['POST'])
def generate():
    try:
        config = request.get_json()
        if not config: return jsonify({'error': 'No config'}), 400
        print(f"Generating: {config.get('deckName','?')}")

        deck_name = config.get('deckName', 'Français Bac')
        
        fc = config.get('frenchColor', '#1e293b')
        mc = config.get('meaningColor', '#1e40af')
        mb = config.get('meaningBg', '#eff6ff')
        mbd = config.get('meaningBorder', '#bfdbfe')
        bnbg = config.get('badgeNomBg', '#dbeafe')
        bnc = config.get('badgeNomColor', '#1e40af')
        babg = config.get('badgeAdjBg', '#fef3c7')
        bac = config.get('badgeAdjColor', '#92400e')
        bvbg = config.get('badgeVerbBg', '#d1fae5')
        bvc = config.get('badgeVerbColor', '#065f46')
        ubg = config.get('unitBg', '#f0fdf4')
        uc = config.get('unitColor', '#166534')
        ubd = config.get('unitBorder', '#bbf7d0')
        sb = config.get('secBg', '#f8f9fa')
        sbd = config.get('secBorder', '#e2e8f0')
        sc = config.get('secTextColor', '#333')
        lc = config.get('labelColor', '#999')
        bg = config.get('cardBg', '#fff')
        bg2 = config.get('cardBg2', '')
        fs_fr = config.get('frenchFontSize', 2.4)
        fw_fr = config.get('frenchFontWeight', 900)
        fs_ar = config.get('meaningFontSize', 1.5)
        fw_ar = config.get('meaningFontWeight', 800)
        mbr = config.get('meaningBorderRadius', 16)
        mbw = config.get('meaningBorderWidth', 2)
        font_fr = config.get('fontFrench', 'Inter')
        font_ar = config.get('fontArabic', 'Noto Sans Arabic')
        fx = config.get('effect', 'none')
        
        bg_style = bg
        if bg2 and bg != bg2:
            bg_style = f"linear-gradient({config.get('bgGradientDir','135deg')},{bg},{bg2})"
        
        effects = {
            'neon': '@keyframes np{0%,100%{text-shadow:0 0 20px currentColor}50%{text-shadow:0 0 40px currentColor,0 0 80px currentColor}}.french{animation:np 2s ease-in-out infinite}',
            'wave': '@keyframes wv{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}.french{animation:wv 3s ease-in-out infinite}',
            'glow': '@keyframes gw{0%,100%{box-shadow:0 0 5px currentColor}50%{box-shadow:0 0 25px currentColor}}.card{animation:gw 3s ease-in-out infinite}',
            'pulse': '@keyframes pl{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}.french{animation:pl 2s ease-in-out infinite}',
            'float': '@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}.french{animation:fl 3s ease-in-out infinite}',
            'shimmer': '@keyframes sh{0%{background-position:-200% 0}100%{background-position:200% 0}}.french{background:linear-gradient(90deg,transparent 30%,rgba(255,255,255,.3) 50%,transparent 70%);background-size:200% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 3s infinite}',
            'sakura': '@keyframes sk{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-2px) rotate(1deg)}}.french{animation:sk 4s ease-in-out infinite}',
        }
        
        css = f"""@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&display=swap');
.card{{font-family:{font_ar};text-align:center;direction:rtl;padding:28px 20px;min-height:300px;display:flex;flex-direction:column;align-items:center;justify-content:center;background:{bg_style};color:#333;overflow:hidden;gap:10px}}
.french{{font-family:{font_fr};font-size:{fs_fr}em;font-weight:{fw_fr};direction:ltr;unicode-bidi:embed;color:{fc};margin-bottom:4px}}
.meaning{{font-family:{font_ar};font-size:{fs_ar}em;font-weight:{fw_ar};direction:rtl;padding:12px 20px;border-radius:{mbr}px;margin:6px 0;background:{mb};border:{mbw}px solid {mbd};color:{mc};max-width:90%}}
.badge{{display:inline-block;font-size:.72em;font-weight:700;padding:4px 14px;border-radius:20px;direction:ltr;margin:2px}}
.badge-nom{{background:{bnbg};color:{bnc}}}.badge-adj{{background:{babg};color:{bac}}}.badge-verb{{background:{bvbg};color:{bvc}}}
.unit-badge{{display:inline-block;font-size:.68em;font-weight:700;padding:3px 12px;border-radius:20px;direction:ltr;margin:2px;background:{ubg};color:{uc};border:1px solid {ubd}}}
.section{{background:{sb};border:1px solid {sbd};border-radius:12px;padding:10px 16px;margin:4px 0;width:100%;max-width:480px;direction:rtl;text-align:center}}
.section-label{{font-size:.6em;color:{lc};text-transform:uppercase;letter-spacing:2px;margin-bottom:3px}}
.section-value{{font-size:.9em;font-weight:700;direction:ltr;unicode-bidi:embed;color:{sc}}}
.sep{{border:none;border-top:1px solid {sbd};margin:4px 20px}}
.page-ref{{font-size:.6em;color:{lc};margin-top:4px}}
{effects.get(fx, '')}"""

        front = '<div class="french">{{French}}</div>\n<span class="unit-badge">Unit {{Unit}}</span>'
        
        order = config.get('sectionOrder', ['Pluriel', 'Synonyme', 'Contraire'])
        if isinstance(order, str): order = order.split(',')
        vis = config.get('sectionVisibility', {})
        sec_map = {'Pluriel': ('Pluriel', '{{Pluriel}}'), 'Synonyme': ('Synonyme', '{{Synonyme}}'), 'Contraire': ('Contraire', '{{Contraire}}')}
        sections = ''
        for k in order:
            if vis.get(k, True) and k in sec_map:
                s = sec_map[k]
                sections += f'<div class="section"><div class="section-label">{s[0]}</div><div class="section-value">{s[1]}</div></div>\n'
        
        meaning = '<div class="meaning">{{Arabic}}</div>' if config.get('showMeaning', True) else ''
        page = '<div class="page-ref">Page {{Page}}</div>' if config.get('showPage', True) else ''
        back = f'{front}\n<hr class="sep">\n{meaning}\n{sections}\n{page}'

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
        apkg_path = f'/tmp/{safe_name}_{os.getpid()}.apkg'
        genanki.Package(my_deck).write_to_file(apkg_path)
        
        print(f"✅ Sent: {len(my_deck.notes)} notes")
        
        return send_file(apkg_path, as_attachment=True, download_name=f'{safe_name}.apkg',
                        mimetype='application/octet-stream')
    except Exception as e:
        print(f"🔴 Error: {e}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print(f"\n🎨 Anki Design Studio (Python)\n   📝 {len(get_all_words())} words\n")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
