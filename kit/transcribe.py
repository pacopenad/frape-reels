"""Voz -> words.json con tiempos por palabra. Uso: python3 transcribe.py voz.wav words.json"""
import sys, json, subprocess, re, numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1:3]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', src, '-ac', '1', '-ar', '16000', '-f', 'f32le', '-'], capture_output=True).stdout
audio = np.frombuffer(raw, np.float32).copy()
m = WhisperModel('small', device='cpu', compute_type='int8')
segs, _ = m.transcribe(audio, language='es', word_timestamps=True, initial_prompt='FRAPÉ, SAT, deducible, RFC, e.firma, RESICO, CFDI.')
ws = [dict(w=w.word.strip(), s=round(w.start, 2), e=round(w.end, 2)) for s in segs for w in s.words]
# unir cifras partidas: "30" ".000" -> "$30,000"
outw = []
for w in ws:
    if outw and re.fullmatch(r'[.,]\d{3}[.,?]?', w['w']) and re.fullmatch(r'\$?\d+', outw[-1]['w']):
        p = outw[-1]; p['w'] = '$' + p['w'].lstrip('$') + ',' + w['w'][1:]; p['e'] = w['e']; continue
    outw.append(w)
FIX = {'si,': 'Sí,', 'cuanto': 'cuánto', 'Escrívenos': 'Escríbenos', 'Frappé': 'FRAPÉ', 'Frapé': 'FRAPÉ', 'efirma': 'e.firma'}
for w in outw:
    if w['w'] in FIX: w['w'] = FIX[w['w']]
json.dump(outw, open(out, 'w'), ensure_ascii=False, indent=0)
print(len(outw), 'palabras; fin', outw[-1]['e'])
print(' '.join(f"{w['w']}@{w['s']}" for w in outw))
