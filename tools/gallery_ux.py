"""Deterministic UX transforms for the four generated non-Bac gallery pages."""
import re

TOUR_CSS = r"""
#onboardOverlay[hidden]{display:none!important}
#onboardTourLauncher{position:fixed;right:18px;bottom:calc(18px + env(safe-area-inset-bottom,0px));z-index:2147483001;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:10px 16px;border:1px solid rgba(196,181,253,.34);border-radius:999px;background:linear-gradient(110deg,#6d28d9,#4f46e5 58%,#0e7490);color:#fff;font:inherit;font-size:.78rem;font-weight:900;box-shadow:0 12px 30px rgba(30,27,75,.38),0 0 0 1px rgba(255,255,255,.06) inset;cursor:pointer;pointer-events:auto;transition:transform .18s,box-shadow .18s,filter .18s}
#onboardTourLauncher[hidden]{display:none!important}
#onboardTourLauncher:hover{transform:translateY(-2px);filter:brightness(1.08);box-shadow:0 16px 36px rgba(30,27,75,.48)}
#onboardTourLauncher:focus-visible{outline:3px solid #67e8f9;outline-offset:4px}
@media(max-width:640px){#onboardTourLauncher{right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));min-height:44px;padding:9px 13px;font-size:.72rem}}
#onboardGuideRoot{position:fixed;inset:0;z-index:2147483000;pointer-events:none;direction:rtl;color:#f8fafc}
#onboardGuideRoot .og-backdrop{position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none}
#onboardGuideRoot .og-card{position:fixed;left:12px;right:auto;top:12px;bottom:auto;width:min(430px,calc(100vw - 24px));max-height:min(54dvh,460px);overflow:auto;overscroll-behavior:contain;padding:20px;border:1px solid rgba(167,139,250,.34);border-radius:22px;background:linear-gradient(145deg,rgba(17,21,38,.985),rgba(8,12,25,.99));box-shadow:0 24px 80px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.045) inset,0 0 36px rgba(99,102,241,.12);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);pointer-events:auto;scrollbar-width:thin;z-index:1;animation:ogEnter .24s cubic-bezier(.2,.8,.2,1) both}
#onboardGuideRoot .og-card:after{content:"";position:absolute;left:var(--og-arrow-x,50%);width:12px;height:12px;background:#111526;border:1px solid rgba(167,139,250,.34);transform:translateX(-50%) rotate(45deg);pointer-events:none}
#onboardGuideRoot .og-card[data-placement="below"]:after{top:-7px;border-right:0;border-bottom:0}
#onboardGuideRoot .og-card[data-placement="above"]:after{bottom:-7px;border-left:0;border-top:0}
#onboardGuideRoot .og-card[data-placement="center"]:after{display:none}
#onboardGuideRoot .og-card:before{content:"";position:absolute;inset:0 16% auto;height:1px;background:linear-gradient(90deg,transparent,#a78bfa,#67e8f9,transparent);pointer-events:none}
@keyframes ogEnter{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
#onboardGuideRoot .og-head{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-bottom:15px}
#onboardGuideRoot .og-brand{display:flex;align-items:center;gap:9px;min-width:0}
#onboardGuideRoot .og-mark{display:grid;place-items:center;flex:0 0 auto;width:33px;height:33px;border:1px solid rgba(167,139,250,.36);border-radius:11px;background:linear-gradient(135deg,#6d28d9,#0e7490);font-size:.88rem;font-weight:950;box-shadow:0 7px 18px rgba(79,70,229,.2)}
#onboardGuideRoot .og-brand-copy{display:grid;gap:2px;min-width:0}
#onboardGuideRoot .og-brand-copy strong{color:#e9e6ff;font-size:.7rem;font-weight:950;letter-spacing:.09em}
#onboardGuideRoot .og-brand-copy small{color:#9ca3b8;font-size:.65rem}
#onboardGuideRoot .og-close{display:grid;place-items:center;flex:0 0 auto;width:36px;height:36px;border:1px solid rgba(255,255,255,.12);border-radius:11px;background:rgba(255,255,255,.045);color:#dbe3f3;font-size:1.15rem;cursor:pointer}
#onboardGuideRoot .og-close:hover{background:rgba(248,113,113,.14);border-color:rgba(248,113,113,.4)}
#onboardGuideRoot .og-progress{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin:0 0 14px}
#onboardGuideRoot .og-progress button{display:block;min-width:0;padding:7px 0;border:0;background:transparent;cursor:pointer}
#onboardGuideRoot .og-progress button span{display:block;height:5px;border-radius:99px;background:rgba(255,255,255,.13);transition:background .2s,box-shadow .2s}
#onboardGuideRoot .og-progress button.done span{background:linear-gradient(90deg,#8b5cf6,#22d3ee)}
#onboardGuideRoot .og-progress button[aria-current="step"] span{background:linear-gradient(90deg,#8b5cf6,#22d3ee);box-shadow:0 0 0 2px rgba(103,232,249,.22),0 0 14px rgba(34,211,238,.2)}
#onboardGuideRoot .og-progress button:focus-visible,#onboardGuideRoot button:focus-visible{outline:3px solid #67e8f9;outline-offset:3px;border-radius:7px}
#onboardGuideRoot .og-meta{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:8px}
#onboardGuideRoot .og-step-label{color:#67e8f9;font-size:.72rem;font-weight:950}
#onboardGuideRoot .og-count{color:#9ca3b8;font-size:.69rem;font-variant-numeric:tabular-nums}
#onboardGuideRoot .og-title{margin:0 0 9px;color:#fff;font-family:var(--font-head,inherit);font-size:clamp(1.13rem,2.5vw,1.42rem);font-weight:950;line-height:1.5}
#onboardGuideRoot .og-text{margin:0;color:#d0d6e5;font-size:.84rem;line-height:1.9}
#onboardGuideRoot .og-target{display:flex;align-items:center;gap:10px;margin-top:13px;padding:10px 12px;border:1px solid rgba(103,232,249,.18);border-radius:13px;background:rgba(8,145,178,.09)}
#onboardGuideRoot .og-target-mark{display:grid;place-items:center;flex:0 0 auto;width:27px;height:27px;border-radius:9px;background:rgba(34,211,238,.12);color:#67e8f9;font-weight:950}
#onboardGuideRoot .og-target-copy{display:grid;gap:2px;min-width:0}
#onboardGuideRoot .og-target-copy small{color:#94a3b8;font-size:.63rem}
#onboardGuideRoot .og-target-copy strong{color:#e0f2fe;font-size:.76rem;font-weight:900}
#onboardGuideRoot .og-note{margin-top:9px;color:#aebbd0;font-size:.7rem;line-height:1.75}
#onboardGuideRoot .og-footer{position:sticky;bottom:-13px;z-index:3;display:flex;align-items:center;justify-content:space-between;gap:10px;margin:15px -13px -13px;padding:13px 13px 13px;border-top:1px solid rgba(255,255,255,.09);background:linear-gradient(180deg,rgba(8,12,25,.9),rgba(8,12,25,.995));backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px)}
#onboardGuideRoot .og-skip{border:0;background:none;color:#9ca3b8;font:inherit;font-size:.73rem;text-decoration:underline;text-underline-offset:4px;cursor:pointer}
#onboardGuideRoot .og-skip:hover{color:#e2e8f0}
#onboardGuideRoot .og-actions{display:flex;align-items:center;gap:8px}
#onboardGuideRoot .og-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:9px 15px;border:1px solid rgba(255,255,255,.13);border-radius:12px;font:inherit;font-size:.77rem;font-weight:900;cursor:pointer;transition:transform .16s,box-shadow .16s,background .16s}
#onboardGuideRoot .og-btn:hover{transform:translateY(-1px)}
#onboardGuideRoot .og-btn.primary{border-color:transparent;background:linear-gradient(110deg,#6d28d9,#4f46e5 58%,#0e7490);color:#fff;box-shadow:0 9px 22px rgba(79,70,229,.25)}
#onboardGuideRoot .og-btn.ghost{background:rgba(255,255,255,.045);color:#dbeafe}
body .og-spotlight{position:relative!important;z-index:2147482998!important;outline:3px solid #67e8f9!important;outline-offset:6px!important;border-radius:14px!important;box-shadow:0 0 0 9px rgba(34,211,238,.15),0 16px 48px rgba(0,0,0,.28)!important;transition:outline-color .18s,box-shadow .18s}
@media(max-width:640px){
#onboardGuideRoot .og-card{width:min(420px,calc(100vw - 24px));max-height:min(54dvh,440px);padding:16px;border-radius:19px}
#onboardGuideRoot .og-head{margin-bottom:11px}
#onboardGuideRoot .og-brand-copy strong{font-size:.65rem}
#onboardGuideRoot .og-brand-copy small{font-size:.6rem}
#onboardGuideRoot .og-meta{margin-bottom:6px}
#onboardGuideRoot .og-title{font-size:1.08rem;margin-bottom:7px}
#onboardGuideRoot .og-text{font-size:.77rem;line-height:1.8}
#onboardGuideRoot .og-target{margin-top:10px;padding:8px 10px}
#onboardGuideRoot .og-note{font-size:.66rem}
#onboardGuideRoot .og-footer{margin-top:11px;padding-top:10px}
#onboardGuideRoot .og-btn{min-height:40px;padding:8px 11px;font-size:.72rem}
}
@media(max-width:360px){
#onboardGuideRoot .og-card{padding:13px}
#onboardGuideRoot .og-brand-copy small{display:none}
#onboardGuideRoot .og-title{font-size:1rem}
#onboardGuideRoot .og-text{font-size:.73rem}
#onboardGuideRoot .og-actions{gap:5px}
}
@media(prefers-reduced-motion:reduce){
#onboardGuideRoot *,#onboardGuideRoot *:before,#onboardGuideRoot *:after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
}

#onboardGuideRoot .og-card[data-step="start"]{left:50%!important;right:auto!important;top:50%!important;bottom:auto!important;width:min(900px,calc(100vw - 32px))!important;max-height:min(88dvh,780px)!important;transform:translate(-50%,-50%);padding:clamp(22px,4vw,46px);border-radius:30px;background:radial-gradient(ellipse at 82% 0%,rgba(34,211,238,.16),transparent 44%),radial-gradient(ellipse at 10% 100%,rgba(139,92,246,.2),transparent 42%),linear-gradient(145deg,#11172b,#0b1020 58%,#10172b);box-shadow:0 36px 120px rgba(0,0,0,.62),0 0 0 1px rgba(167,139,250,.16) inset}
#onboardGuideRoot .og-card[data-step="start"] .og-progress,#onboardGuideRoot .og-card[data-step="start"] .og-target{display:none}
#onboardGuideRoot .og-card[data-step="start"] .og-head{margin-bottom:clamp(20px,4vw,38px)}
#onboardGuideRoot .og-card[data-step="start"] .og-title{font-size:clamp(1.8rem,5vw,3.25rem);line-height:1.32;max-width:720px;margin:0 auto 16px;text-align:center;letter-spacing:-.035em}
#onboardGuideRoot .og-card[data-step="start"] .og-text{font-size:clamp(.95rem,1.8vw,1.12rem);line-height:2;max-width:660px;margin:0 auto;text-align:center;color:#cbd5e1}
#onboardGuideRoot .og-card[data-step="start"] .og-meta{justify-content:center;margin:0 0 12px}
#onboardGuideRoot .og-card[data-step="start"] .og-note{max-width:560px;margin:16px auto 0;text-align:center}
#onboardGuideRoot .og-card[data-step="start"] .og-footer{margin:28px -20px -20px;padding:20px;justify-content:center;border-top:1px solid rgba(255,255,255,.1);background:transparent}
#onboardGuideRoot .og-card[data-step="start"] .og-skip{position:absolute;top:24px;left:28px}
#onboardGuideRoot .og-card[data-step="start"] .og-btn.primary{min-width:190px;min-height:52px;border-radius:15px;font-size:.9rem}
#onboardGuideRoot .og-welcome-art{display:grid;grid-template-columns:1.2fr .8fr;gap:12px;max-width:690px;margin:26px auto 0;direction:ltr}
#onboardGuideRoot .og-art-main,#onboardGuideRoot .og-art-side{min-height:112px;border:1px solid rgba(148,163,184,.2);border-radius:19px;background:linear-gradient(145deg,rgba(255,255,255,.09),rgba(255,255,255,.025));box-shadow:0 18px 40px rgba(0,0,0,.16);padding:16px;display:flex;flex-direction:column;justify-content:space-between;overflow:hidden}
#onboardGuideRoot .og-art-main{background:radial-gradient(ellipse at 90% 0%,rgba(34,211,238,.18),transparent 55%),linear-gradient(145deg,rgba(99,102,241,.16),rgba(255,255,255,.025))}
#onboardGuideRoot .og-art-kicker{font-size:.62rem;font-weight:900;letter-spacing:.18em;color:#a5b4fc}
#onboardGuideRoot .og-art-word{font-size:clamp(1.25rem,3vw,2rem);font-weight:950;color:#f8fafc;letter-spacing:-.04em}
#onboardGuideRoot .og-art-meaning{font-size:.82rem;color:#cbd5e1;direction:rtl;text-align:right}
#onboardGuideRoot .og-art-pills{display:flex;gap:6px;flex-wrap:wrap}
#onboardGuideRoot .og-art-pills span{padding:5px 9px;border:1px solid rgba(165,180,252,.22);border-radius:999px;background:rgba(99,102,241,.12);color:#dbeafe;font-size:.63rem;font-weight:800}
#onboardGuideRoot .og-art-side{gap:10px;justify-content:center}
#onboardGuideRoot .og-art-side strong{font-size:.9rem;color:#f8fafc}
#onboardGuideRoot .og-art-side span{font-size:.72rem;line-height:1.7;color:#aebbd0}
@media(max-width:640px){#onboardGuideRoot .og-card[data-step="start"]{width:calc(100vw - 20px)!important;max-height:calc(100dvh - 24px)!important;padding:18px;border-radius:23px}#onboardGuideRoot .og-card[data-step="start"] .og-head{margin-bottom:20px}#onboardGuideRoot .og-card[data-step="start"] .og-title{font-size:1.65rem}#onboardGuideRoot .og-welcome-art{grid-template-columns:1fr;margin-top:18px}#onboardGuideRoot .og-art-main{min-height:112px}#onboardGuideRoot .og-art-side{min-height:86px}#onboardGuideRoot .og-card[data-step="start"] .og-footer{margin:18px -8px -8px;padding:14px 8px}#onboardGuideRoot .og-card[data-step="start"] .og-skip{top:16px;left:18px}}
@media(max-width:360px){#onboardGuideRoot .og-card[data-step="start"] .og-title{font-size:1.38rem}#onboardGuideRoot .og-card[data-step="start"] .og-art-side{display:none}}
/* Signature gallery experience */
.hero-cta-main{border-radius:16px!important;box-shadow:0 12px 32px rgba(79,70,229,.22),0 0 0 1px rgba(255,255,255,.12) inset!important;transition:transform .2s ease,box-shadow .2s ease!important}
.hero-cta-main:hover{transform:translateY(-2px)!important;box-shadow:0 18px 42px rgba(79,70,229,.3),0 0 0 1px rgba(255,255,255,.18) inset!important}
#galleryBrowser{border-radius:24px!important;overflow:hidden;box-shadow:0 28px 90px rgba(0,0,0,.34)!important}
#gbFilters{padding:14px!important;border:1px solid rgba(148,163,184,.16)!important;border-radius:18px!important;background:linear-gradient(145deg,rgba(30,41,59,.72),rgba(15,23,42,.58))!important;backdrop-filter:blur(14px)}
#gbGrid{gap:clamp(10px,1.5vw,18px)!important;padding:clamp(10px,1.5vw,18px)!important}
#gbGrid .gb-item{position:relative!important;overflow:hidden!important;border-radius:17px!important;border:1px solid rgba(148,163,184,.2)!important;background:linear-gradient(150deg,rgba(30,41,59,.82),rgba(15,23,42,.72))!important;box-shadow:0 8px 22px rgba(0,0,0,.14)!important;transition:transform .2s ease,border-color .2s ease,box-shadow .2s ease!important}
#gbGrid .gb-item:hover{transform:translateY(-4px)!important;border-color:rgba(129,140,248,.72)!important;box-shadow:0 18px 36px rgba(0,0,0,.24),0 0 0 1px rgba(129,140,248,.12) inset!important}
#gbGrid .gb-item:focus-visible{outline:3px solid #67e8f9!important;outline-offset:3px!important}
#gvStage{border-radius:24px!important;overflow:hidden!important;box-shadow:0 24px 70px rgba(0,0,0,.2)!important}
#gvSelectBtn,#exOpenBtn,#gTtsPreviewBtn{border-radius:13px!important;transition:transform .18s ease,filter .18s ease,box-shadow .18s ease!important}
#gvSelectBtn:hover,#exOpenBtn:hover,#gTtsPreviewBtn:hover{transform:translateY(-2px)!important;filter:brightness(1.06)}
#onboardTourLauncher{backdrop-filter:blur(16px)}
@media(max-width:640px){#galleryBrowser{border-radius:18px!important}#gbGrid{grid-template-columns:repeat(2,minmax(0,1fr))!important;gap:9px!important;padding:9px!important}#gbGrid .gb-item{border-radius:13px!important}#gbFilters{padding:10px!important;border-radius:14px!important}#gvStage{border-radius:18px!important}}
@media(prefers-reduced-motion:reduce){.hero-cta-main,#gbGrid .gb-item,#gvSelectBtn,#exOpenBtn,#gTtsPreviewBtn{transition:none!important;transform:none!important}}

"""

TOUR_JS = r"""
var ONBOARD_DECK = "__DECK__";
var ONBOARD_PRIMARY_LANGUAGE = ONBOARD_DECK === "fr9" ? "الفرنسية" : "الإنجليزية";
var ONBOARD_STORAGE_KEY = "anki_" + ONBOARD_DECK + "_onboarded";
var ONBOARD_SNOOZE_KEY = "anki_" + ONBOARD_DECK + "_onboarding_snoozed";
var onboardOpenedBrowser = false;
var onboardOpenedAudio = false;
var onboardPositionFrame = 0;
var onboardScrollingTarget = false;
var ONBOARD_STEPS = [
  {id:"start",label:"الانطلاقة",title:"من الفكرة إلى رزمة جاهزة — في تجربة واحدة",text:"اكتشف مكتبة من 100 تصميم حقيقي، اختبر بطاقتك، ثم جهّز رزمة Anki بإعداداتك. لن ننفّذ أي تصدير أو نطلب صوتًا من الإنترنت دون اختيارك.",target:".hero-cta-main",targetLabel:"زر استعراض القوالب",note:"تجربة قصيرة؛ يمكنك تخطيها أو إعادة فتحها في أي وقت."},
  {id:"library",label:"اكتشف",title:"مكتبة تصاميمك — اختر أسلوبك",text:"تصفّح القوالب المئة، وضيّق النتائج بالفلاتر، ثم افتح أي بطاقة لترى تصميمها الحقيقي. المكتبة هنا ليست صورًا دعائية؛ كل اختيار يحمّل القالب الفعلي إلى المعاينة.",target:"#gbGrid .gb-item",fallback:"#gbFilters",targetLabel:"بطاقات القوالب الحقيقية",note:"اختر قالبًا واحدًا لتنتقل مباشرة إلى معاينته."},
  {id:"preview",label:"جرّب",title:"اختبر البطاقة قبل اعتمادها",text:"اقلب البطاقة، افحص الوجهين، ثم حدّد القوالب التي تريدها. إعدادات الصوت متاحة من اللوحة الصوتية؛ شغّل المعاينة يدويًا فقط عندما ترغب بذلك. تغييراتك تبقى تحت سيطرتك.",target:"#gvShowAns",fallback:"#gvStage",audioTarget:"#gAudioPanelBody",targetLabel:"المعاينة الحية وأدوات البطاقة",note:"يمكنك قلب البطاقة وتحديدها وتجربة الصوت بنفسك — دون إنشاء أي ملف."},
  {id:"export",label:"أنشئ",title:"أنت جاهز لمراجعة رُزمتك",text:"افتح ملخص التصدير لمراجعة الاسم والقوالب والصوت. هذه مراجعة فقط؛ لن يبدأ إنشاء ملف APKG إلا عندما تضغط بنفسك على «بدء التصدير».",target:"#exOpenBtn",targetLabel:"مراجعة إعدادات الرزمة",note:"لا تنزيل تلقائي ولا إنشاء رزمة أثناء الجولة."}
];
var onbStep = 0;
var onboardGuideOpen = false;
var onboardGuideRoot = null;
var onboardGuideReturnFocus = null;
var onboardActiveTarget = null;
var onboardReviewOpened = false;

function isOnboardingCompleted(){
  try{
    if(localStorage.getItem(ONBOARD_STORAGE_KEY) === "1")return true;
  }catch(_e){}
  try{return sessionStorage.getItem(ONBOARD_SNOOZE_KEY) === "1";}
  catch(_e){return false;}
}
function markOnboardingCompleted(){
  try{localStorage.setItem(ONBOARD_STORAGE_KEY,"1");return true;}
  catch(_e){return false;}
}
function onboardStepTarget(step){
  if(!step)return null;
  var selector = (step.id === "export" && onboardReviewOpened) ? "#exViewSummary" : step.target;
  var target = selector ? document.querySelector(selector) : null;
  if(!target && step.fallback)target = document.querySelector(step.fallback);
  return target;
}
function onboardClearSpotlight(){
  if(onboardActiveTarget){
    onboardActiveTarget.classList.remove("og-spotlight");
    onboardActiveTarget = null;
  }
}
function onboardEnsureRoot(){
  if(onboardGuideRoot && onboardGuideRoot.isConnected)return onboardGuideRoot;
  var legacy = document.getElementById("onboardOverlay");
  if(legacy){legacy.hidden = true;legacy.setAttribute("aria-hidden","true");}
  var root = document.createElement("div");
  root.id = "onboardGuideRoot";
  root.className = "onboard-guide-root";
  root.setAttribute("dir","rtl");
  document.body.appendChild(root);
  root.addEventListener("click",function(event){
    var stepButton = event.target.closest ? event.target.closest("[data-guide-step]") : null;
    if(stepButton){
      var nextIndex = parseInt(stepButton.getAttribute("data-guide-step"),10);
      if(Number.isInteger(nextIndex))goToOnboardStep(nextIndex);
      return;
    }
    var actionButton = event.target.closest ? event.target.closest("[data-guide-action]") : null;
    if(actionButton)handleOnboardAction(actionButton.getAttribute("data-guide-action"));
  });
  onboardGuideRoot = root;
  return root;
}
function onboardPrepareStep(index){
  var browser = document.getElementById("galleryBrowser");
  if(index === 1){
    // Ensure the 100 real designs have been mounted before opening the library.
    // The tour can start before the asynchronous gallery watcher has populated gvList.
    try{if(typeof ensureGalleryDesigns === "function")ensureGalleryDesigns();}catch(_e){}
    if(browser && !browser.classList.contains("open") && typeof openGalleryBrowser === "function"){
      openGalleryBrowser();
      onboardOpenedBrowser = true;
    }
  }else if(onboardOpenedBrowser && browser && browser.classList.contains("open") && typeof closeGalleryBrowser === "function"){
    closeGalleryBrowser();
    onboardOpenedBrowser = false;
  }
  var audio = document.getElementById("gAudioPanelBody");
  if(index === 4){
    if(audio && !audio.classList.contains("open") && typeof toggleAudioPanel === "function"){
      toggleAudioPanel();
      onboardOpenedAudio = true;
    }
  }else if(onboardOpenedAudio && audio && audio.classList.contains("open") && typeof toggleAudioPanel === "function"){
    toggleAudioPanel();
    onboardOpenedAudio = false;
  }
}
function goToOnboardStep(index){
  var next = Number(index);
  if(!Number.isInteger(next) || next < 0 || next >= ONBOARD_STEPS.length)return;
  onboardClearSpotlight();
  onbStep = next;
  onboardReviewOpened = false;
  onboardPrepareStep(next);
  renderOnboardStep();
  window.setTimeout(scheduleOnboardPosition,90);
}
function onboardBackdropPath(target,width,height){
  var outer = "M0 0H" + width + "V" + height + "H0Z";
  if(!target || !target.isConnected)return outer;
  var rect = target.getBoundingClientRect();
  if(!rect.width || !rect.height)return outer;
  var pad = 10;
  var left = Math.max(0,rect.left-pad);
  var top = Math.max(0,rect.top-pad);
  var right = Math.min(width,rect.right+pad);
  var bottom = Math.min(height,rect.bottom+pad);
  var radius = Math.min(16,(right-left)/4,(bottom-top)/4);
  var hole = "M" + (left+radius) + " " + top +
    "H" + (right-radius) + "Q" + right + " " + top + " " + right + " " + (top+radius) +
    "V" + (bottom-radius) + "Q" + right + " " + bottom + " " + (right-radius) + " " + bottom +
    "H" + (left+radius) + "Q" + left + " " + bottom + " " + left + " " + (bottom-radius) +
    "V" + (top+radius) + "Q" + left + " " + top + " " + (left+radius) + " " + top + "Z";
  return outer + " " + hole;
}
function positionOnboardGuide(){
  if(!onboardGuideOpen || !onboardGuideRoot)return;
  onboardClearSpotlight();
  var step = ONBOARD_STEPS[onbStep];
  var target = onboardStepTarget(step);
  var card = onboardGuideRoot.querySelector(".og-card");
  var path = onboardGuideRoot.querySelector("#ogBackdropPath");
  var backdrop = onboardGuideRoot.querySelector(".og-backdrop");
  if(!card || !path || !backdrop)return;
  var width = Math.max(320,document.documentElement.clientWidth || window.innerWidth || 320);
  var height = Math.max(320,window.innerHeight || document.documentElement.clientHeight || 320);
  var reduced = !!(window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches);
  backdrop.setAttribute("viewBox","0 0 " + width + " " + height);
  if(target && target.isConnected){
    var initialRect = target.getBoundingClientRect();
    if(!onboardScrollingTarget && (initialRect.top < 76 || initialRect.bottom > height-76)){
      onboardScrollingTarget = true;
      try{target.scrollIntoView({behavior:reduced ? "auto" : "smooth",block:"center",inline:"nearest"});}catch(_e){}
      window.setTimeout(function(){onboardScrollingTarget = false;scheduleOnboardPosition();},reduced ? 40 : 360);
    }
    onboardActiveTarget = target;
    target.classList.add("og-spotlight");
  }else{
    target = null;
  }
  var rect = target ? target.getBoundingClientRect() : null;
  path.setAttribute("d",onboardBackdropPath(target,width,height));
  var margin = 12;
  var gap = 18;
  card.style.right = "auto";
  card.style.bottom = "auto";
  card.style.left = margin + "px";
  card.style.top = margin + "px";
  card.style.width = Math.min(width-24,width <= 640 ? 420 : 430) + "px";
  card.style.maxHeight = Math.min(height*.54,460) + "px";
  card.dataset.placement = "center";
  if(!rect){
    var centered = card.getBoundingClientRect();
    card.style.left = Math.max(margin,(width-centered.width)/2) + "px";
    card.style.top = Math.max(margin,(height-centered.height)/2) + "px";
    return;
  }
  var measured = card.getBoundingClientRect();
  var availableAbove = Math.max(0,rect.top-margin-gap);
  var availableBelow = Math.max(0,height-rect.bottom-margin-gap);
  var placeBelow = availableBelow >= measured.height || availableBelow >= availableAbove;
  var available = placeBelow ? availableBelow : availableAbove;
  var maxCardHeight = Math.max(190,Math.min(height*.68,available-8));
  card.style.maxHeight = maxCardHeight + "px";
  measured = card.getBoundingClientRect();
  var top = placeBelow ? rect.bottom+gap : rect.top-measured.height-gap;
  top = Math.max(margin,Math.min(height-measured.height-margin,top));
  var left = rect.left + rect.width/2 - measured.width/2;
  left = Math.max(margin,Math.min(width-measured.width-margin,left));
  card.style.left = left + "px";
  card.style.top = top + "px";
  card.dataset.placement = placeBelow ? "below" : "above";
  var arrowX = Math.max(22,Math.min(measured.width-22,rect.left+rect.width/2-left));
  card.style.setProperty("--og-arrow-x",arrowX + "px");
}
function scheduleOnboardPosition(){
  if(!onboardGuideOpen || onboardPositionFrame)return;
  var request = window.requestAnimationFrame || function(callback){return window.setTimeout(callback,16);};
  onboardPositionFrame = request(function(){
    onboardPositionFrame = 0;
    positionOnboardGuide();
  });
}
function onboardNode(tag,className,text){
  var node = document.createElement(tag);
  if(className)node.className = className;
  if(text !== undefined && text !== null)node.textContent = String(text);
  return node;
}
function renderOnboardStep(){
  if(!onboardGuideOpen)return;
  var root = onboardEnsureRoot();
  var step = ONBOARD_STEPS[onbStep];
  if(!step)return;
  var review = step.id === "export" && onboardReviewOpened;
  var title = review ? "هكذا تبدو مراجعة الرزمة قبل الإنشاء" : step.title;
  var body = review ? "راجع اسم الرزمة، وعدد القوالب المختارة، وإعدادات الصوت وخيارات التضمين. يمكنك إغلاق النافذة والعودة للتعديل. تذكير: لن يبدأ الإنشاء حتى تضغط زر «بدء التصدير» بنفسك." : step.text;
  var targetLabel = review ? "ملخص إعدادات الرزمة" : step.targetLabel;
  var note = review ? "لم نضغط زر بدء التصدير، ولم يُرسل طلب إنشاء APKG." : step.note;
  var primaryLabel = onbStep === 0 ? "ابدأ التجربة" :
    onbStep === 1 ? "استكشف القوالب" :
    onbStep === 2 ? "انتقل إلى مراجعة الرزمة" :
    (review ? "إنهاء التجربة" : "افتح ملخص الرزمة");
  var primaryAction = onbStep === 0 ? "start" :
    onbStep === 1 ? "browse" :
    onbStep === 2 ? "export" :
    (review ? "finish" : "review");

  var svgNS = "http://www.w3.org/2000/svg";
  var backdrop = document.createElementNS(svgNS,"svg");
  backdrop.setAttribute("class","og-backdrop");
  backdrop.setAttribute("aria-hidden","true");
  backdrop.setAttribute("focusable","false");
  backdrop.setAttribute("viewBox","0 0 100 100");
  backdrop.setAttribute("preserveAspectRatio","none");
  var path = document.createElementNS(svgNS,"path");
  path.setAttribute("id","ogBackdropPath");
  path.setAttribute("fill","rgba(3,7,18,.68)");
  path.setAttribute("fill-rule","evenodd");
  path.setAttribute("d","M0 0H100V100H0Z");
  backdrop.appendChild(path);

  var card = onboardNode("section","og-card");
  card.setAttribute("data-step",step.id);
  card.setAttribute("role","dialog");
  card.setAttribute("aria-modal","false");
  card.setAttribute("aria-labelledby","onboardGuideTitle");
  card.setAttribute("aria-describedby","onboardGuideText");

  var head = onboardNode("div","og-head");
  var brand = onboardNode("div","og-brand");
  brand.appendChild(onboardNode("span","og-mark","A"));
  var brandCopy = onboardNode("span","og-brand-copy");
  brandCopy.appendChild(onboardNode("strong","","ANKI DESIGN STUDIO"));
  brandCopy.appendChild(onboardNode("small","","تجربة سريعة • ٤ مراحل"));
  brand.appendChild(brandCopy);
  var close = onboardNode("button","og-close","×");
  close.type = "button";
  close.setAttribute("data-guide-action","close");
  close.setAttribute("aria-label","إغلاق الجولة");
  head.appendChild(brand);
  head.appendChild(close);
  card.appendChild(head);

  var progress = onboardNode("nav","og-progress");
  progress.setAttribute("aria-label","محطات الجولة");
  ONBOARD_STEPS.forEach(function(item,index){
    var button = onboardNode("button",index <= onbStep ? "done" : "");
    button.type = "button";
    button.setAttribute("data-guide-step",String(index));
    button.setAttribute("aria-label","الانتقال إلى المحطة " + (index+1) + ": " + item.label);
    button.setAttribute("aria-current",index === onbStep ? "step" : "false");
    button.appendChild(onboardNode("span",""));
    progress.appendChild(button);
  });
  card.appendChild(progress);

  var meta = onboardNode("div","og-meta");
  meta.appendChild(onboardNode("span","og-step-label",step.label));
  meta.appendChild(onboardNode("span","og-count","المحطة " + (onbStep+1) + " من " + ONBOARD_STEPS.length));
  card.appendChild(meta);
  var heading = onboardNode("h2","og-title",title);
  heading.id = "onboardGuideTitle";
  heading.tabIndex = -1;
  card.appendChild(heading);
  var description = onboardNode("p","og-text",body);
  description.id = "onboardGuideText";
  description.setAttribute("aria-live","polite");
  card.appendChild(description);
  if(step.id === "start"){
    var art = onboardNode("div","og-welcome-art");
    var mainArt = onboardNode("div","og-art-main");
    mainArt.appendChild(onboardNode("span","og-art-kicker","DESIGN YOUR LEARNING"));
    mainArt.appendChild(onboardNode("strong","og-art-word",ONBOARD_DECK === "fr9" ? "Bonjour · Leçon" : "Learn · Remember"));
    mainArt.appendChild(onboardNode("span","og-art-meaning",ONBOARD_DECK === "fr9" ? "درس · معنى · نطق" : "كلمة · معنى · نطق"));
    var pills = onboardNode("div","og-art-pills");
    ["100 تصميم","معاينة حقيقية","رزمة Anki"].forEach(function(label){pills.appendChild(onboardNode("span","",label));});
    mainArt.appendChild(pills);
    var sideArt = onboardNode("div","og-art-side");
    sideArt.appendChild(onboardNode("strong","","من القالب إلى التعلّم"));
    sideArt.appendChild(onboardNode("span","","اكتشف، جرّب، ثم راجع رُزمتك — بإيقاعك ومن دون خطوات مفروضة."));
    art.appendChild(mainArt);art.appendChild(sideArt);card.appendChild(art);
  }

  var targetBox = onboardNode("div","og-target");
  targetBox.appendChild(onboardNode("span","og-target-mark","◎"));
  var targetCopy = onboardNode("span","og-target-copy");
  targetCopy.appendChild(onboardNode("small","","الأداة الفعلية على الصفحة"));
  targetCopy.appendChild(onboardNode("strong","",targetLabel));
  targetBox.appendChild(targetCopy);
  card.appendChild(targetBox);

  var status = onboardNode("p","og-note",note);
  status.id = "onboardGuideNote";
  status.setAttribute("role","status");
  status.setAttribute("aria-live","polite");
  card.appendChild(status);

  var footer = onboardNode("div","og-footer");
  var later = onboardNode("button","og-skip","لاحقًا");
  later.type = "button";
  later.setAttribute("data-guide-action","later");
  footer.appendChild(later);
  var actions = onboardNode("div","og-actions");
  if(onbStep > 0){
    var previous = onboardNode("button","og-btn ghost","السابق");
    previous.type = "button";
    previous.setAttribute("data-guide-action","previous");
    actions.appendChild(previous);
  }
  var primary = onboardNode("button","og-btn primary",primaryLabel);
  primary.type = "button";
  primary.setAttribute("data-guide-action",primaryAction);
  actions.appendChild(primary);
  footer.appendChild(actions);
  card.appendChild(footer);

  while(root.firstChild)root.removeChild(root.firstChild);
  root.appendChild(backdrop);
  root.appendChild(card);
  if(heading && typeof heading.focus === "function")heading.focus({preventScroll:true});
}
function handleOnboardAction(action){
  if(action === "finish"){closeOnboarding(true);return;}
  if(action === "close" || action === "later"){closeOnboarding(false);return;}
  if(action === "previous"){goToOnboardStep(onbStep-1);return;}
  if(action === "start"){goToOnboardStep(1);return;}
  if(action === "browse"){goToOnboardStep(2);return;}
  if(action === "export"){goToOnboardStep(3);return;}
  if(action === "review"){
    var button = document.getElementById("exOpenBtn");
    if(button)button.click();
    else if(typeof openExport === "function")openExport();
    var closeButton = document.querySelector("#exportOverlay .fs-close");
    if(closeButton)onboardGuideReturnFocus = closeButton;
    onboardReviewOpened = true;
    renderOnboardStep();
    window.setTimeout(scheduleOnboardPosition,120);
  }
}
function showOnboarding(){
  if(onboardGuideOpen)return;
  onboardGuideReturnFocus = document.activeElement;
  onboardGuideOpen = true;
  onboardReviewOpened = false;
  onboardOpenedBrowser = false;
  onboardOpenedAudio = false;
  var launcher = document.getElementById("onboardTourLauncher");
  if(launcher)launcher.hidden = true;
  onboardEnsureRoot();
  goToOnboardStep(0);
}
function closeOnboarding(completed){
  if(!onboardGuideOpen)return;
  onboardGuideOpen = false;
  onboardClearSpotlight();
  var browser = document.getElementById("galleryBrowser");
  if(onboardOpenedBrowser && browser && browser.classList.contains("open") && typeof closeGalleryBrowser === "function")closeGalleryBrowser();
  onboardOpenedBrowser = false;
  var audio = document.getElementById("gAudioPanelBody");
  if(onboardOpenedAudio && audio && audio.classList.contains("open") && typeof toggleAudioPanel === "function")toggleAudioPanel();
  onboardOpenedAudio = false;
  if(onboardGuideRoot && onboardGuideRoot.parentNode)onboardGuideRoot.parentNode.removeChild(onboardGuideRoot);
  onboardGuideRoot = null;
  if(completed){
    var persisted = markOnboardingCompleted();
    try{
      if(persisted)sessionStorage.removeItem(ONBOARD_SNOOZE_KEY);
      else sessionStorage.setItem(ONBOARD_SNOOZE_KEY,"1");
    }catch(_e){}
  }else{
    try{sessionStorage.setItem(ONBOARD_SNOOZE_KEY,"1");}catch(_e){}
  }
  var launcher = document.getElementById("onboardTourLauncher");
  if(launcher)launcher.hidden = false;
  try{
    if(onboardGuideReturnFocus && onboardGuideReturnFocus.isConnected && typeof onboardGuideReturnFocus.focus === "function")onboardGuideReturnFocus.focus();
  }catch(_e){}
  onboardGuideReturnFocus = null;
}
document.addEventListener("click",function(event){
  if(!onboardGuideOpen)return;
  var target = event.target;
  if(!target || !target.closest)return;
  if(onbStep === 1 && target.closest("#gbGrid .gb-item")){
    window.setTimeout(function(){if(onboardGuideOpen && onbStep === 1)goToOnboardStep(2);},360);
    return;
  }
  if(onbStep === 2 && target.closest("#gvShowAns,.gv-flip")){
    window.setTimeout(function(){
      if(!onboardGuideOpen || onbStep !== 2)return;
      var note = document.getElementById("onboardGuideNote");
      if(note)note.textContent = "قلبت البطاقة فعليًا؛ يمكنك الآن تحديد القالب أو تجربة الصوت أو متابعة مراجعة الرزمة.";
    },40);
    return;
  }
  if(onbStep === 2 && target.closest("#gvSelectBtn")){
    window.setTimeout(function(){
      if(!onboardGuideOpen || onbStep !== 2)return;
      var note = document.getElementById("onboardGuideNote");
      var count = (typeof gvSel !== "undefined" && gvSel) ? gvSel.length : 0;
      if(note)note.textContent = count ? "تم تحديث الاختيار فعليًا. عدد القوالب المحددة الآن: " + count + "." : "أُزيل تحديد القالب الحالي. يمكنك اختياره مجددًا أو متابعة الجولة.";
    },40);
    return;
  }
  if(onbStep === 2 && target.closest("#gTtsPreviewBtn")){
    window.setTimeout(function(){
      if(!onboardGuideOpen || onbStep !== 2)return;
      var note = document.getElementById("onboardGuideNote");
      if(note)note.textContent = "بدأت معاينة الصوت بطلب منك. استمع إلى النطق، ثم تابع عندما تنتهي.";
    },40);
    return;
  }
  if(onbStep === 3 && target.closest("#exOpenBtn")){
    window.setTimeout(function(){
      if(onboardGuideOpen && onbStep === 3){
        var closeButton = document.querySelector("#exportOverlay .fs-close");
        if(closeButton)onboardGuideReturnFocus = closeButton;
        onboardReviewOpened = true;
        renderOnboardStep();
        scheduleOnboardPosition();
      }
    },120);
  }
});
document.addEventListener("keydown",function(event){
  if(!onboardGuideOpen)return;
  if(event.key === "Escape"){
    var exportOverlay = document.getElementById("exportOverlay");
    if(onbStep === 3 && exportOverlay && exportOverlay.classList.contains("on") && typeof closeExport === "function"){
      event.preventDefault();
      closeExport();
      window.setTimeout(function(){
        if(onboardGuideOpen && onboardGuideRoot){
          var heading = onboardGuideRoot.querySelector("#onboardGuideTitle");
          if(heading && typeof heading.focus === "function")heading.focus({preventScroll:true});
        }
      },100);
      return;
    }
    event.preventDefault();closeOnboarding();return;
  }
  var target = event.target;
  var typing = target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.tagName === "SELECT" || target.isContentEditable);
  if(typing || event.altKey || event.ctrlKey || event.metaKey)return;
  if(event.key === "ArrowLeft" && onbStep < ONBOARD_STEPS.length-1){event.preventDefault();goToOnboardStep(onbStep+1);}
  else if(event.key === "ArrowRight" && onbStep > 0){event.preventDefault();goToOnboardStep(onbStep-1);}
});
window.addEventListener("resize",scheduleOnboardPosition);
window.addEventListener("scroll",scheduleOnboardPosition,true);
var onboardOriginalCloseExport = null;
if(typeof closeExport === "function" && !window.__ankiGuideWrappedCloseExport){
  onboardOriginalCloseExport = closeExport;
  window.closeExport = function(){
    var result = onboardOriginalCloseExport.apply(this,arguments);
    if(onboardGuideOpen && onbStep === 3 && onboardReviewOpened){
      window.setTimeout(function(){
        var overlay = document.getElementById("exportOverlay");
        if(!overlay || !overlay.classList.contains("on")){
          onboardReviewOpened = false;
          var opener = document.getElementById("exOpenBtn");
          if(opener)onboardGuideReturnFocus = opener;
          renderOnboardStep();
          scheduleOnboardPosition();
        }
      },80);
    }
    return result;
  };
  window.__ankiGuideWrappedCloseExport = true;
}
"""

LOADER_CSS = "/* ============================================================\n   LOADING\n   ============================================================ */\n#loadingMsg{position:fixed;inset:0;z-index:90;display:grid;place-content:center;text-align:center;\n  background:var(--bg)}\n#loadBar{background:var(--ac)}\n#loadPct{color:var(--tx3)}\n"
OLD_TOUR_CSS = "#onboardOverlay.onboard-overlay{background:radial-gradient(120% 100% at 50% 0%,rgba(139,92,246,.22),transparent 60%),linear-gradient(180deg,#14111d,#0b0a12)}\n#onboardOverlay .onboard-box{width:100vw;max-width:100vw;height:100dvh;max-height:100dvh;border:0;border-radius:0;background:transparent;animation:none;display:flex;align-items:center;justify-content:center;padding:24px}\n#onboardOverlay .ob-full{width:100%;max-width:620px;text-align:center;display:flex;flex-direction:column;align-items:center;gap:6px}\n#onboardOverlay .ob-medal{display:grid;place-items:center;width:74px;height:74px;border-radius:50%;font-size:1.7rem;font-weight:900;color:#fff;background:linear-gradient(135deg,#7c3aed,#8b5cf6 50%,#0ea5e9);box-shadow:0 18px 44px rgba(124,58,237,.5);margin-bottom:14px}\n#onboardOverlay .ob-title{font-size:clamp(1.5rem,4.5vw,2.3rem);font-weight:900;font-family:var(--font-head);line-height:1.5;margin:0 0 8px;background:linear-gradient(115deg,#e9e2ff,#a78bfa 55%,#67e8f9);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}\n#onboardOverlay .ob-text{font-size:1rem;color:var(--tx2);line-height:2;max-width:540px;margin:0 0 14px}\n#onboardOverlay .ob-nav{display:flex;gap:12px;justify-content:center;margin-top:14px;flex-wrap:wrap}\n#onboardOverlay .ob-btn{padding:12px 40px;font-size:.9em}\n#onboardOverlay .ob-skip{margin-top:16px}\n#onboardOverlay .ob-skip button{background:none;border:none;color:var(--tx3);text-decoration:underline;cursor:pointer;font-size:.8em}\n#onboardOverlay .onboard-steps{justify-content:center}\n"
LOADER_HTML = "<div id=\"loadingMsg\">\n  <div style=\"font-family:var(--font-mono);font-size:.8em;letter-spacing:1px;color:var(--tx2);margin-bottom:12px;text-transform:uppercase\">جاري تحميل القوالب...</div>\n  <div style=\"width:240px;height:4px;background:var(--s3);border:1px solid var(--bd-strong);border-radius:0;margin:0 auto;overflow:hidden\">\n    <div id=\"loadBar\" style=\"width:0%;height:100%;border-radius:0;transition:width .3s\"></div>\n  </div>\n  <div id=\"loadPct\" style=\"font-family:var(--font-mono);font-size:.62em;color:var(--tx3);margin-top:8px\">0%</div>\n</div>\n"
FLIP_CSS = ".gv-fabs{position:absolute;top:14px;left:14px;z-index:5;display:flex;flex-direction:column;gap:8px}\n.gv-fab{position:absolute;top:14px;left:14px;width:42px;height:42px;border-radius:2px;font-size:1.1rem;display:grid;place-items:center;\n  background:var(--bg-1);border:1px solid var(--bd-strong);color:var(--tx);transition:var(--t-f);z-index:5}\n.gv-fab.gv-flip{top:64px}\n.gv-fab:hover{border-color:var(--ac);color:var(--ac)}\n"
FLIP_EXTRA_CSS = ".gv-fab{font-size:1.3rem}"
FLIP_THEME_CSS = "/* 17) أزرار عائمة بتدرّج عند المرور */\n.gv-fab:hover{background:linear-gradient(135deg,var(--ac),var(--ac3));color:#fff;border-color:transparent;transform:scale(1.06)}\n"
FLIP_HTML = "<button class=\"gv-fab gv-flip\" onclick=\"gvFlip()\" title=\"قلب البطاقة\" aria-label=\"قلب البطاقة\"><svg width=\"1.1em\" height=\"1.1em\" viewBox=\"0 0 24 24\" fill=\"none\" stroke=\"currentColor\" stroke-width=\"2\" stroke-linecap=\"round\" stroke-linejoin=\"round\" aria-hidden=\"true\"><polyline points=\"1 4 1 10 7 10\"/><path d=\"M3.51 15a9 9 0 1 0 2.13-9.36L1 10\"/></svg></button>"

def _replace_once(source, old, new, label):
    count = source.count(old)
    if count != 1:
        raise SystemExit("%s: expected one exact match, found %d" % (label, count))
    return source.replace(old, new, 1)

def apply_gallery_ux(html, deck):
    if deck not in ("en9", "enlit", "ensci", "fr9"):
        raise SystemExit("UX polish is restricted to the four non-Bac galleries")

    # The upstream gallery builder substitutes the per-deck audio-status URL
    # but omits its closing quote. Repair the exact generated token here,
    # without changing the protected builder or the French Bac source.
    audio_source = "tas9" if deck == "fr9" else deck
    audio_status_bad = "fetch(apiBase()+'/api/audio_status?source=" + audio_source + ")"
    audio_status_good = "fetch(apiBase()+'/api/audio_status?source=" + audio_source + "')"
    audio_status_count = html.count(audio_status_bad)
    if audio_status_count != 1:
        raise SystemExit(
            deck + " expected one malformed generated audio-status URL for "
            + audio_source + ", found " + str(audio_status_count)
        )
    html = html.replace(audio_status_bad, audio_status_good, 1)

    html = _replace_once(html, LOADER_CSS, "", deck + " loading CSS")
    html = _replace_once(html, LOADER_HTML, "", deck + " loading markup")
    html = _replace_once(html, FLIP_CSS, "", deck + " floating flip CSS")
    html = _replace_once(html, FLIP_EXTRA_CSS, "", deck + " floating flip extra CSS")
    theme_css_count = html.count(FLIP_THEME_CSS)
    if theme_css_count > 1:
        raise SystemExit(deck + " found duplicate legacy floating flip hover rules")
    if theme_css_count == 1:
        html = html.replace(FLIP_THEME_CSS, "", 1)
    flip_button_count = html.count(FLIP_HTML)
    if flip_button_count > 1:
        raise SystemExit(deck + " expected at most one floating corner flip button, found %d" % flip_button_count)
    if flip_button_count:
        html = html.replace(FLIP_HTML, "", 1)
    html = _replace_once(html, OLD_TOUR_CSS, "", deck + " legacy tour CSS")

    dialog_old = '<dialog class="onboard-overlay" id="onboardOverlay" style="display:none">'
    dialog_new = (
        '<dialog class="onboard-overlay" id="onboardOverlay" '
        'hidden aria-hidden="true">'
    )
    html = _replace_once(html, dialog_old, dialog_new, deck + " tour dialog semantics")

    tour_js = TOUR_JS.replace("__DECK__", deck)
    start = html.find("var ONBOARD_STEPS=[")
    end_marker = "// ============================================================\n// WHAT'S NEW"
    end = html.find(end_marker, start)
    if start < 0 or end < 0:
        raise SystemExit(deck + " could not locate the original onboarding block")
    html = html[:start] + tour_js + "\n\n" + html[end:]

    old_init = "if(!localStorage.getItem('anki_" + deck + "_onboarded'))showOnboarding();"
    new_init = "if(!isOnboardingCompleted())setTimeout(showOnboarding,180);"
    html = _replace_once(html, old_init, new_init, deck + " delayed first-visit tour")

    launcher_html = '<button id="onboardTourLauncher" type="button" onclick="showOnboarding()" aria-label="إعادة فتح الجولة السريعة"><span aria-hidden="true">✦</span><span>الجولة السريعة</span></button>\n'
    body_closers = list(re.finditer(r"</body\s*>", html, flags=re.I))
    if not body_closers:
        raise SystemExit(deck + " has no closing body tag for the persistent quick-tour launcher")
    # Generated pages contain HTML fragments inside JavaScript strings, so the
    # first textual </body> can be inside a script. Use the final document close.
    body_close = body_closers[-1]
    html = html[:body_close.start()] + launcher_html + html[body_close.start():]

    style_tag = '<style id="gallery-tour-redesign">\n' + TOUR_CSS + '\n</style>\n'
    html, inserted = re.subn(r"</head\s*>", style_tag + "</head>", html, count=1, flags=re.I)
    if inserted != 1:
        raise SystemExit(deck + " could not insert the tour stylesheet into the document head")

    residuals = []
    for token in ("gv-fab", 'id="loadingMsg"'):
        cursor = 0
        while len(residuals) < 8:
            position = html.find(token, cursor)
            if position < 0:
                break
            residuals.append((token, html[max(0, position - 70):position + 150]))
            cursor = position + len(token)
    if residuals:
        raise SystemExit(deck + " UX transform left a removed control or loader behind: " + repr(residuals))
    if 'id="fsFlipBtn"' not in html:
        raise SystemExit(deck + " full-screen flip control was unexpectedly removed")
    return html
