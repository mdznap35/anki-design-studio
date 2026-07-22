const express = require('express');
const path = require('path');
const fs = require('fs');
const { execSync } = require('child_process');
const os = require('os');

process.on('uncaughtException', e => console.error('CRASH:', e.message));
process.on('unhandledRejection', e => console.error('REJECT:', e));

const app = express();
const PORT = process.env.PORT || 3000;
app.use(express.json({ limit: '10mb' }));
app.use(express.static(path.join(__dirname, 'public')));

let VOCAB_DATA = null, REPEATED_DATA = null;
try { VOCAB_DATA = JSON.parse(fs.readFileSync(path.join(__dirname, 'parsed_data_full.json'), 'utf8')); } catch(e) {}
try { REPEATED_DATA = JSON.parse(fs.readFileSync(path.join(__dirname, 'repeated_data.json'), 'utf8')); } catch(e) {}

function getAllWords(){
  if(!VOCAB_DATA) return [];
  const w = [];
  for(const uk of Object.keys(VOCAB_DATA)){
    const un = parseInt(uk.split('_')[1]);
    for(const x of (VOCAB_DATA[uk].noms||[]))
      w.push({word:x.singulier,arabe:x.arabe,type:'Nom',type_fr:'N.',unit:un,page:x.page||'',pluriel:x.pluriel||'',feminin_s:'',feminin_p:'',preposition:'',auxiliaire:'',participe:'',synonyme:x.synonyme||'',contraire:x.contraire||''});
    for(const x of (VOCAB_DATA[uk].adj||[]))
      w.push({word:x.masculin_s,arabe:x.arabe,type:'Adjectif',type_fr:'Adj.',unit:un,page:x.page||'',pluriel:'',feminin_s:x.feminin_s||'',feminin_p:x.feminin_p||'',preposition:'',auxiliaire:'',participe:'',synonyme:x.synonyme||'',contraire:x.contraire||''});
    for(const x of (VOCAB_DATA[uk].verbs||[]))
      w.push({word:x.verbe,arabe:x.arabe,type:'Verbe',type_fr:'V.',unit:un,page:x.page||'',pluriel:'',feminin_s:'',feminin_p:'',preposition:x.preposition||'',auxiliaire:x.auxiliaire||'',participe:x.participe||'',synonyme:x.synonyme||'',contraire:''});
  }
  return w;
}

function getImportantWords(){
  if(!REPEATED_DATA) return [];
  const r = [];
  for(const cat of ['noms','adj','verbs'])
    for(const x of (REPEATED_DATA[cat]||[]).slice(0,30))
      r.push({word:x.word,arabe:x.arabe,type:x.type||'',type_fr:(x.type||'').substring(0,2)+'.',unit:(x.units&&x.units[0])||1,page:'',pluriel:'',feminin_s:'',feminin_p:'',preposition:'',auxiliaire:'',participe:'',synonyme:'',contraire:''});
  return r;
}

app.post('/api/generate', async(req, res) => {
  try {
    const config = req.body;
    if (!config || typeof config !== 'object') throw new Error('Invalid config');
    console.log('Generating:', config.deckName);

    const payload = {
      config: config,
      words: getAllWords(),
      important: getImportantWords()
    };

    const tmpJson = path.join(os.tmpdir(), `anki_${Date.now()}.json`);
    const tmpApkg = path.join(os.tmpdir(), `anki_${Date.now()}.apkg`);
    
    fs.writeFileSync(tmpJson, JSON.stringify(payload));
    
    try {
      execSync(`python3 ${path.join(__dirname, 'generate_apkg.py')} "${tmpJson}" "${tmpApkg}"`, { timeout: 120000 });
    } catch(e) {
      throw new Error('Python generation failed: ' + (e.stderr ? e.stderr.toString() : e.message));
    }

    if (!fs.existsSync(tmpApkg)) throw new Error('APKG file not created');
    const apkgBuf = fs.readFileSync(tmpApkg);
    if (apkgBuf.length < 1000) throw new Error('APKG too small: ' + apkgBuf.length);

    try { fs.unlinkSync(tmpJson); } catch(e) {}
    try { fs.unlinkSync(tmpApkg); } catch(e) {}

    const safeName = (config.deckName || 'deck').replace(/[^a-zA-Z0-9\u0600-\u06FF]/g, '_');
    res.set({
      'Content-Type': 'application/octet-stream',
      'Content-Disposition': `attachment; filename="${safeName}.apkg"`,
      'Content-Length': apkgBuf.length
    });
    res.send(apkgBuf);
    console.log('✅ Sent:', apkgBuf.length, 'bytes');
  } catch(e) {
    console.error('🔴 Error:', e.message);
    if (!res.headersSent) res.status(500).json({ error: e.message });
  }
});

app.get('/api/health', (req, res) => res.json({ status: 'ok', words: getAllWords().length }));
app.get('*', (_, res) => res.sendFile(path.join(__dirname, 'public', 'index.html')));
app.listen(PORT, '0.0.0.0', () => console.log(`\n🎨 Anki Design Studio\n   👉 http://localhost:${PORT}\n   📝 ${getAllWords().length} words\n`));
