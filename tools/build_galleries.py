#!/usr/bin/env python3
"""Build 4 gallery pages for the target decks without touching the protected bac12 files.

Reads: /workspace/index.html + /workspace/tools/decks/<id>/templates.json
Writes: /workspace/out/<file>.html
"""
import json, os, re, shutil
from pathlib import Path

ROOT = Path(os.environ.get('WORKSPACE_ROOT') or Path(__file__).resolve().parents[1])
BASE = str(ROOT / 'index.html')
DECKDIR = str(ROOT / 'tools' / 'decks')
OUTDIR = str(ROOT / 'out')

EN_POOL = [
  {"id":"en-US-GuyNeural","label":"إنجليزي (أمريكا) — غاي","gender":"male"},
  {"id":"en-US-ChristopherNeural","label":"إنجليزي (أمريكا) — كريستوفر","gender":"male"},
  {"id":"en-US-EricNeural","label":"إنجليزي (أمريكا) — إريك","gender":"male"},
  {"id":"en-US-RogerNeural","label":"إنجليزي (أمريكا) — روجر","gender":"male"},
  {"id":"en-GB-RyanNeural","label":"إنجليزي (بريطانيا) — رايان","gender":"male"},
  {"id":"en-GB-ThomasNeural","label":"إنجليزي (بريطانيا) — توماس","gender":"male"},
  {"id":"en-AU-WilliamNeural","label":"إنجليزي (أستراليا) — ويليام","gender":"male"},
  {"id":"en-IN-PrabhatNeural","label":"إنجليزي (الهند) — برابهات","gender":"male"},
  {"id":"en-US-JennyNeural","label":"إنجليزي (أمريكا) — جيني","gender":"female"},
  {"id":"en-US-AriaNeural","label":"إنجليزي (أمريكا) — أريا","gender":"female"},
  {"id":"en-US-MichelleNeural","label":"إنجليزي (أمريكا) — ميشيل","gender":"female"},
  {"id":"en-GB-SoniaNeural","label":"إنجليزي (بريطانيا) — سونيا","gender":"female"},
  {"id":"en-GB-LibbyNeural","label":"إنجليزي (بريطانيا) — ليبي","gender":"female"},
  {"id":"en-AU-NatashaNeural","label":"إنجليزي (أستراليا) — ناتاشا","gender":"female"},
]

NAV = (
  '      <a class="hdr-link" href="/en9">English 9</a>\n'
  '      <a class="hdr-link" href="/enlit">English Literature 12</a>\n'
  '      <a class="hdr-link" href="/ensci">English Science 12</a>\n'
  '      <a class="hdr-link" href="/fr9">French 9</a>\n'
  '      <a class="hdr-link" href="/bac12">French Bac 12</a>'
)
NAV_OLD_RE = re.compile(r'(      <a class="hdr-link" href="(?:index\.html|gallery-[a-z0-9]+\.html)">.*?</a>\n?)+')

SAMPS = {
  'en9':   dict(f='Student', a='طالب', p='', s='', c='', dossier='', page='', pos='NOUN', poslabel='اسم', unit='Unit 01', unitnum='01'),
  'enlit': dict(f='Novel', a='رواية', p='', s='', c='', dossier='', page='', pos='', poslabel='', unit='Unit 01 - Future Careers', unitnum=''),
  'ensci': dict(f='Atom', a='ذرة', p='', s='', c='', dossier='', page='', pos='', poslabel='', unit='Unit 01 - A Learned Lesson is a Good Lesson', unitnum=''),
  'fr9':   dict(f='Leçon', a='درس', p='', s='', c='', dossier='Dossier 1', page='', pos='', poslabel='', unit='', unitnum=''),
}

FILLS = {
  'en9': [('{{Word}}','f'),('{{Meaning}}','a'),('{{POS}}','pos'),('{{POSLabel}}','poslabel'),('{{Unit}}','unit'),('{{UnitNum}}','unitnum'),('{{AudioEN}}',''),('{{AudioAR}}',''),('{{AudioBOTH}}','')],
  'enlit': [('{{English}}','f'),('{{Arabic}}','a'),('{{UnitText}}','unit'),('{{AudioEN}}',''),('{{AudioAR}}',''),('{{AudioBOTH}}','')],
  'ensci': [('{{English}}','f'),('{{Arabic}}','a'),('{{UnitText}}','unit'),('{{AudioEN}}',''),('{{AudioAR}}',''),('{{AudioBOTH}}','')],
  'fr9': [('{{Français}}','f'),('{{Arabic}}','a'),('{{Dossier}}','dossier'),('{{AudioFR}}',''),('{{AudioAR}}',''),('{{AudioBOTH}}','')],
}

SWAPS = {
  'en9': [('{{Word}}','{{Meaning}}'),('{{AudioEN}}','{{AudioAR}}')],
  'enlit': [('{{English}}','{{Arabic}}'),('{{AudioEN}}','{{AudioAR}}')],
  'ensci': [('{{English}}','{{Arabic}}'),('{{AudioEN}}','{{AudioAR}}')],
  'fr9': [('{{Français}}','{{Arabic}}'),('{{AudioFR}}','{{AudioAR}}')],
}

NAMES = {
  'en9': ['English 9'],
  'enlit': ['English Literature 12', 'English Literature 12 (Important Words)'],
  'ensci': ['English Science 12', 'English Science 12 (Important Words)'],
  'fr9': ['French 9'],
}

DECKS = {
  'en9': dict(route='/en9', ffile='en9.html', lang='en', ws='en9', deck='English 9',
      title='English 9 — Anki Template Gallery',
      meta='قوالب Anki لمفردات English 9 مع الصوت الإنجليزي والعربي.',
      frdef='en-US-GuyNeural', img='gallery_imgs'),
  'enlit': dict(route='/enlit', ffile='enlit.html', lang='en', ws='enlit', deck='English Literature 12',
      title='English Literature 12 — Anki Template Gallery',
      meta='قوالب Anki لمفردات English Literature 12 مع الصوت الإنجليزي والعربي.',
      frdef='en-US-GuyNeural', img='gallery_imgs'),
  'ensci': dict(route='/ensci', ffile='ensci.html', lang='en', ws='ensci', deck='English Science 12',
      title='English Science 12 — Anki Template Gallery',
      meta='قوالب Anki لمفردات English Science 12 مع الصوت الإنجليزي والعربي.',
      frdef='en-US-GuyNeural', img='gallery_imgs'),
  'fr9': dict(route='/fr9', ffile='fr9.html', lang='fr', ws='tas9', deck='French 9',
      title='French 9 — Anki Template Gallery',
      meta='قوالب Anki لمفردات French 9 مع الصوت الفرنسي والعربي.',
      frdef='fr-FR-HenriNeural', img='gallery_imgs'),
  'bac12': dict(route='/bac12', ffile='bac12.html', lang='fr', ws='bac12', deck='French Bac 12',
      title='French Bac 12 — Anki Template Gallery',
      meta='قوالب Anki لمفردات French Bac 12 مع الصوت الفرنسي والعربي.',
      frdef='fr-FR-HenriNeural', img='gallery_imgs'),
}

FR2EN_TEXTS = [
 ('اختر الصوت الفرنسي والصوت العربي، واضبط السرعة والنغمة والفواصل الزمنية بما يناسبك. يمكنك الاستماع إلى معاينة قبل إنشاء الرزمة، وتُستخدم هذه الإعدادات نفسها عند التصدير.',
  'اختر الصوت الإنجليزي والصوت العربي، واضبط السرعة والنغمة والفواصل الزمنية بما يناسبك. يمكنك الاستماع إلى معاينة قبل إنشاء الرزمة، وتُستخدم هذه الإعدادات نفسها عند التصدير.'),
 ('<label for="gTtsFrVoice" class="aa-lb">الصوت الفرنسي</label>',
  '<label for="gTtsFrVoice" class="aa-lb">الصوت الإنجليزي</label>'),
 ('>فرنسي <select class="sl" id="quickFrVoice"',
  '>إنجليزي <select class="sl" id="quickFrVoice"'),
 ("sec('03','اضبط الصوت','اختر الصوت الفرنسي والصوت العربي، ثم عدّل السرعة",
  "sec('03','اضبط الصوت','اختر الصوت الإنجليزي والصوت العربي، ثم عدّل السرعة"),
 ("{title:'اضبط الصوت',text:'اختر الصوت الفرنسي والعربي، واضبط السرعة والنغمة والفواصل الزمنية، ثم استمع إلى المعاينة.'}",
  "{title:'اضبط الصوت',text:'اختر الصوت الإنجليزي والعربي، واضبط السرعة والنغمة والفواصل الزمنية، ثم استمع إلى المعاينة.'}", 'optional'),
 ('تحصل على رزمة Anki بصيغة APKG تحتوي على البطاقات بالقوالب التي اخترتها، مع الصوت الفرنسي والعربي وفق إعداداتك.',
  'تحصل على رزمة Anki بصيغة APKG تحتوي على البطاقات بالقوالب التي اخترتها، مع الصوت الإنجليزي والعربي وفق إعداداتك.'),
]


def bmatch(s, i, o='[', c=']'):
    assert s[i] == o, s[i:i+20]
    depth = 0
    instr = False
    esc = False
    j = i
    while True:
        ch = s[j]
        if instr:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                instr = False
        else:
            if ch == '"':
                instr = True
            elif ch == o:
                depth += 1
            elif ch == c:
                depth -= 1
                if depth == 0:
                    return j
        j += 1


def rep(h, old, new, cnt, desc):
    c = h.count(old)
    if c != cnt:
        raise SystemExit('ASSERT %s: found %d expected %d :: %.80s' % (desc, c, cnt, old))
    return h.replace(old, new)


def build_entries(did):
    data = json.load(open(os.path.join(DECKDIR, did, 'templates.json'), encoding='utf-8'))
    out = []
    for k, m in enumerate(data['models']):
        out.append({'name': NAMES[did][k], 'fields': m['fields'], 'front': m['qfmt'],
                    'back': m['afmt'], 'css': m['css'], 'pack': did})
    return out


def replace_embedded(h, entries):
    i = h.index('var EMBEDDED_DESIGNS_100 = [')
    j = bmatch(h, h.index('[', i))
    js = json.dumps(entries, ensure_ascii=False)
    js = js.replace('</script', '<\\/script').replace('<!--', '<\\!--')
    return h[:i] + 'var EMBEDDED_DESIGNS_100 = ' + js + ';' + h[j + 2:]



def adapt_embedded_designs(h, did):
    """Preserve the shared 100 visual designs while binding them to this deck."""
    marker = 'var EMBEDDED_DESIGNS_100 = '
    i = h.index(marker) + len(marker)
    start = h.index('[', i)
    end = bmatch(h, start)
    entries = json.loads(h[start:end + 1])
    if not isinstance(entries, list) or len(entries) != 100:
        count = len(entries) if isinstance(entries, list) else 'invalid'
        raise SystemExit('[%s] expected 100 shared designs, found %s' % (did, count))

    with open(os.path.join(DECKDIR, did, 'templates.json'), encoding='utf-8') as f:
        models = json.load(f).get('models') or []
    if not models or not models[0].get('fields'):
        raise SystemExit('[%s] target model fields are missing' % did)
    fields = list(models[0]['fields'])

    primary = {'en9': 'Word', 'enlit': 'English', 'ensci': 'English',
               'fr9': 'Français'}[did]
    secondary = {'en9': 'Meaning', 'enlit': 'Arabic', 'ensci': 'Arabic',
                 'fr9': 'Arabic'}[did]
    audio_primary = 'AudioFR' if did == 'fr9' else 'AudioEN'
    unit = {'en9': 'Unit', 'enlit': 'UnitText', 'ensci': 'UnitText',
            'fr9': 'Dossier'}[did]
    aliases = {
        'French': primary, 'Français': primary, 'English': primary, 'Word': primary,
        'Arabe': secondary, 'Arabic': secondary, 'Meaning': secondary,
        'AudioFR': audio_primary, 'AudioEN': audio_primary,
        'FrSound': audio_primary, 'FrFile': audio_primary,
        'AudioAR': 'AudioAR', 'ArSound': 'AudioAR', 'ArFile': 'AudioAR',
        'AudioBOTH': 'AudioBOTH', 'BothSound': 'AudioBOTH', 'BothFile': 'AudioBOTH',
        'Dossier': unit, 'Unit': unit, 'UnitText': unit,
    }
    for n, design in enumerate(entries, 1):
        if not isinstance(design, dict):
            raise SystemExit('[%s] design %d is not an object' % (did, n))
        design['fields'] = fields[:]
        design['pack'] = did
        for key in ('front', 'back', 'frontRev', 'backRev'):
            value = design.get(key)
            if isinstance(value, str):
                # These optional extra-content panels belong to the French Bac source
                # template, not to the four target note types.
                value = re.sub(
                    r'<div class="extra" id="extra">\{\{(?:ExtraRows|Extras)\}\}</div>',
                    '', value)
                value = value.replace('{{ExtraRows}}', '').replace('{{Extras}}', '')
                for old_name, new_name in aliases.items():
                    value = value.replace('{{' + old_name + '}}',
                                          '{{' + new_name + '}}')
                design[key] = value
    return replace_embedded(h, entries)

def replace_fallback_fr(h, new_fr_json):
    i = h.index('var TTS_VOICES_FALLBACK={')
    bj = h.index('{', i)
    depth = 0
    instr = False
    esc = False
    j = bj
    while True:
        ch = h[j]
        if instr:
            if esc:
                esc = False
            elif ch == '\\':
                esc = True
            elif ch == '"':
                instr = False
        else:
            if ch == '"':
                instr = True
            elif ch == '{':
                depth += 1
            elif ch == '}':
                depth -= 1
                if depth == 0:
                    break
        j += 1
    stmt = h[i:j + 2]
    assert stmt.rstrip().endswith('};'), stmt[-20:]
    inner = stmt[len('var TTS_VOICES_FALLBACK='):-1]
    obj = json.loads(inner)
    new_stmt = 'var TTS_VOICES_FALLBACK={"fr":%s,"ar":%s};' % (
        new_fr_json, json.dumps(obj['ar'], ensure_ascii=False))
    return h[:i] + new_stmt + h[j + 2:]


def build_one(did, spec, base):
    t = '[' + did + '] '
    h = base
    if did != 'bac12':
        h = adapt_embedded_designs(h, did)
        # The French Bac base preview helper knows French placeholders only.
        # Extend its sample substitution for the target deck fields so English
        # previews display their actual sample words instead of stripping them.
        h = rep(h, "front = front.split('{{Unit}}').join('1');",
                "front = front.split('{{Unit}}').join(SAMP.unit||'1');", 1, t + 'preview unit')
        preview_anchor = "  front = front.split('{{Français}}').join(SAMP.f);"
        preview_additions = "\n".join([
            "  front = front.split('{{English}}').join(SAMP.f);",
            "  front = front.split('{{Word}}').join(SAMP.f);",
            "  front = front.split('{{Meaning}}').join(SAMP.a);",
            "  front = front.split('{{POS}}').join(SAMP.pos||'');",
            "  front = front.split('{{POSLabel}}').join(SAMP.poslabel||'');",
            "  front = front.split('{{POSColor}}').join(SAMP.poscolor||'');",
            "  front = front.split('{{UnitText}}').join(SAMP.unit||'');",
            "  front = front.split('{{UnitNum}}').join(SAMP.unitnum||'');",
            "  front = front.split('{{AudioEN}}').join('');",
        ])
        h = rep(h, preview_anchor, preview_anchor + "\n" + preview_additions,
                1, t + 'preview sample field aliases')
        conditional_anchor = "var v={French:SAMP.f,Arabic:SAMP.a,Pluriel:SAMP.p,Synonyme:SAMP.s,Contraire:SAMP.c,Badge:'Nom',Unit:'1',Page:SAMP.page,WordType:'Nom'}[f];"
        conditional_replacement = "var v={French:SAMP.f,Français:SAMP.f,English:SAMP.f,Word:SAMP.f,Arabic:SAMP.a,Meaning:SAMP.a,Pluriel:SAMP.p,Synonyme:SAMP.s,Contraire:SAMP.c,Badge:'Nom',Unit:SAMP.unit||'1',UnitText:SAMP.unit,UnitNum:SAMP.unitnum,POS:SAMP.pos,POSLabel:SAMP.poslabel,Page:SAMP.page,WordType:'Nom'}[f];"
        h = rep(h, conditional_anchor, conditional_replacement,
                1, t + 'preview conditional aliases')
        s = SAMPS[did]
        samp = ("const SAMP={f:'%s',a:'%s',p:'%s',s:'%s',c:'%s',dossier:'%s',page:'%s',pos:'%s',poslabel:'%s',unit:'%s',unitnum:'%s'};"
                % (s['f'], s['a'], s['p'], s['s'], s['c'], s['dossier'], s['page'], s['pos'], s['poslabel'], s['unit'], s['unitnum']))
        h = rep(h, "const SAMP={f:'Un ami',a:'صديق',p:'Des amis',s:'Un copain',c:'Un ennemi',dossier:'الوحدة 1',page:'25',type:'الأسماء'};",
                samp, 1, t + 'SAMP')
        anchor = "front = front.split('{{AudioBOTH}}').join('');"
        assert h.count(anchor) == 1, t + 'fill anchor'
        add = "\n".join("  front = front.split('%s').join(%s);" % (ph, ("SAMP." + k if k else "''")) for ph, k in FILLS[did])
        h = h.replace(anchor, anchor + "\n" + add)
        old_swaps = ("  swap('{{French}}','{{Arabic}}');\n"
                     "  swap('{{Français}}','{{Arabe}}');\n"
                     "  // audio bindings (so the Arabic face plays Arabic sound and vice versa)\n"
                     "  swap('{{AudioFR}}','{{AudioAR}}');\n"
                     "  swap('{{FrSound}}','{{ArSound}}');\n"
                     "  swap('{{FrFile}}','{{ArFile}}');")
        new_swaps = "  " + "\n  ".join("swap('%s','%s');" % p for p in SWAPS[did])
        h = rep(h, old_swaps, new_swaps, 1, t + 'swaps')
        h = rep(h, "// Reverse a card template: swap French<->Arabic (placeholders + sample text) and audio bindings.",
                "// Reverse a card template: swap primary<->secondary language (placeholders + sample text) and audio bindings.", 1, t + 'rev comment')
        h = rep(h, '// Used to build the "رزمة معكوسة" (reversed deck): front=Arabic, back=Arabic on top + French below.',
                '// Used to build the reversed deck: secondary language front, both on back.', 1, t + 'rev comment2')
        h = rep(h, "// noop (plural stays French)", "// noop", 1, t + 'noop comment')
        h = rep(h, "catch(e){dn='Français 12';}", "catch(e){dn='" + spec['deck'] + "';}", 1, t + 'dn catch')
        h = rep(h, "// 'Un ami' <-> 'صديق'", "// SAMP.f <-> SAMP.a", 1, t + 'samp comment')
        h = rep(h, "var pwf='Un ami',pwa='صديق';",
                "var pwf='" + s['f'] + "',pwa='" + s['a'] + "';", 1, t + 'preview words')
        if spec['lang'] == 'en':
            h = replace_fallback_fr(h, json.dumps(EN_POOL, ensure_ascii=False))
        h = rep(h, "'fr-FR-HenriNeural'", "'" + spec['frdef'] + "'", 2, t + 'voice defaults')
        if spec['lang'] == 'en':
            for item in FR2EN_TEXTS:
                a, b = item[0], item[1]
                # Source copy evolves independently; translate exact known phrases when present.
                # A missing optional phrase must not abort generation of all four galleries.
                if a not in h:
                    continue
                h = rep(h, a, b, 1, t + 'txt')
            h = rep(h, "u.lang=lang==='fr'?'fr-FR':'ar-SA';",
                    "u.lang=lang==='en'?'en-US':(lang==='fr'?'fr-FR':'ar-SA');", 1, t + 'speak lang')
            h = rep(h, "var langPrefix=lang==='fr'?'fr':'ar';",
                    "var langPrefix=lang==='en'?'en':(lang==='fr'?'fr':'ar');", 1, t + 'speak prefix')
            h = rep(h, "if(lang==='fr'){chosen=_forceDefault?null:(ttsFRManual||ttsFRVoice);}",
                    "if(lang==='fr'||lang==='en'){chosen=_forceDefault?null:(ttsFRManual||ttsFRVoice);}", 1, t + 'speak voice')
            h = rep(h, 'speakWord(SAMP.f,"fr")', 'speakWord(SAMP.f,"en")', 2, t + 'stub lang')
            h = rep(h, "fetch(apiBase()+'/api/tts_voices')",
                    "fetch(apiBase()+'/api/tts_voices?lang=en')", 1, t + 'voices url')
            h = rep(h, "front = front.split('{{Français}}').join(SAMP.f);", "front = front.split('{{English}}').join(SAMP.f);", 1, t + 'fr field')
            h = rep(h, "front = front.split('{{Dossier}}').join(SAMP.dossier||'Dossier 1');", "front = front.split('{{Dossier}}').join('');", 1, t + 'dossier field')
        h = rep(h, "fetch(apiBase()+'/api/audio_status')",
                "fetch(apiBase()+'/api/audio_status?source=" + spec['ws'] + ")", 1, t + 'status url')
        h = rep(h, "JSON.stringify({fr:pwf,ar:pwa,ttsConfig:cfg})",
                "JSON.stringify({fr:pwf,ar:pwa,lang:'" + spec['lang'] + "',ttsConfig:cfg})", 1, t + 'preview lang')
        h = rep(h, "    includeAudio:inc,\n    quick:dlQuick()\n  };",
                "    includeAudio:inc,\n    quick:dlQuick(),\n    wordSource:'" + spec['ws'] + "'\n  };", 1, t + 'ws selected')
        h = rep(h, "includeAudio:((document.getElementById('includeAudio')&&document.getElementById('includeAudio').checked)!==false),quick:dlQuick()};",
                "includeAudio:((document.getElementById('includeAudio')&&document.getElementById('includeAudio').checked)!==false),quick:dlQuick(),wordSource:'" + spec['ws'] + "'};", 1, t + 'ws selected2')
        h = rep(h, "includeAudio:document.getElementById('includeAudio')?.checked!==false, quick:dlQuick()};",
                "includeAudio:document.getElementById('includeAudio')?.checked!==false, quick:dlQuick(),wordSource:'" + spec['ws'] + "'};", 1, t + 'ws multi')
        h = rep(h, 'value="Français 12"', 'value="' + spec['deck'] + '"', 1, t + 'deck input')
        _nfb = h.count("||'Français 12'")
        assert _nfb >= 2, t + 'deck fallbacks count %d' % _nfb
        h = rep(h, "||'Français 12'", "||'" + spec['deck'] + "'", _nfb, t + 'deck fallbacks')
        h = rep(h, "if(!dn)dn='Français 12';", "if(!dn)dn='" + spec['deck'] + "';", 1, t + 'deck dn')
        h = rep(h, "deckName:'Français 12'", "deckName:'" + spec['deck'] + "'", 1, t + 'deck cfg')
        h = rep(h, "||'Anki Design'", "||'" + spec['deck'] + "'", 1, t + 'deck multi')

    h = rep(h, '<title>Anki Template Gallery — معرض قوالب Anki</title>',
            '<title>' + spec['title'] + '</title>', 1, t + 'title')
    h = rep(h, '<meta name="description" content="قوالب Anki لمفردات French Bac 12 مع الصوت الفرنسي والعربي.">',
            '<meta name="description" content="' + spec['meta'] + '">', 1, t + 'meta')
    h = rep(h, '<meta property="og:title" content="Anki Template Gallery — معرض قوالب Anki">',
            '<meta property="og:title" content="' + spec['title'] + '">', 1, t + 'ogtitle')
    h = rep(h, '<meta property="og:description" content="قوالب Anki لمفردات French Bac 12 مع الصوت الفرنسي والعربي.">',
            '<meta property="og:description" content="' + spec['meta'] + '">', 1, t + 'ogdesc')
    h = rep(h, '<link rel="canonical" href="https://anki-design-studio.onrender.com/">',
            '<link rel="canonical" href="https://anki-design-studio.onrender.com' + spec['route'] + '">', 1, t + 'canonical')

    h2, n = NAV_OLD_RE.subn(NAV, h)
    if n == 0:
        assert h.count('href="/en9"') >= 1 and h.count('href="/bac12"') >= 1, t + 'nav missing'
    else:
        assert n == 1, t + 'nav count %d' % n
        h = h2

    h = rep(h, '<a class="brand" href="index.html" aria-label="الصفحة الرئيسية">',
            '<a class="brand" href="' + spec['route'] + '" aria-label="الصفحة الرئيسية">', 1, t + 'brand')

    h2, n = re.subn(r"localStorage\.(getItem|setItem|removeItem)\('anki_", r"localStorage.\1('anki_" + did + "_", h)
    assert n >= 20, t + 'storage count %d' % n
    h = h2
    h = rep(h, "'anki_ed_'", "'anki_" + did + "_ed_'", 1, t + 'edkey')

    for alias in ["gallery_imgs_en9", "gallery_imgs_enlit", "gallery_imgs_ensci", "gallery_imgs_fr9", "gallery_imgs_bac12"]:
        h = h.replace("'" + alias + "/'", "'gallery_imgs/'")
        h = h.replace('"' + alias + '/"', '"gallery_imgs/"')
        h = h.replace('"' + alias + '"', '"gallery_imgs"')
        h = h.replace("'" + alias + "'", "'gallery_imgs'")

    h = rep(h, "'gallery_imgs/'", "'gallery_imgs/'", 1, t + 'imgdir')

    h = rep(h, "var p={type:type, deviceId:DEVICE_ID, ts:Date.now(), url:location.href};",
            "var p={type:type, deviceId:DEVICE_ID, deck:DECK_ID, ts:Date.now(), url:location.href};", 1, t + 'track deck')
    h = rep(h, "var DEVICE_ID=(function(){try{var d=localStorage.getItem('anki_" + did + "_device_id');",
            "var DECK_ID='" + did + "';\nvar DEVICE_ID=(function(){try{var d=localStorage.getItem('anki_" + did + "_device_id');", 1, t + 'deck const')
    if did in ('en9', 'enlit', 'ensci', 'fr9'):
        h, removed_extra_buttons = re.subn(
            r'<button class=\\*["]extra-btn\\*["][\s\S]*?</button>', '', h)
        if removed_extra_buttons != 100:
            raise SystemExit('[%s] expected to remove 100 extra buttons, removed %d'
                             % (did, removed_extra_buttons))
    return h, spec


if __name__ == '__main__':
    base = open(BASE, encoding='utf-8').read()
    os.makedirs(OUTDIR, exist_ok=True)
    for did, spec in DECKS.items():
        if did == 'bac12':
            continue
        h, _ = build_one(did, spec, base)
        out_path = os.path.join(OUTDIR, spec['ffile'])
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(h)
        print(did, 'written', os.path.getsize(out_path))

    # Keep the Render publish directory self-contained. The source files below
    # are copied byte-for-byte; French Bac is never rebuilt or edited here.
    publish_root = Path(OUTDIR)
    for name in ('index.html', 'bac12.html', 'designs_100.js',
                 'template_colors.js', 'stats.html', '_redirects'):
        source = ROOT / name
        if source.is_file():
            shutil.copy2(source, publish_root / name)

    images_source = ROOT / 'gallery_imgs'
    if images_source.is_dir():
        shutil.copytree(images_source, publish_root / 'gallery_imgs',
                        dirs_exist_ok=True)
        copied_images = list((publish_root / 'gallery_imgs').glob('*.jpg'))
        if len(copied_images) != 100:
            raise SystemExit('Expected 100 published thumbnails, found %d'
                             % len(copied_images))
        print('publish root: 100 shared thumbnails copied')
