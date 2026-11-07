"""A polished, lightweight design layer for the four generated non-Bac galleries."""
import re


EXPERIENCE_CSS = r"""
:root{
  --gx-ink:#f5f7ff;--gx-muted:#a9b3c9;--gx-line:rgba(174,190,222,.16);
  --gx-panel:rgba(15,22,40,.82);--gx-violet:#8b7cff;--gx-cyan:#58d6e7;
}
body{
  background:
    radial-gradient(ellipse at 6% 2%,rgba(90,76,210,.14),transparent 34%),
    radial-gradient(ellipse at 96% 18%,rgba(26,155,178,.10),transparent 30%),
    var(--bg,#0b1020);
}
#gallery-experience-hero{
  position:relative;isolation:isolate;overflow:hidden;margin:clamp(16px,3vw,34px) 0 22px;
  padding:clamp(22px,4vw,48px);border:1px solid var(--gx-line);border-radius:30px;
  background:
    radial-gradient(ellipse at 82% 12%,rgba(94,82,224,.25),transparent 38%),
    radial-gradient(ellipse at 12% 90%,rgba(28,171,185,.13),transparent 32%),
    linear-gradient(135deg,rgba(19,27,49,.98),rgba(11,17,33,.96));
  box-shadow:0 28px 80px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.055);
}
#gallery-experience-hero:before{
  content:"";position:absolute;inset:0;z-index:-1;opacity:.19;pointer-events:none;
  background-image:linear-gradient(rgba(177,190,225,.10) 1px,transparent 1px),linear-gradient(90deg,rgba(177,190,225,.10) 1px,transparent 1px);
  background-size:34px 34px;mask-image:linear-gradient(120deg,#000,transparent 72%);
}
#gallery-experience-hero .gx-hero-inner{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(250px,.85fr);align-items:center;gap:clamp(20px,4vw,56px);max-width:1320px;margin:auto}
#gallery-experience-hero .gx-eyebrow{display:inline-flex;align-items:center;gap:9px;margin-bottom:16px;color:#a5b4fc;font-size:.7rem;font-weight:900;letter-spacing:.14em}
#gallery-experience-hero .gx-eyebrow:before{content:"";width:26px;height:2px;border-radius:9px;background:linear-gradient(90deg,var(--gx-violet),var(--gx-cyan))}
#gallery-experience-hero h1{max-width:760px;margin:0 0 14px;color:var(--gx-ink);font-size:clamp(1.65rem,4vw,3.05rem);line-height:1.28;font-weight:950;letter-spacing:-.035em}
#gallery-experience-hero .gx-description{max-width:690px;margin:0;color:#c4cde0;font-size:clamp(.9rem,1.4vw,1.04rem);line-height:2}
#gallery-experience-hero .gx-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:25px}
#gallery-experience-hero .gx-action{min-height:48px;display:inline-flex;align-items:center;justify-content:center;gap:9px;padding:0 19px;border:1px solid rgba(183,193,221,.2);border-radius:14px;background:rgba(255,255,255,.055);color:#edf2ff;font:inherit;font-size:.83rem;font-weight:850;cursor:pointer;transition:transform .2s,border-color .2s,background .2s}
#gallery-experience-hero .gx-action:hover{transform:translateY(-2px);border-color:rgba(122,211,235,.5);background:rgba(255,255,255,.09)}
#gallery-experience-hero .gx-action.primary{border-color:transparent;background:linear-gradient(110deg,#6754d8,#4b65d5 56%,#087e91);box-shadow:0 12px 28px rgba(76,78,195,.28)}
#gallery-experience-hero .gx-metrics{display:flex;flex-wrap:wrap;gap:10px;margin-top:25px}
#gallery-experience-hero .gx-metric{min-width:118px;padding:11px 14px;border:1px solid rgba(178,193,224,.13);border-radius:14px;background:rgba(255,255,255,.035)}
#gallery-experience-hero .gx-metric strong{display:block;color:#f8fbff;font-size:1.15rem;font-weight:950}
#gallery-experience-hero .gx-metric span{display:block;margin-top:3px;color:#9faec8;font-size:.68rem;font-weight:750}
#gallery-experience-hero .gx-art{position:relative;min-height:260px;display:grid;place-items:center;direction:ltr}
#gallery-experience-hero .gx-art-glow{position:absolute;width:74%;aspect-ratio:1;border-radius:50%;background:radial-gradient(circle,rgba(100,90,236,.28),rgba(42,190,204,.10) 48%,transparent 72%);filter:blur(8px)}
#gallery-experience-hero .gx-art-card{position:absolute;width:min(74%,270px);min-height:176px;padding:20px;border:1px solid rgba(203,213,240,.24);border-radius:22px;background:linear-gradient(145deg,rgba(35,46,76,.96),rgba(14,23,42,.98));box-shadow:0 30px 70px rgba(0,0,0,.32);display:flex;flex-direction:column;justify-content:space-between}
#gallery-experience-hero .gx-art-card.back{transform:translate(-26px,18px) rotate(-9deg);opacity:.52}
#gallery-experience-hero .gx-art-card.mid{transform:translate(18px,7px) rotate(6deg);opacity:.78}
#gallery-experience-hero .gx-art-card.front{transform:translate(0,-4px);border-color:rgba(135,130,255,.55);background:radial-gradient(ellipse at 100% 0,rgba(98,91,224,.22),transparent 55%),linear-gradient(145deg,#202b4b,#111a30)}
#gallery-experience-hero .gx-art-kicker{color:#a6b5ff;font-size:.62rem;font-weight:950;letter-spacing:.16em}
#gallery-experience-hero .gx-art-word{color:#fff;font-size:clamp(1.6rem,3vw,2.35rem);font-weight:950;letter-spacing:-.04em}
#gallery-experience-hero .gx-art-note{color:#aebbd2;font-size:.72rem}
#gbFilters{
  position:relative;z-index:2;display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  padding:clamp(12px,2vw,18px);border:1px solid var(--gx-line);border-radius:20px;
  background:rgba(17,25,44,.82);box-shadow:0 14px 38px rgba(0,0,0,.14);
  backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);
}
#gbFilters input,#gbFilters select,#gbFilters button{
  min-height:42px;border-radius:12px;transition:border-color .18s,box-shadow .18s,background .18s;
}
#gbFilters input:focus-visible,#gbFilters select:focus-visible,#gbFilters button:focus-visible{
  outline:3px solid rgba(88,214,231,.6);outline-offset:2px;
}
#gbGrid{
  display:grid!important;grid-template-columns:repeat(auto-fill,minmax(min(100%,245px),1fr));
  align-items:stretch;gap:clamp(13px,1.8vw,22px);margin-top:18px;
}
#gbGrid .gb-item{
  min-width:0;overflow:hidden;border:1px solid rgba(160,177,211,.17)!important;
  border-radius:20px!important;background:linear-gradient(155deg,rgba(27,38,63,.96),rgba(14,22,39,.98))!important;
  box-shadow:0 12px 30px rgba(0,0,0,.16)!important;
  transition:transform .22s ease,border-color .22s ease,box-shadow .22s ease!important;
}
#gbGrid .gb-item:hover{
  transform:translateY(-5px);border-color:rgba(133,139,255,.55)!important;
  box-shadow:0 22px 44px rgba(0,0,0,.25),0 0 0 1px rgba(133,139,255,.10)!important;
}
#gbGrid .gb-item:focus-visible{outline:3px solid rgba(88,214,231,.75);outline-offset:3px}
#gbGrid .gb-item[data-gx-active="true"]{border-color:rgba(88,214,231,.82)!important;box-shadow:0 0 0 2px rgba(88,214,231,.16),0 18px 38px rgba(0,0,0,.22)!important}
#gbGrid .gb-item img{max-width:100%;height:auto;object-fit:contain}
#gbGrid .gb-preview-frame{
  display:block;position:relative;z-index:0;width:100%;height:auto;aspect-ratio:22/45;
  min-height:180px;border:0;background:#0e0c16;pointer-events:none;
}
#gbGrid .gb-fallback-img{
  display:none;position:absolute;inset:0;z-index:1;width:100%;height:100%;
  object-fit:contain;background:#0e0c16;
}
#gbGrid .gb-fallback-img[data-show="true"]{display:block}
#gvStage{
  overflow:hidden;border:1px solid rgba(165,181,215,.22)!important;border-radius:26px!important;
  background:radial-gradient(ellipse at 50% 0,rgba(104,92,220,.11),transparent 48%),rgba(13,21,38,.94)!important;
  box-shadow:0 24px 65px rgba(0,0,0,.22)!important;
}
#gvSelectBtn,#exOpenBtn,#gTtsPreviewBtn{
  min-height:46px!important;padding-inline:18px!important;border-radius:13px!important;
  font-weight:850!important;transition:transform .18s,filter .18s,box-shadow .18s!important;
}
#gvSelectBtn:hover,#exOpenBtn:hover,#gTtsPreviewBtn:hover{transform:translateY(-2px);filter:brightness(1.08)}
#exportOverlay{backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}
#onboardTourLauncher{
  min-height:49px!important;padding-inline:18px!important;border-radius:16px!important;
  background:linear-gradient(115deg,#6855d9,#4e66d9 58%,#087f91)!important;
  box-shadow:0 14px 34px rgba(51,53,142,.38),0 0 0 1px rgba(255,255,255,.09) inset!important;
}
#onboardGuideRoot .og-card{
  border:1px solid rgba(159,173,221,.28)!important;border-radius:24px!important;
  background:radial-gradient(ellipse at 90% 0,rgba(110,97,231,.15),transparent 48%),linear-gradient(150deg,rgba(17,25,46,.99),rgba(8,14,28,.99))!important;
  box-shadow:0 30px 90px rgba(0,0,0,.54),0 0 0 1px rgba(255,255,255,.035) inset,0 0 48px rgba(91,93,222,.10)!important;
}
#onboardGuideRoot .og-title{font-size:clamp(1.08rem,2vw,1.35rem);line-height:1.55;letter-spacing:-.02em}
#onboardGuideRoot .og-progress button span{height:6px;border-radius:20px}
#onboardGuideRoot .og-btn{min-height:42px;border-radius:12px}
.gx-lock{overflow:hidden!important}
#gxWelcome[hidden]{display:none!important}
#gxWelcome{
  position:fixed;inset:0;z-index:2147483100;display:grid;place-items:center;
  padding:clamp(10px,2vw,24px);background:rgba(4,8,19,.84);
  backdrop-filter:blur(22px);-webkit-backdrop-filter:blur(22px);direction:rtl;
}
#gxWelcome .gx-dialog{
  position:relative;isolation:isolate;display:grid;grid-template-columns:minmax(0,1fr) minmax(310px,.9fr);
  width:min(1120px,100%);max-height:min(900px,94dvh);overflow:auto;
  border:1px solid rgba(172,185,225,.24);border-radius:30px;
  background:radial-gradient(ellipse at 80% 0,rgba(98,91,220,.20),transparent 44%),linear-gradient(140deg,#141d35,#0a1223 72%);
  box-shadow:0 40px 130px rgba(0,0,0,.65),0 0 0 1px rgba(255,255,255,.04) inset;
}
#gxWelcome .gx-close{
  position:absolute;top:16px;left:16px;z-index:3;width:42px;height:42px;display:grid;place-items:center;
  border:1px solid rgba(202,214,242,.18);border-radius:13px;background:rgba(255,255,255,.055);
  color:#e9eeff;font-size:1.25rem;cursor:pointer;
}
#gxWelcome .gx-copy{position:relative;z-index:2;display:flex;flex-direction:column;justify-content:center;padding:clamp(26px,5vw,62px)}
#gxWelcome .gx-kicker{display:inline-flex;align-items:center;gap:9px;color:#a8b5ff;font-size:.68rem;font-weight:950;letter-spacing:.13em}
#gxWelcome .gx-kicker:before{content:"";width:24px;height:2px;background:linear-gradient(90deg,#8b7cff,#58d6e7)}
#gxWelcome h2{margin:20px 0 14px;color:#fbfcff;font-size:clamp(1.8rem,4vw,3.1rem);line-height:1.3;font-weight:950;letter-spacing:-.04em}
#gxWelcome .gx-lead{margin:0;color:#c0cbe0;font-size:.96rem;line-height:2}
#gxWelcome .gx-points{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;margin:26px 0 0}
#gxWelcome .gx-point{padding:13px 12px;border:1px solid rgba(174,190,222,.13);border-radius:15px;background:rgba(255,255,255,.035)}
#gxWelcome .gx-point strong{display:block;color:#f0f3ff;font-size:.77rem;font-weight:900}
#gxWelcome .gx-point span{display:block;margin-top:5px;color:#94a4c0;font-size:.65rem;line-height:1.7}
#gxWelcome .gx-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:28px}
#gxWelcome .gx-button{min-height:49px;padding:0 18px;border:1px solid rgba(185,198,230,.20);border-radius:14px;background:rgba(255,255,255,.055);color:#eef2ff;font:inherit;font-size:.8rem;font-weight:900;cursor:pointer}
#gxWelcome .gx-button.primary{border-color:transparent;background:linear-gradient(110deg,#6b56dc,#5267d9 57%,#078392);box-shadow:0 13px 30px rgba(69,68,170,.32)}
#gxWelcome .gx-small{margin-top:17px;color:#8392ad;font-size:.68rem;line-height:1.8}
#gxWelcome .gx-stage{position:relative;min-height:510px;display:grid;place-items:center;overflow:hidden;padding:32px;direction:ltr}
#gxWelcome .gx-orbit{position:absolute;width:82%;aspect-ratio:1;border:1px solid rgba(145,151,245,.15);border-radius:50%;box-shadow:0 0 0 35px rgba(104,94,217,.025),0 0 0 80px rgba(104,94,217,.02)}
#gxWelcome .gx-orbit:before,#gxWelcome .gx-orbit:after{content:"";position:absolute;border:1px solid rgba(91,205,220,.12);border-radius:50%;inset:12%}
#gxWelcome .gx-orbit:after{inset:25%;border-color:rgba(148,138,255,.15)}
#gxWelcome .gx-stack{position:relative;width:min(100%,360px);height:330px;display:grid;place-items:center}
#gxWelcome .gx-card{position:absolute;width:88%;height:230px;padding:23px;border:1px solid rgba(186,198,233,.25);border-radius:24px;background:linear-gradient(145deg,#263459,#111b31);box-shadow:0 30px 70px rgba(0,0,0,.38);display:flex;flex-direction:column;justify-content:space-between}
#gxWelcome .gx-card.back{transform:translate(-31px,22px) rotate(-10deg);opacity:.45}
#gxWelcome .gx-card.mid{transform:translate(22px,7px) rotate(7deg);opacity:.7}
#gxWelcome .gx-card.front{transform:translateY(-9px);border-color:rgba(133,139,255,.56);background:radial-gradient(ellipse at 90% 0,rgba(125,110,255,.2),transparent 45%),linear-gradient(150deg,#202d50,#10192d)}
#gxWelcome .gx-card-top{display:flex;align-items:center;justify-content:space-between;color:#aebcff;font-size:.63rem;font-weight:900;letter-spacing:.12em}
#gxWelcome .gx-card-word{color:#fff;font-size:2.4rem;font-weight:950;letter-spacing:-.05em}
#gxWelcome .gx-card-lines{display:grid;gap:7px}
#gxWelcome .gx-card-lines span{height:5px;border-radius:20px;background:rgba(199,211,241,.20)}
#gxWelcome .gx-card-lines span:nth-child(2){width:72%}
#gxWelcome .gx-card-lines span:nth-child(3){width:48%}
#gxWelcome .gx-stage-label{position:absolute;right:8%;bottom:8%;padding:10px 14px;border:1px solid rgba(157,177,223,.18);border-radius:12px;background:rgba(13,22,40,.74);color:#aebbd4;font-size:.68rem;font-weight:850;direction:rtl}
#gxWelcome button:focus-visible{outline:3px solid #67e8f9;outline-offset:3px}
@media(max-width:820px){
  #gallery-experience-hero .gx-hero-inner{grid-template-columns:1fr}
  #gallery-experience-hero .gx-art{min-height:220px;grid-row:1}
  #gxWelcome .gx-dialog{grid-template-columns:1fr;max-height:96dvh}
  #gxWelcome .gx-stage{min-height:260px;grid-row:1;padding:22px}
  #gxWelcome .gx-stack{height:220px;width:min(100%,300px)}
  #gxWelcome .gx-card{height:170px;padding:16px}
  #gxWelcome .gx-card-word{font-size:1.8rem}
  #gxWelcome .gx-copy{padding:22px 22px 28px}
  #gxWelcome h2{margin-top:12px;font-size:1.8rem}
  #gxWelcome .gx-points{margin-top:18px}
}
@media(max-width:520px){
  #gallery-experience-hero{border-radius:22px;padding:22px 18px}
  #gallery-experience-hero .gx-art{min-height:190px}
  #gallery-experience-hero .gx-art-card{min-height:145px;padding:15px}
  #gallery-experience-hero .gx-actions .gx-action{flex:1 1 100%}
  #gbGrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px}
  #gbGrid .gb-item{border-radius:15px!important}
  #gxWelcome{padding:8px}
  #gxWelcome .gx-dialog{border-radius:21px}
  #gxWelcome .gx-stage{min-height:205px;padding:12px}
  #gxWelcome .gx-stack{height:180px}
  #gxWelcome .gx-card{height:142px;padding:13px;border-radius:17px}
  #gxWelcome .gx-card-word{font-size:1.55rem}
  #gxWelcome .gx-points{grid-template-columns:1fr;gap:7px}
  #gxWelcome .gx-point{display:flex;align-items:center;justify-content:space-between;gap:12px}
  #gxWelcome .gx-point span{margin:0;text-align:left}
  #gxWelcome .gx-actions{display:grid;grid-template-columns:1fr}
  #gxWelcome .gx-button{width:100%}
}
@media(prefers-reduced-motion:reduce){
  #gallery-experience-hero *,#gxWelcome *,#gbGrid .gb-item,#onboardTourLauncher{scroll-behavior:auto!important;animation:none!important;transition:none!important}
}
"""


WELCOME_MARKUP = r"""
<div id="gxWelcome" hidden>
  <section class="gx-dialog" role="dialog" aria-modal="true" aria-labelledby="gxWelcomeTitle" aria-describedby="gxWelcomeLead">
    <button class="gx-close" id="gxWelcomeClose" type="button" aria-label="إغلاق المقدمة">×</button>
    <div class="gx-copy">
      <div class="gx-kicker">ANKI DESIGN STUDIO · EXPERIENCE</div>
      <h2 id="gxWelcomeTitle">من مكتبة القوالب إلى رزمة تحمل أسلوبك.</h2>
      <p class="gx-lead" id="gxWelcomeLead">ابدأ من مئة تصميم حقيقي، افحص البطاقة قبل اعتمادها، ثم كوّن رُزمتك وراجع إعداداتها بنفسك. كل خطوة واضحة، ولا يحدث أي تصدير دون طلبك.</p>
      <div class="gx-points">
        <div class="gx-point"><strong>استكشف</strong><span>مكتبة كاملة قابلة للفرز</span></div>
        <div class="gx-point"><strong>عاين</strong><span>افحص وجهي البطاقة</span></div>
        <div class="gx-point"><strong>اعتمد</strong><span>اختر ثم راجع قبل التصدير</span></div>
      </div>
      <div class="gx-actions">
        <button class="gx-button primary" id="gxWelcomeStart" type="button">ابدأ الجولة التفاعلية <span aria-hidden="true">←</span></button>
        <button class="gx-button" id="gxWelcomeExplore" type="button">ادخل المعرض مباشرة</button>
      </div>
      <div class="gx-small">لا تنزيل تلقائي، ولا اختيار قوالب نيابةً عنك. ويمكنك إعادة فتح المقدمة من زر الجولة أسفل الصفحة.</div>
    </div>
    <div class="gx-stage" aria-hidden="true">
      <div class="gx-orbit"></div>
      <div class="gx-stack">
        <div class="gx-card back"><div class="gx-card-top"><span>ANKI / 01</span><span>01</span></div><div class="gx-card-word">Design</div><div class="gx-card-lines"><span></span><span></span><span></span></div></div>
        <div class="gx-card mid"><div class="gx-card-top"><span>ANKI / 02</span><span>02</span></div><div class="gx-card-word">Meaning</div><div class="gx-card-lines"><span></span><span></span><span></span></div></div>
        <div class="gx-card front"><div class="gx-card-top"><span>YOUR NEXT DECK</span><span>100</span></div><div class="gx-card-word">Learn.</div><div class="gx-card-lines"><span></span><span></span><span></span></div></div>
      </div>
      <div class="gx-stage-label">مكتبة حقيقية · معاينة · اختيار</div>
    </div>
  </section>
</div>
"""


EXPERIENCE_JS = r"""
(function(){
  "use strict";
  var deck="__DECK__";
  var profiles={
    fr9:{label:"الفرنسية — الصف التاسع",title:"اكتشف القالب الذي يجعل الفرنسية أوضح",description:"مئة تصميم حقيقي لمفرداتك الفرنسية؛ استعرضها، اختبر المعاينة، ثم اختر ما تريد إضافته إلى رُزمتك."},
    en9:{label:"الإنجليزية — الصف التاسع",title:"حوّل مفردات الإنجليزية إلى بطاقات تناسبك",description:"استعرض مئة تصميم حقيقي، وقارن وضوح الكلمة والمعنى، ثم اعتمد القوالب التي تريدها."},
    enlit:{label:"الأدب الإنجليزي — البكالوريا",title:"رتّب مفردات الأدب في تجربة بصرية أوضح",description:"مكتبة من مئة تصميم حقيقي، مع معاينة قبل الاختيار ومسار واضح لمراجعة الرزمة."},
    ensci:{label:"الإنجليزية العلمية — البكالوريا",title:"اجعل المصطلح العلمي أسهل في المراجعة",description:"استكشف مئة تصميم حقيقي، افحص تفاصيل البطاقة، ثم ابنِ رُزمتك بخيارات واضحة."}
  };
  var profile=profiles[deck]||profiles.en9;
  var welcomeKey="anki_"+deck+"_welcome_seen";
  var previousFocus=null;
  var welcomeOpen=false;

  function safeGet(key){
    try{return localStorage.getItem(key);}catch(_e){return null;}
  }
  function safeSet(key,value){
    try{localStorage.setItem(key,value);}catch(_e){}
  }
  function scrollToTarget(target){
    var node=typeof target==="string"?document.querySelector(target):target;
    if(!node)return;
    node.scrollIntoView({behavior:window.matchMedia("(prefers-reduced-motion: reduce)").matches?"auto":"smooth",block:"start"});
    if(node.matches("button,a,input,select,[tabindex]"))node.focus({preventScroll:true});
    else{
      var first=node.querySelector("button,a,input,select,[tabindex]");
      if(first)first.focus({preventScroll:true});
    }
  }
  function addHero(){
    var filters=document.getElementById("gbFilters");
    if(!filters||document.getElementById("gallery-experience-hero"))return;
    var hero=document.createElement("section");
    hero.id="gallery-experience-hero";
    hero.setAttribute("aria-label","مقدمة المعرض");
    hero.innerHTML=
      '<div class="gx-hero-inner">'+
        '<div class="gx-hero-copy">'+
          '<div class="gx-eyebrow">ANKI DESIGN STUDIO / TEMPLATE GALLERY</div>'+
          '<h1 data-gx-title></h1>'+
          '<p class="gx-description" data-gx-description></p>'+
          '<div class="gx-actions">'+
            '<button type="button" class="gx-action primary hero-cta-main" data-gx-browse>استعرض القوالب <span aria-hidden="true">←</span></button>'+
            '<button type="button" class="gx-action" data-gx-welcome>ابدأ الجولة الافتتاحية</button>'+
          '</div>'+
          '<div class="gx-metrics">'+
            '<div class="gx-metric"><strong>100</strong><span>تصميم حقيقي</span></div>'+
            '<div class="gx-metric"><strong>Live</strong><span>معاينة قبل الاختيار</span></div>'+
            '<div class="gx-metric"><strong>Review</strong><span>مراجعة قبل التصدير</span></div>'+
          '</div>'+
        '</div>'+
        '<div class="gx-art" aria-hidden="true">'+
          '<div class="gx-art-glow"></div>'+
          '<div class="gx-art-card back"><span class="gx-art-kicker">ANKI / TEMPLATE 03</span><span class="gx-art-word">Meaning</span><span class="gx-art-note">معنى · مراجعة · تكرار</span></div>'+
          '<div class="gx-art-card mid"><span class="gx-art-kicker">ANKI / TEMPLATE 02</span><span class="gx-art-word">Preview</span><span class="gx-art-note">افحص الوجهين قبل الاعتماد</span></div>'+
          '<div class="gx-art-card front"><span class="gx-art-kicker">YOUR STUDY SYSTEM</span><span class="gx-art-word">One idea.<br>One card.</span><span class="gx-art-note">صمّم تجربة تناسب طريقة دراستك</span></div>'+
        '</div>'+
      '</div>';
    hero.querySelector("[data-gx-title]").textContent=profile.title;
    hero.querySelector("[data-gx-description]").textContent=profile.description;
    var originalHero=document.querySelector("#sec-gal .hero") || (document.querySelector(".hero-cta-main") && document.querySelector(".hero-cta-main").closest(".hero"));
    if(!originalHero || !originalHero.parentNode)return;
    originalHero.parentNode.insertBefore(hero,originalHero);
    originalHero.remove();
    hero.querySelector("[data-gx-browse]").addEventListener("click",function(){
      if(typeof window.openGalleryBrowser==="function")window.openGalleryBrowser();
      else scrollToTarget("#gbGrid");
    });
    hero.querySelector("[data-gx-welcome]").addEventListener("click",openGalleryWelcome);
  }

  function openGalleryWelcome(){
    var modal=document.getElementById("gxWelcome");
    if(!modal)return;
    previousFocus=document.activeElement;
    modal.hidden=false;
    document.body.classList.add("gx-lock");
    welcomeOpen=true;
    var dialog=modal.querySelector(".gx-dialog");
    if(dialog)dialog.scrollTop=0;
    var start=document.getElementById("gxWelcomeStart");
    if(start)start.focus();
  }
  function closeGalleryWelcome(markSeen){
    var modal=document.getElementById("gxWelcome");
    if(!modal)return;
    if(markSeen)safeSet(welcomeKey,"1");
    modal.hidden=true;
    document.body.classList.remove("gx-lock");
    welcomeOpen=false;
    if(previousFocus&&previousFocus.isConnected){
      try{previousFocus.focus({preventScroll:true});}catch(_e){}
    }
  }
  function hasSeenGalleryWelcome(){
    return safeGet(welcomeKey)==="1";
  }
  window.hasSeenGalleryWelcome=hasSeenGalleryWelcome;
  window.openGalleryWelcome=openGalleryWelcome;

  function init(){
    addHero();
    var launcher=document.getElementById("onboardTourLauncher");
    if(launcher){
      launcher.setAttribute("onclick","openGalleryWelcome()");
      launcher.setAttribute("aria-label","فتح المقدمة والجولة التفاعلية");
      launcher.title="افتح مقدمة المعرض والجولة التفاعلية";
    }
    var start=document.getElementById("gxWelcomeStart");
    var explore=document.getElementById("gxWelcomeExplore");
    var close=document.getElementById("gxWelcomeClose");
    if(start)start.addEventListener("click",function(){
      closeGalleryWelcome(true);
      window.setTimeout(function(){
        if(typeof window.showOnboarding==="function")window.showOnboarding();
        else scrollToTarget("#gbGrid");
      },90);
    });
    if(explore)explore.addEventListener("click",function(){
      closeGalleryWelcome(true);
      window.setTimeout(function(){
        if(typeof window.openGalleryBrowser==="function")window.openGalleryBrowser();
        else scrollToTarget("#gbGrid");
      },60);
    });
    if(close)close.addEventListener("click",function(){closeGalleryWelcome(true);});
    var grid=document.getElementById("gbGrid");
    if(grid){
      grid.addEventListener("click",function(event){
        var card=event.target.closest(".gb-item");
        if(!card)return;
        grid.querySelectorAll('.gb-item[data-gx-active="true"]').forEach(function(item){item.removeAttribute("data-gx-active");});
        card.setAttribute("data-gx-active","true");
      });
    }
    document.addEventListener("keydown",function(event){
      if(!welcomeOpen)return;
      if(event.key==="Escape"){
        event.preventDefault();
        closeGalleryWelcome(true);
        return;
      }
      if(event.key!=="Tab")return;
      var modal=document.getElementById("gxWelcome");
      var focusable=Array.from(modal.querySelectorAll('button:not([disabled]),a[href],input:not([disabled]),select:not([disabled]),[tabindex]:not([tabindex="-1"])')).filter(function(node){return !node.hidden;});
      if(!focusable.length)return;
      var first=focusable[0],last=focusable[focusable.length-1];
      if(event.shiftKey&&document.activeElement===first){event.preventDefault();last.focus();}
      else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first.focus();}
    });
  }
  if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
  else init();
})();
"""


def apply_gallery_experience(html, deck):
    """Apply the v2 visual system and accessible welcome layer to one target gallery."""
    if deck not in ("en9", "enlit", "ensci", "fr9"):
        raise SystemExit("Gallery Experience v2 is restricted to the four non-Bac galleries")
    if 'id="gallery-experience-v2"' in html or 'id="gxWelcome"' in html:
        raise SystemExit(deck + ": Gallery Experience v2 is already present")
    for marker in ('id="gbFilters"', 'id="gbGrid"', 'id="onboardTourLauncher"'):
        if marker not in html:
            raise SystemExit(deck + ": required gallery anchor is missing: " + marker)

    old_init = "if(!isOnboardingCompleted())setTimeout(showOnboarding,180);"
    new_init = (
        "if(!isOnboardingCompleted()&&(!window.hasSeenGalleryWelcome||!window.hasSeenGalleryWelcome()))"
        "setTimeout(function(){if(window.openGalleryWelcome)window.openGalleryWelcome();},220);"
    )
    if html.count(old_init) != 1:
        raise SystemExit(deck + ": expected one original first-visit onboarding trigger")
    html = html.replace(old_init, new_init, 1)

    old_launcher = (
        '<button id="onboardTourLauncher" type="button" onclick="showOnboarding()" '
        'aria-label="إعادة فتح الجولة السريعة"><span aria-hidden="true">✦</span>'
        '<span>الجولة السريعة</span></button>'
    )
    new_launcher = (
        '<button id="onboardTourLauncher" type="button" onclick="openGalleryWelcome()" '
        'aria-label="فتح المقدمة والجولة التفاعلية"><span aria-hidden="true">✦</span>'
        '<span>ابدأ الجولة</span></button>'
    )
    if html.count(old_launcher) != 1:
        raise SystemExit(deck + ": expected one persistent onboarding launcher")
    html = html.replace(old_launcher, new_launcher, 1)

    # Replace the generic shared thumbnails with lazy, isolated renders of
    # each real template. The existing image remains a failure fallback.
    old_thumb = '<img class="gb-img" data-loading="1" loading="lazy" decoding="async" src="\'+img+\'" alt="تصميم \'+num+\'">'
    new_thumb = (
        '<iframe class="gb-preview-frame" loading="lazy" title="معاينة تصميم \'+num+\'" '
        'sandbox="allow-same-origin"></iframe>'
        '<img class="gb-fallback-img" loading="lazy" decoding="async" src="\'+img+\'" alt="تصميم \'+num+\'">'
    )
    if html.count(old_thumb) != 1:
        raise SystemExit(deck + ": expected one shared gallery thumbnail renderer")
    html = html.replace(old_thumb, new_thumb, 1)
    image_handlers = re.compile(
        r"var im=it\.querySelector\('\.gb-img'\);\s*"
        r"im\.addEventListener\('load',function\(\)\{this\.removeAttribute\('data-loading'\);"
        r"var sk=this\.parentNode\.querySelector\('\.gb-sk'\);if\(sk\)sk\.style\.display='none';\}\);\s*"
        r"im\.addEventListener\('error',function\(\)\{this\.removeAttribute\('data-loading'\);"
        r"var sk=this\.parentNode\.querySelector\('\.gb-sk'\);if\(sk\)sk\.style\.display='none';\}\);"
    )
    frame_handlers = (
        "var previewFrame=it.querySelector('.gb-preview-frame');"
        "if(previewFrame){"
        "var previewSource=thumbDoc(t);"
        "var previewDocument=new DOMParser().parseFromString(previewSource,'text/html');"
        "previewDocument.querySelectorAll('script,iframe,object,embed').forEach(function(node){node.remove();});"
        "previewDocument.querySelectorAll('*').forEach(function(node){Array.from(node.attributes).forEach(function(attribute){"
        "if(/^on/i.test(attribute.name)||((attribute.name==='href'||attribute.name==='src')&&/^\\s*javascript:/i.test(attribute.value))){node.removeAttribute(attribute.name);}"
        "});});"
        "previewFrame.srcdoc='<!doctype html>'+previewDocument.documentElement.outerHTML;"
        "previewFrame.addEventListener('load',function(){"
        "var doc=this.contentDocument;"
        "var hasContent=doc&&doc.body&&(doc.body.children.length>0||(doc.body.textContent||'').trim().length>0);"
        "var fallback=this.parentNode.querySelector('.gb-fallback-img');"
        "if(!hasContent&&fallback)fallback.setAttribute('data-show','true');"
        "if(hasContent){"
        "var fitPreview=function(){"
        "var selector='.fitme,.ds-word,.ds-trans,.word,.trans,.meaning,.subtitle,.board-txt,.cfit,.frword,.arword,[class*=\"-word\"],[class*=\"-trans\"],[class*=\"-sub\"],[class*=\"-txt\"]';"
        "doc.querySelectorAll(selector).forEach(function(el){"
        "var p=el.parentElement;if(!p)return;"
        "var cs=doc.defaultView.getComputedStyle(el);"
        "var base=parseFloat(el.getAttribute('data-base'))||parseFloat(cs.fontSize)||16;"
        "var min=parseFloat(el.getAttribute('data-min'))||8;if(min<5)min=5;"
        "var aw=p.clientWidth-16,ah=p.clientHeight;if(aw<24||ah<16)return;"
        "el.style.whiteSpace='nowrap';el.style.display='inline-block';el.style.maxWidth='none';el.style.fontSize=base+'px';"
        "var tw=el.scrollWidth,th=el.scrollHeight;if(tw<=2||th<=2)return;"
        "var k=Math.min(aw/tw,ah>10?ah/th:1),fs=base;"
        "if(k<1)fs=Math.max(min,Math.floor(base*k*10)/10);"
        "el.style.fontSize=fs+'px';var tw2=el.scrollWidth;"
        "if(tw2>aw&&fs>min){fs=Math.max(min,Math.floor(fs*aw/tw2*10)/10);el.style.fontSize=fs+'px';}"
        "});};"
        "fitPreview();"
        "if(doc.fonts&&doc.fonts.ready)doc.fonts.ready.then(fitPreview).catch(function(){});"
        "}"
        "var sk=this.parentNode.querySelector('.gb-sk');if(sk)sk.style.display='none';"
        "});"
        "previewFrame.addEventListener('error',function(){"
        "var fallback=this.parentNode.querySelector('.gb-fallback-img');"
        "if(fallback)fallback.setAttribute('data-show','true');"
        "var sk=this.parentNode.querySelector('.gb-sk');if(sk)sk.style.display='none';"
        "});}"
    )
    html, handler_count = image_handlers.subn(lambda _match: frame_handlers, html, count=1)
    if handler_count != 1:
        raise SystemExit(deck + ": could not upgrade gallery cards to live template previews")

    style_tag = '<style id="gallery-experience-v2">\n' + EXPERIENCE_CSS + '\n</style>\n'
    html, style_count = re.subn(r"</head\s*>", style_tag + "</head>", html, count=1, flags=re.I)
    if style_count != 1:
        raise SystemExit(deck + ": could not insert the Gallery Experience v2 stylesheet")

    js = EXPERIENCE_JS.replace("__DECK__", deck)
    script_tag = '<script id="gallery-experience-runtime">\n' + js + '\n</script>\n'
    body_closers = list(re.finditer(r"</body\s*>", html, flags=re.I))
    if not body_closers:
        raise SystemExit(deck + ": missing final body close")
    body_close = body_closers[-1]
    launcher_position = html.find(new_launcher)
    if launcher_position < 0 or html.count(new_launcher) != 1 or launcher_position >= body_close.start():
        raise SystemExit(deck + ": expected one persistent launcher before the final body close")
    # Keep the persistent launcher after every script so it remains a genuine
    # document control and preserves the existing document-order invariant.
    html = html[:launcher_position] + WELCOME_MARKUP + script_tag + html[launcher_position:]

    required = (
        'hero.id="gallery-experience-hero"',
        'id="gxWelcomeStart"',
        'window.hasSeenGalleryWelcome',
        'window.openGalleryWelcome',
        'class="gb-preview-frame"',
        "var previewSource=thumbDoc(t);",
        "previewFrame.srcdoc='<!doctype html>'+previewDocument.documentElement.outerHTML",
        'class="gx-action primary hero-cta-main"',
        'originalHero.remove()',
        'window.openGalleryBrowser'
    )
    for token in required:
        if token not in html:
            raise SystemExit(deck + ": incomplete Gallery Experience v2 output: " + token)
    return html
