#!/bin/bash
# Construye un reel FRAPS completo.
# Uso: bash build.sh <carpeta_reel>   (la carpeta trae voz_raw.wav y spec.py; deja final_4k.mp4, final_hd.mp4, final_ig.mp4 (<10MB), final_sin_musica.mp4)
set -e
K="$(cd "$(dirname "$0")" && pwd)"; R="$(cd "$1" && pwd)"; HF="npx -y hyperframes@0.9.92"
export HYPERFRAMES_TELEMETRY=0 DO_NOT_TRACK=1
cd "$R"
# 1) voz: recorta silencios largos y normaliza (la voz de ElevenLabs sale muy baja)
[ -f voz.wav ] || { ffmpeg -y -v error -i voz_raw.* -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 48000 voz_n.wav
  python3 "$K/pausas.py" voz_n.wav voz.wav 0.45; }
AUD=$(ffprobe -v error -show_entries format=duration -of csv=p=0 voz.wav)
[ -f words.json ] || python3 "$K/transcribe.py" voz.wav words.json
[ -f spec.py ] || { echo "Falta spec.py: escríbelo con los anclajes de words.json"; exit 2; }
# 2) proyecto HyperFrames
[ "$SKIP_RENDER" = 1 ] || { rm -rf proj; SPEC=spec.py WORDS=words.json AUD=$AUD OUT=proj MODE=${MODE:-hibrido} python3 "$K/gen_reel.py"
python3 "$K/mix.py" voz.wav proj/timing.json mix
# 3) render: borrador rápido para revisar, o 4K final
cd proj
if [ "$DRAFT" = 1 ]; then $HF render --quality looks -o ../render.mp4; else $HF render --quality delivery --resolution portrait-4k -o ../render.mp4; fi
cd ..; }
ffmpeg -y -v error -i render.mp4 -i mix.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart final_4k.mp4
ffmpeg -y -v error -i render.mp4 -i mix_sin.wav -map 0:v -map 1:a -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart final_sin_musica.mp4
# 4) versión para subir (Drive/Metricool aceptan máx. 10 MB desde aquí): 1080x1920, 2 pasadas
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 final_4k.mp4); VB=$(python3 -c "print(int(9.3*8*1024*1024/$D/1000-128))")
ffmpeg -y -v error -i final_4k.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -preset slow -tune animation -b:v ${VB}k -pass 1 -passlogfile /tmp/p2 -an -f mp4 /dev/null
ffmpeg -y -v error -i final_4k.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -preset slow -tune animation -b:v ${VB}k -pass 2 -passlogfile /tmp/p2 -c:a aac -b:a 128k -movflags +faststart final_ig.mp4
# 5) versión HD para Metricool (repo público frape-reels; GitHub acepta <100 MB)
ffmpeg -y -v error -i final_4k.mp4 -vf scale=1080:1920:flags=lanczos -c:v libx264 -preset slow -tune animation -crf 17 -maxrate 12M -bufsize 24M -c:a aac -b:a 192k -movflags +faststart final_hd.mp4
ls -la final_*.mp4
