#!/usr/bin/env python3
"""Build 4 gallery pages for the target decks without touching the protected bac12 files.

Reads: ANKI_BASE_HTML (or /workspace/index.html) + /workspace/tools/decks/<id>/templates.json
Writes: /workspace/out/<file>.html
"""
import json, os, re, shutil
from pathlib import Path

ROOT = Path(os.environ.get('WORKSPACE_ROOT') or Path(__file__).resolve().parents[1])
# CI can provide the exact live French Bac page as a read-only base. Local runs
# retain the repository index.html fallback.
BASE = os.environ.get('ANKI_BASE_HTML') or str(ROOT / 'public' / 'index.html')
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
        h = rep(h, "JSON.stringify({fr:pwf,ar:pwa,ttsConfig:cfg})",
                "JSON.stringify({fr:pwf,ar:pwa,lang:'" + spec['lang'] + "',ttsConfig:cfg})",
                1, t + 'audio preview language')
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
                "fetch(apiBase()+'/api/audio_status?source=" + spec['ws'] + "')", 1, t + 'status url')
        # Guard against stale/malformed generated output: every deck-specific
        # audio-status URL must keep the closing JavaScript string delimiter.
        _audio_ok = "fetch(apiBase()+'/api/audio_status?source=" + spec['ws'] + "')"
        _audio_bad = "fetch(apiBase()+'/api/audio_status?source=" + spec['ws'] + ")"
        if _audio_bad in h:
            h = h.replace(_audio_bad, _audio_ok)
        assert _audio_ok in h, t + 'audio status URL must be valid JavaScript'
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
    canonical_tag = '<link rel="canonical" href="https://anki-design-studio.onrender.com' + spec['route'] + '">'
    canonical_re = re.compile(r'<link\s+rel=["\']canonical["\'][^>]*>', re.I)
    h, canonical_count = canonical_re.subn(canonical_tag, h)
    if canonical_count > 1:
        raise SystemExit(t + 'expected at most one canonical tag, found %d' % canonical_count)
    if canonical_count == 0:
        h, inserted = re.subn(r'</head\s*>', canonical_tag + '\n</head>', h, count=1, flags=re.I)
        if inserted != 1:
            raise SystemExit(t + 'could not insert canonical tag into head')

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
    # Render each gallery tile from its own deck-adapted Anki template.
    # The previous static JPGs were captured from French Bac 12 and therefore
    # leaked French sample text into the other three galleries.
    gallery_thumb_old = """      var img='gallery_imgs/'+('000'+(i+1)).slice(-3)+'.jpg';
      it.innerHTML='<span class="gb-sk"></span><span class="gb-num">'+num+'</span><img class="gb-img" data-loading="1" loading="lazy" decoding="async" src="'+img+'" alt="تصميم '+num+'"><span class="gb-ov"><span class="gb-ov-t">تصميم '+num+'</span><span class="gb-ov-b">اختيار ←</span></span>';"""
    gallery_thumb_new = "      var img='/gallery_previews/'+DECK_ID+'/'+('000'+(i+1)).slice(-3)+'.webp';\n      it.innerHTML='<span class=\"gb-sk\"></span><span class=\"gb-num\">'+num+'</span><img class=\"gb-img\" data-loading=\"1\" loading=\"lazy\" decoding=\"async\" fetchpriority=\"low\" src=\"'+img+'\" alt=\"معاينة القالب '+num+'\"><span class=\"gb-ov\"><span class=\"gb-ov-t\">تصميم '+num+'</span><span class=\"gb-ov-b\">اختيار ←</span></span>';"
    h = rep(h, gallery_thumb_old, gallery_thumb_new, 1, t + 'deck-specific live gallery previews')
    gallery_handlers_old = "      var im=it.querySelector('.gb-img');\n      im.addEventListener('load',function(){this.removeAttribute('data-loading');var sk=this.parentNode.querySelector('.gb-sk');if(sk)sk.style.display='none';});\n      im.addEventListener('error',function(){this.removeAttribute('data-loading');var sk=this.parentNode.querySelector('.gb-sk');if(sk)sk.style.display='none';});"
    gallery_handlers_new = "      var im=it.querySelector('.gb-img');\n      im.addEventListener('load',function(){\n        this.removeAttribute('data-loading');\n        var sk=this.parentNode.querySelector('.gb-sk');if(sk)sk.style.display='none';\n      });\n      im.addEventListener('error',function(){\n        this.removeAttribute('data-loading');\n        this.style.display='none';\n        var sk=this.parentNode.querySelector('.gb-sk');if(sk)sk.style.display='none';\n        var fb=document.createElement('span');\n        fb.className='gb-img-fallback';\n        fb.textContent='المعاينة غير متاحة';\n        this.parentNode.insertBefore(fb,this);\n      });"
    h = rep(h, gallery_handlers_old, gallery_handlers_new, 1, t + 'live gallery preview handlers')
    thumb_export_old = "  function thumbDoc(t){try{var d=buildPreviewDoc(t);return d.replace(/<script[\\s\\S]*?<\\/script>/gi,'');}catch(e){return '<html><body style=\"margin:0;background:#14121f\"></body></html>';}}\n  function renderGalleryBrowser(){"
    thumb_export_new = "  function thumbDoc(t){try{var d=buildPreviewDoc(t);return d.replace(/<script[\\s\\S]*?<\\/script>/gi,'');}catch(e){return '<html><body style=\"margin:0;background:#14121f\"></body></html>';}}\n  window.__GALLERY_THUMB_DOC__=thumbDoc;\n  function renderGalleryBrowser(){"
    h = rep(h, thumb_export_old, thumb_export_new, 1, t + 'expose static thumbnail renderer')
    grid_css_anchor = "@keyframes gbSk{from{background-position:200% 0}to{background-position:-200% 0}}"
    grid_css_new = grid_css_anchor + "\n#gbGrid .gb-img{object-fit:contain!important;object-position:center!important;}\n#gbGrid .gb-item,#gbGrid .gb-item *{animation:none!important;transition:none!important;}\n#gbGrid .gb-item:hover{transform:none!important;}\n#gbGrid .gb-item:hover .gb-img{transform:none!important;filter:none!important;}\n#gbGrid .gb-sk{animation:none!important;background:#171421!important;background-image:none!important;}\n#gbGrid .gb-img-fallback{display:grid;place-items:center;aspect-ratio:22/45;min-height:180px;padding:12px;text-align:center;color:var(--tx);background:#171421;font-weight:700;}\n@media(prefers-reduced-motion:reduce){#gbGrid *{animation:none!important;transition:none!important;scroll-behavior:auto!important;}}"
    h = rep(h, grid_css_anchor, grid_css_new, 1, t + 'static grid motion and contain-fit rules')
    h = rep(h, "      it.style.animationDelay=Math.min(i,18)*0.02+'s';", "      // Static thumbnails do not animate in the gallery grid.", 1, t + 'remove card entrance animation')
    # Harden the all-design browser against early initialization races and
    # fit the full preview to the available viewport instead of shrinking it
    # with the old oversized fixed padding.
    gallery_runtime_fix = r'''<script>
(function(){
  var originalOpen=window.openGalleryBrowser;
  window.openGalleryBrowser=function(){
    try{if(typeof ensureGalleryDesigns==='function')ensureGalleryDesigns();if(typeof gvCompute==='function')gvCompute();}catch(e){}
    if(typeof originalOpen==='function')return originalOpen.apply(this,arguments);
  };
  var originalFit=window.gvFitFrame;
  window.gvFitFrame=function(){
    try{if(typeof originalFit==='function')originalFit.apply(this,arguments);}catch(e){}
    var frame=document.getElementById('gvFrame'),stage=document.getElementById('gvStage'),wrap=document.getElementById('gvCardWrap');
    if(!frame||!stage||!wrap)return;
    var w=Math.max(240,parseFloat(frame.style.width)||440),h=Math.max(240,parseFloat(frame.style.height)||900);
    var mobile=window.innerWidth<=600,padX=mobile?20:48,padY=mobile?24:44;
    var aw=Math.max(220,stage.clientWidth-padX),ah=Math.max(260,stage.clientHeight-padY);
    var scale=Math.min(aw/w,ah/h,1.12);
    if(!isFinite(scale)||scale<=0)return;
    wrap.style.transformOrigin='center center';wrap.style.transform='scale('+scale+')';
    wrap.style.width=w+'px';wrap.style.height=h+'px';
  };
  if(typeof window.renderGalleryBrowser==='function'){
    var originalRender=window.renderGalleryBrowser;
    window.renderGalleryBrowser=function(){
      try{if(typeof ensureGalleryDesigns==='function')ensureGalleryDesigns();if(typeof gvCompute==='function')gvCompute();}catch(e){}
      return originalRender.apply(this,arguments);
    };
  }
})();
</script>'''
    # The literal </body> also appears inside JavaScript strings (for preview
    # documents). Insert only before the final HTML body close, never the first
    # textual occurrence, which would corrupt the surrounding JavaScript.
    body_close = h.rfind('</body>')
    if body_close < 0:
        raise SystemExit(t + 'could not find the final HTML </body> tag')
    h = h[:body_close] + gallery_runtime_fix + '\n' + h[body_close:]
    h = upgrade_gallery_ux(h, did, spec)
    return h, spec




TOUR_CSS = r"""
/* Anki Design Studio — onboarding tour v2 */
#onboardOverlay.onboard-overlay{
  position:fixed!important;inset:0!important;z-index:10050!important;
  width:100vw!important;height:100dvh!important;max-width:none!important;max-height:none!important;
  margin:0!important;padding:18px!important;border:0!important;
  display:none;align-items:center;justify-content:center;
  overflow:auto!important;background:
    radial-gradient(850px 520px at 12% 8%,rgba(124,58,237,.24),transparent 62%),
    radial-gradient(700px 480px at 90% 95%,rgba(14,165,233,.16),transparent 60%),
    rgba(5,7,15,.94)!important;color:#f8fafc!important;
  direction:rtl;
}
#onboardOverlay[open]{display:flex!important}
#onboardOverlay .onboard-box{
  width:min(1080px,100%)!important;max-width:1080px!important;
  height:auto!important;max-height:calc(100dvh - 36px)!important;min-height:590px;
  padding:0!important;margin:auto!important;border:1px solid rgba(255,255,255,.12)!important;
  border-radius:28px!important;overflow:hidden!important;
  display:grid!important;grid-template-columns:290px minmax(0,1fr)!important;
  align-items:stretch!important;justify-content:stretch!important;
  background:#0d1220!important;
  box-shadow:0 35px 110px rgba(0,0,0,.58),0 0 0 1px rgba(124,58,237,.12);
  animation:tourEnter .38s cubic-bezier(.2,.8,.2,1) both!important;
}
@keyframes tourEnter{from{opacity:0;transform:translateY(16px) scale(.985)}to{opacity:1;transform:none}}
#onboardOverlay .tour-rail{
  position:relative;display:flex;flex-direction:column;gap:26px;
  padding:32px 24px;background:
    radial-gradient(300px 220px at 35% 0%,rgba(124,58,237,.24),transparent 75%),
    linear-gradient(160deg,#171b31,#101524 72%);
  border-left:1px solid rgba(255,255,255,.08);
}
#onboardOverlay .tour-brand{display:flex;align-items:center;gap:12px}
#onboardOverlay .tour-brand-mark{
  width:44px;height:44px;display:grid;place-items:center;border-radius:15px;
  color:white;font-weight:950;font-size:18px;letter-spacing:-1px;
  background:linear-gradient(140deg,#8b5cf6,#4f46e5 58%,#0ea5e9);
  box-shadow:0 10px 28px rgba(99,102,241,.34)
}
#onboardOverlay .tour-brand-copy b{display:block;font-size:13px;font-weight:900;color:#fff;letter-spacing:.2px}
#onboardOverlay .tour-brand-copy span{display:block;margin-top:3px;color:#929bb4;font-size:11px}
#onboardOverlay .tour-rail-intro{padding:18px 0 2px}
#onboardOverlay .tour-rail-kicker{color:#a78bfa;font-size:10px;font-weight:900;letter-spacing:1.7px}
#onboardOverlay .tour-rail-title{margin:9px 0 7px;color:#fff;font-size:22px;line-height:1.45;font-weight:950}
#onboardOverlay .tour-rail-desc{margin:0;color:#9ca8c0;font-size:12px;line-height:1.9}
#onboardOverlay .tour-route-list{display:grid;gap:10px;margin-top:2px}
#onboardOverlay .tour-route-item{
  display:flex;align-items:center;gap:11px;width:100%;padding:10px 11px;
  color:#8f9ab2;background:transparent;border:1px solid transparent;border-radius:13px;
  text-align:right;font:inherit;cursor:pointer;transition:background .2s,border-color .2s,color .2s
}
#onboardOverlay .tour-route-item:hover{background:rgba(255,255,255,.045);color:#fff}
#onboardOverlay .tour-route-item.active{color:#fff;background:rgba(139,92,246,.13);border-color:rgba(167,139,250,.32)}
#onboardOverlay .tour-route-num{
  display:grid;place-items:center;flex:0 0 28px;height:28px;border-radius:9px;
  background:rgba(255,255,255,.07);font-size:11px;font-weight:900;color:#aab4ca
}
#onboardOverlay .tour-route-item.active .tour-route-num{background:linear-gradient(135deg,#8b5cf6,#4f46e5);color:#fff}
#onboardOverlay .tour-route-item.done .tour-route-num{background:rgba(16,185,129,.16);color:#6ee7b7}
#onboardOverlay .tour-route-text{font-size:12px;font-weight:800}
#onboardOverlay .tour-rail-foot{margin-top:auto;padding-top:18px;border-top:1px solid rgba(255,255,255,.08);color:#818da7;font-size:11px;line-height:1.8}
#onboardOverlay .tour-rail-foot strong{color:#c4b5fd}
#onboardOverlay .tour-main{min-width:0;display:flex;flex-direction:column;padding:30px 34px 24px;background:
  radial-gradient(620px 320px at 96% 0%,rgba(76,29,149,.17),transparent 72%),#0e1422}
#onboardOverlay .tour-top{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:2px 52px 20px 0}
#onboardOverlay .tour-step-label{display:flex;align-items:center;gap:9px;color:#a6b1c8;font-size:11px;font-weight:900;letter-spacing:.5px}
#onboardOverlay .tour-step-label i{font-style:normal;color:#c4b5fd}
#onboardOverlay .tour-progress-copy{color:#8390aa;font-size:11px;font-weight:800;white-space:nowrap}
#onboardOverlay .tour-progress-track{height:5px;background:rgba(255,255,255,.075);border-radius:99px;overflow:hidden;margin-bottom:28px}
#onboardOverlay .tour-progress-fill{height:100%;width:0;background:linear-gradient(90deg,#8b5cf6,#6366f1 55%,#22d3ee);border-radius:99px;box-shadow:0 0 18px rgba(139,92,246,.45);transition:width .35s ease}
#onboardOverlay .tour-content{display:grid;grid-template-columns:minmax(0,.92fr) minmax(280px,1.08fr);gap:28px;align-items:center;flex:1;min-height:0}
#onboardOverlay .tour-copy{min-width:0;padding:8px 0}
#onboardOverlay .tour-icon{
  width:58px;height:58px;display:grid;place-items:center;border-radius:18px;margin-bottom:20px;
  font-size:26px;color:#e9ddff;background:linear-gradient(145deg,rgba(139,92,246,.24),rgba(14,165,233,.12));
  border:1px solid rgba(167,139,250,.23);box-shadow:0 12px 30px rgba(76,29,149,.18)
}
#onboardOverlay .tour-eyebrow{margin:0 0 8px;color:#a78bfa;font-size:11px;font-weight:950;letter-spacing:1.1px}
#onboardOverlay .tour-title{margin:0 0 13px;color:#fff;font-size:clamp(25px,3vw,36px);line-height:1.35;font-weight:950;letter-spacing:-.5px}
#onboardOverlay .tour-text{margin:0;color:#aab5ca;font-size:14px;line-height:2.05;max-width:440px}
#onboardOverlay .tour-tip{
  display:flex;align-items:flex-start;gap:10px;margin-top:23px;padding:13px 14px;
  color:#cbd5e1;background:rgba(30,41,59,.58);border:1px solid rgba(148,163,184,.15);
  border-radius:14px;font-size:11px;line-height:1.85
}
#onboardOverlay .tour-tip b{color:#67e8f9;white-space:nowrap}
#onboardOverlay .tour-visual{
  position:relative;min-width:0;min-height:300px;display:grid;place-items:center;
  padding:22px;border-radius:24px;overflow:hidden;
  background:
    radial-gradient(330px 220px at 50% 10%,rgba(124,58,237,.18),transparent 74%),
    linear-gradient(145deg,#151d32,#111827);
  border:1px solid rgba(255,255,255,.095);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.04),0 20px 60px rgba(0,0,0,.18)
}
#onboardOverlay .tour-visual:before,#onboardOverlay .tour-visual:after{
  content:"";position:absolute;width:140px;height:140px;border:1px solid rgba(167,139,250,.09);border-radius:50%;pointer-events:none
}
#onboardOverlay .tour-visual:before{top:-75px;left:-55px}
#onboardOverlay .tour-visual:after{bottom:-92px;right:-70px;width:190px;height:190px}
#onboardOverlay .tv-wrap{position:relative;z-index:1;width:min(100%,390px)}
#onboardOverlay .tv-window{
  overflow:hidden;border-radius:17px;border:1px solid rgba(255,255,255,.13);
  background:#0e1525;box-shadow:0 18px 45px rgba(0,0,0,.3)
}
#onboardOverlay .tv-bar{height:34px;display:flex;align-items:center;justify-content:space-between;padding:0 12px;background:#1b2438;border-bottom:1px solid rgba(255,255,255,.07)}
#onboardOverlay .tv-dots{display:flex;gap:4px;direction:ltr}
#onboardOverlay .tv-dots i{width:6px;height:6px;border-radius:50%;background:#66718b}
#onboardOverlay .tv-caption{color:#aab6ce;font-size:9px;font-weight:800;letter-spacing:.4px}
#onboardOverlay .tv-body{padding:18px}
#onboardOverlay .tv-brandline{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:15px}
#onboardOverlay .tv-brandline b{color:#f8fafc;font-size:12px}
#onboardOverlay .tv-pill{padding:5px 9px;border-radius:20px;color:#c4b5fd;background:rgba(139,92,246,.15);font-size:9px;font-weight:900}
#onboardOverlay .tv-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}
#onboardOverlay .tv-stat{padding:12px 8px;border-radius:12px;background:rgba(255,255,255,.045);border:1px solid rgba(255,255,255,.07);text-align:center}
#onboardOverlay .tv-stat strong{display:block;color:#fff;font-size:21px;font-weight:950}
#onboardOverlay .tv-stat span{display:block;margin-top:4px;color:#8f9bb3;font-size:9px}
#onboardOverlay .tv-cards{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}
#onboardOverlay .tv-mini-card{min-width:0;padding:13px 7px 10px;border-radius:12px;text-align:center;background:linear-gradient(150deg,#f8fafc,#dbeafe);color:#172033;border:2px solid transparent}
#onboardOverlay .tv-mini-card.active{border-color:#a78bfa;box-shadow:0 0 0 3px rgba(139,92,246,.16)}
#onboardOverlay .tv-mini-card i{display:block;font-size:19px;font-style:normal;margin-bottom:8px}
#onboardOverlay .tv-mini-card b{display:block;font-size:9px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#onboardOverlay .tv-mini-card small{display:block;margin-top:5px;color:#64748b;font-size:8px}
#onboardOverlay .tv-search{padding:9px 11px;margin-bottom:12px;border-radius:10px;background:rgba(255,255,255,.055);color:#8492ab;font-size:9px}
#onboardOverlay .tv-flash{
  min-height:190px;padding:22px;border-radius:16px;display:flex;flex-direction:column;
  justify-content:center;align-items:center;text-align:center;color:#182033;
  background:linear-gradient(145deg,#fff,#e8eaff);box-shadow:0 14px 30px rgba(0,0,0,.22)
}
#onboardOverlay .tv-flash .tv-word{font-size:clamp(25px,4vw,37px);font-weight:950;letter-spacing:.3px}
#onboardOverlay .tv-flash .tv-meaning{margin-top:13px;color:#6d4bd1;font-size:19px;font-weight:800}
#onboardOverlay .tv-flash small{margin-top:19px;color:#64748b;font-size:9px}
#onboardOverlay .tv-voice-grid{display:grid;gap:10px}
#onboardOverlay .tv-voice{padding:13px;border:1px solid rgba(255,255,255,.09);border-radius:12px;background:rgba(255,255,255,.045)}
#onboardOverlay .tv-voice-head{display:flex;align-items:center;justify-content:space-between;gap:8px;color:#e2e8f0;font-size:10px;font-weight:800}
#onboardOverlay .tv-voice-head span:last-child{color:#a78bfa;font-size:9px}
#onboardOverlay .tv-wave{height:5px;margin-top:11px;border-radius:9px;background:linear-gradient(90deg,#8b5cf6 0 62%,rgba(255,255,255,.09) 62%);overflow:hidden}
#onboardOverlay .tv-wave.ar{background:linear-gradient(90deg,#22d3ee 0 78%,rgba(255,255,255,.09) 78%)}
#onboardOverlay .tv-export{padding:18px;border:1px solid rgba(167,139,250,.22);border-radius:16px;background:rgba(139,92,246,.08);text-align:center}
#onboardOverlay .tv-export-icon{width:62px;height:62px;margin:0 auto 12px;display:grid;place-items:center;border-radius:19px;color:#fff;font-size:25px;background:linear-gradient(145deg,#8b5cf6,#4f46e5);box-shadow:0 12px 28px rgba(99,102,241,.28)}
#onboardOverlay .tv-export b{display:block;color:#fff;font-size:18px}
#onboardOverlay .tv-export span{display:block;margin-top:7px;color:#9aa8c2;font-size:10px}
#onboardOverlay .tv-checks{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:13px;text-align:right}
#onboardOverlay .tv-checks span{padding:8px;border-radius:9px;background:rgba(16,185,129,.09);color:#86efac;font-size:9px}
#onboardOverlay .tour-footer{
  display:flex;align-items:center;justify-content:space-between;gap:12px;
  padding-top:22px;margin-top:24px;border-top:1px solid rgba(255,255,255,.08)
}
#onboardOverlay .tour-footer-note{color:#7f8ca5;font-size:10px}
#onboardOverlay .tour-actions{display:flex;align-items:center;gap:9px;flex-wrap:wrap}
#onboardOverlay .tour-btn{
  min-height:43px;padding:0 19px;border-radius:12px;border:1px solid rgba(255,255,255,.12);
  color:#cbd5e1;background:rgba(255,255,255,.045);font:inherit;font-size:12px;font-weight:900;cursor:pointer;
  transition:transform .18s,border-color .18s,background .18s
}
#onboardOverlay .tour-btn:hover{border-color:rgba(167,139,250,.45);background:rgba(255,255,255,.08)}
#onboardOverlay .tour-btn:active{transform:scale(.97)}
#onboardOverlay .tour-btn.primary{color:#fff;border-color:transparent;background:linear-gradient(120deg,#7c3aed,#4f46e5 58%,#2563eb);box-shadow:0 9px 24px rgba(79,70,229,.3)}
#onboardOverlay .tour-btn.primary:hover{filter:brightness(1.1);transform:translateY(-1px)}
#onboardOverlay .tour-btn.text{border-color:transparent;background:transparent;color:#8f9bb3}
#onboardOverlay .tour-close{
  position:absolute;top:18px;left:18px;z-index:5;width:38px;height:38px;border-radius:12px;
  display:grid;place-items:center;color:#b9c3d8;background:rgba(255,255,255,.055);
  border:1px solid rgba(255,255,255,.11);font-size:19px;cursor:pointer
}
#onboardOverlay .tour-close:hover{color:#fff;background:rgba(239,68,68,.16);border-color:rgba(248,113,113,.35)}
#onboardOverlay button:focus-visible{outline:2px solid #67e8f9;outline-offset:3px}
@media(max-width:850px){
  #onboardOverlay.onboard-overlay{padding:0!important;align-items:stretch}
  #onboardOverlay .onboard-box{width:100%!important;max-height:100dvh!important;min-height:100dvh;border-radius:0!important;grid-template-columns:1fr!important;grid-template-rows:auto 1fr!important}
  #onboardOverlay .tour-rail{padding:15px 18px 12px;gap:8px;border-left:0;border-bottom:1px solid rgba(255,255,255,.08)}
  #onboardOverlay .tour-brand{gap:9px}
  #onboardOverlay .tour-brand-mark{width:35px;height:35px;border-radius:11px;font-size:15px}
  #onboardOverlay .tour-brand-copy b{font-size:11px}
  #onboardOverlay .tour-brand-copy span{font-size:9px}
  #onboardOverlay .tour-rail-intro,#onboardOverlay .tour-rail-foot{display:none}
  #onboardOverlay .tour-route-list{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:6px;margin:6px 0 0}
  #onboardOverlay .tour-route-item{justify-content:center;padding:5px 2px;border-radius:9px}
  #onboardOverlay .tour-route-num{width:25px;height:25px;flex-basis:25px;border-radius:8px;font-size:10px}
  #onboardOverlay .tour-route-text{display:none}
  #onboardOverlay .tour-main{padding:18px 18px 16px;min-height:0;overflow:auto}
  #onboardOverlay .tour-top{padding:0 46px 13px 0}
  #onboardOverlay .tour-progress-track{margin-bottom:16px}
  #onboardOverlay .tour-content{grid-template-columns:1fr;gap:16px;align-content:start}
  #onboardOverlay .tour-copy{padding:0}
  #onboardOverlay .tour-icon{width:43px;height:43px;border-radius:13px;margin-bottom:11px;font-size:20px}
  #onboardOverlay .tour-title{font-size:25px;margin-bottom:7px}
  #onboardOverlay .tour-text{font-size:12px;line-height:1.85}
  #onboardOverlay .tour-tip{margin-top:12px;padding:10px 11px;font-size:10px}
  #onboardOverlay .tour-visual{min-height:205px;padding:12px;border-radius:17px}
  #onboardOverlay .tv-wrap{width:min(100%,360px)}
  #onboardOverlay .tv-body{padding:12px}
  #onboardOverlay .tv-flash{min-height:125px}
  #onboardOverlay .tour-footer{margin-top:15px;padding-top:14px;align-items:flex-end}
  #onboardOverlay .tour-footer-note{display:none}
  #onboardOverlay .tour-actions{width:100%;display:grid;grid-template-columns:auto 1fr auto}
  #onboardOverlay .tour-btn{min-height:42px;padding:0 12px;font-size:11px}
  #onboardOverlay .tour-close{top:12px;left:14px;width:33px;height:33px;border-radius:10px}
}
@media(max-width:380px){
  #onboardOverlay .tour-main{padding:14px 13px 12px}
  #onboardOverlay .tour-title{font-size:22px}
  #onboardOverlay .tour-visual{min-height:185px}
  #onboardOverlay .tour-actions{gap:5px}
  #onboardOverlay .tour-btn{padding:0 8px}
}
@media(prefers-reduced-motion:reduce){
  #onboardOverlay *,#onboardOverlay *:before,#onboardOverlay *:after{
    animation:none!important;transition:none!important;scroll-behavior:auto!important
  }
}
"""

def upgrade_gallery_ux(h, did, spec):
    deck_data = {
        "fr9": {"name": "French 9", "nameAr": "الفرنسية للصف التاسع", "language": "الفرنسي", "code": "FR", "word": "Leçon", "meaning": "درس"},
        "en9": {"name": "English 9", "nameAr": "الإنجليزية للصف التاسع", "language": "الإنجليزي", "code": "EN", "word": "Student", "meaning": "طالب"},
        "enlit": {"name": "English Literature 12", "nameAr": "الأدب الإنجليزي للصف الثاني عشر", "language": "الإنجليزي", "code": "EN", "word": "Novel", "meaning": "رواية"},
        "ensci": {"name": "English Science 12", "nameAr": "العلوم باللغة الإنجليزية للصف الثاني عشر", "language": "الإنجليزي", "code": "EN", "word": "Atom", "meaning": "ذرة"},
    }[did]

    # The circular-arrow control in the upper corner of the single-card preview
    # duplicates the large, clearly labelled answer/flip control below it.
    corner_flip = (
        '<button class="gv-fab gv-flip" onclick="gvFlip()" title="قلب البطاقة" aria-label="قلب البطاقة">'
        '<svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
        '<polyline points="1 4 7 10 7"/>'
        '<path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>'
        '</svg></button>'
    )
    # Match by the actual complete source element (SVG whitespace/attributes included).
    corner_start = h.find('<button class="gv-fab gv-flip"')
    if corner_start < 0:
        raise SystemExit("[%s] single-preview corner flip button not found" % did)
    corner_end = h.find("</button>", corner_start)
    if corner_end < 0:
        raise SystemExit("[%s] single-preview corner flip button is malformed" % did)
    actual_corner = h[corner_start:corner_end + len("</button>")]
    if "onclick=\"gvFlip()\"" not in actual_corner or "aria-label=\"قلب البطاقة\"" not in actual_corner:
        raise SystemExit("[%s] unexpected corner control; refusing to remove" % did)
    h = h[:corner_start] + h[corner_end + len("</button>"):]

    # Replace the old text-only onboarding with a deck-aware, illustrated walkthrough.
    start = h.index("var ONBOARD_STEPS=[")
    end = h.index("// ============================================================\n// WHAT'S NEW", start)
    new_tour = r'''var TOUR_DECK = __TOUR_DECK__;
var ONBOARD_STEPS = [
  {eyebrow:'مرحباً بك في الاستوديو',icon:'✦',title:'مساحة واحدة لتصميم رزمة مميزة',text:'أهلاً بك في معرض '+TOUR_DECK.name+'؛ هنا تستعرض التصاميم، تختبر شكل البطاقة، تضبط النطق، ثم تخرج برزمتك الجاهزة لـ Anki.',tip:'ابدأ باستكشاف القوالب، ولا تحتاج إلى أي إعداد مسبق.'},
  {eyebrow:'الخطوة 01 · اختيار التصميم',icon:'▦',title:'اعثر على الشكل الذي يناسبك',text:'تصفّح القوالب المئة، واستخدم البحث والتصنيفات للوصول إلى الشكل الذي تريده. افتح أي تصميم لتشاهد معاينته، ثم حدده لإضافته إلى اختياراتك.',tip:'يمكنك اختيار قالب واحد أو عدة قوالب؛ وتظهر اختياراتك في شريط التحديد.'},
  {eyebrow:'الخطوة 02 · المعاينة',icon:'◫',title:'اختبر وجهي البطاقة قبل الاختيار',text:'افتح المعاينة الكاملة، شاهد الوجه الأمامي والخلفي، وانتقل بين التصاميم للمقارنة. هكذا تتأكد من وضوح الكلمة والمعنى والصوت قبل اعتماد القالب.',tip:'زر «قلب البطاقة» يعرض الجهة الأخرى، و«تحديد» يعتمد التصميم.'},
  {eyebrow:'الخطوة 03 · إعداد الصوت',icon:'♫',title:'اجعل النطق مناسباً لطريقتك',text:'اختر الصوت '+TOUR_DECK.language+' والصوت العربي، واضبط السرعة والنغمة والفواصل الزمنية. استمع إلى المعاينة أولاً، ثم احتفظ بالإعدادات التي تناسبك.',tip:'إعدادات الصوت نفسها تُستخدم عند إنشاء الرزمة، ويمكنك إلغاء تضمين الصوت عند التصدير.'},
  {eyebrow:'الخطوة 04 · التصدير',icon:'⇩',title:'حوّل اختياراتك إلى رزمة Anki',text:'اكتب اسم الرزمة، راجع خيار تضمين الصوت والتشغيل التلقائي، ثم ابدأ التصدير. ستحصل على ملف APKG تستورده داخل تطبيق Anki.',tip:'بعد الاستيراد، افتح الرزمة في Anki وتأكد من ظهور البطاقات والصوت كما عاينتهما.'}
];
var onbStep=0;
var tourPreviousFocus=null;

function tourVisualForStep(index){
  if(index===0){
    return '<div class="tv-wrap"><div class="tv-window"><div class="tv-bar"><span class="tv-dots"><i></i><i></i><i></i></span><span class="tv-caption">ANKI DESIGN STUDIO</span></div><div class="tv-body"><div class="tv-brandline"><b>'+TOUR_DECK.name+'</b><span class="tv-pill">'+TOUR_DECK.code+' · DECK</span></div><div class="tv-stats"><div class="tv-stat"><strong>100</strong><span>قالب قابل للمعاينة</span></div><div class="tv-stat"><strong>01</strong><span>معرض مستقل</span></div><div class="tv-stat"><strong>APKG</strong><span>صيغة التصدير</span></div></div><div style="margin-top:14px;padding:12px;border-radius:12px;background:linear-gradient(100deg,rgba(139,92,246,.18),rgba(14,165,233,.1));color:#dbeafe;font-size:10px;text-align:center">من الفكرة إلى بطاقة جاهزة للمراجعة ✨</div></div></div></div>';
  }
  if(index===1){
    return '<div class="tv-wrap"><div class="tv-window"><div class="tv-bar"><span class="tv-dots"><i></i><i></i><i></i></span><span class="tv-caption">TEMPLATE GALLERY</span></div><div class="tv-body"><div class="tv-search">⌕ &nbsp; ابحث عن تصميم...</div><div class="tv-cards"><div class="tv-mini-card"><i>▤</i><b>تصميم 08</b><small>هادئ وبسيط</small></div><div class="tv-mini-card active"><i>✦</i><b>تصميم 24</b><small>محدد للمعاينة</small></div><div class="tv-mini-card"><i>◈</i><b>تصميم 51</b><small>ألوان مميزة</small></div></div><div style="margin-top:13px;display:flex;justify-content:space-between;color:#93a4bf;font-size:9px"><span>100 تصميم</span><span style="color:#c4b5fd">اختيار القالب ←</span></div></div></div></div>';
  }
  if(index===2){
    return '<div class="tv-wrap"><div class="tv-window"><div class="tv-bar"><span class="tv-dots"><i></i><i></i><i></i></span><span class="tv-caption">CARD PREVIEW</span></div><div class="tv-body"><div class="tv-brandline"><b>معاينة البطاقة</b><span class="tv-pill">FRONT / BACK</span></div><div class="tv-flash"><div class="tv-word">'+TOUR_DECK.word+'</div><div class="tv-meaning">'+TOUR_DECK.meaning+'</div><small>اضغط لقلب البطاقة ومشاهدة الوجه الآخر</small></div><div style="display:flex;justify-content:center;gap:8px;margin-top:12px"><span class="tv-pill">السابق</span><span class="tv-pill">قلب البطاقة ↻</span><span class="tv-pill">التالي</span></div></div></div></div>';
  }
  if(index===3){
    return '<div class="tv-wrap"><div class="tv-window"><div class="tv-bar"><span class="tv-dots"><i></i><i></i><i></i></span><span class="tv-caption">VOICE STUDIO</span></div><div class="tv-body"><div class="tv-brandline"><b>إعدادات النطق</b><span class="tv-pill">AUDIO</span></div><div class="tv-voice-grid"><div class="tv-voice"><div class="tv-voice-head"><span>الصوت '+TOUR_DECK.language+'</span><span>'+TOUR_DECK.code+'</span></div><div class="tv-wave"></div></div><div class="tv-voice"><div class="tv-voice-head"><span>الصوت العربي</span><span>AR</span></div><div class="tv-wave ar"></div></div><div class="tv-voice"><div class="tv-voice-head"><span>السرعة والنغمة</span><span>1.0×</span></div><div class="tv-wave"></div></div></div></div></div></div>';
  }
  return '<div class="tv-wrap"><div class="tv-window"><div class="tv-bar"><span class="tv-dots"><i></i><i></i><i></i></span><span class="tv-caption">READY TO EXPORT</span></div><div class="tv-body"><div class="tv-export"><div class="tv-export-icon">⇩</div><b>ملف Anki جاهز</b><span>'+TOUR_DECK.name+' · .APKG</span><div class="tv-checks"><span>✓ القوالب المحددة</span><span>✓ إعدادات الصوت</span><span>✓ اسم الرزمة</span><span>✓ جاهز للاستيراد</span></div></div></div></div></div>';
}

function showOnboarding(){
  var overlay=document.getElementById('onboardOverlay');
  if(!overlay)return;
  tourPreviousFocus=document.activeElement;
  onbStep=0;
  renderOnboardStep();
  overlay.setAttribute('role','dialog');
  overlay.setAttribute('aria-modal','true');
  overlay.setAttribute('aria-label','جولة استخدام معرض '+TOUR_DECK.name);
  try{
    if(typeof overlay.showModal==='function'&&!overlay.open)overlay.showModal();
  }catch(_e){}
  overlay.style.display='flex';
  document.body.style.overflow='hidden';
  setTimeout(function(){var next=overlay.querySelector('[data-tour-next]');if(next)next.focus();},30);
}

function closeOnboarding(){
  var overlay=document.getElementById('onboardOverlay');
  if(!overlay)return;
  try{if(overlay.open)overlay.close();}catch(_e){}
  overlay.style.display='none';
  document.body.style.overflow='';
  try{localStorage.setItem(__TOUR_STORAGE_KEY__,'1');}catch(_e){}
  var previous=tourPreviousFocus;
  tourPreviousFocus=null;
  if(previous&&typeof previous.focus==='function'&&document.contains(previous)){
    try{previous.focus({preventScroll:true});}catch(_e){try{previous.focus();}catch(_e2){}}
  }
}

function goOnboardingStep(next){
  var n=parseInt(next,10);
  if(!isFinite(n))return;
  onbStep=Math.max(0,Math.min(ONBOARD_STEPS.length-1,n));
  renderOnboardStep();
}

function renderOnboardStep(){
  var box=document.getElementById('onboardBox');
  if(!box)return;
  onbStep=Math.max(0,Math.min(ONBOARD_STEPS.length-1,onbStep));
  var step=ONBOARD_STEPS[onbStep];
  var total=ONBOARD_STEPS.length;
  var percent=Math.round(((onbStep+1)/total)*100);
  var h='<button class="tour-close" type="button" onclick="closeOnboarding()" aria-label="إغلاق الجولة">×</button>';
  h+='<aside class="tour-rail"><div class="tour-brand"><span class="tour-brand-mark">A</span><div class="tour-brand-copy"><b>ANKI DESIGN STUDIO</b><span>دليل البداية السريع</span></div></div>';
  h+='<div class="tour-rail-intro"><div class="tour-rail-kicker">YOUR WORKFLOW</div><h2 class="tour-rail-title">من اختيار القالب إلى رزمة جاهزة</h2><p class="tour-rail-desc">خمس محطات قصيرة لتتعرف على الأدوات الأساسية وتبدأ بثقة.</p></div>';
  h+='<nav class="tour-route-list" aria-label="مراحل الجولة">';
  ONBOARD_STEPS.forEach(function(item,i){
    var state=i===onbStep?' active':i<onbStep?' done':'';
    h+='<button type="button" class="tour-route-item'+state+'" onclick="goOnboardingStep('+i+')" '+(i===onbStep?'aria-current="step"':'')+'><span class="tour-route-num">'+(i<onbStep?'✓':String(i+1).padStart(2,'0'))+'</span><span class="tour-route-text">'+['البداية','اختيار التصميم','المعاينة','الصوت','التصدير'][i]+'</span></button>';
  });
  h+='</nav><div class="tour-rail-foot">المعرض الحالي<br><strong>'+TOUR_DECK.name+'</strong><br>كل خطوة تحفظ وقتك وتقلل التجربة العشوائية.</div></aside>';
  h+='<main class="tour-main"><div class="tour-top"><div class="tour-step-label"><i>STEP '+String(onbStep+1).padStart(2,'0')+'</i><span>/</span><span>'+String(total).padStart(2,'0')+'</span></div><div class="tour-progress-copy">'+percent+'٪ مكتمل</div></div>';
  h+='<div class="tour-progress-track" role="progressbar" aria-label="تقدم الجولة" aria-valuemin="0" aria-valuemax="100" aria-valuenow="'+percent+'"><div class="tour-progress-fill" style="width:'+percent+'%"></div></div>';
  h+='<section class="tour-content" aria-live="polite"><div class="tour-copy"><div class="tour-icon" aria-hidden="true">'+step.icon+'</div><p class="tour-eyebrow">'+step.eyebrow+'</p><h1 class="tour-title" id="tourStepTitle">'+step.title+'</h1><p class="tour-text">'+step.text+'</p><div class="tour-tip"><b>نصيحة</b><span>'+step.tip+'</span></div></div>';
  h+='<div class="tour-visual" aria-hidden="true">'+tourVisualForStep(onbStep)+'</div></section>';
  h+='<footer class="tour-footer"><div class="tour-footer-note">خطوة '+(onbStep+1)+' من '+total+' · '+TOUR_DECK.nameAr+'</div><div class="tour-actions">';
  h+='<button type="button" class="tour-btn text" onclick="closeOnboarding()">تخطي الجولة</button>';
  if(onbStep>0)h+='<button type="button" class="tour-btn" data-tour-prev onclick="goOnboardingStep('+(onbStep-1)+')">السابق</button>';
  if(onbStep<total-1)h+='<button type="button" class="tour-btn primary" data-tour-next onclick="goOnboardingStep('+(onbStep+1)+')">'+(onbStep===0?'ابدأ الجولة':'التالي')+' ←</button>';
  else h+='<button type="button" class="tour-btn primary" data-tour-next onclick="closeOnboarding()">إنهاء الجولة وابدأ ←</button>';
  h+='</div></footer></main>';
  box.innerHTML=h;
  var overlay=document.getElementById('onboardOverlay');
  if(overlay){
    overlay.setAttribute('aria-labelledby','tourStepTitle');
    setTimeout(function(){var target=box.querySelector('[data-tour-next]')||box.querySelector('[data-tour-prev]');if(target)target.focus();},0);
  }
}

(function bindOnboardingKeys(){
  var overlay=document.getElementById('onboardOverlay');
  if(!overlay||overlay.dataset.tourBound)return;
  overlay.dataset.tourBound='1';
  overlay.addEventListener('click',function(event){if(event.target===overlay)closeOnboarding();});
  overlay.addEventListener('cancel',function(event){event.preventDefault();closeOnboarding();});
  document.addEventListener('keydown',function(event){
    var active=document.getElementById('onboardOverlay');
    if(!active||(active.style.display==='none'&&!active.open))return;
    if(event.key==='Escape'){event.preventDefault();closeOnboarding();return;}
    if(event.altKey||event.ctrlKey||event.metaKey)return;
    if(event.key==='ArrowLeft'){event.preventDefault();goOnboardingStep(onbStep+1);}
    else if(event.key==='ArrowRight'){event.preventDefault();goOnboardingStep(onbStep-1);}
  });
})();
'''
    new_tour = new_tour.replace("__TOUR_DECK__", json.dumps(deck_data, ensure_ascii=False))
    new_tour = new_tour.replace("__TOUR_STORAGE_KEY__", json.dumps("anki_%s_onboarded" % did))
    h = h[:start] + new_tour + "\n" + h[end:]

    # Repair leftover primary-language wording in the English voice controls and export FAQ.
    if did in ("en9", "enlit", "ensci"):
        replacements = [
            ("صمت قبل الفرنسي", "صمت قبل الإنجليزي"),
            ("اختر الصوت الفرنسي والصوت العربي، ثم عدّل السرعة والنغمة والفواصل الزمنية حسب الطريقة التي تفضّلها. استخدم «معاينة الصوت» للاستماع إلى النطق قبل إنشاء الرزمة.",
             "اختر الصوت الإنجليزي والصوت العربي، ثم عدّل السرعة والنغمة والفواصل الزمنية حسب الطريقة التي تفضّلها. استخدم «معاينة الصوت» للاستماع إلى النطق قبل إنشاء الرزمة."),
            ("مع الصوت الفرنسي والعربي وفق إعداداتك", "مع الصوت الإنجليزي والعربي وفق إعداداتك"),
        ]
        for old, new in replacements:
            count = h.count(old)
            if count != 1:
                raise SystemExit("[%s] expected exactly one stale voice label (%d): %s" % (did, count, old[:70]))
            h = h.replace(old, new, 1)

    # Convert the remaining primary-language UI labels in English galleries.
    # Internal field names such as fontFrench remain unchanged for compatibility;
    # only their Arabic-facing labels and explanatory copy are adapted.
    if did in ("en9", "enlit", "ensci"):
        for old, new in (
            ("🇫🇷", "🇬🇧"),
            ("الفرنسية", "الإنجليزية"),
            ("الفرنسي", "الإنجليزي"),
            ("فرنسية", "إنجليزية"),
            ("فرنسي", "إنجليزي"),
        ):
            h = h.replace(old, new)

    # Add the new visual system at the end so it safely overrides the old tour styles.
    body_close = h.rfind("</body>")
    if body_close < 0:
        raise SystemExit("[%s] no final body tag for tour stylesheet" % did)
    h = h[:body_close] + '\n<style id="anki-tour-v2">\n' + TOUR_CSS + '\n</style>\n' + h[body_close:]
    return h


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
