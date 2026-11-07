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
#onboardGuideRoot .og-progress{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px;margin:0 0 14px}
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


/* Guided tour v2: compact coachmark with collision-aware placement. */
#onboardGuideRoot .og-card{
  width:min(430px,calc(100vw - 24px));max-height:min(42dvh,360px);
  padding:clamp(15px,2vw,20px);border:1px solid rgba(151,174,226,.34);
  border-radius:22px;background:
    radial-gradient(ellipse at 100% 0,rgba(111,98,239,.17),transparent 48%),
    linear-gradient(150deg,rgba(18,28,51,.99),rgba(7,13,27,.995));
  box-shadow:0 28px 84px rgba(0,0,0,.58),0 0 0 1px rgba(255,255,255,.045) inset;
}
#onboardGuideRoot .og-card:after{display:none!important}
#onboardGuideRoot .og-head{margin-bottom:12px}
#onboardGuideRoot .og-mark{width:36px;height:36px;border-radius:12px}
#onboardGuideRoot .og-progress{gap:7px;margin-bottom:12px}
#onboardGuideRoot .og-progress button{padding:5px 0}
#onboardGuideRoot .og-progress button span{height:6px}
#onboardGuideRoot .og-meta{margin-bottom:7px}
#onboardGuideRoot .og-step-label{font-size:.76rem}
#onboardGuideRoot .og-count{font-size:.7rem}
#onboardGuideRoot .og-title{font-size:clamp(1.08rem,2vw,1.34rem);line-height:1.48;margin-bottom:8px}
#onboardGuideRoot .og-text{font-size:.81rem;line-height:1.78;color:#d5deef}
#onboardGuideRoot .og-target{margin-top:11px;padding:9px 11px;border-color:rgba(103,232,249,.22);background:rgba(8,145,178,.11)}
#onboardGuideRoot .og-note{margin-top:8px;font-size:.68rem;line-height:1.65}
#onboardGuideRoot .og-footer{margin:12px -10px -10px;padding:11px 10px 10px;gap:8px}
#onboardGuideRoot .og-btn{min-height:43px;padding:9px 14px;border-radius:13px}
#onboardGuideRoot .og-btn.primary{background:linear-gradient(112deg,#6956dc,#4c65d8 58%,#087e91);box-shadow:0 8px 20px rgba(70,75,180,.28)}
#onboardGuideRoot .og-skip{font-size:.72rem}
@media(max-width:640px){
  #onboardGuideRoot .og-card{width:calc(100vw - 20px);max-height:min(42dvh,340px);padding:14px;border-radius:19px}
  #onboardGuideRoot .og-head{margin-bottom:9px}
  #onboardGuideRoot .og-brand-copy strong{font-size:.67rem}
  #onboardGuideRoot .og-brand-copy small{font-size:.6rem}
  #onboardGuideRoot .og-title{font-size:1.02rem;line-height:1.48}
  #onboardGuideRoot .og-text{font-size:.75rem;line-height:1.72}
  #onboardGuideRoot .og-target{margin-top:9px;padding:8px 9px}
  #onboardGuideRoot .og-target-copy strong{font-size:.72rem}
  #onboardGuideRoot .og-note{font-size:.64rem}
  #onboardGuideRoot .og-footer{margin-top:9px;padding-top:9px}
  #onboardGuideRoot .og-btn{min-height:40px;padding:8px 10px;font-size:.69rem}
  #onboardGuideRoot .og-skip{font-size:.67rem}
}
@media(max-width:360px){
  #onboardGuideRoot .og-card{padding:11px}
  #onboardGuideRoot .og-brand-copy small{display:none}
  #onboardGuideRoot .og-text{font-size:.71rem}
  #onboardGuideRoot .og-target-copy small{font-size:.58rem}
  #onboardGuideRoot .og-footer{gap:5px}
  #onboardGuideRoot .og-btn{padding-inline:8px}
}
/* Refined coachmark system: readable hierarchy, roomier controls and consistent touch targets. */
#onboardGuideRoot .og-card{width:min(480px,calc(100vw - 24px));max-height:min(56dvh,520px);padding:clamp(18px,2.2vw,24px);border:1px solid rgba(164,177,224,.34);border-radius:24px;background:radial-gradient(ellipse at 92% 0,rgba(113,104,238,.19),transparent 46%),linear-gradient(148deg,rgba(18,27,49,.995),rgba(7,13,27,.995));box-shadow:0 28px 90px rgba(0,0,0,.56),0 0 0 1px rgba(255,255,255,.04) inset}
#onboardGuideRoot .og-progress{gap:7px;margin-bottom:18px}
#onboardGuideRoot .og-progress button{padding:8px 0}
#onboardGuideRoot .og-progress button span{height:6px;border-radius:99px}
#onboardGuideRoot .og-meta{margin-bottom:10px}
#onboardGuideRoot .og-step-label{font-size:.76rem;letter-spacing:.01em}
#onboardGuideRoot .og-count{font-size:.72rem}
#onboardGuideRoot .og-title{font-size:clamp(1.18rem,2.2vw,1.48rem);line-height:1.48;letter-spacing:-.025em;margin-bottom:12px}
#onboardGuideRoot .og-text{font-size:.88rem;line-height:1.85;color:#e0e6f2}
#onboardGuideRoot .og-target{margin-top:17px;padding:12px 14px;border-radius:15px;background:rgba(34,211,238,.075);border-color:rgba(103,232,249,.22)}
#onboardGuideRoot .og-target-mark{width:31px;height:31px;border-radius:10px}
#onboardGuideRoot .og-target-copy small{font-size:.67rem}
#onboardGuideRoot .og-target-copy strong{font-size:.8rem}
#onboardGuideRoot .og-note{font-size:.73rem;line-height:1.75;margin-top:12px;color:#bac7db}
#onboardGuideRoot .og-footer{margin:18px -15px -15px;padding:14px 15px 13px;gap:12px}
#onboardGuideRoot .og-actions{gap:9px}
#onboardGuideRoot .og-btn{min-height:46px;padding:10px 17px;border-radius:13px;font-size:.79rem}
#onboardGuideRoot .og-btn.primary{background:linear-gradient(110deg,#6d5ce7,#4e66d9 58%,#087f91);box-shadow:0 9px 24px rgba(70,75,180,.3)}
#onboardGuideRoot .og-skip{font-size:.76rem}
#onboardGuideRoot .og-close{width:38px;height:38px;border-radius:12px}
@media(max-width:640px){#onboardGuideRoot .og-card{width:calc(100vw - 20px);max-height:min(58dvh,520px);padding:16px;border-radius:21px}#onboardGuideRoot .og-title{font-size:1.12rem;line-height:1.48}#onboardGuideRoot .og-text{font-size:.81rem;line-height:1.8}#onboardGuideRoot .og-target{margin-top:12px;padding:10px 11px}#onboardGuideRoot .og-note{font-size:.69rem}#onboardGuideRoot .og-footer{margin:13px -11px -11px;padding:11px}#onboardGuideRoot .og-btn{min-height:44px;padding:9px 12px;font-size:.74rem}}
@media(max-width:360px){#onboardGuideRoot .og-card{width:calc(100vw - 16px);padding:13px}#onboardGuideRoot .og-title{font-size:1.04rem}#onboardGuideRoot .og-text{font-size:.75rem}#onboardGuideRoot .og-footer{gap:7px}#onboardGuideRoot .og-btn{padding:8px 9px;font-size:.69rem}}

"""

TOUR_JS = r"""
var ONBOARD_DECK = "__DECK__";
var ONBOARD_PRIMARY_LANGUAGE = ONBOARD_DECK === "fr9" ? "الفرنسية" : "الإنجليزية";
var ONBOARD_STORAGE_KEY = "anki_" + ONBOARD_DECK + "_onboarded_v3";
var ONBOARD_SNOOZE_KEY = "anki_" + ONBOARD_DECK + "_onboarding_snoozed_v3";
var onboardOpenedBrowser = false;
var onboardOpenedAudio = false;
var onboardPositionFrame = 0;

var ONBOARD_STEPS = [
  {id:"start",label:"نظرة عامة",title:"من اختيار القالب إلى تجهيز رزمة Anki",text:"تضم هذه المكتبة 100 قالب. سنمرّ معاً على طريقة العثور على تصميم، ومعاينة وجهي البطاقة، واختيار ما يناسبك، ثم ضبط الصوت ومراجعة الرزمة. الجولة تشرح الأدوات الفعلية؛ ولا تختار قوالبك أو تنشئ ملفاً نيابةً عنك.",target:".hero-cta-main",targetLabel:"زر استكشاف القوالب",note:"ستبقى اختياراتك بيدك. يمكنك التنقل بين المحطات أو إغلاق الجولة متى شئت."},
  {id:"library",label:"مكتبة القوالب",title:"اعثر على التصميم من بين 100 قالب",text:"تُفتح المكتبة لتعرض القوالب الفعلية. استخدم التصنيفات لتصفية النتائج، ثم افتح أي بطاقة لمشاهدة معاينتها. فتح القالب لا يضيفه إلى رُزمتك؛ الاختيار يتم بخطوة منفصلة.",target:"#gbFilters .gb-chip",fallback:"#galleryBrowser .gb-title",targetLabel:"تصنيفات القوالب",note:"افتح أي قالب من الشبكة؛ ستنتقل الجولة تلقائياً إلى معاينته. ويمكنك أيضاً المتابعة دون اختيار."},
  {id:"preview",label:"معاينة البطاقة",title:"افحص الوجهين قبل أن تختار",text:"هذه معاينة للقالب بمحتوى المفردات، وليست صورة ثابتة. جرّب قلب البطاقة، وتحقق من وضوح الكلمة والمعنى وتوزيع العناصر على الوجهين.",target:"#gvShowAns",fallback:"#gvStage",targetLabel:"زر قلب البطاقة",note:"جرّب زر قلب البطاقة في المعاينة أو استخدم زر الجولة أدناه للانتقال بعد التجربة."},
  {id:"selection",label:"اختيار القوالب",title:"حدّد ما تريد استخدامه في رُزمتك",text:"عندما يناسبك التصميم، اضغط زر التحديد لإضافته إلى اختياراتك. يمكنك تحديد أكثر من قالب، والضغط مرة أخرى لإلغاء أي اختيار. لن تحدد الجولة أي تصميم تلقائياً.",target:"#gvSelectBtn",targetLabel:"زر تحديد القالب",note:"يمكنك تجربة التحديد بنفسك؛ سيظهر عدد القوالب المختارة بعد تنفيذ اختيارك."},
  {id:"audio",label:"إعداد الصوت",title:"اختر الصوت واضبط طريقة النطق",text:"من إعدادات الصوت يمكنك اختيار صوت الإنجليزية والعربية، وتعديل السرعة والنغمة والفواصل. ابدأ من قائمة اختيار الصوت، ثم جرّب النطق من زر المعاينة عندما تكون مستعداً.",target:"#gAudioPanelBody select",targetLabel:"قائمة اختيار الصوت",note:"هذه الإعدادات تُستخدم عند تجهيز الرزمة. لن يبدأ تشغيل أي صوت إلا عندما تطلب ذلك."},
  {id:"export",label:"مراجعة الرزمة",title:"تأكّد من اختياراتك قبل إنشاء الملف",text:"راجع اسم الرزمة، والقوالب التي حددتها، وإعدادات الصوت والخيارات المتاحة. فتح شاشة المراجعة لا ينشئ الملف؛ لا يبدأ إنشاء APKG إلا إذا ضغطت أنت زر بدء التصدير. وبعد التنزيل، اتبع قسم «كيفية الاستيراد إلى Anki» أسفل الصفحة.",target:"#exOpenBtn",targetLabel:"زر مراجعة الرزمة",note:"سنفتح شاشة المراجعة فقط. لن نضغط بدء التصدير ولن ننشئ ملفاً أثناء الجولة."}
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
  }catch(_e){}  try{return sessionStorage.getItem(ONBOARD_SNOOZE_KEY) === "1";}
  catch(_e){return false;}
}
function markOnboardingCompleted(){
  try{localStorage.setItem(ONBOARD_STORAGE_KEY,"1");return true;}
  catch(_e){return false;}
}
function onboardTargetVisible(node){
  if(!node||!node.isConnected)return false;
  var rect=node.getBoundingClientRect();
  var style=window.getComputedStyle(node);
  return rect.width>0&&rect.height>0&&style.display!=="none"&&style.visibility!=="hidden";
}
function onboardStepTarget(step){
  if(!step)return null;
  var selector=(step.id==="export"&&onboardReviewOpened)?"#exportOverlay .fs-close":step.target;
  var target=selector?document.querySelector(selector):null;
  if(!onboardTargetVisible(target)&&step.fallback)target=document.querySelector(step.fallback);
  return onboardTargetVisible(target)?target:null;
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
    if(browser && !browser.classList.contains("open")){
      try{if(typeof gbBuildFilters === "function")gbBuildFilters();}catch(_e){}
      try{if(typeof renderGalleryBrowser === "function")renderGalleryBrowser();}catch(_e){}
      try{if(typeof openGalleryBrowser === "function")openGalleryBrowser();}catch(_e){}
      if(!browser.classList.contains("open")){
        browser.classList.add("open");
        try{document.body.style.overflow="hidden";}catch(_e){}
      }
      onboardOpenedBrowser = browser.classList.contains("open");
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
  var settleDelay=(next===1||next===2||next===4)?460:90;
  window.setTimeout(scheduleOnboardPosition,settleDelay);
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
  var step=ONBOARD_STEPS[onbStep];
  var target=onboardStepTarget(step);
  var card=onboardGuideRoot.querySelector(".og-card");
  var backdrop=onboardGuideRoot.querySelector(".og-backdrop");
  var path=onboardGuideRoot.querySelector("#ogBackdropPath");
  if(!card||!backdrop||!path)return;
  var width=Math.max(320,document.documentElement.clientWidth||window.innerWidth||320);
  var height=Math.max(320,window.innerHeight||document.documentElement.clientHeight||320);
  backdrop.setAttribute("viewBox","0 0 " + width + " " + height);
  if(target&&target.isConnected){
    var fixedOverlay=target.closest(".gallery-browser,.help-overlay,.onboard-overlay");
    var before=target.getBoundingClientRect();
    // Audio controls live inside a wide settings panel. Move the active
    // control near the top of the viewport so the coachmark can occupy the
    // opposite (lower) zone instead of covering the control.
    if(step.id==="audio"&&!fixedOverlay){
      try{
        target.scrollIntoView({behavior:"instant",block:"start",inline:"nearest"});
        var audioRect=target.getBoundingClientRect();
        window.scrollBy(0,audioRect.top-112);
      }catch(_e){
        try{target.scrollIntoView({behavior:"auto",block:"start",inline:"nearest"});}catch(_e2){}
      }
      before=target.getBoundingClientRect();
    }
    var targetOutsideViewport=before.top<0||before.bottom>height;
    if(!fixedOverlay&&targetOutsideViewport){
      try{target.scrollIntoView({behavior:"instant",block:"center",inline:"nearest"});}
      catch(_e){try{target.scrollIntoView({behavior:"auto",block:"center",inline:"nearest"});}catch(_e2){}}
      before=target.getBoundingClientRect();
    }
    onboardActiveTarget=target;
    target.classList.add("og-spotlight");
  }else target=null;
  var rect=target?target.getBoundingClientRect():null;
  path.setAttribute("d",onboardBackdropPath(target,width,height));
  card.style.left="12px";
  card.style.top="12px";
  card.style.right="auto";
  card.style.bottom="auto";
  card.dataset.placement="center";
  var margin=12;
  var baseWidth=Math.min(width-24,width<=640?440:480);
  var widthOptions=[baseWidth,Math.min(width-24,420),Math.min(width-24,380),Math.min(width-24,340)];
  var best=null;
  widthOptions.forEach(function(candidateWidth){
    if(best&&best.overlap===0)return;
    card.style.width=candidateWidth+"px";
    card.style.maxHeight=Math.min(height*.42,460)+"px";
    var measured=card.getBoundingClientRect();
    if(!rect){
      best={left:Math.max(margin,(width-measured.width)/2),top:Math.max(margin,(height-measured.height)/2),name:"center",overlap:0};
      return;
    }
    var centeredLeft=Math.max(margin,(width-measured.width)/2);
    var centeredTop=Math.max(margin,(height-measured.height)/2);
    var candidates=[
      {left:centeredLeft,top:margin,name:"top-center"},
      {left:centeredLeft,top:height-measured.height-margin,name:"bottom-center"},
      {left:margin,top:centeredTop,name:"middle-left"},
      {left:width-measured.width-margin,top:centeredTop,name:"middle-right"},
      {left:margin,top:margin,name:"top-left"},
      {left:width-measured.width-margin,top:margin,name:"top-right"},
      {left:margin,top:height-measured.height-margin,name:"bottom-left"},
      {left:width-measured.width-margin,top:height-measured.height-margin,name:"bottom-right"}
    ];
    candidates.forEach(function(candidate){
      var left=Math.max(margin,Math.min(width-measured.width-margin,candidate.left));
      var top=Math.max(margin,Math.min(height-measured.height-margin,candidate.top));
      var overlapW=Math.max(0,Math.min(left+measured.width,rect.right)-Math.max(left,rect.left));
      var overlapH=Math.max(0,Math.min(top+measured.height,rect.bottom)-Math.max(top,rect.top));
      var overlap=overlapW*overlapH;
      var distance=Math.abs((left+measured.width/2)-(rect.left+rect.width/2))+Math.abs((top+measured.height/2)-(rect.top+rect.height/2));
      var candidateScore=overlap*1000000+distance;
      if(!best||candidateScore<best.score)best={left:left,top:top,name:candidate.name,overlap:overlap,score:candidateScore};
    });
  });
  if(best){
    card.style.left=best.left+"px";
    card.style.top=best.top+"px";
    card.dataset.placement=best.name;
  }}
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
  var title = review ? "راجع إعدادات رُزمتك قبل إنشائها" : step.title;
  var body = review ? "في نافذة المراجعة، تأكد من اسم الرزمة والقوالب التي اخترتها وإعدادات الصوت وخيارات التضمين. يمكنك إغلاق النافذة والعودة إلى المعرض لإجراء أي تعديل." : step.text;
  var targetLabel = review ? "زر إغلاق نافذة المراجعة" : step.targetLabel;
  var note = review ? "هذه مراجعة فقط؛ لم يبدأ إنشاء ملف APKG. لن يبدأ إلا عندما تضغط «بدء التصدير» بنفسك." : step.note;
  var primaryLabel = onbStep === 0 ? "ابدأ الجولة" :
    onbStep === 1 ? "تابع إلى المعاينة" :
    onbStep === 2 ? "جرّب قلب البطاقة" :
    onbStep === 3 ? "انتقل إلى إعدادات الصوت" :
    onbStep === 4 ? "انتقل إلى مراجعة الرزمة" :
    (review ? "إنهاء الجولة" : "افتح شاشة المراجعة");
  var primaryAction = onbStep === 0 ? "start" :
    onbStep === 1 ? "preview" :
    onbStep === 2 ? "flip" :
    onbStep === 3 ? "audio" :
    onbStep === 4 ? "export" :
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
  card.setAttribute("role","dialog");
  card.setAttribute("aria-modal","false");
  card.setAttribute("aria-labelledby","onboardGuideTitle");
  card.setAttribute("aria-describedby","onboardGuideText");

  var head = onboardNode("div","og-head");
  var brand = onboardNode("div","og-brand");
  brand.appendChild(onboardNode("span","og-mark","A"));
  var brandCopy = onboardNode("span","og-brand-copy");
  brandCopy.appendChild(onboardNode("strong","","ANKI DESIGN STUDIO"));
  brandCopy.appendChild(onboardNode("small","","جولة عملية • ٦ محطات"));
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
  if(action === "preview"){goToOnboardStep(2);return;}
  if(action === "flip"){
    if(typeof gvFlip === "function")gvFlip();
    window.setTimeout(function(){if(onboardGuideOpen && onbStep === 2)goToOnboardStep(3);},240);
    return;
  }
  if(action === "audio"){goToOnboardStep(4);return;}
  if(action === "export"){goToOnboardStep(5);return;}
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
  onboardOpenedBrowser = false;  var audio = document.getElementById("gAudioPanelBody");
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
    window.setTimeout(function(){if(onboardGuideOpen && onbStep === 2)goToOnboardStep(3);},220);
    return;
  }
  if(onbStep === 3 && target.closest("#gvSelectBtn")){
    window.setTimeout(function(){
      if(!onboardGuideOpen || onbStep !== 3)return;
      var note = document.getElementById("onboardGuideNote");
      var count = (typeof gvSel !== "undefined" && gvSel) ? gvSel.length : 0;
      if(note)note.textContent = count ? "تم تحديث الاختيار فعليًا. عدد القوالب المحددة الآن: " + count + "." : "أُزيل تحديد القالب الحالي. يمكنك اختياره مجددًا أو متابعة الجولة.";
    },40);
    return;
  }
  if(onbStep === 4 && target.closest("#gTtsPreviewBtn")){
    window.setTimeout(function(){
      if(!onboardGuideOpen || onbStep !== 4)return;
      var note = document.getElementById("onboardGuideNote");
      if(note)note.textContent = "بدأت معاينة الصوت بطلب منك. استمع إلى النطق، ثم تابع عندما تنتهي.";
    },40);
    return;
  }
  if(onbStep === 5 && target.closest("#exOpenBtn")){
    window.setTimeout(function(){
      if(onboardGuideOpen && onbStep === 5){
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
    if(onbStep === 5 && exportOverlay && exportOverlay.classList.contains("on") && typeof closeExport === "function"){
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
    if(onboardGuideOpen && onbStep === 5 && onboardReviewOpened){
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