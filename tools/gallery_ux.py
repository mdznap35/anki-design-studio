"""Deterministic UX transforms for the four generated non-Bac gallery pages."""
import re

TOUR_CSS = r"""
#onboardOverlay[hidden]{display:none!important}
#onboardGuideRoot{position:fixed;inset:0;z-index:2147483000;pointer-events:none;direction:rtl;color:#f8fafc}
#onboardGuideRoot .og-card{position:fixed;right:max(14px,env(safe-area-inset-right,0px));bottom:max(14px,env(safe-area-inset-bottom,0px));width:min(430px,calc(100vw - 28px));max-height:min(44dvh,390px);overflow:auto;overscroll-behavior:contain;padding:20px;border:1px solid rgba(167,139,250,.34);border-radius:22px;background:linear-gradient(145deg,rgba(17,21,38,.985),rgba(8,12,25,.99));box-shadow:0 24px 80px rgba(0,0,0,.48),0 0 0 1px rgba(255,255,255,.045) inset,0 0 36px rgba(99,102,241,.12);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);pointer-events:auto;scrollbar-width:thin;animation:ogEnter .24s cubic-bezier(.2,.8,.2,1) both}
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
#onboardGuideRoot .og-footer{display:flex;align-items:center;justify-content:space-between;gap:10px;margin-top:15px;padding-top:13px;border-top:1px solid rgba(255,255,255,.09)}
#onboardGuideRoot .og-skip{border:0;background:none;color:#9ca3b8;font:inherit;font-size:.73rem;text-decoration:underline;text-underline-offset:4px;cursor:pointer}
#onboardGuideRoot .og-skip:hover{color:#e2e8f0}
#onboardGuideRoot .og-actions{display:flex;align-items:center;gap:8px}
#onboardGuideRoot .og-btn{display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:42px;padding:9px 15px;border:1px solid rgba(255,255,255,.13);border-radius:12px;font:inherit;font-size:.77rem;font-weight:900;cursor:pointer;transition:transform .16s,box-shadow .16s,background .16s}
#onboardGuideRoot .og-btn:hover{transform:translateY(-1px)}
#onboardGuideRoot .og-btn.primary{border-color:transparent;background:linear-gradient(110deg,#6d28d9,#4f46e5 58%,#0e7490);color:#fff;box-shadow:0 9px 22px rgba(79,70,229,.25)}
#onboardGuideRoot .og-btn.ghost{background:rgba(255,255,255,.045);color:#dbeafe}
#onboardGuideRoot .og-spotlight{position:relative!important;z-index:2147482998!important;outline:3px solid #67e8f9!important;outline-offset:6px!important;border-radius:14px!important;box-shadow:0 0 0 9px rgba(34,211,238,.15),0 16px 48px rgba(0,0,0,.28)!important;transition:outline-color .18s,box-shadow .18s}
@media(max-width:640px){
#onboardGuideRoot .og-card{left:10px;right:10px;bottom:calc(env(safe-area-inset-bottom,0px) + 10px);width:auto;max-height:min(43dvh,350px);padding:16px;border-radius:19px}
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
"""

TOUR_JS = r"""
var ONBOARD_DECK = "__DECK__";
var ONBOARD_PRIMARY_LANGUAGE = ONBOARD_DECK === "fr9" ? "الفرنسية" : "الإنجليزية";
var ONBOARD_STORAGE_KEY = "anki_" + ONBOARD_DECK + "_onboarded";
var ONBOARD_STEPS = [
  {id:"start",label:"ابدأ هنا",title:"من القالب إلى رزمة Anki — بخطوات واضحة",text:"هذه ليست نافذة شرح منفصلة. سنمشي داخل المعرض نفسه: افتح المكتبة، جرّب المعاينة، افهم التحديد، اضبط الصوت، ثم راجع إعدادات التصدير. لن تُنشأ أي رزمة أثناء الجولة.",target:".hero-cta-main",targetLabel:"زر «استعرض القوالب»",note:"ستبقى أدوات الصفحة قابلة للاستخدام، ويمكنك إغلاق الجولة أو إعادة فتحها متى شئت."},
  {id:"library",label:"المكتبة",title:"استكشف القوالب الحقيقية — لا صورًا تجريبية",text:"هذه هي مكتبة التصاميم الفعلية. استخدم التصنيفات لتقليل الخيارات، وتصفّح الصور المصغّرة، ثم اضغط أي قالب لترى معاينته في الصفحة. اختيار قالب هنا يبدّل المعاينة فقط؛ لا ينشئ ملفًا.",target:"#gbGrid .gb-item",fallback:"#gbGrid",targetLabel:"بطاقة حقيقية من شبكة القوالب",note:"جرّب اختيار قالب من الشبكة؛ ستنتقل الجولة تلقائيًا إلى معاينته."},
  {id:"preview",label:"المعاينة",title:"افحص البطاقة كما ستظهر فعلًا",text:"هذه معاينة القالب الحقيقي داخل إطار البطاقة. راجع وضوح النص والمسافات، وتنقّل بين التصاميم بالأسهم. جرّب زر «قلب البطاقة» لترى الوجه الآخر قبل أن تعتمد التصميم.",target:"#gvShowAns",fallback:"#gvStage",targetLabel:"زر «قلب البطاقة»",note:"قلب البطاقة يغيّر المعاينة فقط، ولا يغيّر محتوى رُزمتك."},
  {id:"selection",label:"التحديد",title:"اختر القوالب التي تريد استخدامها",text:"زر «تحديد» يضيف القالب الحالي إلى اختياراتك أو يزيله منها. يمكنك تحديد قالب واحد أو عدة قوالب؛ وستظهر حالة الاختيار وعدد القوالب في شريط التحديد. لا يحدث أي تصدير هنا.",target:"#gvSelectBtn",targetLabel:"زر تحديد القالب",note:"الجولة لا تحدّد قوالب نيابةً عنك؛ أي تغيير تجريه هنا يكون باختيارك."},
  {id:"audio",label:"الصوت",title:"اضبط نطق " + ONBOARD_PRIMARY_LANGUAGE + " والعربية",text:"من هذه اللوحة تختار صوت اللغة الأساسية والعربية، وتعدّل السرعة والنغمة والفواصل. يمكنك تشغيل معاينة الصوت بنفسك عند توفر اتصال مناسب؛ الجولة لن تطلب ملفات صوتية أو تشغّل طلبات شبكة تلقائيًا.",target:"#gTtsPreviewBtn",fallback:"#gAudioPanelBody",targetLabel:"زر معاينة الصوت",note:"للمعرض الفرنسي اللغة الأساسية هي الفرنسية، وللمعارض الإنجليزية هي الإنجليزية."},
  {id:"export",label:"مراجعة التصدير",title:"راجع الإعدادات قبل إنشاء الرزمة",text:"هذا الزر يفتح شاشة مراجعة اسم الرزمة والقوالب والصوت والحجم المتوقع. فتح شاشة المراجعة لا ينشئ ملفًا؛ إنشاء APKG يبدأ فقط عند ضغط «بدء التصدير» بنفسك.",target:"#exOpenBtn",targetLabel:"زر «تصدير رزمة Anki»",note:"سنفتح شاشة الملخص عند طلبك، لكننا لن نضغط «بدء التصدير» ولن ننشئ ملفًا ضمن الجولة."}
];
var onbStep = 0;
var onboardGuideOpen = false;
var onboardGuideRoot = null;
var onboardGuideReturnFocus = null;
var onboardActiveTarget = null;
var onboardReviewOpened = false;

function escapeOnboardText(value){
  return String(value == null ? "" : value).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;").replace(/"/g,"&quot;").replace(/'/g,"&#39;");
}
function isOnboardingCompleted(){
  try{return localStorage.getItem(ONBOARD_STORAGE_KEY) === "1";}
  catch(_e){return false;}
}
function markOnboardingCompleted(){
  try{localStorage.setItem(ONBOARD_STORAGE_KEY,"1");}
  catch(_e){}
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
    if(browser && !browser.classList.contains("open") && typeof openGalleryBrowser === "function")openGalleryBrowser();
  }else if(browser && browser.classList.contains("open") && typeof closeGalleryBrowser === "function"){
    closeGalleryBrowser();
  }
  if(index === 4){
    var audio = document.getElementById("gAudioPanelBody");
    if(audio && !audio.classList.contains("open") && typeof toggleAudioPanel === "function")toggleAudioPanel();
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
  window.setTimeout(positionOnboardGuide,90);
}
function positionOnboardGuide(){
  if(!onboardGuideOpen || !onboardGuideRoot)return;
  onboardClearSpotlight();
  var step = ONBOARD_STEPS[onbStep];
  var target = onboardStepTarget(step);
  var card = onboardGuideRoot.querySelector(".og-card");
  if(!card)return;
  card.style.top = "auto";
  card.style.bottom = "max(14px,env(safe-area-inset-bottom,0px))";
  if(target){
    onboardActiveTarget = target;
    target.classList.add("og-spotlight");
    try{target.scrollIntoView({behavior:window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth",block:"center",inline:"nearest"});}catch(_e){}
    var rect = target.getBoundingClientRect();
    if(rect.bottom > window.innerHeight * 0.54){
      card.style.bottom = "auto";
      card.style.top = "max(14px,env(safe-area-inset-top,0px))";
    }
  }
}
function renderOnboardStep(){
  if(!onboardGuideOpen)return;
  var root = onboardEnsureRoot();
  var step = ONBOARD_STEPS[onbStep];
  if(!step)return;
  var review = step.id === "export" && onboardReviewOpened;
  var progress = "";
  ONBOARD_STEPS.forEach(function(item,index){
    progress += '<button type="button" data-guide-step="' + index + '" class="' + (index <= onbStep ? "done" : "") + '" aria-label="الانتقال إلى المحطة ' + (index+1) + ': ' + escapeOnboardText(item.label) + '" aria-current="' + (index === onbStep ? "step" : "false") + '"><span></span></button>';
  });
  var title = review ? "هكذا تبدو مراجعة الرزمة قبل الإنشاء" : step.title;
  var body = review ? "راجع اسم الرزمة، وعدد القوالب المختارة، وإعدادات الصوت وخيارات التضمين. يمكنك إغلاق النافذة والعودة للتعديل. تذكير: لن يبدأ الإنشاء حتى تضغط زر «بدء التصدير» بنفسك." : step.text;
  var targetLabel = review ? "ملخص إعدادات الرزمة" : step.targetLabel;
  var note = review ? "لم نضغط زر بدء التصدير، ولم يُرسل طلب إنشاء APKG." : step.note;
  var primaryLabel = onbStep === 0 ? "ابدأ الجولة" :
    onbStep === 1 ? "انتقل إلى المعاينة" :
    onbStep === 2 ? "جرّب قلب البطاقة" :
    onbStep === 3 ? "تابع إلى إعدادات الصوت" :
    onbStep === 4 ? "تابع إلى التصدير" :
    (review ? "إنهاء الجولة" : "افتح شاشة المراجعة");
  var primaryAction = onbStep === 0 ? "start" :
    onbStep === 1 ? "preview" :
    onbStep === 2 ? "flip" :
    onbStep === 3 ? "audio" :
    onbStep === 4 ? "export" :
    (review ? "finish" : "review");
  var previous = onbStep > 0 ? '<button class="og-btn ghost" type="button" data-guide-action="previous">السابق</button>' : "";
  root.innerHTML =
    '<section class="og-card" role="dialog" aria-modal="false" aria-labelledby="onboardGuideTitle" aria-describedby="onboardGuideText">' +
      '<div class="og-head"><div class="og-brand"><span class="og-mark" aria-hidden="true">A</span><span class="og-brand-copy"><strong>ANKI DESIGN STUDIO</strong><small>جولة داخل المعرض • ٦ محطات</small></span></div><button class="og-close" type="button" data-guide-action="close" aria-label="إغلاق الجولة">×</button></div>' +
      '<nav class="og-progress" aria-label="محطات الجولة">' + progress + '</nav>' +
      '<div class="og-meta"><span class="og-step-label">' + escapeOnboardText(step.label) + '</span><span class="og-count">المحطة ' + (onbStep+1) + ' من ' + ONBOARD_STEPS.length + '</span></div>' +
      '<h2 class="og-title" id="onboardGuideTitle" tabindex="-1">' + escapeOnboardText(title) + '</h2>' +
      '<p class="og-text" id="onboardGuideText" aria-live="polite">' + escapeOnboardText(body) + '</p>' +
      '<div class="og-target"><span class="og-target-mark" aria-hidden="true">◎</span><span class="og-target-copy"><small>الأداة الفعلية على الصفحة</small><strong>' + escapeOnboardText(targetLabel) + '</strong></span></div>' +
      '<p class="og-note">' + escapeOnboardText(note) + '</p>' +
      '<div class="og-footer"><button class="og-skip" type="button" data-guide-action="close">إنهاء / تخطي</button><div class="og-actions">' + previous + '<button class="og-btn primary" type="button" data-guide-action="' + primaryAction + '">' + escapeOnboardText(primaryLabel) + '</button></div></div>' +
    '</section>';
  var heading = root.querySelector("#onboardGuideTitle");
  if(heading && typeof heading.focus === "function")heading.focus({preventScroll:true});
}
function handleOnboardAction(action){
  if(action === "close" || action === "finish"){closeOnboarding();return;}
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
    onboardReviewOpened = true;
    renderOnboardStep();
    window.setTimeout(positionOnboardGuide,120);
  }
}
function showOnboarding(){
  if(onboardGuideOpen)return;
  onboardGuideReturnFocus = document.activeElement;
  onboardGuideOpen = true;
  onboardReviewOpened = false;
  var launcher = document.getElementById("onboardTourLauncher");
  if(launcher)launcher.hidden = true;
  onboardEnsureRoot();
  goToOnboardStep(0);
}
function closeOnboarding(){
  if(!onboardGuideOpen)return;
  onboardGuideOpen = false;
  onboardClearSpotlight();
  var browser = document.getElementById("galleryBrowser");
  if(browser && browser.classList.contains("open") && typeof closeGalleryBrowser === "function")closeGalleryBrowser();
  if(onboardGuideRoot && onboardGuideRoot.parentNode)onboardGuideRoot.parentNode.removeChild(onboardGuideRoot);
  onboardGuideRoot = null;
  markOnboardingCompleted();
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
  if(onbStep === 5 && target.closest("#exOpenBtn")){
    window.setTimeout(function(){
      if(onboardGuideOpen && onbStep === 5){
        onboardReviewOpened = true;
        renderOnboardStep();
        positionOnboardGuide();
      }
    },120);
  }
});
document.addEventListener("keydown",function(event){
  if(!onboardGuideOpen)return;
  if(event.key === "Escape"){event.preventDefault();closeOnboarding();return;}
  var target = event.target;
  var typing = target && (target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.tagName === "SELECT" || target.isContentEditable);
  if(typing || event.altKey || event.ctrlKey || event.metaKey)return;
  if(event.key === "ArrowLeft" && onbStep < ONBOARD_STEPS.length-1){event.preventDefault();goToOnboardStep(onbStep+1);}
  else if(event.key === "ArrowRight" && onbStep > 0){event.preventDefault();goToOnboardStep(onbStep-1);}
});
window.addEventListener("resize",function(){if(onboardGuideOpen)positionOnboardGuide();});
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
          renderOnboardStep();
          positionOnboardGuide();
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
    new_init = "if(!isOnboardingCompleted())setTimeout(showOnboarding,80);"
    html = _replace_once(html, old_init, new_init, deck + " delayed first-visit tour")

    launcher_html = '<button id="onboardTourLauncher" type="button" onclick="showOnboarding()" aria-label="إعادة فتح الجولة السريعة"><span aria-hidden="true">✦</span><span>الجولة السريعة</span></button>\n'
    html, launcher_inserted = re.subn(r"</body\s*>", launcher_html + "</body>", html, count=1, flags=re.I)
    if launcher_inserted != 1:
        raise SystemExit(deck + " could not add the persistent quick-tour launcher")

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
