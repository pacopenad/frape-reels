# Kit de reels FRAPS (motor + biblioteca)

Todo lo necesario para producir un reel FRAPS con la plantilla aprobada (híbrido, 4K) en un contenedor limpio.

## Archivos
- `gen_reel.py`: motor. Lee `spec.py` (escenas, frases clave, etiquetas ✓/✗, escena de cálculo, cierre) y arma el proyecto HyperFrames.
- `spec_deducible.py`: ejemplo completo y aprobado ("¿Es deducible o no?"). Copiarlo como base de cada reel nuevo.
- `build.sh <carpeta>`: voz → normaliza y recorta pausas → transcribe (whisper) → proyecto → mezcla (sfx + música con ducking) → render 4K → `final_4k.mp4`, `final_hd.mp4` (1080p para Metricool, <90 MB), `final_ig.mp4` (<10 MB, para revisar) y `final_sin_musica.mp4`. Con `DRAFT=1` renderiza rápido (borrador).
- `transcribe.py`, `mix.py`, `pausas.py`: piezas de build.sh.
- `portada.py portada.json salida`: portada 1080x1920 y recorte feed 3:4.
- `clips/`: biblioteca (5 s, 9:16). Índice en `clips.md`.
- `sfx/`: whoosh, ding, error, cha-ching, música.
- `assets/`: gsap, logos.

## Preparar el contenedor
```
pip install --break-system-packages faster-whisper   # si falta
# HyperFrames corre con: npx -y hyperframes@0.9.92 (build.sh ya lo usa). Inter ya viene instalada.
```

## Reglas de la plantilla (aprobada por Paco, 25 nov 2026)
- Solo FRAPS animado. Nunca personas generadas por IA.
- Voz "Paquito" (voice_id nlUr5kFJ0NmrKIVUvHZB), modelo eleven_v4 con etiquetas de tono: [curious]/[asking] en preguntas, [confident] en respuestas, [conspiratorial] para "el secreto", [playful]/[laughs softly] en remates, [warm]/[friendly] al cerrar. Preguntas separadas ("¿El dentista? ¿El doctor?") para que suban. Nunca [excited] en el cierre. En el guion escribir "Frapé"; en pantalla "FRAPÉ".
- Gancho = una sola pregunta, sin coma en medio ("[curious] ¿El SAT te debe dinero y no lo sabes?").
- Estructura: gancho → situación cotidiana → "lo que nadie te dice" → preguntas/respuestas rápidas → "el secreto" → ejemplo con cifras (escena calc) → cierre.
- Cierre fijo: "¿Quieres saber [cuánto te toca / si te aplica]? Escríbenos." + frase final que regresa al gancho ("porque a lo mejor..."), para que el loop enganche.
- Texto grande arriba solo en 4 momentos clave (`key`): gancho, giro ("PERO OJO"), secreto, remate. Subtítulos abajo el resto del tiempo; nunca los dos a la vez (el motor los quita solo).
- "Comenta PALABRA" va en el pie del post, no en el video.
- 30–55 s. Una escena cada 2–5 s.
- Cifras fiscales: ejemplo ilustrativo y prudente, con nota "*Ejemplo ilustrativo." Marcar en el correo de revisión qué cifras debe validar Jorge o José Ángel.

## Cómo escribir spec.py
Anclas con `at(palabra, n=1, atras=0)`: inicio de la n-ésima vez que aparece `palabra` (minúsculas, sin signos; cifras como `'$30000'`), retrocediendo `atras` palabras. Si falta un ancla el motor se detiene con "anchor missing".
- `S`: lista de escenas `(inicio, 'v', 'clip', seg_inicio_clip, entrada)` o `(inicio, 'g', 'calc'|'cta', 0, 'zoom')`. Entradas: punch, whip, blur, zoom. La primera escena en 0.0 con 'punch'.
- `key`: `(inicio, fin, [(texto, t_aparece, color, tamaño), ...], 'top')`.
- `labels` (opcional, para series de ✓/✗): `(inicio, 'TEXTO', 'ok'|'no', t_palomita)`, más `LABELS_END` y `CHIPS=(inicio, fin)` (o `CHIPS=None`).
- `CALC` (opcional): dict con tag, a_top, a_value, a_at, a_bottom, b_top, b_value, b_at, foot. Si no hay escena 'calc' no hace falta.
- `CTA`: l1, l2, pill, tail y tiempos t1, t2, t3.
- `LOGO_HIDE` (= inicio del cierre − 0.15), `CAPS_END` (= inicio de calc o cierre − 0.15), `MONEY` (tiempos de cha-ching; puede ser []).

## Clips nuevos (cuando la biblioteca no alcanza; máx. 2 por reel)
Flow ElevenLabs `lbqT73wECftjJAzdlv3S`. Hoja de personaje FRAPS: nodo `qKW4YrLyv2jj9E9LRfLH`.
1. `creative_edit_image` (connect_from el nodo de la hoja, prompt de la escena, "ONLY ONE FRAPS", estilo caricatura igual a la hoja, `estimate_only:true`) → `creative_update_node` con aspect_ratio 9:16 (modelo gemini-3.1-flash-image, ~609 créditos).
2. `creative_generate_video` desde esa imagen con kling-2.5-turbo, 5 s, 9:16, sin audio (`estimate_only:true` → update_node → run). ~2,121 créditos.
3. `creative_run_flow_nodes` y luego `creative_get_flow_run_status` para el content_url; descargar a `clips/<nombre>.mp4` y afilar: `ffmpeg -i in.mp4 -vf unsharp=5:5:0.7:5:5:0 -c:v libx264 -crf 14 -an out.mp4`. Agregarlo a `clips.md` y volver a publicar el kit.
Tope: ~10,000 créditos por reel (voz ~1,000 + 2 clips nuevos ~5,500).
