# Reel: ¿e.firma o FIEL? (serie Lo básico) · validado por FPM 26 nov 2026
S = [
    (0.0, 'v', 'no_se', 0.0, 'punch'),
    (at('spoiler') - .1, 'v', 'confiado', 0.0, 'whip'),
    (at('antes') - .1, 'v', 'efirma_usb', 0.0, 'blur'),
    (at('hoy') - .1, 'v', 'portal', 0.0, 'whip'),
    (at('pero') - .1, 'v', 'ojo', 0.0, 'zoom'),
    (at('es', 2) - .1, 'v', 'firmando', 0.0, 'whip'),
    (at('y') - .1, 'v', 'pensando', 0.0, 'blur'),
    (at('para', 2) - .1, 'v', 'factura', 0.0, 'whip'),
    (at('pedir') - .1, 'v', 'sobre_dinero', 0.0, 'whip'),
    (at('y', 3) - .1, 'v', 'credencial', 0.0, 'whip'),
    (at('el', 3) - .1, 'v', 'fecha_limite', 0.0, 'blur'),
    (at('si') - .1, 'v', 'prisa', 0.0, 'whip'),
    (at('revisa') - .1, 'v', 'lupa', 0.0, 'whip'),
    (at('no', 2) - .1, 'g', 'cta', 0, 'zoom'),
]
key = [
    (0.0, at('spoiler') - .15, [('¿E.FIRMA', 0.05, '#fff', 130), ('O FIEL?', at('fiel'), YEL, 150)], 'top'),
    (at('pero'), at('es', 2) - .1, [('PERO OJO:', at('pero'), YEL, 120), ('ES TU FIRMA', at('es', 2) - .4, '#fff', 104)], 'top'),
    (at('el', 3), at('si') - .15, [('EL SECRETO', at('el', 3), YEL, 100), ('DURA', at('dura'), '#fff', 110), ('4 AÑOS', at('cuatro'), YEL, 160)], 'top'),
    (at('revisa'), at('no', 2) - .15, [('REVISA HOY', at('revisa'), '#fff', 120), ('CUÁNDO VENCE', at('cuándo'), YEL, 110)], 'top'),
]
CTA = dict(l1='¿NO SABES SI', l2='SIGUE VIGENTE?', pill='ESCRÍBENOS', tail='porque a lo mejor la tuya ya venció...',
           t1=at('sigue'), t2=at('escríbenos'), t3=at('porque'))
LOGO_HIDE = at('no', 2) - .15
CAPS_END = at('no', 2) - 0.15
MONEY = []
