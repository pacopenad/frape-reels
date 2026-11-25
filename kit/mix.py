import sys, json, subprocess, wave, numpy as np
SR = 44100
import os; S = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx') + '/'
voice_f, timing_f, out = sys.argv[1:4]
T = json.load(open(timing_f))
def ld(f): return np.frombuffer(subprocess.run(['ffmpeg','-v','error','-i',f,'-ac','1','-ar',str(SR),'-f','f32le','-'],capture_output=True).stdout, np.float32).copy()
def nz(x, v): return x / (np.abs(x).max() + 1e-6) * v
voice = nz(ld(voice_f), 0.7)
n = int(SR * (T['total'] + 0.5)); mix = np.zeros(n, np.float32); mix[:len(voice)] += voice
def place(s, t):
    a = int(max(0, t) * SR); b = min(n, a + len(s)); mix[a:b] += s[:b - a]
wh = nz(ld(S + 'whoosh.mp3'), 0.06); ding = nz(ld(S + 'ding.mp3'), 0.07); err = nz(ld(S + 'error.mp3'), 0.06); cha = nz(ld(S + 'chaching.mp3'), 0.09)
for st in T['starts'][1:]: place(wh, st - 0.12)
place(wh * 1.3, 0.0)
for t in T['ok']: place(ding, t + 0.32)
for t in T['no']: place(err, t + 0.3)
for t in T['money']: place(cha, t + 0.2)
def save(fn, m):
    m = np.clip(m, -1, 1)
    with wave.open(fn, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((m * 32767).astype(np.int16).tobytes())
save(out + '_sin.wav', mix.copy())
mus0 = nz(ld(S + 'musica.mp3'), 1.0)
xf = int(SR * 2.0); mus = mus0.copy()
while len(mus) < n:
    r = np.linspace(0, 1, xf, dtype=np.float32)
    mus = np.concatenate([mus[:-xf], mus[-xf:] * (1 - r) + mus0[:xf] * r, mus0[xf:]])
mus = mus[:n]
fo = int(SR * 1.2); mus[-fo:] *= np.linspace(1, 0, fo, dtype=np.float32)
vv = np.pad(np.abs(voice), (0, max(0, n - len(voice))))[:n]; hop = int(0.05*SR); env = np.zeros(n, np.float32)
for k in range(0, n, hop): env[k:k+hop] = vv[k:k+hop].mean()
act = np.clip(np.convolve((env > 0.02).astype(np.float32), np.ones(int(0.3*SR), np.float32)/int(0.3*SR), mode='same') * 1.5, 0, 1)
g = 0.2 - 0.11 * act; e = int(T['total'] * SR); fo = int(1.5*SR); g[e-fo:e] *= np.linspace(1, 0.3, fo); g[e:] *= 0.3
save(out + '.wav', mix + mus * g)
print('mix ok')
