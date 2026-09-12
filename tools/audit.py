import re, sys
FORBID = {
 'en9':   ['French Bac','بكلوريا','Literature','Science','French 9','فرنسي 9','Henri','Dossier'],
 'enlit': ['French Bac','بكلوريا','French 9','فرنسي 9','Henri','Dossier','Science 12'],
 'ensci': ['French Bac','بكلوريا','French 9','فرنسي 9','Henri','Dossier','Literature 12'],
 'fr9':   ['English 9','English Literature','English Science','French Bac','بكلوريا','GuyNeural','Unit 01'],
}
FILES = {'en9':'en9','enlit':'enlit','ensci':'ensci','fr9':'fr9'}
ok=True
for did, terms in FORBID.items():
    h=open('/workspace/out/%s.html'%FILES[did],encoding='utf-8').read()
    # remove scripts and header links for content check
    h_text = re.sub(r'<script.*?</script>', '', h, flags=re.DOTALL)
    h2=re.sub(r'<a class="hdr-link" href="/[a-z0-9]+">.*?</a>','',h_text)
    hits={}
    for t in terms:
        c=h2.count(t)
        if c: hits[t]=c
    fw=len(re.findall(r'(?<![A-Za-z])French(?![A-Za-z])',h2))
    fr2=h2.count('Français')
    bad = dict(hits)
    if did!='fr9' and fr2: bad['Français']=fr2
    if did!='fr9' and fw: bad['French-word']=fw
    st='CLEAN' if not bad else 'DIRTY'
    if bad: ok=False
    print(did,st,bad if bad else '-')
sys.exit(0 if ok else 1)
