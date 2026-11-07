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

/* Guided tour v4: compact contextual coaching, never a second welcome screen. */
#onboardGuideRoot .og-card{width:min(420px,calc(100vw - 24px));max-height:min(38dvh,340px);padding:17px 18px;border:1px solid rgba(155,181,225,.28);border-radius:21px;background:radial-gradient(ellipse at 94% 0,rgba(94,103,224,.18),transparent 48%),linear-gradient(150deg,rgba(15,26,48,.99),rgba(6,14,29,.995));box-shadow:0 24px 72px rgba(0,0,0,.55),0 0 0 1px rgba(255,255,255,.04) inset}
#onboardGuideRoot .og-head{margin-bottom:9px}
#onboardGuideRoot .og-mark{width:31px;height:31px;border-radius:10px}
#onboardGuideRoot .og-brand-copy strong{font-size:.65rem;letter-spacing:.08em}
#onboardGuideRoot .og-brand-copy small{font-size:.6rem}
#onboardGuideRoot .og-close{width:33px;height:33px;border-radius:10px}
#onboardGuideRoot .og-progress{gap:6px;margin-bottom:11px}
#onboardGuideRoot .og-progress button{padding:4px 0}
#onboardGuideRoot .og-progress button span{height:5px}
#onboardGuideRoot .og-meta{margin-bottom:5px}
#onboardGuideRoot .og-step-label{font-size:.69rem}
#onboardGuideRoot .og-count{font-size:.64rem}
#onboardGuideRoot .og-title{margin:0 0 7px;font-size:clamp(1.03rem,1.8vw,1.24rem);line-height:1.42;letter-spacing:-.02em}
#onboardGuideRoot .og-text{font-size:.76rem;line-height:1.68;color:#d3ddec}
#onboardGuideRoot .og-target{display:flex;gap:8px;margin-top:9px;padding:7px 9px;border-radius:11px;background:rgba(34,211,238,.06)}
#onboardGuideRoot .og-target-mark{width:23px;height:23px;border-radius:7px;font-size:.76rem}
#onboardGuideRoot .og-target-copy small{font-size:.57rem}
#onboardGuideRoot .og-target-copy strong{font-size:.69rem}
#onboardGuideRoot .og-note{margin-top:7px;font-size:.62rem;line-height:1.55;color:#9eafc8}
#onboardGuideRoot .og-footer{margin:10px -10px -10px;padding:9px 10px 8px;gap:8px}
#onboardGuideRoot .og-actions{gap:7px}
#onboardGuideRoot .og-btn{min-height:39px;padding:8px 12px;border-radius:11px;font-size:.7rem}
#onboardGuideRoot .og-skip{font-size:.66rem}
body .og-spotlight{outline-width:2px!important;outline-offset:4px!important;box-shadow:0 0 0 6px rgba(34,211,238,.13),0 12px 34px rgba(0,0,0,.22)!important}
@media(max-width:640px){
  #onboardGuideRoot .og-card{width:calc(100vw - 20px);max-height:min(40dvh,320px);padding:14px;border-radius:18px}
  #onboardGuideRoot .og-head{margin-bottom:7px}
  #onboardGuideRoot .og-title{font-size:1rem;line-height:1.4}
  #onboardGuideRoot .og-text{font-size:.72rem;line-height:1.6}
  #onboardGuideRoot .og-target{margin-top:7px;padding:6px 8px}
  #onboardGuideRoot .og-note{font-size:.59rem}
  #onboardGuideRoot .og-footer{margin:8px -8px -8px;padding:8px}
  #onboardGuideRoot .og-btn{min-height:38px;padding:7px 9px;font-size:.66rem}
  #onboardGuideRoot .og-skip{font-size:.62rem}
}
@media(max-width:360px){
  #onboardGuideRoot .og-card{max-height:min(43dvh,300px);padding:11px}
  #onboardGuideRoot .og-text{font-size:.68rem}
  #onboardGuideRoot .og-target{display:none}
  #onboardGuideRoot .og-footer{gap:5px}
}

/* Institutional guided experience v5: editorial navigation, clear hierarchy, task-led actions. */
#onboardTourLauncher{right:22px;bottom:22px;min-height:48px;padding:0 19px;border:1px solid rgba(148,163,184,.24);border-radius:12px;background:#14243b;color:#f8fafc;font-size:.78rem;letter-spacing:.01em;box-shadow:0 12px 32px rgba(5,15,30,.24)}
#onboardTourLauncher:hover{background:#1d3554;filter:none;transform:translateY(-2px);box-shadow:0 16px 38px rgba(5,15,30,.3)}
#onboardGuideRoot{color:#f8fafc}
#onboardGuideRoot .og-card.og-institutional{width:min(456px,calc(100vw - 28px));max-height:min(40dvh,390px);overflow:auto;padding:0;border:1px solid rgba(154,174,203,.24);border-radius:18px;background:#101d30;box-shadow:0 28px 90px rgba(1,8,20,.5),0 0 0 1px rgba(255,255,255,.035) inset;backdrop-filter:blur(18px);scrollbar-width:thin}
#onboardGuideRoot .og-card.og-institutional:before,#onboardGuideRoot .og-card.og-institutional:after{display:none}
#onboardGuideRoot .og-institutional .og-head{display:flex;align-items:center;gap:12px;margin:0;padding:17px 19px;border-bottom:1px solid rgba(190,205,226,.11);background:#13243a}
#onboardGuideRoot .og-institutional .og-brand{gap:10px}
#onboardGuideRoot .og-institutional .og-mark{width:35px;height:35px;border:1px solid rgba(153,181,219,.28);border-radius:10px;background:#233c5c;color:#dbeafe;box-shadow:none;font-size:.82rem}
#onboardGuideRoot .og-institutional .og-brand-copy{gap:3px}
#onboardGuideRoot .og-institutional .og-brand-copy strong{font-size:.66rem;letter-spacing:.11em;color:#f0f5fc}
#onboardGuideRoot .og-institutional .og-brand-copy small{font-size:.63rem;color:#91a5c0}
#onboardGuideRoot .og-institutional .og-head-meta{display:flex;align-items:center;gap:7px;margin-inline-start:auto;color:#a8bad1;font-size:.64rem;white-space:nowrap}
#onboardGuideRoot .og-institutional .og-live-dot{width:7px;height:7px;border-radius:50%;background:#55c2b2;box-shadow:0 0 0 4px rgba(85,194,178,.11)}
#onboardGuideRoot .og-institutional .og-close{width:32px;height:32px;border:1px solid rgba(190,205,226,.16);border-radius:9px;background:rgba(255,255,255,.035);color:#b9c8dc}
#onboardGuideRoot .og-institutional .og-progress-wrap{padding:15px 19px 14px;background:#0d192a;border-bottom:1px solid rgba(190,205,226,.1)}
#onboardGuideRoot .og-institutional .og-progress-meta{display:flex;align-items:center;justify-content:space-between;margin-bottom:11px;color:#8fa4bf;font-size:.64rem}
#onboardGuideRoot .og-institutional .og-progress-meta strong{color:#c8d7ea;font-size:.65rem;font-variant-numeric:tabular-nums;letter-spacing:.06em}
#onboardGuideRoot .og-institutional .og-progress{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:6px;margin:0}
#onboardGuideRoot .og-institutional .og-progress button{display:flex;flex-direction:column;align-items:center;gap:7px;min-width:0;padding:0;border:0;background:none;color:#7489a5}
#onboardGuideRoot .og-institutional .og-progress-index{display:grid;place-items:center;width:27px;height:27px;border:1px solid rgba(145,165,194,.2);border-radius:8px;background:#15253a;font-size:.61rem;font-weight:850;font-variant-numeric:tabular-nums}
#onboardGuideRoot .og-institutional .og-progress-name{display:block;width:100%;overflow:hidden;color:#8498b2;font-size:.54rem;line-height:1.35;text-align:center;text-overflow:ellipsis;white-space:nowrap}
#onboardGuideRoot .og-institutional .og-progress button.done .og-progress-index{border-color:rgba(85,194,178,.36);background:rgba(46,132,125,.2);color:#9ce3d8}
#onboardGuideRoot .og-institutional .og-progress button.current .og-progress-index{border-color:#8cb4e8;background:#29496d;color:#fff;box-shadow:0 0 0 3px rgba(104,153,209,.12)}
#onboardGuideRoot .og-institutional .og-progress button.current .og-progress-name{color:#e0ebf8;font-weight:850}
#onboardGuideRoot .og-institutional .og-content{padding:19px 21px 16px}
#onboardGuideRoot .og-institutional .og-meta{display:flex;align-items:center;gap:9px;margin:0 0 10px}
#onboardGuideRoot .og-institutional .og-step-label{color:#75cfc4;font-size:.65rem;font-weight:900;letter-spacing:.07em}
#onboardGuideRoot .og-institutional .og-count{color:#92a6c0;font-size:.65rem}
#onboardGuideRoot .og-institutional .og-title{margin:0 0 10px;color:#f7f9fc;font-size:clamp(1.15rem,2vw,1.42rem);font-weight:850;line-height:1.45;letter-spacing:-.025em}
#onboardGuideRoot .og-institutional .og-text{margin:0;color:#c0ccdc;font-size:.81rem;line-height:1.9}
#onboardGuideRoot .og-institutional .og-task{display:flex;align-items:center;gap:11px;margin-top:17px;padding:12px 13px;border:1px solid rgba(123,166,211,.2);border-radius:11px;background:#142943}
#onboardGuideRoot .og-institutional .og-task-icon{display:grid;place-items:center;flex:0 0 29px;width:29px;height:29px;border:1px solid rgba(117,207,196,.24);border-radius:8px;background:rgba(58,142,136,.13);color:#8fe0d4;font-size:1rem;font-weight:800}
#onboardGuideRoot .og-institutional .og-task-copy{display:grid;gap:3px;min-width:0}
#onboardGuideRoot .og-institutional .og-task-copy small{color:#8da4bf;font-size:.59rem}
#onboardGuideRoot .og-institutional .og-task-copy strong{color:#e4eef9;font-size:.74rem;font-weight:850}
#onboardGuideRoot .og-institutional .og-note{margin:12px 0 0;color:#91a4bd;font-size:.66rem;line-height:1.7}
#onboardGuideRoot .og-institutional .og-footer{position:sticky;bottom:0;display:flex;align-items:center;justify-content:space-between;gap:10px;margin:0;padding:13px 19px;border-top:1px solid rgba(190,205,226,.11);background:#0d192a}
#onboardGuideRoot .og-institutional .og-skip{color:#9aabc0;font-size:.67rem;text-decoration:none}
#onboardGuideRoot .og-institutional .og-skip:hover{color:#e4eef9}
#onboardGuideRoot .og-institutional .og-actions{gap:7px}
#onboardGuideRoot .og-institutional .og-btn{min-height:40px;padding:8px 13px;border:1px solid rgba(159,183,212,.18);border-radius:9px;font-size:.69rem}
#onboardGuideRoot .og-institutional .og-btn.ghost{background:rgba(255,255,255,.035);color:#c1cee0}
#onboardGuideRoot .og-institutional .og-btn.primary{border-color:#426c9d;background:#315b89;color:#fff;box-shadow:none}
#onboardGuideRoot .og-institutional .og-btn.primary:hover{background:#3c6c9f}
#onboardGuideRoot .og-institutional button:focus-visible{outline:2px solid #8dc8e8;outline-offset:3px}
body .og-spotlight{outline:2px solid #77cfc5!important;outline-offset:5px!important;border-radius:10px!important;box-shadow:0 0 0 8px rgba(77,181,169,.12),0 12px 32px rgba(2,12,26,.22)!important}
@media(max-width:640px){
 #onboardTourLauncher{right:12px;bottom:calc(12px + env(safe-area-inset-bottom,0px));min-height:44px;padding:0 14px}
 #onboardGuideRoot .og-card.og-institutional{width:calc(100vw - 16px);max-height:min(42dvh,340px);border-radius:15px}
 #onboardGuideRoot .og-institutional .og-head{padding:13px 14px}
 #onboardGuideRoot .og-institutional .og-progress-wrap{padding:12px 13px}
 #onboardGuideRoot .og-institutional .og-progress{gap:3px}
 #onboardGuideRoot .og-institutional .og-progress-index{width:24px;height:24px;font-size:.57rem}
 #onboardGuideRoot .og-institutional .og-progress-name{font-size:.48rem}
 #onboardGuideRoot .og-institutional .og-content{padding:15px 15px 13px}
 #onboardGuideRoot .og-institutional .og-title{font-size:1.08rem}
 #onboardGuideRoot .og-institutional .og-text{font-size:.75rem;line-height:1.8}
 #onboardGuideRoot .og-institutional .og-footer{padding:11px 13px}
 #onboardGuideRoot .og-institutional .og-btn{min-height:40px;padding:8px 10px;font-size:.66rem}
}
@media(max-width:360px){
 #onboardGuideRoot .og-card.og-institutional{max-height:76dvh}
 #onboardGuideRoot .og-institutional .og-head-meta{display:none}
 #onboardGuideRoot .og-institutional .og-progress-name{font-size:.43rem}
 #onboardGuideRoot .og-institutional .og-content{padding:12px}
 #onboardGuideRoot .og-institutional .og-text{font-size:.71rem}
 #onboardGuideRoot .og-institutional .og-task{margin-top:12px;padding:9px}
 #onboardGuideRoot .og-institutional .og-footer{gap:5px;padding:9px}
 #onboardGuideRoot .og-institutional .og-btn{padding:7px 8px;font-size:.62rem}
}
@media(prefers-reduced-motion:reduce){#onboardGuideRoot .og-institutional *,#onboardGuideRoot .og-institutional *:before,#onboardGuideRoot .og-institutional *:after{animation:none!important;transition:none!important}}


/* v5 responsive refinement: readable chapter labels and a complete mobile instruction panel. */
#onboardGuideRoot .og-institutional .og-progress button .og-progress-index{height:27px!important;min-height:27px!important;line-height:1}
#onboardGuideRoot .og-institutional .og-progress button .og-progress-name{height:auto!important;min-height:0;overflow:visible;line-height:1.3}
#onboardGuideRoot .og-institutional .og-task{flex:0 0 auto}
@media(max-width:640px){
 #onboardGuideRoot .og-card.og-institutional{max-height:min(55dvh,460px)}
 #onboardGuideRoot .og-institutional .og-head{padding:11px 13px}
 #onboardGuideRoot .og-institutional .og-progress-wrap{padding:9px 13px 8px}
 #onboardGuideRoot .og-institutional .og-progress-meta{margin-bottom:7px}
 #onboardGuideRoot .og-institutional .og-progress{gap:4px}
 #onboardGuideRoot .og-institutional .og-progress button .og-progress-index{width:23px;height:23px!important;min-height:23px!important;font-size:.54rem}
 #onboardGuideRoot .og-institutional .og-progress button .og-progress-name{font-size:.47rem}
 #onboardGuideRoot .og-institutional .og-content{padding:13px 15px 11px}
 #onboardGuideRoot .og-institutional .og-meta{margin-bottom:6px}
 #onboardGuideRoot .og-institutional .og-title{font-size:1.02rem;margin-bottom:7px}
 #onboardGuideRoot .og-institutional .og-text{font-size:.72rem;line-height:1.68}
 #onboardGuideRoot .og-institutional .og-task{margin-top:11px;padding:9px 10px}
 #onboardGuideRoot .og-institutional .og-note{margin-top:8px;font-size:.61rem;line-height:1.55}
 #onboardGuideRoot .og-institutional .og-footer{padding:9px 12px}
}
@media(max-width:360px){
 #onboardGuideRoot .og-card.og-institutional{max-height:min(55dvh,360px)}
 #onboardGuideRoot .og-institutional .og-progress-name{display:none}
 #onboardGuideRoot .og-institutional .og-content{padding:10px 12px}
 #onboardGuideRoot .og-institutional .og-title{font-size:.94rem}
 #onboardGuideRoot .og-institutional .og-text{font-size:.67rem;line-height:1.55}
 #onboardGuideRoot .og-institutional .og-task{margin-top:8px;padding:7px 8px}
 #onboardGuideRoot .og-institutional .og-note{font-size:.57rem;margin-top:6px}
}


"""

TOUR_JS = r"""
var ONBOARD_DECK = "__DECK__";
var ONBOARD_PRIMARY_LANGUAGE = ONBOARD_DECK === "fr9" ? "الفرنسية" : "الإنجليزية";
var ONBOARD_STORAGE_KEY = "anki_" + ONBOARD_DECK + "_onboarded_v5";
var ONBOARD_SNOOZE_KEY = "anki_" + ONBOARD_DECK + "_onboarding_snoozed_v5";
var onboardOpenedBrowser = false;
var onboardOpenedAudio = false;
var onboardPositionFrame = 0;

var ONBOARD_STEPS = [
  {id:"start",label:"بداية الجولة",title:"ابدأ من زر تصفّح القوالب",text:"من زر «تصفّح القوالب» افتح المكتبة. أمامك 100 قالب؛ وبعد فتحها تستطيع استخدام التصنيفات للوصول إلى التصاميم التي تريد فحصها. لا يُضاف أي قالب إلى رُزمتك بمجرد فتح المكتبة.",target:".hero-cta-main",targetLabel:"زر تصفّح القوالب",note:"اضغط الزر المظلّل أو انتقل إلى المكتبة من زر الجولة أدناه."},
  {id:"library",label:"استكشاف المكتبة",title:"صفِّ النتائج ثم افتح تصميماً",text:"استخدم تصنيفات المكتبة لتضييق النتائج، ثم اختر بطاقة من الشبكة لمعاينة تصميمها. فتح البطاقة لا يضيفها إلى اختيارات الرزمة.",target:"#gbFilters .gb-chip",fallback:"#gbGrid .gb-item",targetLabel:"تصنيفات القوالب",note:"اختر بطاقة من الشبكة؛ ستنتقل الجولة تلقائياً إلى معاينتها."},
  {id:"preview",label:"معاينة الوجهين",title:"افحص الوجهين قبل الاختيار",text:"اقلب البطاقة وتحقق من وضوح المفردة ومعناها وتوزيع العناصر. هذه معاينة للتصميم وليست تعديلاً على محتوى الرزمة.",target:"#gvShowAns",fallback:"#gvStage",targetLabel:"زر قلب البطاقة",note:"جرّب زر القلب بنفسك أو انتقل إلى خطوة التحديد."},
  {id:"selection",label:"اعتماد القالب",title:"أضف التصميم إلى اختياراتك",text:"زر التحديد يضيف القالب الحالي أو يزيله من مجموعتك. يمكنك اختيار أكثر من تصميم، ولن تختار الجولة أي قالب نيابةً عنك.",target:"#gvSelectBtn",targetLabel:"زر تحديد القالب",note:"عدد القوالب المختارة يتحدث بعد اختيارك مباشرةً."},
  {id:"audio",label:"إعداد الصوت",title:"اضبط النطق لكل لغة",text:"اختر الصوتين واضبط السرعة والنغمة والفواصل. استخدم زر المعاينة عندما ترغب في الاستماع؛ لن يبدأ أي صوت من تلقاء نفسه.",target:"#gAudioPanelBody select",fallback:"#gAudioPanelBody",targetLabel:"قائمة اختيار الصوت",note:"يمكنك تعديل الإعدادات لاحقاً أيضاً؛ لن يبدأ تشغيل الصوت إلا بطلبك."},
  {id:"export",label:"مراجعة الرزمة",title:"راجع إعداداتك قبل إنشاء الملف",text:"افتح شاشة المراجعة لتفحص اسم الرزمة والقوالب المختارة وإعدادات الصوت. لن يبدأ إنشاء APKG إلا عندما تضغط زر بدء التصدير بنفسك.",target:"#exOpenBtn",targetLabel:"زر مراجعة الرزمة",note:"سنفتح شاشة المراجعة فقط. بعد التنزيل، اتبع قسم «كيفية الاستيراد إلى Anki» أسفل الصفحة؛ ولن نبدأ التنزيل أو إنشاء الملف خلال الجولة."}
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
    // Open the real library from the first guided stop and keep it open while
    // the visitor moves from filters to the template grid.
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
  }else if(index !== 1 && onboardOpenedBrowser && browser && browser.classList.contains("open") && typeof closeGalleryBrowser === "function"){
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
    var before=target.getBoundingClientRect();
    var fixedOverlay=target.closest(".gallery-browser,.help-overlay,.onboard-overlay");
    // The audio settings panel sits below the main preview. Bring its first
    // actual control into the upper viewport band; the coachmark can then sit
    // beneath it without covering the highlighted select.
    if(step.id==="audio"&&!fixedOverlay){
      try{
        target.scrollIntoView({behavior:"instant",block:"start",inline:"nearest"});
        before=target.getBoundingClientRect();
        window.scrollBy(0,before.top-132);
        before=target.getBoundingClientRect();
      }catch(_e){
        try{target.scrollIntoView({behavior:"auto",block:"start",inline:"nearest"});}catch(_e2){}
      }
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
    card.style.maxHeight=(width<=640?Math.min(height*.55,460):Math.min(height*.43,430))+"px";
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
  }
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
  var root=onboardEnsureRoot();
  var step=ONBOARD_STEPS[onbStep];
  if(!step)return;
  var review=step.id==="export"&&onboardReviewOpened;
  var title=review?"راجع إعدادات رُزمتك قبل إنشائها":step.title;
  var body=review?"في نافذة المراجعة، تأكد من اسم الرزمة والقوالب التي اخترتها وإعدادات الصوت وخيارات التضمين. يمكنك إغلاق النافذة والعودة إلى المعرض لإجراء أي تعديل.":step.text;
  var targetLabel=review?"زر إغلاق نافذة المراجعة":step.targetLabel;
  var note=review?"هذه مراجعة فقط؛ لم يبدأ إنشاء ملف APKG. لن يبدأ إلا عندما تضغط «بدء التصدير» بنفسك.":step.note;
  var primaryLabel=onbStep===0?"افتح مكتبة القوالب":
    onbStep===1?"اعرض هذا التصميم":
    onbStep===2?"اقلب البطاقة":
    onbStep===3?"انتقل إلى الصوت":
    onbStep===4?"راجع الرزمة":
    (review?"إنهاء الجولة":"افتح المراجعة");
  var primaryAction=onbStep===0?"start":
    onbStep===1?"preview":
    onbStep===2?"flip":
    onbStep===3?"audio":
    onbStep===4?"export":
    (review?"finish":"review");

  var card=onboardNode("section","og-card og-institutional");
  card.setAttribute("role","dialog");
  card.setAttribute("aria-modal","false");
  card.setAttribute("aria-labelledby","onboardGuideTitle");
  card.setAttribute("aria-describedby","onboardGuideText");

  var head=onboardNode("header","og-head");
  var brand=onboardNode("div","og-brand");
  brand.appendChild(onboardNode("span","og-mark","A"));
  var brandCopy=onboardNode("span","og-brand-copy");
  brandCopy.appendChild(onboardNode("strong","","ANKI DESIGN STUDIO"));
  brandCopy.appendChild(onboardNode("small","","دليل استخدام المعرض"));
  brand.appendChild(brandCopy);
  var headMeta=onboardNode("div","og-head-meta");
  headMeta.appendChild(onboardNode("span","og-live-dot",""));
  headMeta.appendChild(onboardNode("span","","جولة تفاعلية"));
  var close=onboardNode("button","og-close","×");
  close.type="button";close.setAttribute("data-guide-action","close");
  close.setAttribute("aria-label","إغلاق الجولة");
  head.appendChild(brand);head.appendChild(headMeta);head.appendChild(close);
  card.appendChild(head);

  var progressWrap=onboardNode("div","og-progress-wrap");
  var progressMeta=onboardNode("div","og-progress-meta");
  progressMeta.appendChild(onboardNode("span","","مسار التعرّف"));
  progressMeta.appendChild(onboardNode("strong","",String(onbStep+1).padStart(2,"0")+" / "+String(ONBOARD_STEPS.length).padStart(2,"0")));
  progressWrap.appendChild(progressMeta);
  var progress=onboardNode("nav","og-progress");
  progress.setAttribute("aria-label","مراحل الجولة");
  ONBOARD_STEPS.forEach(function(item,index){
    var button=onboardNode("button",index<onbStep?"done":(index===onbStep?"current":""));
    button.type="button";button.setAttribute("data-guide-step",String(index));
    button.setAttribute("aria-label","الانتقال إلى المرحلة "+(index+1)+": "+item.label);
    button.setAttribute("aria-current",index === onbStep ? "step" : "false");
    button.appendChild(onboardNode("span","og-progress-index",String(index+1).padStart(2,"0")));
    button.appendChild(onboardNode("span","og-progress-name",item.label));
    progress.appendChild(button);
  });
  progressWrap.appendChild(progress);card.appendChild(progressWrap);

  var content=onboardNode("div","og-content");
  var meta=onboardNode("div","og-meta");
  meta.appendChild(onboardNode("span","og-step-label","المرحلة "+String(onbStep+1).padStart(2,"0")));
  meta.appendChild(onboardNode("span","og-count",step.label));
  content.appendChild(meta);
  var heading=onboardNode("h2","og-title",title);heading.id="onboardGuideTitle";heading.tabIndex=-1;
  content.appendChild(heading);
  var description=onboardNode("p","og-text",body);description.id="onboardGuideText";description.setAttribute("aria-live","polite");
  content.appendChild(description);

  var task=onboardNode("div","og-task");
  task.appendChild(onboardNode("span","og-task-icon","↗"));
  var taskCopy=onboardNode("span","og-task-copy");
  taskCopy.appendChild(onboardNode("small","","الإجراء داخل الصفحة"));
  taskCopy.appendChild(onboardNode("strong","",targetLabel));
  task.appendChild(taskCopy);content.appendChild(task);

  var status=onboardNode("p","og-note",note);status.id = "onboardGuideNote";
  status.setAttribute("role","status");status.setAttribute("aria-live","polite");
  content.appendChild(status);card.appendChild(content);

  var footer=onboardNode("footer","og-footer");
  var later=onboardNode("button","og-skip","إنهاء لاحقاً");
  later.type="button";later.setAttribute("data-guide-action","later");footer.appendChild(later);
  var actions=onboardNode("div","og-actions");
  if(onbStep>0){var previous=onboardNode("button","og-btn ghost","السابق");previous.type="button";previous.setAttribute("data-guide-action","previous");actions.appendChild(previous);}
  var primary=onboardNode("button","og-btn primary",primaryLabel);primary.type="button";primary.setAttribute("data-guide-action",primaryAction);actions.appendChild(primary);
  footer.appendChild(actions);card.appendChild(footer);

  var backdrop=document.createElementNS("http://www.w3.org/2000/svg","svg");
  backdrop.setAttribute("class","og-backdrop");backdrop.setAttribute("aria-hidden","true");
  backdrop.setAttribute("focusable","false");backdrop.setAttribute("viewBox","0 0 100 100");backdrop.setAttribute("preserveAspectRatio","none");
  var path=document.createElementNS("http://www.w3.org/2000/svg","path");
  path.setAttribute("id","ogBackdropPath");path.setAttribute("fill","rgba(3,7,18,.48)");
  path.setAttribute("fill-rule","evenodd");path.setAttribute("d","M0 0H100V100H0Z");backdrop.appendChild(path);
  while(root.firstChild)root.removeChild(root.firstChild);
  root.appendChild(backdrop);root.appendChild(card);
  if(heading&&typeof heading.focus==="function")heading.focus({preventScroll:true});
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
  if(onbStep === 0 && target.closest(".hero-cta-main")){
    window.setTimeout(function(){if(onboardGuideOpen && onbStep === 0)goToOnboardStep(1);},360);
    return;
  }
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
