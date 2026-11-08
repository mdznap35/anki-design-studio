"""ENSCI welcome and preview polish, layered over the proven v6 page.

Only adds or clarifies content. It deliberately preserves the original
100-design payload, all original gallery/filter controls, onboarding logic,
template selection, export flow, and dark-first theme.
"""
import re

from gallery_experience import WELCOME_MARKUP


WELCOME_CSS = r"""
/* English Science: refined dark-first welcome and preview introduction. */
#gxWelcome .gx-opening-v3{
  border-color:rgba(159,177,230,.30)!important;
  background:
    radial-gradient(ellipse at 84% 5%,rgba(111,91,238,.25),transparent 42%),
    radial-gradient(ellipse at 8% 92%,rgba(29,174,190,.12),transparent 36%),
    linear-gradient(142deg,#17213b 0%,#101a31 54%,#0a1428 100%)!important;
}
#gxWelcome .gx-opening-v3 .gx-kicker{
  color:#d1d8ff!important;
  letter-spacing:.015em!important;
}
#gxWelcome .gx-opening-v3 .gx-deck-label{
  border-color:rgba(143,181,214,.25)!important;
  background:rgba(12,23,43,.54)!important;
  color:#cad7f0!important;
}
#gxWelcome .gx-opening-v3 h2{
  max-width:660px!important;
  font-size:clamp(1.9rem,3.4vw,2.75rem)!important;
  line-height:1.38!important;
}
#gxWelcome .gx-opening-v3 .gx-lead{
  max-width:670px!important;
  color:#d1d9e9!important;
  font-size:.97rem!important;
  line-height:2.08!important;
}
#gxWelcome .gx-opening-v3 .gx-point{
  min-height:118px!important;
  border-color:rgba(157,181,220,.19)!important;
  background:linear-gradient(150deg,rgba(255,255,255,.065),rgba(255,255,255,.025))!important;
}
#gxWelcome .gx-opening-v3 .gx-point strong{color:#f4f6ff!important}
#gxWelcome .gx-opening-v3 .gx-point span:not(.gx-point-no){color:#b5c2d8!important}
#gxWelcome .gx-opening-v3 .gx-button{
  min-height:52px!important;
  padding-inline:21px!important;
  border-radius:15px!important;
  font-size:.85rem!important;
}
#gxWelcome .gx-opening-v3 .gx-button.primary{
  background:linear-gradient(112deg,#725ee7,#536dde 58%,#087f91)!important;
  box-shadow:0 13px 31px rgba(70,76,189,.31),inset 0 1px 0 rgba(255,255,255,.13)!important;
}
#gxWelcome .gx-opening-v3 .gx-button:not(.primary){
  border-color:rgba(164,184,222,.27)!important;
  background:rgba(255,255,255,.055)!important;
}
#gxWelcome .gx-opening-v3 .gx-small{
  color:#a9b8d0!important;
  line-height:1.9!important;
}
#gxWelcome .gx-opening-v3 .gx-stage{
  background:
    radial-gradient(ellipse at 52% 42%,rgba(105,94,232,.20),transparent 58%),
    linear-gradient(160deg,rgba(255,255,255,.035),rgba(3,10,24,.16))!important;
}
#gxWelcome .gx-opening-v3 .gx-card.front{
  border-color:rgba(155,161,255,.70)!important;
  box-shadow:0 28px 68px rgba(0,0,0,.45),0 0 38px rgba(110,101,237,.12)!important;
}
#gxWelcome .gx-opening-v3 .gx-stage-label{
  border-color:rgba(156,184,225,.26)!important;
  background:rgba(8,16,32,.88)!important;
  color:#c8d4e9!important;
}

/* Individual preview: add context without replacing its working controls. */
#ensci-preview-guide{
  display:flex;
  align-items:flex-end;
  justify-content:space-between;
  gap:24px;
  max-width:1360px;
  margin:clamp(28px,4vw,48px) auto 15px;
  padding:0 clamp(14px,2vw,26px);
  direction:rtl;
}
#ensci-preview-guide .ensci-preview-copy{max-width:760px}
#ensci-preview-guide .ensci-preview-kicker{
  display:inline-flex;align-items:center;gap:8px;
  color:#aeb7ff;font-size:.72rem;font-weight:950;letter-spacing:.03em;
}
#ensci-preview-guide .ensci-preview-kicker:before{
  content:"";width:21px;height:2px;border-radius:8px;
  background:linear-gradient(90deg,#8b7cff,#58d6e7);
}
#ensci-preview-guide h2{
  margin:9px 0 7px;color:#f3f5ff;
  font-size:clamp(1.25rem,2.2vw,1.8rem);
  line-height:1.45;font-weight:950;letter-spacing:-.025em;
}
#ensci-preview-guide p{
  margin:0;color:#aebbd2;font-size:.88rem;line-height:1.9;
}
#ensci-preview-guide .ensci-preview-actions{
  display:flex;flex-wrap:wrap;justify-content:flex-start;gap:8px;
}
#ensci-preview-guide .ensci-preview-action{
  display:inline-flex;align-items:center;gap:7px;
  padding:9px 12px;border:1px solid rgba(163,182,220,.19);
  border-radius:12px;background:rgba(255,255,255,.035);
  color:#cbd5e8;font-size:.72rem;font-weight:850;white-space:nowrap;
}
#ensci-preview-guide .ensci-preview-action b{
  color:#82dbe8;font-size:.67rem;font-variant-numeric:tabular-nums;
}
#gv{scroll-margin-top:20px}
/* Mobile gallery header: keep all original category chips in a horizontal scroll row. */
@media(max-width:640px){
  #galleryBrowser .gb-head{
    display:grid!important;
    grid-template-columns:minmax(0,1fr) auto;
    grid-template-areas:"title count" "tools tools";
    align-items:center;
    gap:10px;
    padding:12px 68px 12px 14px!important;
  }
  #galleryBrowser .gb-title{grid-area:title;min-width:0;white-space:normal;font-size:1rem}
  #galleryBrowser .gb-count{grid-area:count;justify-self:end;font-size:.72rem;padding:5px 9px}
  #galleryBrowser .gb-tools{
    grid-area:tools;
    display:flex!important;
    flex-wrap:nowrap!important;
    align-items:center;
    width:100%!important;
    max-width:none!important;
    min-width:0;
    margin:0!important;
    overflow-x:auto!important;
    overflow-y:hidden;
    padding:1px 0 5px;
    -webkit-overflow-scrolling:touch;
  }
  #galleryBrowser .gb-chip{flex:0 0 auto;min-height:38px;white-space:nowrap}
  #galleryBrowser .gb-close{top:12px;left:12px;width:42px;height:42px}
  #galleryBrowser .gb-bar{padding:8px 14px}
  #galleryBrowser .gb-hint{font-size:.68rem;line-height:1.7}
}
@media(max-width:820px){
  #gxWelcome .gx-opening-v3 .gx-dialog{grid-template-columns:1fr}
  #gxWelcome .gx-opening-v3 .gx-points{grid-template-columns:1fr}
  #gxWelcome .gx-opening-v3 .gx-point{min-height:0}
  #ensci-preview-guide{display:block;margin:16px auto 18px;padding:0 14px}
  #ensci-preview-guide .ensci-preview-actions{margin-top:13px}
}
@media(max-width:520px){
  #gxWelcome .gx-opening-v3 h2{font-size:1.72rem!important}
  #gxWelcome .gx-opening-v3 .gx-stage{min-height:220px!important}
  #gxWelcome .gx-opening-v3 .gx-copy{padding:18px 17px 24px!important}
  #gxWelcome .gx-opening-v3 .gx-actions{display:grid!important;grid-template-columns:1fr!important}
  #gxWelcome .gx-opening-v3 .gx-button{width:100%!important}
  #ensci-preview-guide{padding:0 12px}
  #ensci-preview-guide .ensci-preview-actions{display:grid;grid-template-columns:1fr}
  #ensci-preview-guide .ensci-preview-action{white-space:normal}
}
"""


PREVIEW_GUIDE_JS = r"""
(function(){
  "use strict";
  function addPreviewGuide(){
    var gallery=document.getElementById("gv");
    if(!gallery||document.getElementById("ensci-preview-guide"))return;
    var guide=document.createElement("section");
    guide.id="ensci-preview-guide";
    guide.setAttribute("aria-labelledby","ensci-preview-guide-title");
    guide.setAttribute("role","note");
    guide.innerHTML=
      '<div class="ensci-preview-copy">'+
        '<span class="ensci-preview-kicker">معاينة القالب الفردية</span>'+
        '<h2 id="ensci-preview-guide-title">افحص البطاقة قبل اعتماد التصميم</h2>'+
        '<p>تنقّل بين القوالب، واقلب البطاقة لرؤية الوجه الآخر، ثم حدّد التصميم الذي تريد إضافته إلى رُزمتك.</p>'+
      '</div>'+
      '<div class="ensci-preview-actions" aria-label="طريقة استخدام المعاينة">'+
        '<span class="ensci-preview-action"><b>01</b> السابق والتالي للتنقّل</span>'+
        '<span class="ensci-preview-action"><b>02</b> اقلب البطاقة لمشاهدة الوجهين</span>'+
        '<span class="ensci-preview-action"><b>03</b> حدّد القالب الذي يناسبك</span>'+
      '</div>';
    gallery.insertBefore(guide,gallery.firstElementChild);
  }
  if(document.readyState==="loading"){
    document.addEventListener("DOMContentLoaded",addPreviewGuide,{once:true});
  }else{
    addPreviewGuide();
  }
})();
"""


def _replace_once(source, old, new, label):
    count = source.count(old)
    if count != 1:
        raise SystemExit("%s: expected one exact occurrence, found %d" % (label, count))
    return source.replace(old, new, 1)


def _refine_welcome_markup():
    markup = WELCOME_MARKUP
    swaps = (
        (
            '<div class="gx-point"><span class="gx-point-no">01</span><div class="gx-point-copy"><strong>استكشف 100 تصميماً</strong><span>ابحث وصفِّ القوالب حتى تصل إلى ما يناسبك.</span></div></div>',
            '<div class="gx-point"><span class="gx-point-no">01</span><div class="gx-point-copy"><strong>استكشف القوالب</strong><span>استخدم التصنيفات للوصول إلى التصميم الذي تفضّله.</span></div></div>',
            "welcome step one",
        ),
        (
            '<div class="gx-point"><span class="gx-point-no">02</span><div class="gx-point-copy"><strong>عاين الوجهين</strong><span>افحص شكل البطاقة قبل اعتماد أي تصميم.</span></div></div>',
            '<div class="gx-point"><span class="gx-point-no">02</span><div class="gx-point-copy"><strong>عاين البطاقة</strong><span>شاهد الكلمة ومعناها، ثم اقلب البطاقة لفحص الوجهين.</span></div></div>',
            "welcome step two",
        ),
        (
            '<div class="gx-point"><span class="gx-point-no">03</span><div class="gx-point-copy"><strong>حدّد ثم راجع</strong><span>اختر قوالبك، واضبط الصوت، وراجع الرزمة قبل إنشائها.</span></div></div>',
            '<div class="gx-point"><span class="gx-point-no">03</span><div class="gx-point-copy"><strong>كوّن رُزمتك</strong><span>حدّد ما تريد، واضبط الصوت، وراجع التصدير قبل الإنشاء.</span></div></div>',
            "welcome step three",
        ),
        (
            '<button class="gx-button primary" id="gxWelcomeStart" type="button">ابدأ الجولة التفاعلية <span aria-hidden="true">←</span></button>\n        <button class="gx-button" id="gxWelcomeExplore" type="button">تصفّح القوالب</button>',
            '<button class="gx-button primary" id="gxWelcomeExplore" type="button">تصفّح القوالب الـ100 <span aria-hidden="true">←</span></button>\n        <button class="gx-button" id="gxWelcomeStart" type="button">شاهد الجولة التفاعلية</button>',
            "welcome action hierarchy",
        ),
        (
            'تصفّح بحرية. لا يُحدَّد أي قالب ولا تُنشأ أي رزمة تلقائياً؛ كل خطوة تنفيذية تبدأ باختيارك.',
            'جرّب المعرض بحرية. لا يُعتمد أي قالب ولا تُنشأ رُزمتك إلا باختيارك.',
            "welcome reassurance",
        ),
    )
    for old, new, label in swaps:
        markup = _replace_once(markup, old, new, label)
    return markup


def apply_ensci_welcome(html):
    """Clarify the first visit and individual preview without removing anything."""
    required = (
        'id="gallery-experience-hero"',
        'id="gallery-experience-runtime"',
        'id="gxWelcome"',
        'id="gxWelcomeStart"',
        'id="gxWelcomeExplore"',
        'id="gbFilters"',
        'id="gbGrid"',
        'id="gvStage"',
        'id="gvSelectBtn"',
        'class="gb-preview-frame"',
        "var previewSource=thumbDoc(t)",
    )
    for token in required:
        if token not in html:
            raise SystemExit("ENSCI welcome: required original v6 feature is missing: " + token)

    profile_swaps = (
        (
            'title:"اختر تصميم Anki المناسب لمفردات الإنجليزية — بكالوريا علمي 12"',
            'title:"اختر شكل بطاقة Anki الذي يناسب طريقة مراجعتك."',
            "hero title",
        ),
        (
            'description:"100 تصميم لبطاقات مفردات اللغة الإنجليزية المخصّصة لبكالوريا علمي 12. قارن وضوح الكلمة ومعناها، وافحص القالب قبل اعتماده."',
            'description:"معرض تفاعلي يضم 100 قالب فعلي لمفردات الإنجليزية — بكالوريا علمي 12. عاين الكلمة ومعناها ووجهي البطاقة، ثم اختر التصميم الذي تريده في رُزمتك."',
            "hero description",
        ),
        (
            'welcomeTitle:"اجعل مراجعة مفردات الإنجليزية أوضح وأسهل."',
            'welcomeTitle:"اختر قالب Anki قبل أن تبني رُزمتك."',
            "welcome title",
        ),
        (
            'welcomeLead:"هذا المعرض مخصّص للغة الإنجليزية — بكالوريا علمي 12. أمامك 100 قالب؛ افتح أي قالب لمعاينة وجهَي البطاقة، ثم حدّد ما يناسبك وراجع إعداداتك قبل إنشاء الرزمة."',
            'welcomeLead:"يضم المعرض 100 قالب فعلي لمفردات الإنجليزية — بكالوريا علمي 12. افتح أي تصميم لتشاهد الكلمة ومعناها كما سيظهران في البطاقة، ثم اختر القوالب التي تريدها واضبط الصوت قبل إنشاء الرزمة."',
            "welcome lead",
        ),
    )
    for old, new, label in profile_swaps:
        html = _replace_once(html, old, new, label)

    original_welcome = html.count(WELCOME_MARKUP)
    if original_welcome != 1:
        raise SystemExit("ENSCI welcome: expected exactly one original welcome layer, found %d" % original_welcome)
    html = html.replace(WELCOME_MARKUP, _refine_welcome_markup(), 1)

    style_tag = '<style id="ensci-welcome-polish">\n' + WELCOME_CSS + '\n</style>\n'
    html, style_count = re.subn(r"</head\s*>", style_tag + "</head>", html, count=1, flags=re.I)
    if style_count != 1:
        raise SystemExit("ENSCI welcome: unable to add the additive dark-first polish stylesheet")

    script_tag = '<script id="ensci-preview-guide-runtime">\n' + PREVIEW_GUIDE_JS + '\n</script>\n'
    body_closers = list(re.finditer(r"</body\s*>", html, flags=re.I))
    if not body_closers:
        raise SystemExit("ENSCI welcome: missing final body close")
    body_close = body_closers[-1]
    html = html[:body_close.start()] + script_tag + html[body_close.start():]

    required_after = (
        'id="ensci-welcome-polish"',
        'id="ensci-preview-guide-runtime"',
        'id="ensci-preview-guide"',
        'id="gxWelcomeExplore"',
        'id="gxWelcomeStart"',
        'id="gbFilters"',
        'id="gbGrid"',
        'id="gvStage"',
        'id="gvSelectBtn"',
        'id="gvShowAns"',
        'class="gb-preview-frame"',
    )
    for token in required_after:
        # The preview guide itself is inserted at runtime, so its ID belongs in JS.
        if token == 'id="ensci-preview-guide"' and token not in html:
            continue
        if token not in html:
            raise SystemExit("ENSCI welcome: expected feature missing after enhancement: " + token)

    for forbidden in (
        'id="onboardOverlay"',
        'id="gxWelcome"',
        'id="gbFilters"',
        'id="gbGrid"',
    ):
        if html.count(forbidden) != 1:
            raise SystemExit("ENSCI welcome: original feature was removed or duplicated: " + forbidden)

    return html
