"""Clean product-led gallery introduction and efficient template browsing."""
import re

EXPERIENCE_CSS = r"""
:root{--gx-ink:#f5f8fb;--gx-muted:#a8bacb;--gx-line:rgba(173,195,215,.16);--gx-panel:#11243a;--gx-teal:#77c7bc}
#gallery-experience-hero{position:relative;isolation:isolate;display:grid;grid-template-columns:minmax(0,1.05fr) minmax(330px,.95fr);align-items:stretch;gap:clamp(24px,4vw,64px);max-width:1480px;margin:clamp(22px,4vw,48px) auto 32px;padding:clamp(28px,5vw,68px);overflow:hidden;border:1px solid rgba(174,197,218,.17);border-radius:28px;background:linear-gradient(120deg,#132940 0%,#102238 52%,#0e1b2c 100%);box-shadow:0 30px 80px rgba(0,0,0,.22)}
#gallery-experience-hero:before{content:"";position:absolute;z-index:-1;inset:0;background:radial-gradient(ellipse at 8% 100%,rgba(85,173,161,.14),transparent 34%),radial-gradient(ellipse at 85% 5%,rgba(91,132,184,.16),transparent 38%)}
#gallery-experience-hero .gx-copy{display:flex;flex-direction:column;align-items:flex-start;justify-content:center;min-width:0}
#gallery-experience-hero .gx-eyebrow{display:flex;align-items:center;gap:10px;margin-bottom:20px;color:#b5cadb;font-size:.68rem;font-weight:900;letter-spacing:.15em}
#gallery-experience-hero .gx-mark{display:grid;place-items:center;width:32px;height:32px;border:1px solid rgba(158,202,203,.28);border-radius:9px;background:#20485a;color:#b8e5dc;font-size:.83rem}
#gallery-experience-hero .gx-deck{display:inline-flex;align-items:center;gap:8px;margin-bottom:15px;padding:7px 11px;border:1px solid rgba(173,195,215,.2);border-radius:7px;color:#b7c9d8;font-size:.73rem;font-weight:800}
#gallery-experience-hero h1{max-width:15ch;margin:0;color:#f7fafc;font-size:clamp(2rem,4vw,3.65rem);font-weight:950;line-height:1.25;letter-spacing:-.045em}
#gallery-experience-hero .gx-description{max-width:58ch;margin:17px 0 0;color:#c0ceda;font-size:clamp(.91rem,1.25vw,1.05rem);line-height:2}
#gallery-experience-hero .gx-actions{display:flex;flex-wrap:wrap;gap:10px;margin-top:27px}
#gallery-experience-hero .gx-action{min-height:49px;display:inline-flex;align-items:center;justify-content:center;gap:12px;padding:0 19px;border:1px solid rgba(180,202,221,.23);border-radius:9px;background:rgba(255,255,255,.045);color:#eaf2f8;font:inherit;font-size:.78rem;font-weight:900;cursor:pointer;transition:background .18s,transform .18s,border-color .18s}
#gallery-experience-hero .gx-action:hover{transform:translateY(-2px);background:rgba(255,255,255,.09);border-color:rgba(122,197,186,.56)}
#gallery-experience-hero .gx-action.primary{border-color:#4e8d88;background:#337b76;color:white;box-shadow:0 10px 24px rgba(19,102,98,.2)}
#gallery-experience-hero .gx-action.primary:hover{background:#3e8a83}
#gallery-experience-hero .gx-facts{display:flex;flex-wrap:wrap;gap:8px 18px;margin-top:25px;color:#9fb2c4;font-size:.67rem}
#gallery-experience-hero .gx-facts span{display:inline-flex;align-items:center;gap:7px}
#gallery-experience-hero .gx-facts span:before{content:"";width:5px;height:5px;border-radius:50%;background:#72c5b8}
#gallery-experience-hero .gx-showcase{position:relative;min-width:0;display:grid;grid-template-columns:minmax(0,1fr) 112px;grid-template-rows:auto 1fr auto;gap:12px;padding:17px;border:1px solid rgba(173,195,215,.17);border-radius:18px;background:rgba(6,17,30,.38)}
#gallery-experience-hero .gx-showcase-head{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;gap:8px;color:#a9bfd0;font-size:.61rem;font-weight:900;letter-spacing:.1em}
#gallery-experience-hero .gx-live{display:inline-flex;align-items:center;gap:7px;color:#8bcfc2;letter-spacing:0}
#gallery-experience-hero .gx-live:before{content:"";width:6px;height:6px;border-radius:50%;background:#6cc6b8;box-shadow:0 0 0 4px rgba(108,198,184,.1)}
#gallery-experience-hero .gx-featured{min-width:0;min-height:270px;overflow:hidden;border:1px solid rgba(171,193,216,.22);border-radius:13px;background:#152c43;box-shadow:0 22px 50px rgba(0,0,0,.25)}
#gallery-experience-hero .gx-featured iframe{display:block;width:100%;height:100%;min-height:270px;border:0;background:#172b40;pointer-events:none}
#gallery-experience-hero .gx-side-previews{display:grid;grid-template-rows:1fr 1fr;gap:12px;min-height:0}
#gallery-experience-hero .gx-mini{min-height:120px;overflow:hidden;border:1px solid rgba(171,193,216,.17);border-radius:10px;background:#14283e}
#gallery-experience-hero .gx-mini iframe{display:block;width:100%;height:100%;min-height:120px;border:0;background:#172b40;pointer-events:none}
#gallery-experience-hero .gx-showcase-foot{grid-column:1/-1;color:#8ea5b9;font-size:.62rem;line-height:1.7}
#gbFilters{display:none!important}
.gallery-browser{background:var(--bg,#0b1020)}
.gallery-browser .gb-head{min-height:72px;padding:14px clamp(16px,3vw,34px);display:flex;align-items:center;gap:15px;border-bottom:1px solid rgba(170,190,215,.13);background:#101f32}
.gallery-browser .gb-title{margin:0;color:#f2f6fa;font-size:1rem;font-weight:900}
.gallery-browser .gb-count{margin-inline-start:auto;color:#a8bdce;font-size:.73rem;font-variant-numeric:tabular-nums}
.gallery-browser .gb-close{width:40px;height:40px;border-radius:9px;border:1px solid rgba(180,199,219,.18);background:rgba(255,255,255,.04);color:#edf4f9}
.gallery-browser .gb-bar{min-height:44px;padding:9px clamp(16px,3vw,34px);display:flex;align-items:center;border-bottom:1px solid rgba(170,190,215,.1);background:#0e1b2c}
.gallery-browser .gb-hint{color:#98aec1;font-size:.69rem;line-height:1.6}
#gbGrid{display:grid!important;grid-template-columns:repeat(auto-fill,minmax(min(100%,250px),1fr));align-items:stretch;align-content:start;gap:clamp(12px,1.4vw,20px);margin:0;padding:clamp(14px,2vw,26px);overflow:auto;overscroll-behavior:contain;scroll-behavior:smooth}
#gbGrid .gb-item{position:relative;display:flex;flex-direction:column;min-width:0;min-height:0;overflow:hidden;border:1px solid rgba(169,190,211,.17)!important;border-radius:13px!important;background:#14283e!important;box-shadow:0 8px 24px rgba(0,0,0,.15)!important;transition:transform .2s,border-color .2s,box-shadow .2s!important}
#gbGrid .gb-item:hover{transform:translateY(-3px);border-color:rgba(117,192,179,.6)!important;box-shadow:0 16px 34px rgba(0,0,0,.24)!important}
#gbGrid .gb-item:focus-visible{outline:3px solid #6dc1b4;outline-offset:3px}
#gbGrid .gb-item.on{border-color:#67b9ad!important;box-shadow:0 0 0 2px rgba(103,185,173,.15)!important}
#gbGrid .gb-num{position:absolute;z-index:2;top:9px;right:9px;display:grid;place-items:center;min-width:28px;height:26px;padding:0 7px;border:1px solid rgba(190,210,225,.18);border-radius:7px;background:rgba(8,20,34,.86);color:#d7e6ef;font-size:.62rem;font-weight:900;font-variant-numeric:tabular-nums}
#gbGrid .gb-preview-host{position:relative;display:grid;place-items:center;min-height:0;width:100%;aspect-ratio:4/5;overflow:hidden;background:linear-gradient(145deg,#192e45,#101e30)}
#gbGrid .gb-preview-host iframe{position:absolute;inset:0;width:100%;height:100%;border:0;background:#14283e;opacity:0;pointer-events:none;transition:opacity .18s}
#gbGrid .gb-preview-host.is-ready iframe{opacity:1}
#gbGrid .gb-preview-loading{padding:14px;color:#7f9ab0;font-size:.63rem;text-align:center}
#gbGrid .gb-preview-host.is-error .gb-preview-loading{color:#d4b8a2}
#gbGrid .gb-ov{position:static;display:flex;align-items:center;justify-content:space-between;gap:8px;min-height:42px;padding:8px 11px;border-top:1px solid rgba(174,194,213,.1);background:#12253a;color:#e8f0f6;opacity:1;transform:none}
#gbGrid .gb-ov-t{font-size:.68rem;font-weight:850}
#gbGrid .gb-ov-b{color:#80c9bd;font-size:.65rem;font-weight:900}
#gbGrid .gb-sk{position:absolute;inset:0;z-index:0;display:none!important}
#gbProgress{background:#64b9ad}
#gv:not(.gx-visible){display:none!important}
#gv.gx-visible{display:block!important}
#gvStage{border-radius:20px!important}
#gvSelectBtn,#exOpenBtn,#gTtsPreviewBtn{min-height:45px!important;border-radius:10px!important;font-weight:850!important}
@media(max-width:820px){
 #gallery-experience-hero{grid-template-columns:1fr;gap:25px;padding:30px}
 #gallery-experience-hero .gx-showcase{grid-template-columns:minmax(0,1fr) 94px}
 #gallery-experience-hero .gx-featured,#gallery-experience-hero .gx-featured iframe{min-height:245px}
}
@media(max-width:560px){
 #gallery-experience-hero{margin:12px 0 16px;padding:18px 14px;border-radius:17px;gap:15px}
 #gallery-experience-hero h1{font-size:clamp(1.65rem,7.2vw,2.1rem);line-height:1.2}
 #gallery-experience-hero .gx-description{margin-top:10px;font-size:.78rem;line-height:1.65}
 #gallery-experience-hero .gx-actions{display:grid;grid-template-columns:1fr;width:100%;gap:6px;margin-top:14px}
 #gallery-experience-hero .gx-action{width:100%;min-height:43px}
 #gallery-experience-hero .gx-action:not(.primary){min-height:34px;border-color:transparent;background:transparent;color:#b6c9d8}
 #gallery-experience-hero .gx-showcase{grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:auto minmax(170px,auto) auto auto;gap:8px;padding:8px;border-radius:13px}
 #gallery-experience-hero .gx-featured{grid-column:1/-1}
 #gallery-experience-hero .gx-featured,#gallery-experience-hero .gx-featured iframe{min-height:170px}
 #gallery-experience-hero .gx-side-previews{grid-column:1/-1;grid-template-columns:repeat(2,minmax(0,1fr));grid-template-rows:none;gap:9px}
 #gallery-experience-hero .gx-mini,#gallery-experience-hero .gx-mini iframe{min-height:86px}
 #gallery-experience-hero .gx-showcase-foot{display:none}
 #gbGrid{grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;padding:12px}
 #gbGrid .gb-item{border-radius:10px!important}
 #gbGrid .gb-preview-host{aspect-ratio:4/5}
 .gallery-browser .gb-head{min-height:60px;padding:10px 13px}
 .gallery-browser .gb-title{font-size:.85rem}
 .gallery-browser .gb-hint{font-size:.62rem}
}
@media(max-width:350px){
 #gallery-experience-hero .gx-showcase{grid-template-columns:repeat(2,minmax(0,1fr));gap:7px;padding:8px}
 #gallery-experience-hero .gx-featured,#gallery-experience-hero .gx-featured iframe{min-height:150px}
 #gallery-experience-hero .gx-mini,#gallery-experience-hero .gx-mini iframe{min-height:76px}
 #gallery-experience-hero .gx-showcase-foot{font-size:.56rem}
 #gbGrid{gap:8px;padding:9px}
 #gbGrid .gb-ov{padding:7px 8px;min-height:38px}
 #gbGrid .gb-ov-t,#gbGrid .gb-ov-b{font-size:.58rem}
}
@media(prefers-reduced-motion:reduce){
 #gallery-experience-hero *,#gbGrid .gb-item{animation:none!important;transition:none!important;scroll-behavior:auto!important}
}
"""

EXPERIENCE_JS = r"""
(function(){
"use strict";
var deck="__DECK__";
var profiles={
 fr9:{label:"اللغة الفرنسية · الصف التاسع",title:"اختر شكلاً يليق بمفرداتك الفرنسية.",description:"مئة تصميم مختلف لبطاقات المفردات. شاهد القالب الحقيقي، وافحص الوجهين، ثم اعتمد ما يناسب طريقة دراستك.",word:"Leçon",meaning:"درس"},
 en9:{label:"اللغة الإنجليزية · الصف التاسع",title:"اجعل كل مفردة واضحة من النظرة الأولى.",description:"مئة تصميم لبطاقات مفردات الإنجليزية. استعرضها دون تصنيفات، افتح أي تصميم لمعاينته، ثم اختر القوالب التي تريدها.",word:"Student",meaning:"طالب"},
 enlit:{label:"بكالوريا 12 · الفرع الأدبي",title:"اختر طريقة عرض مفردات الإنجليزية.",description:"مئة تصميم لبطاقات مفردات الإنجليزية لطلاب بكالوريا 12 — الفرع الأدبي. استعرض التصاميم كما ستظهر على بطاقاتك، ثم اعتمد اختياراتك.",word:"Achievement",meaning:"إنجاز"},
 ensci:{label:"بكالوريا 12 · الفرع العلمي",title:"اختر طريقة عرض مفردات الإنجليزية.",description:"مئة تصميم لبطاقات مفردات الإنجليزية لطلاب بكالوريا 12 — الفرع العلمي. استعرض التصاميم كما ستظهر على بطاقاتك، ثم اعتمد اختياراتك.",word:"Achievement",meaning:"إنجاز"}
};
var profile=profiles[deck]||profiles.en9;
function text(node,value){if(node)node.textContent=value;}
function safePreviewSource(template){
 try{
  var source=typeof thumbDoc==="function"?thumbDoc(template):buildPreviewDoc(template);
  var doc=new DOMParser().parseFromString(source,"text/html");
  doc.querySelectorAll("script,iframe,object,embed,form").forEach(function(node){node.remove();});
  doc.querySelectorAll("*").forEach(function(node){
   Array.from(node.attributes).forEach(function(attribute){
    if(/^on/i.test(attribute.name)||((attribute.name==="href"||attribute.name==="src")&&/^\s*javascript:/i.test(attribute.value)))node.removeAttribute(attribute.name);
   });
  });
  return "<!doctype html>"+doc.documentElement.outerHTML;
 }catch(_e){return "";}
}
function fitFrame(frame){
 try{
  var doc=frame.contentDocument;if(!doc||!doc.body)return;
  var selector='.fitme,.ds-word,.ds-trans,.word,.trans,.meaning,.subtitle,.board-txt,.cfit,.frword,.arword,[class*="-word"],[class*="-trans"],[class*="-sub"],[class*="-txt"]';
  doc.querySelectorAll(selector).forEach(function(el){
   var parent=el.parentElement;if(!parent)return;
   var style=doc.defaultView.getComputedStyle(el),base=parseFloat(el.getAttribute("data-base"))||parseFloat(style.fontSize)||16;
   var min=Math.max(5,parseFloat(el.getAttribute("data-min"))||8),available=parent.clientWidth-16;
   if(available<24)return;
   el.style.whiteSpace="nowrap";el.style.display="inline-block";el.style.maxWidth="none";el.style.fontSize=base+"px";
   var width=el.scrollWidth;if(width>available)el.style.fontSize=Math.max(min,Math.floor(base*available/width*10)/10)+"px";
  });
 }catch(_e){}
}
function mountFrame(host,template,title){
 if(!host||!template)return;
 var iframe=document.createElement("iframe");iframe.setAttribute("sandbox","allow-same-origin");
 iframe.setAttribute("loading","lazy");iframe.setAttribute("title",title);
 iframe.addEventListener("load",function(){
  var doc=iframe.contentDocument,hasContent=!!(doc&&doc.body&&(doc.body.children.length||(doc.body.textContent||"").trim()));
  if(hasContent){host.classList.add("is-ready");fitFrame(iframe);if(doc.fonts&&doc.fonts.ready)doc.fonts.ready.then(function(){fitFrame(iframe);}).catch(function(){});}
  else{host.classList.add("is-error");text(host.querySelector(".gb-preview-loading"),"تعذرت معاينة هذا التصميم");}
 });
 iframe.addEventListener("error",function(){host.classList.add("is-error");text(host.querySelector(".gb-preview-loading"),"تعذرت معاينة هذا التصميم");});
 iframe.srcdoc=safePreviewSource(template);
 if(!iframe.srcdoc){host.classList.add("is-error");text(host.querySelector(".gb-preview-loading"),"المعاينة غير متاحة");return;}
 host.appendChild(iframe);
}
function addHero(){
 var section=document.querySelector("#sec-gal");if(!section||document.getElementById("gallery-experience-hero"))return;
 var oldHero=section.querySelector(".hero");if(!oldHero)return;
 var hero=document.createElement("section");hero.id="gallery-experience-hero";hero.setAttribute("aria-label","معرض "+profile.label);
 hero.innerHTML=
 '<div class="gx-copy">'+
  '<div class="gx-eyebrow"><span class="gx-mark" aria-hidden="true">A</span><span>ANKI DESIGN STUDIO</span></div>'+
  '<div class="gx-deck" data-gx-deck></div>'+
  '<h1 data-gx-title></h1><p class="gx-description" data-gx-description></p>'+
  '<div class="gx-actions"><button class="gx-action primary hero-cta-main" type="button" data-gx-browse>استعرض القوالب المئة <span aria-hidden="true">←</span></button><button class="gx-action" type="button" data-gx-tour>شاهد الجولة التفاعلية</button></div>'+
  '<div class="gx-facts"><span>100 تصميم فعلي</span><span>معاينة قبل الاعتماد</span><span>لا تصنيفات ولا فرز</span></div>'+
 '</div>'+
 '<div class="gx-showcase" aria-label="معاينات حقيقية من مكتبة القوالب">'+
  '<div class="gx-showcase-head"><span>من داخل المكتبة</span><span class="gx-live">معاينات فعلية</span></div>'+
  '<div class="gx-featured gx-preview-host" id="gxPreviewMain"><span class="gb-preview-loading">جارٍ تجهيز المعاينة</span></div>'+
  '<div class="gx-side-previews"><div class="gx-mini gx-preview-host" id="gxPreviewAlt1"><span class="gb-preview-loading">قالب آخر</span></div><div class="gx-mini gx-preview-host" id="gxPreviewAlt2"><span class="gb-preview-loading">تصميم آخر</span></div></div>'+
  '<div class="gx-showcase-foot">هذه معاينات من القوالب الفعلية المرتبطة بهذه الرزمة، وليست رسومات توضيحية بديلة.</div>'+
 '</div>';
 oldHero.parentNode.insertBefore(hero,oldHero);oldHero.remove();
 text(hero.querySelector("[data-gx-deck]"),profile.label);
 text(hero.querySelector("[data-gx-title]"),profile.title);
 text(hero.querySelector("[data-gx-description]"),profile.description);
 hero.querySelector("[data-gx-browse]").addEventListener("click",function(){
  if(typeof ensureGalleryDesigns==="function")ensureGalleryDesigns();
  if(typeof window.openGalleryBrowser==="function")window.openGalleryBrowser();
 });
 hero.querySelector("[data-gx-tour]").addEventListener("click",function(){
  var launcher=document.getElementById("onboardTourLauncher");if(launcher)launcher.click();
 });
}
function mountShowcase(){
 try{if(typeof ensureGalleryDesigns==="function")ensureGalleryDesigns();}catch(_e){}
 var list=(typeof gvList!=="undefined"&&Array.isArray(gvList))?gvList:[];
 var choices=[0,16,40],hosts=["gxPreviewMain","gxPreviewAlt1","gxPreviewAlt2"];
 choices.forEach(function(index,i){
  var host=document.getElementById(hosts[i]);if(!host)return;
  var template=list[index]||list[i];
  if(template)mountFrame(host,template,"معاينة فعلية لتصميم "+(index+1));
 });
}
function disableFilters(){
 try{if(typeof gbFam!=="undefined")gbFam="all";}catch(_e){}
 window.gbBuildFilters=function(){try{if(typeof gbFam!=="undefined")gbFam="all";}catch(_e){}};
 window.gbSetFilter=function(){try{if(typeof gbFam!=="undefined")gbFam="all";}catch(_e){};if(typeof renderGalleryBrowser==="function")renderGalleryBrowser();};
}
function init(){
 addHero();disableFilters();mountShowcase();
 var launcher=document.getElementById("onboardTourLauncher");
 if(launcher){
  launcher.textContent="الجولة التفاعلية";launcher.setAttribute("aria-label","ابدأ الجولة التفاعلية");
  launcher.title="تعرف إلى خطوات المعرض من داخله";
  launcher.addEventListener("click",function(){if(typeof showOnboarding==="function")showOnboarding();});
 }
 var grid=document.getElementById("gbGrid");
 if(grid)grid.addEventListener("click",function(event){
  var card=event.target.closest(".gb-item");if(!card)return;
   var preview=document.getElementById("gv");if(preview)preview.classList.add("gx-visible");
  grid.querySelectorAll('.gb-item[data-gx-active="true"]').forEach(function(item){item.removeAttribute("data-gx-active");});
  card.setAttribute("data-gx-active","true");
 },true);
}
if(document.readyState==="loading")document.addEventListener("DOMContentLoaded",init,{once:true});
else init();
})();
"""

def apply_gallery_experience(html, deck):
    if deck not in ("en9", "enlit", "ensci", "fr9"):
        raise SystemExit("Gallery experience is restricted to the four non-Bac galleries")
    if 'id="gallery-experience-v6"' in html:
        raise SystemExit(deck + ": clean-slate gallery experience is already present")
    if 'id="gbGrid"' not in html or 'id="onboardTourLauncher"' not in html:
        raise SystemExit(deck + ": required gallery anchors are missing")

    # Remove color-family chips entirely; the library is one uninterrupted 100-design collection.
    html, removed = re.subn(r'\s*<div class="gb-tools" id="gbFilters"></div>', "", html, count=1)
    if removed != 1:
        raise SystemExit(deck + ": the old filter-strip anchor was not found")
    html = html.replace("اضغط على أي قالب لاختياره والعودة إلى المعرض", "اضغط على أي قالب لفتح معاينته الكبيرة", 1)
    html = html.replace("اختيار ←", "معاينة ←")
    html = html.replace("تم اختيار التصميم ", "تم فتح معاينة التصميم ")

    old_thumb = '<img class="gb-img" data-loading="1" loading="lazy" decoding="async" src="\'+img+\'" alt="تصميم \'+num+\'">'
    new_thumb = '<div class="gb-preview-host" aria-label="معاينة تصميم \'+num+\'"><span class="gb-preview-loading">تظهر المعاينة عند الوصول إلى هذا القالب</span></div>'
    if html.count(old_thumb) != 1:
        raise SystemExit(deck + ": expected one base thumbnail renderer")
    html = html.replace(old_thumb, new_thumb, 1)

    handlers = re.compile(
        r"var im=it\.querySelector\('\.gb-img'\);\s*"
        r"im\.addEventListener\('load',function\(\)\{this\.removeAttribute\('data-loading'\);"
        r"var sk=this\.parentNode\.querySelector\('\.gb-sk'\);if\(sk\)sk\.style\.display='none';\}\);\s*"
        r"im\.addEventListener\('error',function\(\)\{this\.removeAttribute\('data-loading'\);"
        r"var sk=this\.parentNode\.querySelector\('\.gb-sk'\);if\(sk\)sk\.style\.display='none';\}\);"
    )
    lazy_mount = (
        "var previewHost=it.querySelector('.gb-preview-host');"
        "var previewMounted=false;"
        "function mountGalleryPreview(){"
        "if(previewMounted||!previewHost)return;previewMounted=true;"
        "var previewSource=thumbDoc(t);"
        "var previewDocument=new DOMParser().parseFromString(previewSource,'text/html');"
        "previewDocument.querySelectorAll('script,iframe,object,embed,form').forEach(function(node){node.remove();});"
        "previewDocument.querySelectorAll('*').forEach(function(node){Array.from(node.attributes).forEach(function(attribute){"
        "if(/^on/i.test(attribute.name)||((attribute.name==='href'||attribute.name==='src')&&/^\\s*javascript:/i.test(attribute.value))){node.removeAttribute(attribute.name);}"
        "});});"
        "var previewFrame=document.createElement('iframe');previewFrame.className='gb-preview-frame';"
        "previewFrame.setAttribute('sandbox','allow-same-origin');previewFrame.setAttribute('loading','lazy');"
        "previewFrame.setAttribute('title','معاينة تصميم '+num);"
        "previewFrame.addEventListener('load',function(){var doc=this.contentDocument;"
        "var hasContent=doc&&doc.body&&(doc.body.children.length>0||(doc.body.textContent||'').trim().length>0);"
        "if(hasContent){previewHost.classList.add('is-ready');"
        "var fitPreview=function(){var selector='.fitme,.ds-word,.ds-trans,.word,.trans,.meaning,.subtitle,.board-txt,.cfit,.frword,.arword,[class*=\\\"-word\\\"],[class*=\\\"-trans\\\"],[class*=\\\"-sub\\\"],[class*=\\\"-txt\\\"]';"
        "doc.querySelectorAll(selector).forEach(function(el){var p=el.parentElement;if(!p)return;var cs=doc.defaultView.getComputedStyle(el);"
        "var base=parseFloat(el.getAttribute('data-base'))||parseFloat(cs.fontSize)||16;var min=Math.max(5,parseFloat(el.getAttribute('data-min'))||8);"
        "var aw=p.clientWidth-16;if(aw<24)return;el.style.whiteSpace='nowrap';el.style.display='inline-block';el.style.maxWidth='none';"
        "el.style.fontSize=base+'px';var tw=el.scrollWidth;if(tw>aw)el.style.fontSize=Math.max(min,Math.floor(base*aw/tw*10)/10)+'px';});};"
        "fitPreview();if(doc.fonts&&doc.fonts.ready)doc.fonts.ready.then(fitPreview).catch(function(){});"
        "}else{previewHost.classList.add('is-error');var label=previewHost.querySelector('.gb-preview-loading');if(label)label.textContent='تعذرت معاينة هذا التصميم';}});"
        "previewFrame.addEventListener('error',function(){previewHost.classList.add('is-error');"
        "var label=previewHost.querySelector('.gb-preview-loading');if(label)label.textContent='تعذرت معاينة هذا التصميم';});"
        "previewFrame.srcdoc='<!doctype html>'+previewDocument.documentElement.outerHTML;previewHost.appendChild(previewFrame);"
        "}"
        "if('IntersectionObserver' in window){var previewObserver=new IntersectionObserver(function(entries){entries.forEach(function(entry){"
        "if(entry.isIntersecting){previewObserver.unobserve(entry.target);mountGalleryPreview();}});},{root:document.getElementById('gbGrid'),rootMargin:'320px 0px',threshold:0.01});"
        "previewObserver.observe(it);}else if(i<10){mountGalleryPreview();}"
    )
    html, count = handlers.subn(lambda _match: lazy_mount, html, count=1)
    if count != 1:
        raise SystemExit(deck + ": could not install viewport-based thumbnail rendering")

    # The gallery browser keeps all designs visible and always starts from the full set.
    html = html.replace("var gbCur=0,gbFam='all'", "var gbCur=0,gbFam='all'", 1)
    css = '<style id="gallery-experience-v6">\n' + EXPERIENCE_CSS + '\n</style>\n'
    html, inserted = re.subn(r"</head\s*>", css + "</head>", html, count=1, flags=re.I)
    if inserted != 1:
        raise SystemExit(deck + ": could not add the clean gallery visual system")
    js = EXPERIENCE_JS.replace("__DECK__", deck)
    script = '<script id="gallery-experience-runtime-v6">\n' + js + '\n</script>\n'
    closers = list(re.finditer(r"</body\s*>", html, flags=re.I))
    if not closers:
        raise SystemExit(deck + ": missing final body close")
    # Runtime after the shared page scripts, before the real tour launcher.
    launcher = html.find('<button id="onboardTourLauncher"')
    if launcher < 0 or launcher >= closers[-1].start():
        raise SystemExit(deck + ": tour launcher insertion point is missing")
    html = html[:launcher] + script + html[launcher:]

    required = (
        'id="gallery-experience-v6"', 'id="gallery-experience-runtime-v6"',
        'id="gallery-experience-hero"', 'class="gx-action primary hero-cta-main"',
        'id="gxPreviewMain"', 'id="gxPreviewAlt1"', 'id="gxPreviewAlt2"',
        'window.gbSetFilter=function()', 'function mountGalleryPreview()',
        "new IntersectionObserver", "rootMargin:'320px 0px'",
        "previewFrame.srcdoc='<!doctype html>'+previewDocument.documentElement.outerHTML",
    )
    for token in required:
        if token not in html:
            raise SystemExit(deck + ": incomplete gallery experience: " + token)
    if 'id="gbFilters"' in html:
        raise SystemExit(deck + ": old filter controls remain in generated gallery")
    if 'id="gxWelcome"' in html or 'id="gxWelcomeStart"' in html:
        raise SystemExit(deck + ": old blocking welcome modal remains")
    return html
