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
BASE = os.environ.get('ANKI_BASE_HTML') or str(ROOT / 'index.html')
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


def apply_gallery_ux(h, did):
    """Apply shared interaction and onboarding polish to the four non-protected galleries."""
    # Remove the floating circular-arrow control from the single-card gallery preview.
    h2, removed = re.subn(
        r'\s*<button class="gv-fab gv-flip"[^>]*>.*?</button>\s*',
        '\n',
        h,
        count=1,
        flags=re.DOTALL,
    )
    if removed != 1:
        raise SystemExit('[%s] expected exactly one floating preview flip control, removed %d'
                         % (did, removed))
    h = h2

    # Replace the old text-only onboarding with a responsive, illustrated walkthrough.
    start_marker = 'var ONBOARD_STEPS=['
    end_marker = '\n\n// ============================================================\n// WHAT'
    start = h.find(start_marker)
    end = h.find(end_marker, start)
    if start < 0 or end < 0:
        raise SystemExit('[%s] onboarding source block was not found' % did)

    onboarding = r"""var ONBOARD_STEPS=[
  {title:'أهلًا بك في معرض قوالب Anki',text:'جولة قصيرة تساعدك على اختيار تصميم البطاقة، معاينته، ضبط الصوت، ثم إنشاء رزمة جاهزة للمراجعة.',icon:'✨',artTag:'مرحبًا بك',artTitle:'من الفكرة إلى رزمة جاهزة',artMeta:'كل أدواتك في مكان واحد',tip:'سنمشي معك خطوة بخطوة — ويمكنك تخطي الجولة في أي وقت.'},
  {title:'اختر التصميم الذي يناسبك',text:'تصفّح القوالب المئة، واستخدم البحث والتصنيفات للوصول إلى الشكل الذي يعجبك. يمكنك اختيار قالب واحد أو مجموعة قوالب.',icon:'🎨',artTag:'01 · التصميم',artTitle:'100 قالب بصري',artMeta:'ابحث، صفِّ، واختر',tip:'جرّب أكثر من قالب قبل أن تحسم اختيارك.'},
  {title:'عاين البطاقة قبل اعتمادها',text:'شاهد شكل البطاقة ومحتواها، وانتقل بين القوالب. يمكنك قلب البطاقة من زر المعاينة السفلي لمراجعة الوجه الآخر.',icon:'👀',artTag:'02 · المعاينة',artTitle:'شاهد النتيجة أولًا',artMeta:'تأكد من وضوح الوجهين',tip:'المعاينة تساعدك على اكتشاف أي مشكلة قبل إنشاء الرزمة.'},
  {title:'اضبط الصوت كما تحب',text:'اختر الأصوات المتاحة، وعدّل السرعة والنغمة والفواصل الزمنية، ثم استمع إلى عينة للتأكد من الإعدادات.',icon:'🔊',artTag:'03 · الصوت',artTitle:'صوت واضح ومناسب',artMeta:'تحكم بالإعدادات واستمع للعينة',tip:'يمكنك متابعة العمل دون صوت، ثم تفعيل الصوت عند التصدير.'},
  {title:'أنشئ رزمة Anki وابدأ المراجعة',text:'راجع اختياراتك وإعدادات التصدير، ثم أنشئ ملف APKG واستورده إلى تطبيق Anki لبدء المراجعة.',icon:'🚀',artTag:'04 · التصدير',artTitle:'رُزمتك أصبحت جاهزة',artMeta:'ملف APKG للاستيراد إلى Anki',tip:'قبل التصدير، تأكد من القوالب والصوت والخيارات التي تريد تضمينها.'}
];
var onbStep=0;

function showOnboarding(){
  onbStep=0;
  renderOnboardStep();
  var ov=document.getElementById('onboardOverlay');
  if(ov){ov.style.display='flex';ov.setAttribute('aria-hidden','false');}
  var first=document.querySelector('#onboardBox .ob-primary');
  if(first)setTimeout(function(){try{first.focus();}catch(_e){}},0);
}

function closeOnboarding(){
  var ov=document.getElementById('onboardOverlay');
  if(ov){ov.style.display='none';ov.setAttribute('aria-hidden','true');}
  try{localStorage.setItem('anki_fr9_onboarded','1');}catch(_e){}
}

function renderOnboardStep(){
  var box=document.getElementById('onboardBox');
  if(!box)return;
  var total=ONBOARD_STEPS.length;
  onbStep=Math.max(0,Math.min(onbStep,total-1));
  var step=ONBOARD_STEPS[onbStep];
  var current=onbStep+1;
  var pct=Math.round(current/total*100);
  var num=String(current).padStart(2,'0');
  var h='<div class="ob-shell">';
  h+='<div class="ob-topbar">';
  h+='<div class="ob-brand"><span class="ob-brand-mark">A</span><span><strong>دليل المعرض</strong><small>جولة سريعة وتفاعلية</small></span></div>';
  h+='<div class="ob-top-meta"><span class="ob-live-dot"></span><span>خطوة '+num+' من '+String(total).padStart(2,'0')+'</span></div>';
  h+='<button class="ob-close" type="button" onclick="closeOnboarding()" aria-label="إغلاق الجولة">×</button>';
  h+='</div>';
  h+='<div class="ob-main">';
  h+='<div class="ob-visual ob-visual-'+current+'" aria-hidden="true">';
  h+='<div class="ob-orbit ob-orbit-one"></div><div class="ob-orbit ob-orbit-two"></div>';
  h+='<div class="ob-float ob-float-top"><span class="ob-float-dot"></span>'+step.artTag+'</div>';
  h+='<div class="ob-preview-window">';
  h+='<div class="ob-window-bar"><span></span><span></span><span></span><i>ANKI STUDIO</i></div>';
  h+='<div class="ob-preview-content">';
  h+='<div class="ob-preview-icon">'+step.icon+'</div>';
  h+='<strong>'+step.artTitle+'</strong><small>'+step.artMeta+'</small>';
  h+='<div class="ob-preview-lines"><i></i><i></i><i></i></div>';
  h+='</div></div>';
  h+='<div class="ob-float ob-float-bottom"><span>✦</span> تعلّم · اختر · أنشئ</div>';
  h+='<div class="ob-visual-glow"></div>';
  h+='</div>';
  h+='<div class="ob-copy">';
  h+='<div class="ob-eyebrow"><span>ANKI DESIGN STUDIO</span><i></i><span>الدليل التفاعلي</span></div>';
  h+='<div class="ob-step-label">الخطوة '+num+' <span>/ '+String(total).padStart(2,'0')+'</span></div>';
  h+='<h2 class="ob-title">'+step.title+'</h2>';
  h+='<p class="ob-description">'+step.text+'</p>';
  h+='<div class="ob-tip"><span class="ob-tip-icon">✦</span><span><strong>معلومة مفيدة</strong><small>'+step.tip+'</small></span></div>';
  h+='</div>';
  h+='</div>';
  h+='<div class="ob-footer">';
  h+='<div class="ob-progress-meta"><span>تقدّم الجولة</span><strong>'+pct+'%</strong></div>';
  h+='<div class="ob-progress-track"><span style="width:'+pct+'%"></span></div>';
  h+='<div class="ob-footer-actions">';
  if(onbStep>0)h+='<button type="button" class="ob-secondary" onclick="onbStep--;renderOnboardStep()">السابق</button>';
  else h+='<button type="button" class="ob-secondary" onclick="closeOnboarding()">تخطي الجولة</button>';
  if(onbStep<total-1)h+='<button type="button" class="ob-primary" onclick="onbStep++;renderOnboardStep()">التالي <span aria-hidden="true">←</span></button>';
  else h+='<button type="button" class="ob-primary" onclick="closeOnboarding()">ابدأ استخدام المعرض <span aria-hidden="true">✓</span></button>';
  h+='</div></div>';
  h+='</div>';
  box.innerHTML=h;
}"""
    h = h[:start] + onboarding + h[end:]

    old_dialog = '<dialog class="onboard-overlay" id="onboardOverlay" style="display:none">'
    new_dialog = ('<dialog class="onboard-overlay" id="onboardOverlay" role="dialog" '
                  'aria-modal="true" aria-label="الجولة الإرشادية" aria-hidden="true" '
                  'onclick="if(event.target===this)closeOnboarding()" style="display:none">')
    if h.count(old_dialog) != 1:
        raise SystemExit('[%s] onboarding dialog anchor count is not one' % did)
    h = h.replace(old_dialog, new_dialog, 1)

    style = r"""<style id="gallery-ux-polish">
#onboardOverlay.onboard-overlay{position:fixed;inset:0;z-index:99999;display:none;align-items:center;justify-content:center;width:100vw;height:100dvh;max-width:none;max-height:none;margin:0;padding:18px;border:0;background:radial-gradient(ellipse at 15% 10%,rgba(74,222,209,.13),transparent 38%),radial-gradient(ellipse at 85% 90%,rgba(139,92,246,.23),transparent 42%),rgba(5,7,15,.88);backdrop-filter:blur(16px);color:#f8fafc;overflow:auto}
#onboardOverlay::backdrop{background:rgba(5,7,15,.88);backdrop-filter:blur(16px)}
#onboardOverlay .onboard-box{width:min(960px,100%);max-width:960px;max-height:calc(100dvh - 36px);height:auto;padding:0;margin:auto;border:1px solid rgba(167,139,250,.24);border-radius:26px;background:linear-gradient(145deg,#15182a 0%,#101321 55%,#111827 100%);box-shadow:0 32px 100px rgba(0,0,0,.58),0 0 0 1px rgba(255,255,255,.035) inset;overflow:auto;animation:obEnter .38s cubic-bezier(.2,.8,.2,1) both}
@keyframes obEnter{from{opacity:0;transform:translateY(16px) scale(.985)}to{opacity:1;transform:translateY(0) scale(1)}}
#onboardOverlay .ob-shell{--ob-violet:#a78bfa;--ob-cyan:#67e8f9;direction:rtl;min-height:560px;display:flex;flex-direction:column}
#onboardOverlay .ob-topbar{height:76px;min-height:76px;padding:0 30px;display:flex;align-items:center;gap:18px;border-bottom:1px solid rgba(255,255,255,.075);background:rgba(255,255,255,.018)}
#onboardOverlay .ob-brand{display:flex;align-items:center;gap:11px;margin-left:auto}
#onboardOverlay .ob-brand-mark{width:38px;height:38px;display:grid;place-items:center;border-radius:12px;background:linear-gradient(135deg,#8b5cf6,#06b6d4);box-shadow:0 8px 24px rgba(124,58,237,.3);font-size:19px;font-weight:900;color:#fff}
#onboardOverlay .ob-brand strong,#onboardOverlay .ob-brand small{display:block}
#onboardOverlay .ob-brand strong{font-size:14px;color:#f8fafc;font-weight:800}
#onboardOverlay .ob-brand small{font-size:11px;color:#94a3b8;margin-top:3px}
#onboardOverlay .ob-top-meta{display:flex;align-items:center;gap:8px;color:#a5b4c8;font-size:12px}
#onboardOverlay .ob-live-dot{width:7px;height:7px;border-radius:50%;background:#34d399;box-shadow:0 0 0 4px rgba(52,211,153,.12)}
#onboardOverlay .ob-close{width:36px;height:36px;border:1px solid rgba(255,255,255,.1);border-radius:11px;background:rgba(255,255,255,.045);color:#cbd5e1;font-size:23px;line-height:1;cursor:pointer;transition:.2s}
#onboardOverlay .ob-close:hover{background:rgba(248,113,113,.13);border-color:rgba(248,113,113,.35);color:#fecaca}
#onboardOverlay .ob-main{display:grid;grid-template-columns:minmax(0,.94fr) minmax(0,1.06fr);align-items:center;gap:42px;padding:42px 48px 34px;flex:1}
#onboardOverlay .ob-visual{position:relative;min-height:340px;display:grid;place-items:center;isolation:isolate}
#onboardOverlay .ob-visual::before{content:"";position:absolute;width:260px;height:260px;border-radius:50%;background:radial-gradient(circle,rgba(139,92,246,.25),rgba(6,182,212,.08) 55%,transparent 72%);filter:blur(8px);z-index:-2}
#onboardOverlay .ob-orbit{position:absolute;border:1px solid rgba(167,139,250,.17);border-radius:50%;transform:rotate(-22deg)}
#onboardOverlay .ob-orbit-one{width:310px;height:190px}
#onboardOverlay .ob-orbit-two{width:260px;height:310px;transform:rotate(48deg);border-color:rgba(103,232,249,.14)}
#onboardOverlay .ob-preview-window{position:relative;width:min(330px,90%);padding:0 0 22px;border:1px solid rgba(196,181,253,.24);border-radius:19px;background:linear-gradient(155deg,rgba(36,39,64,.96),rgba(19,24,42,.97));box-shadow:0 28px 65px rgba(0,0,0,.4),0 0 45px rgba(139,92,246,.12);transform:rotate(-3deg);overflow:hidden}
#onboardOverlay .ob-window-bar{height:38px;padding:0 14px;display:flex;align-items:center;gap:6px;border-bottom:1px solid rgba(255,255,255,.07);background:rgba(255,255,255,.035)}
#onboardOverlay .ob-window-bar>span{width:7px;height:7px;border-radius:50%;background:#64748b}
#onboardOverlay .ob-window-bar>span:first-child{background:#fb7185}
#onboardOverlay .ob-window-bar>span:nth-child(2){background:#fbbf24}
#onboardOverlay .ob-window-bar>span:nth-child(3){background:#34d399}
#onboardOverlay .ob-window-bar i{margin-right:auto;font-style:normal;font-size:9px;letter-spacing:2px;color:#64748b;font-weight:800}
#onboardOverlay .ob-preview-content{min-height:230px;padding:27px 22px 18px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center}
#onboardOverlay .ob-preview-icon{width:66px;height:66px;display:grid;place-items:center;border-radius:20px;background:linear-gradient(135deg,rgba(139,92,246,.24),rgba(6,182,212,.17));border:1px solid rgba(196,181,253,.22);font-size:32px;margin-bottom:18px;box-shadow:0 12px 28px rgba(0,0,0,.2)}
#onboardOverlay .ob-preview-content strong{font-size:19px;line-height:1.5;color:#f8fafc}
#onboardOverlay .ob-preview-content small{margin-top:7px;font-size:12px;line-height:1.6;color:#9caec5}
#onboardOverlay .ob-preview-lines{width:72%;display:grid;gap:7px;margin-top:22px}
#onboardOverlay .ob-preview-lines i{height:5px;border-radius:8px;background:linear-gradient(90deg,rgba(167,139,250,.4),rgba(103,232,249,.12))}
#onboardOverlay .ob-preview-lines i:nth-child(2){width:78%;margin:auto}
#onboardOverlay .ob-preview-lines i:nth-child(3){width:54%;margin:auto}
#onboardOverlay .ob-float{position:absolute;z-index:2;padding:10px 14px;border:1px solid rgba(255,255,255,.12);border-radius:12px;background:rgba(24,29,49,.88);box-shadow:0 12px 30px rgba(0,0,0,.25);color:#dbeafe;font-size:11px;backdrop-filter:blur(10px)}
#onboardOverlay .ob-float-top{top:28px;right:2px}
#onboardOverlay .ob-float-bottom{bottom:26px;left:0;color:#c4b5fd}
#onboardOverlay .ob-float-bottom span{color:#67e8f9;margin-left:5px}
#onboardOverlay .ob-float-dot{display:inline-block;width:6px;height:6px;border-radius:50%;background:#34d399;margin-left:7px}
#onboardOverlay .ob-visual-glow{position:absolute;bottom:7%;width:200px;height:18px;border-radius:50%;background:rgba(139,92,246,.3);filter:blur(24px);z-index:-1}
#onboardOverlay .ob-copy{max-width:470px}
#onboardOverlay .ob-eyebrow{display:flex;align-items:center;gap:10px;color:#8fa2bb;font-size:10px;font-weight:800;letter-spacing:1.3px;margin-bottom:23px}
#onboardOverlay .ob-eyebrow span:first-child{color:#a78bfa}
#onboardOverlay .ob-eyebrow i{width:22px;height:1px;background:rgba(167,139,250,.45)}
#onboardOverlay .ob-step-label{font-size:12px;font-weight:800;color:#67e8f9;margin-bottom:10px}
#onboardOverlay .ob-step-label span{color:#64748b;font-weight:500}
#onboardOverlay .ob-title{font-family:var(--font-head);font-size:clamp(25px,3vw,35px);font-weight:900;line-height:1.5;color:#f8fafc;margin:0 0 13px;background:none;-webkit-text-fill-color:initial}
#onboardOverlay .ob-description{font-size:15px;line-height:2;color:#b7c3d5;margin:0;max-width:450px}
#onboardOverlay .ob-tip{display:flex;align-items:flex-start;gap:12px;margin-top:25px;padding:14px 15px;border:1px solid rgba(103,232,249,.15);border-radius:14px;background:linear-gradient(110deg,rgba(103,232,249,.055),rgba(167,139,250,.07))}
#onboardOverlay .ob-tip-icon{width:25px;height:25px;flex:0 0 25px;display:grid;place-items:center;border-radius:8px;background:rgba(103,232,249,.12);color:#67e8f9}
#onboardOverlay .ob-tip strong,#onboardOverlay .ob-tip small{display:block}
#onboardOverlay .ob-tip strong{font-size:11px;color:#67e8f9;margin-bottom:5px}
#onboardOverlay .ob-tip small{font-size:12px;line-height:1.8;color:#aebbd0}
#onboardOverlay .ob-footer{padding:0 48px 30px}
#onboardOverlay .ob-progress-meta{display:flex;justify-content:space-between;align-items:center;margin-bottom:9px;color:#8392a9;font-size:11px}
#onboardOverlay .ob-progress-meta strong{color:#c4b5fd;font-size:12px}
#onboardOverlay .ob-progress-track{height:5px;border-radius:9px;background:rgba(255,255,255,.08);overflow:hidden}
#onboardOverlay .ob-progress-track span{display:block;height:100%;border-radius:inherit;background:linear-gradient(90deg,#8b5cf6,#22d3ee);box-shadow:0 0 16px rgba(34,211,238,.28);transition:width .3s ease}
#onboardOverlay .ob-footer-actions{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-top:22px}
#onboardOverlay .ob-primary,#onboardOverlay .ob-secondary{min-height:45px;padding:0 22px;border-radius:12px;font-family:inherit;font-size:13px;font-weight:800;cursor:pointer;transition:transform .18s,box-shadow .18s,border-color .18s}
#onboardOverlay .ob-primary{border:1px solid transparent;background:linear-gradient(110deg,#8b5cf6,#6d5dfc 55%,#0891b2);color:white;box-shadow:0 9px 24px rgba(109,93,252,.25)}
#onboardOverlay .ob-primary:hover{transform:translateY(-2px);box-shadow:0 13px 30px rgba(109,93,252,.38)}
#onboardOverlay .ob-secondary{border:1px solid rgba(255,255,255,.13);background:rgba(255,255,255,.035);color:#c1ccdc}
#onboardOverlay .ob-secondary:hover{border-color:rgba(167,139,250,.45);background:rgba(167,139,250,.08)}
#onboardOverlay .ob-primary:focus-visible,#onboardOverlay .ob-secondary:focus-visible,#onboardOverlay .ob-close:focus-visible{outline:2px solid #67e8f9;outline-offset:3px}
@media(max-width:760px){
 #onboardOverlay.onboard-overlay{padding:9px}
 #onboardOverlay .onboard-box{max-height:calc(100dvh - 18px);border-radius:20px}
 #onboardOverlay .ob-shell{min-height:0}
 #onboardOverlay .ob-topbar{height:64px;min-height:64px;padding:0 16px;gap:9px}
 #onboardOverlay .ob-brand-mark{width:33px;height:33px;border-radius:10px}
 #onboardOverlay .ob-top-meta{font-size:10px}
 #onboardOverlay .ob-main{grid-template-columns:1fr;gap:16px;padding:18px 20px 18px}
 #onboardOverlay .ob-visual{min-height:190px;max-height:190px}
 #onboardOverlay .ob-visual::before{width:180px;height:180px}
 #onboardOverlay .ob-orbit-one{width:230px;height:140px}
 #onboardOverlay .ob-orbit-two{width:190px;height:220px}
 #onboardOverlay .ob-preview-window{width:min(270px,78%);padding-bottom:12px}
 #onboardOverlay .ob-window-bar{height:28px}
 #onboardOverlay .ob-preview-content{min-height:130px;padding:12px 14px}
 #onboardOverlay .ob-preview-icon{width:42px;height:42px;border-radius:13px;font-size:22px;margin-bottom:8px}
 #onboardOverlay .ob-preview-content strong{font-size:14px}
 #onboardOverlay .ob-preview-content small{font-size:10px;margin-top:3px}
 #onboardOverlay .ob-preview-lines{margin-top:10px;gap:4px}
 #onboardOverlay .ob-float{padding:7px 10px;font-size:9px}
 #onboardOverlay .ob-float-top{top:4px;right:0}
 #onboardOverlay .ob-float-bottom{bottom:0;left:0}
 #onboardOverlay .ob-copy{max-width:none}
 #onboardOverlay .ob-eyebrow{margin-bottom:10px;font-size:8px}
 #onboardOverlay .ob-step-label{margin-bottom:4px}
 #onboardOverlay .ob-title{font-size:23px;margin-bottom:7px}
 #onboardOverlay .ob-description{font-size:12px;line-height:1.8}
 #onboardOverlay .ob-tip{margin-top:12px;padding:10px 11px}
 #onboardOverlay .ob-tip small{font-size:10px;line-height:1.65}
 #onboardOverlay .ob-footer{padding:0 20px 18px}
 #onboardOverlay .ob-footer-actions{margin-top:14px}
 #onboardOverlay .ob-primary,#onboardOverlay .ob-secondary{min-height:42px;padding:0 16px;font-size:12px}
}
@media(max-width:380px){
 #onboardOverlay .ob-main{padding:13px 14px}
 #onboardOverlay .ob-visual{min-height:155px;max-height:155px}
 #onboardOverlay .ob-preview-content{min-height:105px}
 #onboardOverlay .ob-title{font-size:20px}
 #onboardOverlay .ob-footer{padding:0 14px 14px}
}
@media(prefers-reduced-motion:reduce){
 #onboardOverlay .onboard-box,#onboardOverlay .ob-progress-track span{animation:none;transition:none}
}
</style>"""
    h2, inserted = re.subn(r'</head\s*>', style + '\n</head>', h, count=1, flags=re.IGNORECASE)
    if inserted != 1:
        raise SystemExit('[%s] could not install responsive onboarding styles' % did)
    return h2


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
    h = apply_gallery_ux(h, did)
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
