h=open('/workspace/index.html',encoding='utf-8').read()
keys=['SAMP.f,"fr"','gallery_imgs/',"Français 12",'Anki Design Studio','anki_ed_','wordSource','tts_voices','audio_status','ttsFrVoice','quickFrVoice']
for k in keys:
    print(k,'>>',h.count(k))
