const express = require('express');
const path = require('path');
const initSqlJs = require('sql.js');
const crypto = require('crypto');
const fs = require('fs');
const zlib = require('zlib');

process.on('uncaughtException', e => console.error('🔴 CRASH:', e.message));
process.on('unhandledRejection', e => console.error('🔴 REJECT:', e));

const app = express();
const PORT = process.env.PORT || 3000;
app.use(express.json({ limit: '10mb' }));
app.use(express.static(path.join(__dirname, 'public')));

let VOCAB_DATA = null, REPEATED_DATA = null;
try { VOCAB_DATA = JSON.parse(fs.readFileSync(path.join(__dirname, 'parsed_data_full.json'), 'utf8')); } catch(e) {}
try { REPEATED_DATA = JSON.parse(fs.readFileSync(path.join(__dirname, 'repeated_data.json'), 'utf8')); } catch(e) {}

function stableId(n){let h=0;for(let i=0;i<n.length;i++)h=((h<<5)-h+n.charCodeAt(i))|0;return Math.abs(h)+1000000000;}

function getAllWords(){
  if(!VOCAB_DATA)return[];
  const w=[];
  for(const uk of Object.keys(VOCAB_DATA)){const un=parseInt(uk.split('_')[1]);
    for(const x of(VOCAB_DATA[uk].noms||[]))w.push({word:x.singulier,arabe:x.arabe,type:'Nom',type_fr:'N.',unit:un,page:x.page||'',pluriel:x.pluriel||'',feminin_s:'',feminin_p:'',preposition:'',auxiliaire:'',participe:'',synonyme:x.synonyme||'',contraire:x.contraire||'',masculin_s:'',masculin_p:''});
    for(const x of(VOCAB_DATA[uk].adj||[]))w.push({word:x.masculin_s,arabe:x.arabe,type:'Adjectif',type_fr:'Adj.',unit:un,page:x.page||'',pluriel:'',feminin_s:x.feminin_s||'',feminin_p:x.feminin_p||'',masculin_s:x.masculin_s||'',masculin_p:x.masculin_p||'',preposition:'',auxiliaire:'',participe:'',synonyme:x.synonyme||'',contraire:x.contraire||''});
    for(const x of(VOCAB_DATA[uk].verbs||[]))w.push({word:x.verbe,arabe:x.arabe,type:'Verbe',type_fr:'V.',unit:un,page:x.page||'',pluriel:'',feminin_s:'',feminin_p:'',masculin_s:'',masculin_p:'',preposition:x.preposition||'',auxiliaire:x.auxiliaire||'',participe:x.participe||'',synonyme:x.synonyme||'',contraire:''});
  }
  return w;
}

function getImportantWords(){
  if(!REPEATED_DATA)return[];
  const r=[];
  for(const cat of['noms','adj','verbs'])for(const x of(REPEATED_DATA[cat]||[]).slice(0,30))
    r.push({word:x.word,arabe:x.arabe,type:x.type||'',type_fr:(x.type||'').substring(0,2)+'.',unit:(x.units&&x.units[0])||1,page:'',pluriel:'',feminin_s:'',feminin_p:'',masculin_s:'',masculin_p:'',preposition:'',auxiliaire:'',participe:'',synonyme:'',contraire:'',starred:true});
  return r;
}

function hexToRgb(h){if(!h||h.includes('gradient')||h.startsWith('rgba'))return'255,255,255';h=h.replace('#','');if(h.length===3)h=h[0]+h[0]+h[1]+h[1]+h[2]+h[2];return`${parseInt(h.substr(0,2),16)},${parseInt(h.substr(2,2),16)},${parseInt(h.substr(4,2),16)}`;}

function buildCSS(c){
  const fontFr=c.fontFrench||"'Inter',sans-serif";
  const fontAr=c.fontArabic||"'Noto Sans Arabic',sans-serif";
  const fsFr=c.frenchFontSize||2.4,fwFr=c.frenchFontWeight||900;
  const fsAr=c.meaningFontSize||1.5,fwAr=c.meaningFontWeight||800;
  const lsFr=c.frenchLetterSpacing||0,lhFr=c.frenchLineHeight||1.2;
  const bg=c.cardBg||'#fff',bg2=c.cardBg2||'';
  const fc=c.frenchColor||'#1e293b',mc=c.meaningColor||'#1e40af',tc=c.textColor||'#333';
  const mb=c.meaningBg||'#eff6ff',mbd=c.meaningBorder||'#bfdbfe';
  const mbr=c.meaningBorderRadius||16,mbw=c.meaningBorderWidth||2;
  const bnbg=c.badgeNomBg||'#dbeafe',bnc=c.badgeNomColor||'#1e40af';
  const babg=c.badgeAdjBg||'#fef3c7',bac=c.badgeAdjColor||'#92400e';
  const bvbg=c.badgeVerbBg||'#d1fae5',bvc=c.badgeVerbColor||'#065f46';
  const ubg=c.unitBg||'#f0fdf4',uc=c.unitColor||'#166534',ubd=c.unitBorder||'#bbf7d0';
  const sb=c.secBg||'#f8f9fa',sbd=c.secBorder||'#e2e8f0';
  const sc=c.secTextColor||'#333',lc=c.labelColor||'#999';
  const br=c.borderRadius||16,pd=c.cardPadding||28,cmw=c.cardMinHeight||300;
  const cd=c.cardDirection||'column',ca=c.cardAlign||'center',cg=c.cardGap||10;
  const cbw=c.cardBorderWidth||0,cbc=c.cardBorderColor||'#e2e8f0';
  const csh=c.cardShadow||'none';
  const bgImg=c.cardBgImage||'',bgOp=c.cardBgOpacity||1,bgBl=c.cardBgBlur||0;
  const fts=c.frenchTextShadow||'',mts=c.meaningTextShadow||'';
  const bsh=c.badgeShadow||'',ush=c.unitShadow||'',ssh=c.secShadow||'';
  let bgStyle=bg;
  if(bg2&&bg!==bg2)bgStyle=`linear-gradient(${c.bgGradientDir||'135deg'},${bg},${bg2})`;
  const fx=c.effect||'none';
  const effects={none:'',neon:'@keyframes np{0%,100%{text-shadow:0 0 20px currentColor}50%{text-shadow:0 0 40px currentColor,0 0 80px currentColor}}.french{animation:np 2s ease-in-out infinite}',wave:'@keyframes wv{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}.french{animation:wv 3s ease-in-out infinite}',sakura:'@keyframes sk{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-2px) rotate(1deg)}}.french{animation:sk 4s ease-in-out infinite}',ember:'@keyframes em{0%,100%{text-shadow:0 0 15px currentColor}50%{text-shadow:0 0 35px currentColor}}.french{animation:em 2.5s ease-in-out infinite}',float:'@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}.french{animation:fl 3s ease-in-out infinite}',glow:'@keyframes gw{0%,100%{box-shadow:0 0 5px currentColor}50%{box-shadow:0 0 25px currentColor}}.card{animation:gw 3s ease-in-out infinite}',scanline:'@keyframes sl{0%{box-shadow:inset 0 0 0 1000px rgba(0,0,0,.02)}50%{box-shadow:inset 0 0 0 1000px rgba(0,0,0,0)}}.card{animation:sl 4s linear infinite}',heartbeat:'@keyframes hb{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}.french{animation:hb 1.5s ease-in-out infinite}',rotate:'@keyframes rt{from{transform:rotate(0)}to{transform:rotate(360deg)}}.card::before{content:"";position:absolute;top:-50%;left:-50%;width:200%;height:200%;background:conic-gradient(from 0deg,rgba(255,0,128,.06),rgba(0,200,255,.06),rgba(128,0,255,.06));animation:rt 10s linear infinite;z-index:0}.card>*{position:relative;z-index:1}',pulse_border:'@keyframes pb{0%,100%{border-color:rgba(0,0,0,.08)}50%{border-color:rgba(0,0,0,.25)}}.card{animation:pb 2s ease-in-out infinite}',gradient:'@keyframes gds{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}.card{background-size:200% 200%;animation:gds 8s ease infinite}',shimmer:'@keyframes sh{0%{background-position:-200% 0}100%{background-position:200% 0}}.french{background:linear-gradient(90deg,transparent 30%,rgba(255,255,255,.3) 50%,transparent 70%);background-size:200% 100%;-webkit-background-clip:text;-webkit-text-fill-color:transparent;animation:sh 3s infinite}',bounce:'@keyframes bn{0%,100%{transform:translateY(0)}25%{transform:translateY(-8px)}75%{transform:translateY(4px)}}.french{animation:bn 2s ease-in-out infinite}',zoom:'@keyframes zm{0%,100%{transform:scale(1)}50%{transform:scale(1.08)}}.french{animation:zm 2s ease-in-out infinite}',glitch:'@keyframes gl{0%,100%{text-shadow:2px 0 #ff0080,-2px 0 #00ffff}50%{text-shadow:-2px 0 #ff0080,2px 0 #00ffff}}.french{animation:gl .3s linear infinite}',wobble:'@keyframes wb{0%,100%{transform:rotate(0)}25%{transform:rotate(2deg)}75%{transform:rotate(-2deg)}}.french{animation:wb 1s ease-in-out infinite}',fade_scale:'@keyframes fs{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.7;transform:scale(.95)}}.meaning{animation:fs 3s ease-in-out infinite}',slide_left:'@keyframes sll{0%,100%{transform:translateX(0)}50%{transform:translateX(-5px)}}.french{animation:sll 3s ease-in-out infinite}',glow_text:'@keyframes gt{0%,100%{text-shadow:0 0 5px currentColor}50%{text-shadow:0 0 15px currentColor,0 0 30px currentColor,0 0 45px currentColor}}.french{animation:gt 2s ease-in-out infinite}'};
  const sepStyles={solid:'1px solid',dashed:'1px dashed',dotted:'1px dotted',double:'3px double',none:'none',thick:'4px solid'};
  const sepStyle=sepStyles[c.separatorStyle]||'1px dashed';
  const sepColor=c.separatorColor||sbd;
  const sepWidth=c.separatorWidth||1;
  return `@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+Arabic:wght@400;600;700;800;900&family=Inter:wght@300;400;500;600;700;800;900&family=Poppins:wght@400;600;800&family=Playfair+Display:wght@700;900&family=Cairo:wght@400;700;900&display=swap');
.card{font-family:${fontAr};text-align:center;direction:rtl;padding:${pd}px 20px;min-height:${cmw}px;display:flex;flex-direction:${cd};align-items:${ca};justify-content:center;background:${bgStyle};color:${tc};position:relative;overflow:hidden;gap:${cg}px;${cbw?`border:${cbw}px solid ${cbc};`:''}${csh!=='none'?`box-shadow:${csh};`:''}${bgImg?`background-image:url('${bgImg}');background-size:cover;background-position:center;`:''}}
${bgImg?`.card::before{content:"";position:absolute;inset:0;background:rgba(${hexToRgb(bg)},${bgOp});${bgBl?`backdrop-filter:blur(${bgBl}px);`:''}z-index:0}.card>*{position:relative;z-index:1}`:''}
.french{font-family:${fontFr};font-size:${fsFr}em;font-weight:${fwFr};direction:ltr;unicode-bidi:embed;color:${fc};margin-bottom:4px;${lsFr?`letter-spacing:${lsFr}px;`:''}${lhFr?`line-height:${lhFr};`:''}${fts?`text-shadow:${fts};`:''}}
.meaning{font-family:${fontAr};font-size:${fsAr}em;font-weight:${fwAr};direction:rtl;padding:12px 20px;border-radius:${mbr}px;margin:6px 0;background:${mb};border:${mbw}px solid ${mbd};color:${mc};max-width:90%;${mts?`text-shadow:${mts};`:''}}
.badge{display:inline-block;font-size:.72em;font-weight:700;padding:4px 14px;border-radius:20px;direction:ltr;margin:2px;${bsh?`box-shadow:${bsh};`:''}}
.badge-nom{background:${bnbg};color:${bnc}}.badge-adj{background:${babg};color:${bac}}.badge-verb{background:${bvbg};color:${bvc}}
.unit-badge{display:inline-block;font-size:.68em;font-weight:700;padding:3px 12px;border-radius:20px;direction:ltr;margin:2px;background:${ubg};color:${uc};border:1px solid ${ubd};${ush?`box-shadow:${ush};`:''}}
.section{background:${sb};border:1px solid ${sbd};border-radius:12px;padding:10px 16px;margin:4px 0;width:100%;max-width:480px;direction:rtl;text-align:center;${ssh?`box-shadow:${ssh};`:''}}
.section-label{font-size:.6em;color:${lc};text-transform:uppercase;letter-spacing:2px;margin-bottom:3px}
.section-value{font-size:.9em;font-weight:700;direction:ltr;unicode-bidi:embed;color:${sc}}
.sep{border:none;border-top:${sepStyle} ${sepColor};margin:4px 20px;${sepWidth?`border-top-width:${sepWidth}px;`:''}}
.page-ref{font-size:.6em;color:${lc};margin-top:4px}
${effects[fx]||''}`;
}

function buildFront(c){
  const layout=c.frontLayout||'vertical';
  const badge=c.showBadge!==false;
  const unitBadge=c.showUnitBadge!==false;
  if(layout==='horizontal'){
    return `<div style="display:flex;align-items:center;justify-content:center;gap:12px;flex-wrap:wrap">
<div class="french">{{French}}</div>
<div>${badge?'<span class="badge badge-nom" style="display:{{#WordType Nom}}inline-block{{/WordType}}{{^WordType Nom}}none{{/WordType}}">N.</span><span class="badge badge-adj" style="display:{{#WordType Adjectif}}inline-block{{/WordType}}{{^WordType Adjectif}}none{{/WordType}}">Adj.</span><span class="badge badge-verb" style="display:{{#WordType Verbe}}inline-block{{/WordType}}{{^WordType Verbe}}none{{/WordType}}">V.</span>':''}
${unitBadge?'<span class="unit-badge">Unit {{Unit}}</span>':''}</div></div>`;
  }
  return `<div class="french">{{French}}</div>
${badge?'<span class="badge badge-nom" style="display:{{#WordType Nom}}inline-block{{/WordType}}{{^WordType Nom}}none{{/WordType}}">N.</span><span class="badge badge-adj" style="display:{{#WordType Adjectif}}inline-block{{/WordType}}{{^WordType Adjectif}}none{{/WordType}}">Adj.</span><span class="badge badge-verb" style="display:{{#WordType Verbe}}inline-block{{/WordType}}{{^WordType Verbe}}none{{/WordType}}">V.</span>':''}
${unitBadge?'<span class="unit-badge">Unit {{Unit}}</span>':''}`;
}

function buildBack(c){
  const front=buildFront(c);
  const order=(Array.isArray(c.sectionOrder)?c.sectionOrder.join(','):(c.sectionOrder||'Pluriel,Synonyme,Contraire')).split(',');
  const vis=c.sectionVisibility||{};
  const show=c.showMeaning!==false;
  const showPage=c.showPage!==false;
  const infoPos=c.infoPosition||'below';
  const secDefs={
    pluriel:{lbl:'Pluriel',val:'{{Pluriel}}',cond:'Pluriel'},
    masculine:{lbl:'Masc. Sing. / Pl.',val:'{{MasculinS}} / {{MasculinP}}',cond:'MasculinS'},
    feminin:{lbl:'Fem. Sing. / Pl.',val:'{{FemininS}} / {{FemininP}}',cond:'FemininS'},
    preposition:{lbl:'Preposition',val:'{{Preposition}}',cond:'Preposition'},
    auxiliaire:{lbl:'Auxiliaire',val:'{{Auxiliaire}}',cond:'Auxiliaire'},
    participe:{lbl:'Participe',val:'{{Participe}}',cond:'Participe'},
    synonyme:{lbl:'Synonyme',val:'{{Synonyme}}',cond:'Synonyme'},
    contraire:{lbl:'Contraire',val:'{{Contraire}}',cond:'Contraire'}
  };
  let sections='';
  for(const k of order){
    const s=secDefs[k];if(!s||vis[k]===false)continue;
    sections+=`{{#${s.cond}}}<div class="section"><div class="section-label">${s.lbl}</div><div class="section-value">${s.val}</div></div>{{/${s.cond}}}\n`;
  }
  let info=`
<hr class="sep">
${show?`<div class="meaning">{{Arabic}}</div>`:''}
${sections}
${showPage?'<div class="page-ref">Page {{Page}}</div>':''}`;
  if(infoPos==='side'){
    return `<div style="display:flex;width:100%;min-height:200px">
<div style="flex:1;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:16px;border-left:2px solid rgba(0,0,0,.08)">
${front}
<hr class="sep">
${show?`<div class="meaning">{{Arabic}}</div>`:''}
</div>
<div style="flex:1;padding:12px;display:flex;flex-direction:column;gap:4px;overflow-y:auto">
${sections}
${showPage?'<div class="page-ref">Page {{Page}}</div>':''}
</div></div>`;
  }
  return front+info;
}

// ============================================================
// ZIP BUILDER (no dependencies)
// ============================================================
function crc32(buf){
  const t=new Int32Array(256);
  for(let n=0;n<256;n++){let c=n;for(let k=0;k<8;k++)c=(c&1)?(0xEDB88320^(c>>>1)):(c>>>1);t[n]=c;}
  let crc=0xFFFFFFFF;
  for(let i=0;i<buf.length;i++)crc=t[(crc^buf[i])&0xFF]^(crc>>>8);
  return(crc^0xFFFFFFFF)>>>0;
}
function makeZip(files){
  let localBuf=Buffer.alloc(0), centralBuf=Buffer.alloc(0), offset=0;
  for(const{name,data}of files){
    const comp=zlib.deflateRawSync(data);
    const crc=crc32(data);
    const lh=Buffer.alloc(30+name.length);
    lh.writeUInt32LE(0x04034b50,0);
    lh.writeUInt16LE(20,4);lh.writeUInt16LE(8,8);
    lh.writeUInt32LE(crc,14);lh.writeUInt32LE(comp.length,18);lh.writeUInt32LE(data.length,22);
    lh.writeUInt16LE(name.length,26);
    Buffer.from(name,'utf8').copy(lh,30);
    const ch=Buffer.alloc(46+name.length);
    ch.writeUInt32LE(0x02014b50,0);
    ch.writeUInt16LE(20,4);ch.writeUInt16LE(20,6);ch.writeUInt16LE(8,10);
    ch.writeUInt32LE(crc,16);ch.writeUInt32LE(comp.length,20);ch.writeUInt32LE(data.length,24);
    ch.writeUInt16LE(name.length,28);ch.writeUInt32LE(offset,42);
    Buffer.from(name,'utf8').copy(ch,46);
    localBuf=Buffer.concat([localBuf,lh,comp]);
    centralBuf=Buffer.concat([centralBuf,ch]);
    offset+=lh.length+comp.length;
  }
  const eocd=Buffer.alloc(22);
  eocd.writeUInt32LE(0x06054b50,0);
  eocd.writeUInt16LE(files.length,8);eocd.writeUInt16LE(files.length,10);
  eocd.writeUInt32LE(centralBuf.length,12);eocd.writeUInt32LE(offset,16);
  return Buffer.concat([localBuf,centralBuf,eocd]);
}

// ============================================================
// GENERATE APK
// ============================================================
let _SQL=null;
async function generateApkg(config){
  if(!_SQL)_SQL=await initSqlJs();
  const db=new _SQL.Database();
  try{
    db.run(`CREATE TABLE col (id integer primary key,crt integer not null,mod integer not null,scm integer not null,ver integer not null,dty integer not null,usn integer not null,ls integer not null,conf text not null,models text not null,decks text not null,dconf text not null,tags text not null)`);
    db.run(`CREATE TABLE notes (id integer primary key,guid text not null,mid integer not null,mod integer not null,usn integer not null,tags text not null,flds text not null,sfld text not null,csum integer not null,flags integer not null,data text not null)`);
    db.run(`CREATE TABLE cards (id integer primary key,nid integer not null,did integer not null,ord integer not null,mod integer not null,usn integer not null,type integer not null,queue integer not null,due integer not null,ivl integer not null,factor integer not null,reps integer not null,lapses integer not null,left integer not null,odue integer not null,odid integer not null,flags integer not null,data text not null)`);
    db.run(`CREATE TABLE graves (usn integer not null,oid integer not null,type integer not null)`);
    db.run(`CREATE TABLE revlog (id integer primary key,cid integer not null,usn integer not null,ease integer not null,ivl integer not null,lastIvl integer not null,factor integer not null,time integer not null,type integer not null)`);

    const now=Math.floor(Date.now()/1000);
    const deckName=config.deckName||'📘 Français Bac 2021-2022';
    const split=config.splitDirection||'unified';
    const modelId=stableId('FrancaisBac2021');
    const fields=["French","Arabic","WordType","TypeBadge","Unit","Page","Pluriel","FemininS","FemininP","Preposition","Auxiliaire","Participe","Synonyme","Contraire","IsStarred","Family","FamilyName","FirstLetter","CharCount","MasculinS","MasculinP","Difficulty","SessionCount"].map(n=>({name:n,font:'',size:20,media:[],sticky:false,rightToLeft:false}));
    const css=buildCSS(config);
    const front=buildFront(config);
    const back=buildBack(config);
    const model={css,name:'FrancaisBac2021',sortf:0,tags:[],
      tmpls:[{name:'FR→AR',qfmt:front,afmt:back,did:null,bafmt:'',bfont:'',bsize:0,bformat:0},
             {name:'AR→FR',qfmt:front.replace(/\{\{French\}\}/g,'{{Arabic}}'),afmt:back,did:null,bafmt:'',bfont:'',bsize:0,bformat:0}],
      fields,req:[[0,'any',[0]],[1,'any',[1]]],type:0,ver:1,
      vers:[{minor:1,busy:0}],
      latexPre:'\\\\documentclass[12pt]{article}\\\\usepackage{polyglossia}\\\\usepackage{amsmath}\\\\pagestyle{empty}\\\\begin{document}',
      latexPost:'\\\\end{document}',latexsvg:false};
    const decks={};
    const deckConf={"id":1,"mod":0,"name":"Default","browserCollapsed":false,"new":{"bury":true,"delays":[1,10],"initialFactor":2500,"ints":[1,4,0],"order":1,"perDay":20,"separate":true},"lapse":{"delays":[10],"ease1":0,"goodInterval":1,"ivlFct":1,"minInt":1,"mult":0,"resetsTo":0,"leechAction":0},"rev":{"bury":true,"ease4":1.3,"ivlFct":1,"maxIvl":36500,"perDay":200,"softLimit":0,"hardFactor":1.2,"fuzz":0.05},"revlog":{"useFuzz":true},"timer":0,"dyn":0,"maxTake":0};
    function createDeck(name){const id=stableId(name);decks[id]={collapsed:false,conf:1,desc:'',dyn:0,extendNew:0,extendRev:0,id,lrnToday:[0,0],name,newToday:[0,0],revToday:[0,0],timeToday:[0,0],usn:0};return id;}
    const deckIds={};
    if(split==='separate'){for(let d=1;d<=6;d++){deckIds[`fr${d}`]=createDeck(`${deckName}::Unit ${d}::🇫🇷 FR→AR`);deckIds[`ar${d}`]=createDeck(`${deckName}::Unit ${d}::🇸🇾 AR→FR`);}}
    else{for(let d=1;d<=6;d++)deckIds[`u${d}`]=createDeck(`${deckName}::Unit ${d}`);}
    deckIds['imp']=createDeck(`${deckName}::⭐ الكلمات المهمة`);
    let nc=1,cc=1,dc=0;
    function addWord(w,dk,s){
      const fl=w.word?w.word[0]:'?';
      const flds=[w.word,w.arabe||'',w.type||'',w.type_fr||'',String(w.unit||1),w.page||'',w.pluriel||'',w.feminin_s||'',w.feminin_p||'',w.preposition||'',w.auxiliaire||'',w.participe||'',w.synonyme||'',w.contraire||'',s?'1':'','','',fl,String((w.word||'').replace(/ /g,'').length),w.masculin_s||'',w.masculin_p||'','','0'].join('\x1f');
      const nid=(nc++)*(1<<20);
      db.run('INSERT INTO notes (id,guid,mid,mod,usn,tags,flds,sfld,csum,flags,data) VALUES (?,?,?,?,?,?,?,?,?,?,?)',
        [nid,crypto.randomBytes(12).toString('hex'),modelId,now,-1,`${w.type||''} Unit${w.unit||1} ${w.page?'Page'+w.page:''}${s?' Starred':''}`,flds,w.word||'',0,0,'']);
      for(let o=0;o<2;o++)db.run('INSERT INTO cards (id,nid,did,ord,mod,usn,type,queue,due,ivl,factor,reps,lapses,left,odue,odid,flags,data) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)',
        [(cc++)*(1<<20),nid,deckIds[dk],o,now,-1,0,0,(dc++),0,0,0,0,0,0,0,0,'']);
    }
    for(const w of getAllWords()){if(split==='separate'){addWord(w,`fr${w.unit}`,false);addWord(w,`ar${w.unit}`,false);}else addWord(w,`u${w.unit}`,false);}
    for(const w of getImportantWords())addWord(w,'imp',true);
    db.run('INSERT INTO col VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)',[1,now,now,now,11,0,-1,0,
      JSON.stringify({"activeDecks":[],"curDeck":0,"newSpread":0,"collapseTime":1200,"timeLim":0,"estTimes":true,"dueCounts":true,"dayLearnFirst":false,"schedVer":2}),
      JSON.stringify({[modelId]:model}),JSON.stringify(decks),JSON.stringify({"1":deckConf}),'{}']);
    const result=Buffer.from(db.export());
    return result;
  }finally{
    try{db.close();}catch(e){}
  }
}

// ============================================================
// API
// ============================================================
app.post('/api/generate',async(req,res)=>{
  try{
    const config=req.body;
    if(!config||typeof config!=='object')throw new Error('Invalid config');
    console.log('Generating:',config.deckName);
    const dbBuf=await generateApkg(config);
    if(!dbBuf||dbBuf.length===0)throw new Error('Empty database');
    const zip=makeZip([
      {name:'collection.anki21',data:dbBuf},
      {name:'media',data:Buffer.from('{}')}
    ]);
    const safeName=(config.deckName||'deck').replace(/[^a-zA-Z0-9\u0600-\u06FF]/g,'_');
    res.set({'Content-Type':'application/octet-stream','Content-Disposition':`attachment; filename="${safeName}.apkg"`,'Content-Length':zip.length});
    res.send(zip);
    console.log('✅ Sent:',zip.length,'bytes');
  }catch(e){
    console.error('🔴 Error:',e.message);
    if(!res.headersSent)res.status(500).json({error:e.message});
  }
});

app.get('/api/health',(req,res)=>res.json({status:'ok',words:getAllWords().length}));
app.get('*',(_,res)=>res.sendFile(path.join(__dirname,'public','index.html')));
app.listen(PORT,'0.0.0.0',()=>console.log(`\n🎨 Anki Design Studio\n   👉 http://localhost:${PORT}\n   📝 ${getAllWords().length} words\n`));
