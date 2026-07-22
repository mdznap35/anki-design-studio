#!/usr/bin/env python3
import sys, json, genanki

def stable_id(s):
    import hashlib
    return int(hashlib.md5(s.encode()).hexdigest()[:15], 16)

def generate(config_path, output_path):
    with open(config_path) as f:
        cfg = json.load(f)
    
    config = cfg.get('config', {})
    words = cfg.get('words', [])
    important = cfg.get('important', [])
    deck_name = config.get('deckName', 'Français Bac')
    
    # Build CSS
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
    br = config.get('borderRadius', 16)
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

    # Simple templates - no Anki conditionals
    front = '<div class="french">{{French}}</div>\n<span class="unit-badge">Unit {{Unit}}</span>'
    
    order = config.get('sectionOrder', ['Pluriel', 'Synonyme', 'Contraire'])
    if isinstance(order, str):
        order = order.split(',')
    vis = config.get('sectionVisibility', {})
    
    sec_map = {
        'Pluriel': ('Pluriel', '{{Pluriel}}'),
        'Synonyme': ('Synonyme', '{{Synonyme}}'),
        'Contraire': ('Contraire', '{{Contraire}}'),
    }
    sections = ''
    for k in order:
        if not vis.get(k, True):
            continue
        s = sec_map.get(k)
        if s:
            sections += f'<div class="section"><div class="section-label">{s[0]}</div><div class="section-value">{s[1]}</div></div>\n'
    
    meaning = '<div class="meaning">{{Arabic}}</div>' if config.get('showMeaning', True) else ''
    page = '<div class="page-ref">Page {{Page}}</div>' if config.get('showPage', True) else ''
    back = f'{front}\n<hr class="sep">\n{meaning}\n{sections}\n{page}'

    model_id = stable_id('FrancaisBac2021')
    deck_id = stable_id(deck_name)
    
    my_model = genanki.Model(
        model_id, 'FrancaisBac2021',
        fields=[
            {'name': 'French'}, {'name': 'Arabic'}, {'name': 'WordType'},
            {'name': 'Unit'}, {'name': 'Page'}, {'name': 'Pluriel'},
            {'name': 'FemininS'}, {'name': 'FemininP'},
            {'name': 'Preposition'}, {'name': 'Auxiliaire'}, {'name': 'Participe'},
            {'name': 'Synonyme'}, {'name': 'Contraire'},
        ],
        templates=[
            {'name': 'FR→AR', 'qfmt': front, 'afmt': back},
            {'name': 'AR→FR', 'qfmt': front.replace('{{French}}', '{{Arabic}}'), 'afmt': back},
        ],
        css=css,
    )
    
    my_deck = genanki.Deck(deck_id, deck_name)
    
    fields_order = ['word', 'arabe', 'type', 'unit', 'page', 'pluriel',
                    'feminin_s', 'feminin_p', 'preposition', 'auxiliaire', 'participe',
                    'synonyme', 'contraire']
    
    for w in words + important:
        note_fields = [str(w.get(f, '')) for f in fields_order]
        note = genanki.Note(model=my_model, fields=note_fields)
        my_deck.add_note(note)
    
    package = genanki.Package(my_deck)
    package.write_to_file(output_path)
    print(f"OK: {len(my_deck.notes)} notes", file=sys.stderr)

if __name__ == '__main__':
    generate(sys.argv[1], sys.argv[2])
