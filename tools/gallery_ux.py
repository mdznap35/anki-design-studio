"""Clean, task-led onboarding for the four generated non-Bac galleries."""
import re

TOUR_CSS = r"""
#onboardTourLauncher{position:fixed;z-index:2147483001;right:22px;bottom:20px;display:inline-flex;align-items:center;justify-content:center;gap:10px;min-height:48px;padding:0 18px;border:1px solid rgba(177,196,219,.22);border-radius:999px;background:#18334b;color:#f4f8fc;font:inherit;font-size:.78rem;font-weight:850;box-shadow:0 12px 34px rgba(5,14,27,.28);cursor:pointer;transition:background .18s,transform .18s}
#onboardTourLauncher:hover{background:#244c68;transform:translateY(-2px)}
#onboardTourLauncher:focus-visible,#onboardGuideRoot button:focus-visible{outline:3px solid #62c7bc;outline-offset:3px}
#onboardTourLauncher[hidden]{display:none!important}
#onboardGuideRoot{position:fixed;inset:0;z-index:2147483000;pointer-events:none;direction:rtl;color:#f5f8fb}
#onboardGuideRoot .og-card{position:absolute;left:50%;top:var(--og-safe-top,82px);bottom:auto;width:min(760px,calc(100vw - 28px));max-height:min(320px,42dvh);overflow:auto;transform:translateX(-50%);padding:15px 18px 13px;border:1px solid rgba(161,190,211,.28);border-radius:16px;background:#10243a;box-shadow:0 18px 58px rgba(0,0,0,.32);pointer-events:auto;scrollbar-width:thin}
#onboardGuideRoot[data-placement="top"] .og-card{top:var(--og-safe-top,82px);bottom:auto}
#onboardGuideRoot[data-placement="bottom"] .og-card{bottom:max(24px,env(safe-area-inset-bottom,0px));top:auto}
#onboardGuideRoot .og-head{display:flex;align-items:center;gap:12px;margin-bottom:9px}
#onboardGuideRoot .og-brand{display:flex;align-items:center;gap:9px;min-width:0}
#onboardGuideRoot .og-mark{display:grid;place-items:center;width:31px;height:31px;flex:0 0 auto;border-radius:9px;background:#28506b;color:#e9f7f6;font-size:.76rem;font-weight:950}
#onboardGuideRoot .og-brand-copy{display:grid;gap:2px}
#onboardGuideRoot .og-brand-copy strong{font-size:.64rem;letter-spacing:.12em;color:#e8f0f6}
#onboardGuideRoot .og-brand-copy small{font-size:.61rem;color:#91a8bc}
#onboardGuideRoot .og-meta{margin-inline-start:auto;color:#a9c1d1;font-size:.65rem}
#onboardGuideRoot .og-close{width:44px;height:44px;min-width:44px;border:1px solid rgba(190,211,228,.2);border-radius:8px;background:transparent;color:#dce8f1;font-size:1rem;cursor:pointer}
#onboardGuideRoot .og-progress{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:5px;margin:0 0 10px}
#onboardGuideRoot .og-progress button{min-width:0;padding:0;border:0;background:transparent;cursor:pointer}
#onboardGuideRoot .og-progress button span{display:block;height:3px;border-radius:8px;background:rgba(200,218,233,.18)}
#onboardGuideRoot .og-progress button.done span{background:#5aafa5}
#onboardGuideRoot .og-progress button[aria-current="step"] span{height:4px;background:#81c9be}
#onboardGuideRoot .og-content{display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:5px 20px}
#onboardGuideRoot .og-step-label{color:#80c9bd;font-size:.66rem;font-weight:850}
#onboardGuideRoot .og-title{margin:2px 0 3px;color:#f8fbfd;font-size:clamp(1rem,1.8vw,1.27rem);font-weight:900;line-height:1.45}
#onboardGuideRoot .og-text{grid-column:1;margin:0;color:#c0cedb;font-size:.75rem;line-height:1.75}
#onboardGuideRoot .og-target{grid-column:1;margin:4px 0 0;color:#8fa9bf;font-size:.65rem}
#onboardGuideRoot .og-note{grid-column:1;margin:4px 0 0;color:#8bc7be;font-size:.65rem;line-height:1.6}
#onboardGuideRoot .og-footer{grid-column:2;grid-row:1 / span 4;display:flex;align-items:center;gap:7px}
#onboardGuideRoot .og-actions{display:flex;gap:7px}
#onboardGuideRoot .og-btn{min-height:48px;padding:0 13px;border:1px solid rgba(182,205,225,.2);border-radius:9px;background:#1a354e;color:#eaf2f8;font:inherit;font-size:.69rem;font-weight:850;cursor:pointer}
#onboardGuideRoot .og-btn.primary{border-color:#477b7b;background:#2b7774;color:#fff}
#onboardGuideRoot .og-skip{border:0;background:transparent;color:#9cb0c2;font:inherit;font-size:.65rem;text-decoration:underline;text-underline-offset:3px;cursor:pointer}
body .og-spotlight{position:relative!important;z-index:2147482998!important;outline:2px solid #69c2b6!important;outline-offset:4px!important;box-shadow:0 0 0 7px rgba(91,183,170,.14)!important;border-radius:10px!important}
@media(max-width:640px){
 #onboardTourLauncher{right:12px;bottom:max(12px,env(safe-area-inset-bottom,0px));min-height:44px;padding:0 14px}
 #onboardGuideRoot .og-card{width:calc(100vw - 20px);max-height:min(300px,42dvh);padding:12px;border-radius:13px}
 #onboardGuideRoot .og-head{margin-bottom:7px}
 #onboardGuideRoot .og-content{grid-template-columns:minmax(0,1fr);gap:3px}
 #onboardGuideRoot .og-footer{grid-column:1;grid-row:auto;justify-content:space-between;margin-top:8px}
 #onboardGuideRoot .og-title{font-size:.98rem}
 #onboardGuideRoot .og-text{font-size:.7rem;line-height:1.6}
 #onboardGuideRoot .og-target,#onboardGuideRoot .og-note{font-size:.61rem}
 #onboardGuideRoot .og-btn{min-height:48px;padding:0 13px;font-size:.68rem}
}
@media(prefers-reduced-motion:reduce){#onboardGuideRoot *,#onboardTourLauncher{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
"""

TOUR_JS = r"""
var ONBOARD_DECK = "__DECK__";
var ONBOARD_PRIMARY_LANGUAGE = ONBOARD_DECK === "fr9" ? "الفرنسية" : "الإنجليزية";
var ONBOARD_STORAGE_KEY = "anki_" + ONBOARD_DECK + "_onboarded_v6";
var ONBOARD_SNOOZE_KEY = "anki_" + ONBOARD_DECK + "_onboarding_snoozed_v6";
var ONBOARD_STEPS = [
  {id:"start",label:"الدخول",title:"ابدأ من مكتبة التصاميم",text:"افتح المكتبة لتشاهد القوالب المئة كما هي، في شبكة واحدة واضحة. لا توجد تصنيفات أو قوائم فرز تقطع عليك الاستعراض.",target:".hero-cta-main",targetLabel:"فتح مكتبة القوالب",note:"لن يتغير أي اختيار في رُزمتك عند فتح المكتبة."},
  {id:"library",label:"الاستعراض",title:"اختر تصميماً لتفحصه",text:"تصفّح الشبكة كاملة. اضغط على أي بطاقة لفتح معاينتها الكبيرة؛ فتح المعاينة لا يعني اعتماد القالب.",target:"#gbGrid .gb-item",targetLabel:"أي بطاقة في شبكة القوالب",note:"كل القوالب المئة متاحة في هذه الشبكة."},
  {id:"preview",label:"المعاينة",title:"افحص وجهي البطاقة",text:"راجع طريقة ظهور المفردة والمعنى، ثم اقلب البطاقة من زرها الحقيقي. انتبه إلى وضوح النص والمسافات وترتيب العناصر.",target:"#gvShowAns",fallback:"#fsFlipBtn",targetLabel:"زر قلب البطاقة",note:"هذه معاينة للقالب وليست تغييراً في بيانات المفردات."},
  {id:"selection",label:"الاعتماد",title:"أضف التصميم الذي اخترته",text:"بعد أن ترتاح إلى شكل البطاقة، استخدم زر التحديد. يمكنك العودة إلى المعرض وفحص تصاميم أخرى قبل المتابعة.",target:"#gvSelectBtn",targetLabel:"زر تحديد القالب",note:"التحديد وحده هو الذي يضيف القالب إلى اختيارات رُزمتك."},
  {id:"audio",label:"الصوت",title:"استمع إلى النطق",text:"افتح إعدادات الصوت، اختر الصوت المناسب لـ" + ONBOARD_PRIMARY_LANGUAGE + " والعربية، ثم اطلب معاينة النطق بنفسك.",target:"#gTtsPreviewBtn",fallback:"#gAudioPanelBody",targetLabel:"معاينة الصوت",note:"لا يبدأ أي تشغيل صوتي من دون ضغطك."},
  {id:"export",label:"المراجعة",title:"راجع الرزمة قبل إنشائها",text:"افتح شاشة المراجعة لتتحقق من القوالب والصوت والإعدادات. هذه الجولة لا تنشئ ملفاً ولا تبدأ التصدير.",target:"#exOpenBtn",targetLabel:"فتح مراجعة الرزمة",note:"لن يبدأ إنشاء APKG إلا من زر التصدير الذي تضغطه بنفسك."}
];
var onbStep = 0;
var onboardGuideOpen = false;
var onboardGuideRoot = null;
var onboardGuideReturnFocus = null;
var onboardActiveTarget = null;
var onboardOpenedBrowser = false;
var onboardOpenedAudio = false;
var onboardPositionFrame = 0;

function isOnboardingCompleted(){try{return localStorage.getItem(ONBOARD_STORAGE_KEY)==="1";}catch(_e){return false;}}
function onboardStepTarget(step){
  if(!step)return null;
  var selectors=[step.target,step.fallback].filter(Boolean);
  for(var i=0;i<selectors.length;i++){
    var node=document.querySelector(selectors[i]);
    if(node&&node.getClientRects().length)return node;
  }
  return null;
}
function onboardClearSpotlight(){
  if(onboardActiveTarget)onboardActiveTarget.classList.remove("og-spotlight");
  onboardActiveTarget=null;
}
function onboardEnsureRoot(){
  if(onboardGuideRoot&&onboardGuideRoot.isConnected)return onboardGuideRoot;
  var root=document.createElement("div");
  root.id="onboardGuideRoot";root.setAttribute("dir","rtl");root.setAttribute("role","presentation");root.dataset.placement="top";
  document.body.appendChild(root);
  root.addEventListener("click",function(event){
    var stepButton=event.target.closest?event.target.closest("[data-guide-step]"):null;
    if(stepButton){var next=parseInt(stepButton.getAttribute("data-guide-step"),10);if(Number.isInteger(next))goToOnboardStep(next);return;}
    var action=event.target.closest?event.target.closest("[data-guide-action]"):null;
    if(action)handleOnboardAction(action.getAttribute("data-guide-action"));
  });
  onboardGuideRoot=root;return root;
}
function onboardPrepareStep(index){
  if(index>=2)document.body.classList.add("gx-selection-ready");
  var preview=document.getElementById("gv");
  if(index>=2&&preview)preview.classList.add("gx-visible");
  var browser=document.getElementById("galleryBrowser");
  if(index===1&&browser&&!browser.classList.contains("open")){
    try{if(typeof ensureGalleryDesigns==="function")ensureGalleryDesigns();}catch(_e){}
    try{if(typeof gbBuildFilters==="function")gbBuildFilters();}catch(_e){}
    try{if(typeof renderGalleryBrowser==="function")renderGalleryBrowser();}catch(_e){}
    try{if(typeof openGalleryBrowser==="function")openGalleryBrowser();}catch(_e){}
    onboardOpenedBrowser=browser.classList.contains("open");
  }else if(index!==1&&onboardOpenedBrowser&&browser&&browser.classList.contains("open")&&typeof closeGalleryBrowser==="function"){
    closeGalleryBrowser();onboardOpenedBrowser=false;
  }
  var audio=document.getElementById("gAudioPanelBody");
  if(index===4&&audio&&!audio.classList.contains("open")&&typeof toggleAudioPanel==="function"){
    toggleAudioPanel();onboardOpenedAudio=true;
  }else if(index!==4&&onboardOpenedAudio&&audio&&audio.classList.contains("open")&&typeof toggleAudioPanel==="function"){
    toggleAudioPanel();onboardOpenedAudio=false;
  }
}
function onboardNode(tag,className,value){
  var node=document.createElement(tag);if(className)node.className=className;
  if(value!==undefined&&value!==null)node.textContent=String(value);
  return node;
}
function renderOnboardStep(){
  if(!onboardGuideOpen)return;
  var root=onboardEnsureRoot(),step=ONBOARD_STEPS[onbStep];
  var card=onboardNode("section","og-card");card.setAttribute("role","dialog");card.setAttribute("aria-modal","false");
  card.setAttribute("aria-labelledby","onboardGuideTitle");card.setAttribute("aria-describedby","onboardGuideText");
  var head=onboardNode("header","og-head"),brand=onboardNode("div","og-brand");
  brand.appendChild(onboardNode("span","og-mark","A"));
  var brandCopy=onboardNode("span","og-brand-copy");brandCopy.appendChild(onboardNode("strong","","ANKI DESIGN STUDIO"));
  brandCopy.appendChild(onboardNode("small","","دليل داخل المعرض"));brand.appendChild(brandCopy);
  head.appendChild(brand);head.appendChild(onboardNode("span","og-meta","المرحلة "+(onbStep+1)+" من "+ONBOARD_STEPS.length));
  var close=onboardNode("button","og-close","×");close.type="button";close.setAttribute("aria-label","إغلاق الجولة");close.setAttribute("data-guide-action","close");head.appendChild(close);card.appendChild(head);
  var progress=onboardNode("nav","og-progress");progress.setAttribute("aria-label","مراحل الجولة");
  ONBOARD_STEPS.forEach(function(item,index){
    var button=onboardNode("button",index<onbStep?"done":"");button.type="button";
    button.setAttribute("data-guide-step",String(index));button.setAttribute("aria-label","المرحلة "+(index+1)+": "+item.label);
    button.setAttribute("aria-current",index===onbStep?"step":"false");button.appendChild(onboardNode("span","", ""));progress.appendChild(button);
  });card.appendChild(progress);
  var content=onboardNode("div","og-content");content.appendChild(onboardNode("span","og-step-label",step.label));
  var title=onboardNode("h2","og-title",step.title);title.id="onboardGuideTitle";title.tabIndex=-1;content.appendChild(title);
  var description=onboardNode("p","og-text",step.text);description.id="onboardGuideText";description.setAttribute("aria-live","polite");content.appendChild(description);
  content.appendChild(onboardNode("p","og-target","المكان الذي ستستخدمه: "+step.targetLabel));
  var note=onboardNode("p","og-note",step.note);note.id="onboardGuideNote";note.setAttribute("role","status");note.setAttribute("aria-live","polite");content.appendChild(note);
  var footer=onboardNode("footer","og-footer"),skip=onboardNode("button","og-skip","إنهاء الجولة");
  skip.type="button";skip.setAttribute("data-guide-action","close");footer.appendChild(skip);
  var actions=onboardNode("div","og-actions");
  if(onbStep>0){var back=onboardNode("button","og-btn","السابق");back.type="button";back.setAttribute("data-guide-action","previous");actions.appendChild(back);}
  var next=onboardNode("button","og-btn primary",onbStep===0?"افتح المكتبة":(onbStep===5?"إنهاء":"التالي"));
  next.type="button";next.setAttribute("data-guide-action",onbStep===0?"start":(onbStep===5?"finish":"next"));actions.appendChild(next);
  footer.appendChild(actions);content.appendChild(footer);card.appendChild(content);
  root.replaceChildren(card);title.focus({preventScroll:true});
}
function positionOnboardGuide(){
  if(!onboardGuideOpen||!onboardGuideRoot)return;
  var header=document.querySelector("header.hdr, .hdr");
  var headerBottom=header?Math.max(0,header.getBoundingClientRect().bottom):70;
  onboardGuideRoot.style.setProperty("--og-safe-top",Math.ceil(Math.max(12,headerBottom+12))+"px");
  onboardClearSpotlight();
  var target=onboardStepTarget(ONBOARD_STEPS[onbStep]);
  if(target){
    var context=onbStep===0?target.closest("#gallery-experience-hero"):null;
    if(context){
      var contextRect=context.getBoundingClientRect();
      if(contextRect.top<headerBottom+12){
        var html=document.documentElement,body=document.body;
        var htmlScroll=html.style.scrollBehavior,bodyScroll=body.style.scrollBehavior;
        html.style.scrollBehavior="auto";body.style.scrollBehavior="auto";
        try{window.scrollTo(0,Math.max(0,window.scrollY+contextRect.top-headerBottom-12));}
        finally{html.style.scrollBehavior=htmlScroll;body.style.scrollBehavior=bodyScroll;}
      }
    }
    var before=target.getBoundingClientRect();
    var targetOutsideViewport=before.top<0||before.bottom>window.innerHeight;
    if(targetOutsideViewport){
      var scrollStyles=[],ancestor=target;
      while(ancestor&&ancestor.nodeType===1){
        scrollStyles.push([ancestor,ancestor.style.scrollBehavior]);
        ancestor.style.scrollBehavior="auto";
        ancestor=ancestor.parentElement;
      }
      try{target.scrollIntoView({behavior:"auto",block:"center",inline:"nearest"});}
      finally{for(var restoreIndex=scrollStyles.length-1;restoreIndex>=0;restoreIndex--)scrollStyles[restoreIndex][0].style.scrollBehavior=scrollStyles[restoreIndex][1];}
    }
    onboardActiveTarget=target;target.classList.add("og-spotlight");
    var rect=target.getBoundingClientRect();
    onboardGuideRoot.dataset.placement=onbStep===0?"bottom":(rect.top>window.innerHeight*.48?"top":"bottom");
  }else onboardGuideRoot.dataset.placement="bottom";
}
function scheduleOnboardPosition(){
  if(!onboardGuideOpen||onboardPositionFrame)return;
  var raf=window.requestAnimationFrame||function(cb){return window.setTimeout(cb,16);};
  onboardPositionFrame=raf(function(){onboardPositionFrame=0;positionOnboardGuide();});
}
function goToOnboardStep(index){
  var next=Number(index);if(!Number.isInteger(next)||next<0||next>=ONBOARD_STEPS.length)return;
  onboardClearSpotlight();onbStep=next;onboardPrepareStep(next);renderOnboardStep();
  positionOnboardGuide();
  window.setTimeout(scheduleOnboardPosition,90);
}
function showOnboarding(){
  if(onboardGuideOpen)return;
  onboardGuideReturnFocus=document.activeElement;onboardGuideOpen=true;
  var launcher=document.getElementById("onboardTourLauncher");if(launcher)launcher.hidden=true;
  onboardEnsureRoot();goToOnboardStep(0);
}
function closeOnboarding(completed){
  if(!onboardGuideOpen)return;
  onboardGuideOpen=false;onboardClearSpotlight();
  var browser=document.getElementById("galleryBrowser");
  if(onboardOpenedBrowser&&browser&&browser.classList.contains("open")&&typeof closeGalleryBrowser==="function")closeGalleryBrowser();
  onboardOpenedBrowser=false;
  var audio=document.getElementById("gAudioPanelBody");
  if(onboardOpenedAudio&&audio&&audio.classList.contains("open")&&typeof toggleAudioPanel==="function")toggleAudioPanel();
  onboardOpenedAudio=false;
  if(completed){try{localStorage.setItem(ONBOARD_STORAGE_KEY,"1");sessionStorage.removeItem(ONBOARD_SNOOZE_KEY);}catch(_e){}}
  else{try{sessionStorage.setItem(ONBOARD_SNOOZE_KEY,"1");}catch(_e){}}
  if(onboardGuideRoot&&onboardGuideRoot.parentNode)onboardGuideRoot.parentNode.removeChild(onboardGuideRoot);
  onboardGuideRoot=null;
  var launcher=document.getElementById("onboardTourLauncher");if(launcher)launcher.hidden=false;
  if(onboardGuideReturnFocus&&onboardGuideReturnFocus.isConnected&&typeof onboardGuideReturnFocus.focus==="function"){
    try{onboardGuideReturnFocus.focus({preventScroll:true});}catch(_e){}
  }
  onboardGuideReturnFocus=null;
}
function handleOnboardAction(action){
  if(action==="close"){closeOnboarding(false);return;}
  if(action==="finish"){closeOnboarding(true);return;}
  if(action==="previous"){goToOnboardStep(onbStep-1);return;}
  if(action==="start"){
    var browse=document.querySelector(".hero-cta-main");if(browse)browse.click();
    else if(typeof openGalleryBrowser==="function")openGalleryBrowser();
    if(onboardGuideOpen)goToOnboardStep(1);return;
  }
  if(action==="next"){goToOnboardStep(Math.min(ONBOARD_STEPS.length-1,onbStep+1));return;}
  if(action==="review"){
    var review=document.getElementById("exOpenBtn");if(review)review.click();
  }
}
document.addEventListener("click",function(event){
  if(!onboardGuideOpen||!event.target||!event.target.closest)return;
  var target=event.target;
  if(onbStep===0&&target.closest(".hero-cta-main")){
    window.setTimeout(function(){if(onboardGuideOpen&&onbStep===0)goToOnboardStep(1);},180);return;
  }
  if(onbStep===1&&target.closest("#gbGrid .gb-item")){
    window.setTimeout(function(){if(onboardGuideOpen&&onbStep===1)goToOnboardStep(2);},180);return;
  }
  if(onbStep===2&&target.closest("#gvShowAns,#fsFlipBtn")){
    window.setTimeout(function(){if(onboardGuideOpen&&onbStep===2)goToOnboardStep(3);},100);return;
  }
  if(onbStep===3&&target.closest("#gvSelectBtn")){
    window.setTimeout(function(){
      var note=document.getElementById("onboardGuideNote");
      var count=(typeof gvSel!=="undefined"&&gvSel)?gvSel.length:0;
      if(note)note.textContent=count?"تم تحديث اختيار القوالب فعلياً. العدد الحالي: "+count+".":"لم يُحدد هذا القالب؛ يمكنك تحديده أو المتابعة.";
    },40);return;
  }
  if(onbStep===4&&target.closest("#gTtsPreviewBtn")){
    var note=document.getElementById("onboardGuideNote");if(note)note.textContent="طلبت معاينة الصوت بنفسك. استمع ثم تابع.";return;
  }
  if(onbStep===5&&target.closest("#exOpenBtn")){
    window.setTimeout(function(){if(onboardGuideOpen)closeOnboarding(true);},120);
  }
});
document.addEventListener("keydown",function(event){
  if(!onboardGuideOpen)return;
  if(event.key==="Escape"){event.preventDefault();closeOnboarding(false);return;}
  if(event.key==="ArrowLeft"&&onbStep<ONBOARD_STEPS.length-1){event.preventDefault();goToOnboardStep(onbStep+1);}
  else if(event.key==="ArrowRight"&&onbStep>0){event.preventDefault();goToOnboardStep(onbStep-1);}
});
window.addEventListener("resize",scheduleOnboardPosition);
window.addEventListener("scroll",scheduleOnboardPosition,true);
"""

LOADER_CSS = """/* ============================================================
   LOADING
   ============================================================ */
#loadingMsg{position:fixed;inset:0;z-index:90;display:grid;place-content:center;text-align:center;
  background:var(--bg)}
#loadBar{background:var(--ac)}
#loadPct{color:var(--tx3)}
"""
LOADER_HTML = """<div id="loadingMsg">
  <div style="font-family:var(--font-mono);font-size:.8em;letter-spacing:1px;color:var(--tx2);margin-bottom:12px;text-transform:uppercase">جاري تحميل القوالب...</div>
  <div style="width:240px;height:4px;background:var(--s3);border:1px solid var(--bd-strong);border-radius:0;margin:0 auto;overflow:hidden">
    <div id="loadBar" style="width:0%;height:100%;border-radius:0;transition:width .3s"></div>
  </div>
  <div id="loadPct" style="font-family:var(--font-mono);font-size:.62em;color:var(--tx3);margin-top:8px">0%</div>
</div>
"""
FLIP_HTML = '<button class="gv-fab gv-flip" onclick="gvFlip()" title="قلب البطاقة" aria-label="قلب البطاقة"><svg width="1.1em" height="1.1em" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/></svg></button>'

def apply_gallery_ux(html, deck):
    if deck not in ("en9", "enlit", "ensci", "fr9"):
        raise SystemExit("Onboarding transform is restricted to the four non-Bac galleries")
    audio_source = "tas9" if deck == "fr9" else deck
    bad = "fetch(apiBase()+'/api/audio_status?source=" + audio_source + ")"
    good = "fetch(apiBase()+'/api/audio_status?source=" + audio_source + "')"
    if html.count(bad) != 1:
        raise SystemExit(deck + ": expected one malformed generated audio-status URL")
    html = html.replace(bad, good, 1)
    if html.count(LOADER_HTML) != 1:
        raise SystemExit(deck + ": blocking loader markup changed unexpectedly")
    html = html.replace(LOADER_HTML, "", 1)
    html = html.replace(LOADER_CSS, "", 1)
    if html.count(FLIP_HTML) > 1:
        raise SystemExit(deck + ": duplicate floating flip controls")
    html = html.replace(FLIP_HTML, "", 1)
    old_dialog = '<dialog class="onboard-overlay" id="onboardOverlay" style="display:none">'
    new_dialog = '<dialog class="onboard-overlay" id="onboardOverlay" hidden aria-hidden="true">'
    if html.count(old_dialog) != 1:
        raise SystemExit(deck + ": legacy onboarding dialog anchor is missing")
    html = html.replace(old_dialog, new_dialog, 1)
    start = html.find("var ONBOARD_STEPS=[")
    marker = "// ============================================================\n// WHAT'S NEW"
    end = html.find(marker, start)
    if start < 0 or end < 0:
        raise SystemExit(deck + ": could not locate original onboarding script")
    html = html[:start] + TOUR_JS.replace("__DECK__", deck) + "\n\n" + html[end:]
    old_init = "if(!localStorage.getItem('anki_" + deck + "_onboarded'))showOnboarding();"
    if html.count(old_init) != 1:
        raise SystemExit(deck + ": first-visit blocking tour trigger changed unexpectedly")
    html = html.replace(old_init, "/* Guided tour is intentionally user-initiated. */", 1)
    launcher = '<button id="onboardTourLauncher" type="button" onclick="showOnboarding()" aria-label="ابدأ الجولة التفاعلية"><span aria-hidden="true">↗</span><span>الجولة التفاعلية</span></button>\n'
    closers = list(re.finditer(r"</body\s*>", html, flags=re.I))
    if not closers:
        raise SystemExit(deck + ": missing document body close")
    position = closers[-1].start()
    html = html[:position] + launcher + html[position:]
    style = '<style id="gallery-tour-redesign">\n' + TOUR_CSS + '\n</style>\n'
    html, count = re.subn(r"</head\s*>", style + "</head>", html, count=1, flags=re.I)
    if count != 1:
        raise SystemExit(deck + ": could not add clean guided-tour styles")
    for token in ('id="loadingMsg"', "جاري تحميل القوالب...", 'class="gv-fab gv-flip"'):
        if token in html:
            raise SystemExit(deck + ": obsolete blocking or floating control remains: " + token)
    if 'id="fsFlipBtn"' not in html or 'id="gvShowAns"' not in html:
        raise SystemExit(deck + ": actual card flip controls are missing")
    return html
