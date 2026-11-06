"""Deterministic UX transforms for the four generated non-Bac gallery pages."""
import re

TOUR_CSS = r"""#onboardOverlay.onboard-overlay{position:fixed;inset:0;z-index:99999;display:none;place-items:center;margin:0;padding:18px;width:100%;height:100%;max-width:none;max-height:none;border:0;background:radial-gradient(ellipse at 12% 12%,rgba(124,58,237,.28),transparent 42%),radial-gradient(ellipse at 88% 84%,rgba(14,165,233,.2),transparent 42%),rgba(5,7,15,.88);backdrop-filter:blur(18px);-webkit-backdrop-filter:blur(18px);color:#f8fafc}
#onboardOverlay.onboard-overlay[open]{display:grid}
#onboardOverlay::backdrop{background:rgba(3,6,18,.68);backdrop-filter:blur(8px)}
#onboardOverlay .onboard-box{position:relative;width:min(960px,calc(100vw - 36px));max-height:min(900px,calc(100dvh - 36px));overflow:auto;margin:auto;padding:clamp(18px,3.2vw,34px);border:1px solid rgba(196,181,253,.22);border-radius:28px;background:linear-gradient(145deg,rgba(21,24,43,.985),rgba(9,14,28,.99));box-shadow:0 35px 110px rgba(0,0,0,.58),0 0 0 1px rgba(255,255,255,.035) inset;overscroll-behavior:contain;animation:obEnter .34s cubic-bezier(.2,.8,.2,1) both}
#onboardOverlay .onboard-box:before{content:"";position:absolute;inset:0 12% auto;height:1px;background:linear-gradient(90deg,transparent,#a78bfa,#67e8f9,transparent);opacity:.9;pointer-events:none}
@keyframes obEnter{from{opacity:0;transform:translateY(14px) scale(.99)}to{opacity:1;transform:translateY(0) scale(1)}}
#onboardOverlay .ob-shell{display:flex;flex-direction:column;gap:clamp(14px,2.2vw,22px)}
#onboardOverlay .ob-top{display:flex;align-items:center;justify-content:space-between;gap:12px}
#onboardOverlay .ob-brand{display:flex;align-items:center;gap:11px;min-width:0;color:#c4b5fd}
#onboardOverlay .ob-brand-mark{display:grid;place-items:center;flex:0 0 auto;width:38px;height:38px;border:1px solid rgba(196,181,253,.26);border-radius:13px;background:linear-gradient(135deg,#7c3aed,#0891b2);box-shadow:0 8px 24px rgba(124,58,237,.28);font-size:1.05rem;font-weight:950}
#onboardOverlay .ob-brand-copy{display:flex;flex-direction:column;gap:2px;min-width:0}
#onboardOverlay .ob-brand-copy strong{font-size:.78rem;font-weight:950;letter-spacing:.11em}
#onboardOverlay .ob-brand-copy small{color:#94a3b8;font-size:.7rem;font-weight:650;letter-spacing:0}
#onboardOverlay .ob-top-actions{display:flex;align-items:center;gap:10px}
#onboardOverlay .ob-count{padding:8px 12px;border:1px solid rgba(196,181,253,.16);border-radius:999px;background:rgba(255,255,255,.045);color:#dbeafe;font-size:.78rem;font-weight:850;font-variant-numeric:tabular-nums;white-space:nowrap}
#onboardOverlay .ob-close{display:grid;place-items:center;flex:0 0 auto;width:42px;height:42px;border:1px solid rgba(255,255,255,.12);border-radius:13px;background:rgba(255,255,255,.045);color:#cbd5e1;font-size:1.25rem;cursor:pointer;transition:background .18s,border-color .18s,transform .18s}
#onboardOverlay .ob-close:hover{background:rgba(248,113,113,.13);border-color:rgba(248,113,113,.4);transform:rotate(90deg)}
#onboardOverlay .ob-progress{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:7px;direction:rtl}
#onboardOverlay .ob-progress span{height:6px;border-radius:99px;background:rgba(255,255,255,.105);transition:background .22s,box-shadow .22s}
#onboardOverlay .ob-progress span.done{background:linear-gradient(90deg,#8b5cf6,#22d3ee);box-shadow:0 0 13px rgba(139,92,246,.25)}
#onboardOverlay .ob-content{display:grid;grid-template-columns:minmax(0,.92fr) minmax(0,1.08fr);align-items:stretch;gap:clamp(18px,3vw,30px);min-height:340px;direction:ltr}
#onboardOverlay .ob-visual{position:relative;display:grid;place-items:center;min-width:0;min-height:320px;overflow:hidden;padding:22px;border:1px solid rgba(167,139,250,.19);border-radius:24px;background:radial-gradient(circle at 50% 35%,rgba(139,92,246,.2),transparent 57%),linear-gradient(145deg,rgba(255,255,255,.065),rgba(255,255,255,.012))}
#onboardOverlay .ob-visual:before,#onboardOverlay .ob-visual:after{content:"";position:absolute;border:1px solid rgba(103,232,249,.1);border-radius:50%;width:220px;height:220px;pointer-events:none}
#onboardOverlay .ob-visual:after{width:300px;height:300px;border-color:rgba(167,139,250,.075)}
#onboardOverlay .ob-visual>*{position:relative;z-index:1;width:100%}
#onboardOverlay .ob-visual-caption{margin-top:18px;color:#a5b4fc;text-align:center;font-size:.78rem;font-weight:850;letter-spacing:.02em}
#onboardOverlay .ob-journey{display:grid;gap:12px;max-width:340px;margin:auto}
#onboardOverlay .ob-journey-item{display:flex;align-items:center;gap:13px;padding:13px 15px;border:1px solid rgba(255,255,255,.1);border-radius:15px;background:rgba(8,13,27,.72)}
#onboardOverlay .ob-journey-num{display:grid;place-items:center;flex:0 0 auto;width:37px;height:37px;border-radius:12px;background:rgba(139,92,246,.18);color:#c4b5fd;font-size:.8rem;font-weight:950}
#onboardOverlay .ob-journey-item strong{display:block;color:#f8fafc;font-size:.91rem;font-weight:900}
#onboardOverlay .ob-journey-item small{display:block;margin-top:3px;color:#94a3b8;font-size:.73rem}
#onboardOverlay .ob-journey-item.is-final .ob-journey-num{background:rgba(34,211,238,.16);color:#67e8f9}
#onboardOverlay .ob-search-mock{display:flex;align-items:center;gap:10px;max-width:380px;margin:0 auto 14px;padding:13px 15px;border:1px solid rgba(196,181,253,.24);border-radius:14px;background:rgba(8,13,27,.82);color:#94a3b8;font-size:.82rem}
#onboardOverlay .ob-search-icon{color:#67e8f9;font-size:1.1rem}
#onboardOverlay .ob-chip-row{display:flex;justify-content:center;gap:7px;flex-wrap:wrap;margin-bottom:17px}
#onboardOverlay .ob-chip-row span{padding:6px 10px;border:1px solid rgba(255,255,255,.1);border-radius:999px;background:rgba(255,255,255,.045);color:#cbd5e1;font-size:.69rem;font-weight:800}
#onboardOverlay .ob-chip-row span.active{border-color:rgba(103,232,249,.36);background:rgba(8,145,178,.16);color:#a5f3fc}
#onboardOverlay .ob-template-samples{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px;max-width:390px;margin:auto}
#onboardOverlay .ob-template-sample{display:grid;place-items:center;gap:9px;min-height:112px;padding:10px 6px;border:1px solid rgba(255,255,255,.12);border-radius:14px;background:linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.02))}
#onboardOverlay .ob-template-sample:nth-child(2){border-color:rgba(103,232,249,.34);background:linear-gradient(145deg,rgba(8,145,178,.18),rgba(255,255,255,.025))}
#onboardOverlay .ob-template-sample i{display:block;width:42px;height:52px;border:2px solid rgba(196,181,253,.7);border-radius:8px;background:linear-gradient(160deg,rgba(139,92,246,.35),rgba(8,145,178,.12))}
#onboardOverlay .ob-template-sample:nth-child(2) i{border-color:#67e8f9;background:linear-gradient(160deg,rgba(34,211,238,.3),rgba(139,92,246,.14))}
#onboardOverlay .ob-template-sample small{color:#cbd5e1;font-size:.68rem;font-weight:800}
#onboardOverlay .ob-face-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:12px;max-width:410px;margin:auto}
#onboardOverlay .ob-face-card{display:flex;flex-direction:column;justify-content:space-between;min-height:198px;padding:15px;border:1px solid rgba(196,181,253,.22);border-radius:17px;background:linear-gradient(145deg,rgba(255,255,255,.075),rgba(255,255,255,.02));text-align:center}
#onboardOverlay .ob-face-card.back{border-color:rgba(103,232,249,.3);background:linear-gradient(145deg,rgba(8,145,178,.14),rgba(255,255,255,.025))}
#onboardOverlay .ob-face-label{color:#94a3b8;font-size:.67rem;font-weight:850}
#onboardOverlay .ob-face-card strong{display:block;margin:18px 0 8px;color:#f8fafc;font-size:clamp(1.15rem,3vw,1.55rem);font-weight:950;overflow-wrap:anywhere}
#onboardOverlay .ob-face-card small{color:#cbd5e1;font-size:.84rem}
#onboardOverlay .ob-face-card em{margin-top:14px;color:#67e8f9;font-size:.66rem;font-style:normal;font-weight:800}
#onboardOverlay .ob-pick-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;max-width:390px;margin:auto}
#onboardOverlay .ob-pick-card{position:relative;display:flex;align-items:center;gap:11px;padding:15px 12px;border:1px solid rgba(255,255,255,.12);border-radius:15px;background:rgba(8,13,27,.72)}
#onboardOverlay .ob-pick-card.selected{border-color:rgba(103,232,249,.42);background:rgba(8,145,178,.12)}
#onboardOverlay .ob-pick-art{width:34px;height:44px;flex:0 0 auto;border:2px solid rgba(196,181,253,.6);border-radius:7px;background:linear-gradient(155deg,rgba(139,92,246,.3),rgba(8,145,178,.08))}
#onboardOverlay .ob-pick-card.selected .ob-pick-art{border-color:#67e8f9}
#onboardOverlay .ob-pick-copy strong{display:block;color:#f8fafc;font-size:.78rem}
#onboardOverlay .ob-pick-copy small{display:block;margin-top:4px;color:#94a3b8;font-size:.65rem}
#onboardOverlay .ob-pick-check{margin-inline-start:auto;color:#67e8f9;font-size:1.05rem;font-weight:950}
#onboardOverlay .ob-audio-board{display:grid;gap:12px;max-width:390px;margin:auto}
#onboardOverlay .ob-audio-row{display:flex;align-items:center;gap:12px;padding:14px;border:1px solid rgba(255,255,255,.12);border-radius:15px;background:rgba(8,13,27,.72)}
#onboardOverlay .ob-audio-icon{display:grid;place-items:center;flex:0 0 auto;width:38px;height:38px;border-radius:12px;background:rgba(139,92,246,.2);color:#c4b5fd;font-size:1rem}
#onboardOverlay .ob-audio-row.secondary .ob-audio-icon{background:rgba(8,145,178,.18);color:#67e8f9}
#onboardOverlay .ob-audio-copy{min-width:0;flex:1}
#onboardOverlay .ob-audio-copy strong{display:block;color:#f8fafc;font-size:.8rem}
#onboardOverlay .ob-audio-copy small{display:block;margin-top:4px;color:#94a3b8;font-size:.67rem}
#onboardOverlay .ob-play-mark{display:grid;place-items:center;width:30px;height:30px;border:1px solid rgba(255,255,255,.12);border-radius:50%;color:#a5f3fc;font-size:.7rem}
#onboardOverlay .ob-audio-sliders{display:grid;gap:10px;padding:14px;border:1px solid rgba(255,255,255,.09);border-radius:14px;background:rgba(255,255,255,.035)}
#onboardOverlay .ob-slider-line{display:flex;align-items:center;gap:10px;color:#94a3b8;font-size:.68rem}
#onboardOverlay .ob-slider-line i{height:5px;flex:1;border-radius:99px;background:linear-gradient(90deg,#8b5cf6,#22d3ee)}
#onboardOverlay .ob-export-board{display:grid;place-items:center;gap:13px;max-width:350px;margin:auto;text-align:center}
#onboardOverlay .ob-file-icon{display:grid;place-items:center;width:108px;height:126px;border:1px solid rgba(103,232,249,.3);border-radius:18px;background:linear-gradient(145deg,rgba(8,145,178,.2),rgba(139,92,246,.16));box-shadow:0 18px 42px rgba(8,145,178,.12);color:#a5f3fc;font-size:2.2rem;font-weight:950}
#onboardOverlay .ob-export-board strong{color:#f8fafc;font-size:1rem}
#onboardOverlay .ob-export-board small{color:#94a3b8;font-size:.74rem;line-height:1.8}
#onboardOverlay .ob-export-checks{display:flex;justify-content:center;gap:7px;flex-wrap:wrap}
#onboardOverlay .ob-export-checks span{padding:7px 9px;border:1px solid rgba(34,211,238,.17);border-radius:999px;background:rgba(8,145,178,.09);color:#a5f3fc;font-size:.67rem;font-weight:800}
#onboardOverlay .ob-copy{display:flex;flex-direction:column;justify-content:center;min-width:0;text-align:right;padding:4px 0;direction:rtl}
#onboardOverlay .ob-kicker{display:flex;align-items:center;gap:8px;margin:0 0 12px;color:#67e8f9;font-size:.75rem;font-weight:950;letter-spacing:.02em}
#onboardOverlay .ob-kicker:before{content:"";width:24px;height:2px;border-radius:2px;background:#67e8f9}
#onboardOverlay .ob-kicker-icon{display:grid;place-items:center;width:28px;height:28px;border:1px solid rgba(103,232,249,.2);border-radius:9px;background:rgba(8,145,178,.1);font-size:.85rem}
#onboardOverlay .ob-title{margin:0 0 12px;color:#f8fafc;font-family:var(--font-head);font-size:clamp(1.45rem,3.2vw,2.15rem);font-weight:950;line-height:1.45;letter-spacing:-.025em}
#onboardOverlay .ob-text{margin:0;color:#cbd5e1;font-size:clamp(.91rem,1.6vw,1rem);line-height:1.95}
#onboardOverlay .ob-checklist{display:grid;gap:8px;margin:17px 0 0;padding:0;list-style:none}
#onboardOverlay .ob-checklist li{position:relative;padding-right:25px;color:#dbeafe;font-size:.81rem;line-height:1.75}
#onboardOverlay .ob-checklist li:before{content:"✓";position:absolute;right:0;top:1px;display:grid;place-items:center;width:17px;height:17px;border:1px solid rgba(103,232,249,.25);border-radius:50%;background:rgba(8,145,178,.12);color:#67e8f9;font-size:.66rem;font-weight:950}
#onboardOverlay .ob-outcome{margin-top:15px;padding:12px 14px;border:1px solid rgba(139,92,246,.2);border-radius:13px;background:rgba(139,92,246,.09);color:#e0e7ff;font-size:.78rem;line-height:1.8}
#onboardOverlay .ob-outcome strong{color:#c4b5fd}
#onboardOverlay .ob-tip{display:flex;align-items:flex-start;gap:9px;margin-top:11px;padding:11px 13px;border:1px solid rgba(34,211,238,.15);border-radius:13px;background:rgba(8,145,178,.075);color:#cbd5e1;font-size:.76rem;line-height:1.8}
#onboardOverlay .ob-tip-icon{flex:0 0 auto;color:#67e8f9;font-weight:950}
#onboardOverlay .ob-footer{display:flex;align-items:center;justify-content:space-between;gap:14px;padding-top:16px;border-top:1px solid rgba(255,255,255,.09)}
#onboardOverlay .ob-skip{border:0;background:none;color:#94a3b8;font:inherit;font-size:.8rem;cursor:pointer;text-decoration:underline;text-underline-offset:4px}
#onboardOverlay .ob-skip:hover{color:#e2e8f0}
#onboardOverlay .ob-nav{display:flex;align-items:center;gap:10px;flex-wrap:wrap}
#onboardOverlay .ob-btn{display:inline-flex;align-items:center;justify-content:center;gap:9px;min-height:46px;padding:11px 20px;border:1px solid rgba(255,255,255,.13);border-radius:13px;font:inherit;font-size:.86rem;font-weight:900;cursor:pointer;transition:transform .18s,box-shadow .18s,background .18s}
#onboardOverlay .ob-btn:hover{transform:translateY(-2px)}
#onboardOverlay .ob-btn:active{transform:translateY(0) scale(.98)}
#onboardOverlay .ob-btn.primary{border-color:transparent;background:linear-gradient(110deg,#7c3aed,#4f46e5 55%,#0891b2);color:#fff;box-shadow:0 10px 28px rgba(79,70,229,.28)}
#onboardOverlay .ob-btn.primary:hover{box-shadow:0 14px 34px rgba(79,70,229,.4)}
#onboardOverlay .ob-btn.ghost{background:rgba(255,255,255,.045);color:#dbeafe}
#onboardOverlay .ob-btn.ghost:hover{background:rgba(255,255,255,.09)}
#onboardOverlay button:focus-visible{outline:3px solid #67e8f9;outline-offset:3px}
#onboardOverlay .ob-sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
@media(max-width:720px){
#onboardOverlay.onboard-overlay{padding:10px}
#onboardOverlay .onboard-box{width:calc(100vw - 20px);max-height:calc(100dvh - 20px);padding:17px 15px;border-radius:22px}
#onboardOverlay .ob-shell{gap:14px}
#onboardOverlay .ob-brand-mark{width:34px;height:34px;border-radius:11px}
#onboardOverlay .ob-brand-copy strong{font-size:.68rem}
#onboardOverlay .ob-brand-copy small{font-size:.65rem}
#onboardOverlay .ob-count{padding:7px 9px;font-size:.7rem}
#onboardOverlay .ob-close{width:38px;height:38px}
#onboardOverlay .ob-content{grid-template-columns:1fr;grid-template-areas:"copy" "visual";gap:14px;min-height:0}
#onboardOverlay .ob-visual{grid-area:visual;min-height:205px;padding:16px;border-radius:18px}
#onboardOverlay .ob-journey{grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}
#onboardOverlay .ob-journey-item{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:7px;min-width:0;padding:10px 5px;text-align:center}
#onboardOverlay .ob-journey-num{width:30px;height:30px;border-radius:10px}
#onboardOverlay .ob-journey-item strong{font-size:.72rem}
#onboardOverlay .ob-journey-item small{font-size:.58rem}
#onboardOverlay .ob-template-sample{min-height:94px}
#onboardOverlay .ob-face-card{min-height:150px;padding:11px}
#onboardOverlay .ob-copy{grid-area:copy;text-align:right}
#onboardOverlay .ob-title{font-size:1.4rem;margin-bottom:8px}
#onboardOverlay .ob-text{font-size:.87rem;line-height:1.8}
#onboardOverlay .ob-checklist{gap:6px;margin-top:12px}
#onboardOverlay .ob-checklist li{font-size:.75rem}
#onboardOverlay .ob-outcome{margin-top:11px;padding:10px 11px;font-size:.72rem}
#onboardOverlay .ob-tip{margin-top:9px;padding:9px 11px;font-size:.7rem}
#onboardOverlay .ob-footer{align-items:stretch;flex-direction:column-reverse;gap:10px;padding-top:12px}
#onboardOverlay .ob-nav{display:grid;grid-template-columns:1fr 1.25fr}
#onboardOverlay .ob-btn{min-height:46px;padding:10px 12px;font-size:.8rem}
#onboardOverlay .ob-skip{align-self:center;padding:5px}
}
@media(max-width:370px){
#onboardOverlay .ob-top{gap:6px}
#onboardOverlay .ob-brand{gap:7px}
#onboardOverlay .ob-brand-copy small{display:none}
#onboardOverlay .ob-count{padding:6px 7px;font-size:.65rem}
#onboardOverlay .ob-visual{min-height:180px;padding:12px}
#onboardOverlay .ob-template-samples{gap:5px}
#onboardOverlay .ob-template-sample{min-height:82px}
#onboardOverlay .ob-face-grid{gap:7px}
#onboardOverlay .ob-face-card{min-height:132px;padding:8px}
}
@media(max-height:680px) and (min-width:721px){
#onboardOverlay .onboard-box{max-height:calc(100dvh - 20px);padding:18px}
#onboardOverlay .ob-content{min-height:0}
#onboardOverlay .ob-visual{min-height:230px}
}
@media(prefers-reduced-motion:reduce){
#onboardOverlay *,#onboardOverlay *:before,#onboardOverlay *:after{animation-duration:.01ms!important;transition-duration:.01ms!important;scroll-behavior:auto!important}
}"""

TOUR_JS = r"""var ONBOARD_DECK = "__DECK__";
var ONBOARD_IS_FRENCH = ONBOARD_DECK === "fr9";
var ONBOARD_PRIMARY_LANGUAGE = ONBOARD_IS_FRENCH ? "الفرنسية" : "الإنجليزية";
var ONBOARD_SAMPLE_WORD = ONBOARD_DECK === "en9" ? "Student" : ONBOARD_DECK === "enlit" ? "Novel" : ONBOARD_DECK === "ensci" ? "Atom" : "Leçon";
var ONBOARD_SAMPLE_MEANING = ONBOARD_DECK === "en9" ? "طالب" : ONBOARD_DECK === "enlit" ? "رواية" : ONBOARD_DECK === "ensci" ? "ذرة" : "درس";
var ONBOARD_STORAGE_KEY = "anki_" + ONBOARD_DECK + "_onboarded";

var ONBOARD_STEPS=[
  {icon:'✦',label:'خريطة الطريق',title:'من قالب مناسب إلى رزمة جاهزة لـ Anki',text:'المعرض يساعدك على اختيار شكل البطاقات وتجهيزه للرزمة. سنمشي معًا في المسار كاملًا: اكتشاف التصاميم، فحص البطاقة، اختيار القوالب، ضبط الصوت، ثم إنشاء ملف الرزمة.',checks:['لن يتغير محتوى كلمات رُزمتك بسبب مشاهدة الجولة.','لن يُنشأ ملف أو يبدأ التصدير إلا عندما تختار ذلك بنفسك.'],outcome:'بعد الجولة ستعرف أين تبحث، وما الذي تفحصه، وكيف تصل إلى ملف APKG.',tip:'اعتبرها خريطة استخدام؛ تستطيع الانتقال بين الخطوات أو تخطي الجولة.',visual:'journey'},
  {icon:'⌕',label:'اكتشف التصميم',title:'اعثر على القالب المناسب دون تضييع الوقت',text:'تضم هذه الصفحة مكتبة من 100 تصميم. ابدأ بالبحث عن اسم أو فكرة، أو استخدم التصنيفات لتقليل النتائج. عندما يلفت قالب انتباهك، افتحه للمعاينة بدل الاعتماد على صورته المصغّرة فقط.',checks:['استخدم البحث عندما تعرف ما تريد.','استخدم التصنيفات والمجموعات عندما تريد استكشاف الخيارات.'],outcome:'النتيجة المطلوبة: قائمة قصيرة من التصاميم التي تستحق الفحص.',tip:'لا تختَر بسرعة؛ الصورة المصغّرة تعطي انطباعًا أوليًا فقط.',visual:'discover'},
  {icon:'◫',label:'افحص البطاقة',title:'اختبر الوجهين قبل اعتماد أي تصميم',text:'افتح المعاينة المفردة، ثم راجع الوجه الأمامي والوجه الخلفي. تأكد من أن الكلمة والترجمة واضحتان، وأن المسافات والخطوط مريحة على شاشة الهاتف. في المعاينة الكبيرة استخدم زر «قلب البطاقة» الموجود داخلها لرؤية الوجه الآخر.',checks:['اقرأ النصوص كما ستظهر أثناء المراجعة.','تأكد من أن الوجهين متوازنان ولا يخفي التصميم معلومة مهمة.'],outcome:'النتيجة المطلوبة: قالب واضح ومريح في الاستخدام الفعلي، لا في الصورة فقط.',tip:'افحص الوجهين دائمًا؛ جمال الوجه الأمامي وحده لا يكفي.',visual:'inspect'},
  {icon:'✓',label:'حدّد القوالب',title:'اختر ما تريد استخدامه في رُزمتك',text:'بعد المقارنة، حدّد القالب الذي يناسبك. يمكنك اختيار قالب واحد أو أكثر بحسب التنوع الذي تريده. اجعل الاختيار مقصودًا: وضوح المعلومة وسهولة قراءتها أهم من كثرة الأشكال.',checks:['اختر قالبًا واحدًا لمظهر موحّد، أو أكثر إذا كنت تريد تنويع البطاقات.','راجع التحديد قبل الانتقال إلى إعدادات الرزمة.'],outcome:'النتيجة المطلوبة: مجموعة قوالب مختارة عن قصد وجاهزة للتطبيق.',tip:'ابدأ بعدد قليل ومتناسق؛ يمكنك تعديل اختيارك قبل إنشاء الرزمة.',visual:'choose'},
  {icon:'♫',label:'جهّز الصوت',title:'اضبط نطق اللغتين قبل التصدير',text:'اختر صوتًا مناسبًا للغة الأساسية (' + ONBOARD_PRIMARY_LANGUAGE + ') وللعربية، ثم جرّب المعاينة الصوتية. اضبط السرعة والنغمة والفواصل الزمنية كما يناسبك، وراجع خيار تضمين الصوت حتى تعرف هل سيُرفق الصوت بملف APKG.',checks:['استمع إلى عينة قصيرة لكل لغة قبل إنشاء الرزمة.','فعّل تضمين الصوت عند رغبتك في إرفاق الملفات الصوتية داخل الرزمة.'],outcome:'النتيجة المطلوبة: نطق واضح وإعدادات صوت مفهومة قبل التصدير.',tip:'اختبر عينة أولًا؛ لا تنتظر حتى إنشاء الرزمة كاملة لاكتشاف أن الصوت غير مناسب.',visual:'audio'},
  {icon:'⇩',label:'أنشئ رُزمتك',title:'راجع اختياراتك ثم صدّر ملف APKG',text:'قبل الإنشاء، راجع القوالب التي اخترتها وإعدادات الصوت. بعد ذلك نفّذ أمر إنشاء الرزمة ونزّل ملف APKG، ثم افتحه باستخدام تطبيق Anki لاستيراد البطاقات والبدء بمراجعتها.',checks:['تأكد من أنك اخترت القوالب وإعدادات الصوت المطلوبة.','احتفظ بنسخة من ملف APKG بعد تنزيله.','افتح الملف في Anki لإتمام الاستيراد.'],outcome:'أصبحت تعرف المسار من اختيار التصميم حتى استيراد الرزمة في Anki.',tip:'هذه هي الخطوة التي تنشئ الملف فعلًا؛ راجع اختياراتك قبل تنفيذها.',visual:'export'}
];

var onbStep=0;
var onboardPreviousOverflow='';
var onboardReturnFocus=null;

function escapeOnboardText(value){
  return String(value).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;').replace(/'/g,'&#39;');
}

function renderOnboardVisual(kind){
  var word=escapeOnboardText(ONBOARD_SAMPLE_WORD);
  var meaning=escapeOnboardText(ONBOARD_SAMPLE_MEANING);
  var primary=escapeOnboardText(ONBOARD_PRIMARY_LANGUAGE);
  if(kind==='journey'){
    return '<div class="ob-journey">'+
      '<div class="ob-journey-item"><span class="ob-journey-num">01</span><div><strong>اكتشف</strong><small>ابحث بين التصاميم</small></div></div>'+
      '<div class="ob-journey-item"><span class="ob-journey-num">02</span><div><strong>افحص واختر</strong><small>راجع الوجهين وحدّد القالب</small></div></div>'+
      '<div class="ob-journey-item is-final"><span class="ob-journey-num">03</span><div><strong>أنشئ واستورد</strong><small>ملف APKG ثم Anki</small></div></div>'+
      '</div><div class="ob-visual-caption">مسار واضح من أول اختيار إلى أول مراجعة</div>';
  }
  if(kind==='discover'){
    return '<div class="ob-search-mock"><span class="ob-search-icon">⌕</span><span>ابحث عن كلمة أو تصميم...</span></div>'+
      '<div class="ob-chip-row"><span class="active">الكل</span><span>بسيط</span><span>ملوّن</span><span>مجموعات</span></div>'+
      '<div class="ob-template-samples"><div class="ob-template-sample"><i></i><small>تصميم 01</small></div><div class="ob-template-sample"><i></i><small>تصميم 02</small></div><div class="ob-template-sample"><i></i><small>تصميم 03</small></div></div>'+
      '<div class="ob-visual-caption">ابحث ← صفِّ النتائج ← افتح المعاينة</div>';
  }
  if(kind==='inspect'){
    return '<div class="ob-face-grid"><article class="ob-face-card"><span class="ob-face-label">الوجه الأمامي</span><strong>'+word+'</strong><small>الكلمة الأساسية</small><em>اقرأ بوضوح</em></article><article class="ob-face-card back"><span class="ob-face-label">الوجه الخلفي</span><strong>'+meaning+'</strong><small>المعنى والترجمة</small><em>اقلب البطاقة للفحص</em></article></div>'+
      '<div class="ob-visual-caption">مثال توضيحي — افحص الوجهين في المعاينة الحقيقية</div>';
  }
  if(kind==='choose'){
    return '<div class="ob-pick-grid"><div class="ob-pick-card selected"><span class="ob-pick-art"></span><span class="ob-pick-copy"><strong>قالب مختار</strong><small>ضمن اختيارك</small></span><span class="ob-pick-check">✓</span></div><div class="ob-pick-card"><span class="ob-pick-art"></span><span class="ob-pick-copy"><strong>قالب آخر</strong><small>غير محدد</small></span></div><div class="ob-pick-card selected"><span class="ob-pick-art"></span><span class="ob-pick-copy"><strong>قالب متناسق</strong><small>ضمن اختيارك</small></span><span class="ob-pick-check">✓</span></div><div class="ob-pick-card"><span class="ob-pick-art"></span><span class="ob-pick-copy"><strong>خيار إضافي</strong><small>غير محدد</small></span></div></div>'+
      '<div class="ob-visual-caption">اختر بوعي — ليس بكثرة الاختيارات</div>';
  }
  if(kind==='audio'){
    return '<div class="ob-audio-board"><div class="ob-audio-row"><span class="ob-audio-icon">♫</span><span class="ob-audio-copy"><strong>الصوت '+primary+'</strong><small>اختر الصوت وجرّب النطق</small></span><span class="ob-play-mark">▶</span></div><div class="ob-audio-row secondary"><span class="ob-audio-icon">ع</span><span class="ob-audio-copy"><strong>الصوت العربي</strong><small>معاينة مستقلة للغة الثانية</small></span><span class="ob-play-mark">▶</span></div><div class="ob-audio-sliders"><span class="ob-slider-line">السرعة <i></i></span><span class="ob-slider-line">النغمة <i></i></span><span class="ob-slider-line">الفواصل <i></i></span></div></div>'+
      '<div class="ob-visual-caption">اختر الصوت ← استمع ← اضبط ← قرّر تضمينه</div>';
  }
  return '<div class="ob-export-board"><div class="ob-file-icon">APKG</div><strong>رزمة Anki جاهزة للاستيراد</strong><small>راجع القوالب والصوت، أنشئ الملف، ثم افتحه باستخدام Anki.</small><div class="ob-export-checks"><span>✓ القوالب</span><span>✓ الصوت</span><span>✓ التصدير</span></div></div>';
}

function isOnboardingCompleted(){
  try{return localStorage.getItem(ONBOARD_STORAGE_KEY)==='1';}
  catch(_e){return false;}
}

function markOnboardingCompleted(){
  try{localStorage.setItem(ONBOARD_STORAGE_KEY,'1');}
  catch(_e){}
}

function focusOnboardHeading(){
  window.setTimeout(function(){
    var heading=document.getElementById('onboardStepTitle');
    if(heading&&typeof heading.focus==='function')heading.focus();
  },0);
}

function showOnboarding(){
  var overlay=document.getElementById('onboardOverlay');
  if(!overlay||overlay.open)return;
  onbStep=0;
  renderOnboardStep();
  onboardReturnFocus=document.activeElement;
  onboardPreviousOverflow=document.body.style.overflow||'';
  document.body.style.overflow='hidden';
  if(typeof overlay.showModal==='function'){
    try{overlay.showModal();}
    catch(_e){overlay.setAttribute('open','');}
  }else{
    overlay.setAttribute('open','');
  }
  focusOnboardHeading();
}

function closeOnboarding(){
  var overlay=document.getElementById('onboardOverlay');
  if(overlay){
    if(typeof overlay.close==='function'&&overlay.open)overlay.close();
    else overlay.removeAttribute('open');
  }
  document.body.style.overflow=onboardPreviousOverflow;
  try{
    if(onboardReturnFocus&&onboardReturnFocus.isConnected&&typeof onboardReturnFocus.focus==='function')onboardReturnFocus.focus();
  }catch(_e){}
  onboardReturnFocus=null;
  markOnboardingCompleted();
}

function goToOnboardStep(index){
  var next=Number(index);
  if(!Number.isInteger(next)||next<0||next>=ONBOARD_STEPS.length)return;
  onbStep=next;
  renderOnboardStep();
  focusOnboardHeading();
}

function moveOnboardStep(delta){
  var next=onbStep+Number(delta);
  if(next<0)return;
  if(next>=ONBOARD_STEPS.length){closeOnboarding();return;}
  goToOnboardStep(next);
}

function renderOnboardStep(){
  var box=document.getElementById('onboardBox');
  if(!box)return;
  var step=ONBOARD_STEPS[onbStep];
  if(!step)return;
  var progress='';
  ONBOARD_STEPS.forEach(function(_,i){progress+='<span class="'+(i<=onbStep?'done':'')+'"></span>';});
  var checks='';
  step.checks.forEach(function(item){checks+='<li>'+escapeOnboardText(item)+'</li>';});
  var h='<div class="ob-shell" role="group" aria-label="خطوات الجولة">';
  h+='<div class="ob-top"><div class="ob-brand"><span class="ob-brand-mark" aria-hidden="true">A</span><span class="ob-brand-copy"><strong>ANKI DESIGN STUDIO</strong><small>دليل الاستخدام التفاعلي</small></span></div>';
  h+='<div class="ob-top-actions"><span class="ob-count" aria-hidden="true">الخطوة '+(onbStep+1)+' من '+ONBOARD_STEPS.length+'</span><button class="ob-close" type="button" onclick="closeOnboarding()" aria-label="إغلاق الجولة">×</button></div></div>';
  h+='<div class="ob-progress" role="progressbar" aria-label="التقدم في الجولة" aria-valuemin="1" aria-valuemax="'+ONBOARD_STEPS.length+'" aria-valuenow="'+(onbStep+1)+'">'+progress+'</div>';
  h+='<p class="ob-sr-only" role="status" aria-live="polite">الخطوة '+(onbStep+1)+' من '+ONBOARD_STEPS.length+': '+escapeOnboardText(step.title)+'</p>';
  h+='<div class="ob-content"><div class="ob-visual" role="img" aria-label="'+escapeOnboardText(step.label)+'">'+renderOnboardVisual(step.visual)+'</div>';
  h+='<div class="ob-copy"><p class="ob-kicker"><span class="ob-kicker-icon" aria-hidden="true">'+escapeOnboardText(step.icon)+'</span>'+escapeOnboardText(step.label)+'</p><h2 class="ob-title" id="onboardStepTitle" tabindex="-1">'+escapeOnboardText(step.title)+'</h2><p class="ob-text">'+escapeOnboardText(step.text)+'</p>';
  h+='<ul class="ob-checklist">'+checks+'</ul><div class="ob-outcome"><strong>النتيجة:</strong> '+escapeOnboardText(step.outcome)+'</div>';
  h+='<div class="ob-tip"><span class="ob-tip-icon" aria-hidden="true">✦</span><span>'+escapeOnboardText(step.tip)+'</span></div></div></div>';
  h+='<div class="ob-footer"><button class="ob-skip" type="button" onclick="closeOnboarding()">تخطي الجولة</button><div class="ob-nav">';
  if(onbStep>0)h+='<button class="ob-btn ghost" type="button" onclick="moveOnboardStep(-1)">السابق</button>';
  else h+='<button class="ob-btn ghost" type="button" onclick="closeOnboarding()">إغلاق</button>';
  if(onbStep<ONBOARD_STEPS.length-1)h+='<button class="ob-btn primary" type="button" onclick="moveOnboardStep(1)">التالي <span aria-hidden="true">←</span></button>';
  else h+='<button class="ob-btn primary" type="button" onclick="closeOnboarding()">ابدأ استخدام المعرض <span aria-hidden="true">✓</span></button>';
  h+='</div></div></div>';
  box.innerHTML=h;
  box.setAttribute('aria-labelledby','onboardStepTitle');
}

document.addEventListener('keydown',function(e){
  var overlay=document.getElementById('onboardOverlay');
  if(!overlay||!overlay.hasAttribute('open'))return;
  if(e.key==='Escape'){e.preventDefault();closeOnboarding();return;}
  if(e.key==='Tab'){
    var focusable=Array.prototype.slice.call(overlay.querySelectorAll(
      'button:not([disabled]),a[href],input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])'
    )).filter(function(el){return !!(el.offsetWidth||el.offsetHeight||el.getClientRects().length);});
    if(!focusable.length){e.preventDefault();return;}
    var first=focusable[0],last=focusable[focusable.length-1];
    if(e.shiftKey&&(document.activeElement===first||document.activeElement===overlay)){
      e.preventDefault();last.focus();
    }else if(!e.shiftKey&&document.activeElement===last){
      e.preventDefault();first.focus();
    }
    return;
  }
  var target=e.target;
  var typing=target&&(target.tagName==='INPUT'||target.tagName==='TEXTAREA'||target.tagName==='SELECT'||target.isContentEditable);
  if(typing||e.altKey||e.ctrlKey||e.metaKey)return;
  if(e.key==='ArrowLeft'){e.preventDefault();moveOnboardStep(1);}
  else if(e.key==='ArrowRight'&&onbStep>0){e.preventDefault();moveOnboardStep(-1);}
});"""

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
        'aria-label="جولة سريعة" aria-labelledby="onboardStepTitle" '
        'aria-modal="true" onclick="if(event.target===this)closeOnboarding()">'
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
