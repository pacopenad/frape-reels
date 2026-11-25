# Reel: ¿Es deducible o no? (plantilla aprobada 25 nov 2026)
# Escenas: (inicio, 'v'|'g', clip|'calc'|'cta', segundo de inicio del clip, entrada punch|whip|blur|zoom)
S = [
    (0.0, 'v', 'hook', 0.0, 'punch'),
    (at('este') - .1, 'v', 'd_c1', 0.0, 'whip'),
    (at('compraste', 1, 1) - .1, 'v', 'd_c2', 0.0, 'whip'),
    (at('pagaste', 1, 1) - .1, 'v', 'd_c3', 0.0, 'whip'),
    (at('nadie', 1, 2) - .1, 'v', 'd_c4', 0.0, 'blur'),
    (at('pero') - .1, 'v', 'ojo', 0.0, 'zoom'),
    (at('dentista', 2, 1) - .1, 'v', 'd_c1', 0.3, 'whip'),
    (at('pero', 2) - .1, 'v', 'd_c5', 0.0, 'whip'),
    (at('efectivo', 1, 3) - .1, 'v', 'd_c6', 0.0, 'blur'),
    (at('lentes', 2, 1) - .1, 'v', 'd_c2', 0.6, 'whip'),
    (at('colegiaturas', 1, 1) - .1, 'v', 'd_c3', 0.0, 'whip'),
    (at('gym', 1, 2) - .1, 'v', 'd_c7', 0.5, 'zoom'),
    (at('netflix', 1, 1) - .1, 'v', 'tele', 0.0, 'whip'),
    (at('secreto', 1, 1) - .1, 'v', 'factura', 0.0, 'blur'),
    (at('porque') - .1, 'v', 'declaracion', 0.0, 'whip'),
    (at('dinero', 3, 1) - .1, 'v', 'd_c4', 2.6, 'blur'),
    (at('por', 2) - .1, 'g', 'calc', 0, 'zoom'),
    (at('quieres') - .1, 'g', 'cta', 0, 'zoom'),
]

labels = [  # (scene start, text, kind, stamp time)
    (at('dentista', 2, 1), 'GASTOS MÉDICOS', 'ok', at('sí')),
    (at('pero', 2), 'TARJETA O TRANSFERENCIA', 'ok', at('transferencia')),
    (at('efectivo', 1, 3), 'EFECTIVO', 'no', at('no', 4)),
    (at('lentes', 2), 'LENTES GRADUADOS', 'ok', at('también')),
    (at('colegiaturas', 1, 1), 'COLEGIATURAS · CON TOPE', 'ok', at('sí', 2)),
    (at('gym', 1, 2), 'GYM', 'no', at('no', 5)),
    (at('netflix', 1, 1), 'NETFLIX', 'no', at('tampoco')),
]

LABELS_END = at('secreto', 1, 1)
CHIPS = (at('dentista', 2, 1), at('secreto', 1, 1))
key = [
    (0.0, at('este') - .15, [('¿EL SAT TE DEBE', 0.05, '#fff', 100), ('DINERO', at('dinero'), YEL, 160), ('Y NO LO SABES?', at('sabes'), '#fff', 100)], 'top'),
    (at('pero'), at('es', 2) - .1, [('PERO OJO:', at('pero'), YEL, 120), ('NO TODO CUENTA', at('todo'), '#fff', 104)], 'top'),
    (at('secreto', 1, 1), at('porque') - .15, [('EL SECRETO', at('secreto', 1, 1), YEL, 96), ('PIDE FACTURA', at('pide'), '#fff', 110),
                                               ('A TU NOMBRE', at('nombre'), '#fff', 110), ('DE TODO', at('todo', 2), YEL, 96)], 'top'),
    (at('dinero', 3, 1), at('por', 2) - .15, [('ESE DINERO PUEDE', at('dinero', 3, 1), '#fff', 84), ('VOLVER', at('volver'), YEL, 150),
                                              ('A TU CUENTA', at('cuenta', 3), '#fff', 100)], 'top'),
]
extra = [
    (at('este'), at('nadie', 1, 2) - .15, [('AL DENTISTA', at('dentista'), '#fff', 96), ('LENTES NUEVOS', at('lentes'), '#fff', 96), ('COLEGIATURA', at('colegiatura'), YEL, 96)], 'low'),
    (at('nadie', 1, 2), at('pero') - .15, [('LO QUE NADIE', at('nadie', 1, 2), '#fff', 110), ('TE DICE...', at('dice'), YEL, 110),
                                          ('EL SAT TE LO PUEDE', at('sat', 2), '#fff', 76), ('REGRESAR', at('regresar'), YEL, 130)], 'mid'),
    (at('es', 2) - .05, at('dentista', 2, 1) - .15, [('¿ES DEDUCIBLE', at('es', 2), '#fff', 120), ('O NO?', at('no', 3), YEL, 150)], 'top'),
    (at('dentista', 2, 1), at('pero', 2) - .15, [('¿DOCTOR? ¿HOSPITAL?', at('dentista', 2, 1), '#fff', 84), ('SÍ', at('sí'), G, 170)], 'low'),
    (at('pero', 2), at('efectivo', 1, 3) - .15, [('CON TARJETA', at('tarjeta'), '#fff', 110), ('O TRANSFERENCIA', at('transferencia'), YEL, 100)], 'low'),
    (at('efectivo', 1, 3), at('lentes', 2, 1) - .15, [('EN EFECTIVO', at('efectivo'), '#fff', 110), ('NO CUENTA', at('no', 4), RD, 130)], 'low'),
    (at('lentes', 2, 1), at('colegiaturas', 1, 1) - .15, [('¿LENTES?', at('lentes', 2), '#fff', 120), ('SOLO GRADUADOS', at('graduados'), G, 100)], 'low'),
    (at('colegiaturas', 1, 1), at('gym', 1, 2) - .15, [('¿COLEGIATURAS?', at('colegiaturas'), '#fff', 104), ('SÍ, CON TOPE', at('sí', 2), G, 110)], 'low'),
    (at('gym', 1, 2), at('netflix', 1, 1) - .15, [('¿GYM?', at('gym'), '#fff', 130), ('NO', at('no', 5), RD, 170)], 'low'),
    (at('netflix', 1, 1), at('secreto', 1, 1) - .15, [('¿NETFLIX?', at('netflix'), '#fff', 130), ('TAMPOCO', at('tampoco'), RD, 150)], 'low'),
    (at('porque'), at('dinero', 3, 1) - .15, [('EN ABRIL', at('abril'), YEL, 120), ('DECLARACIÓN ANUAL', at('declaración'), '#fff', 82)], 'top'),
]

CALC = dict(tag='EJEMPLO', a_top='SI GASTASTE', a_value=30000, a_at=at('$30000'), a_bottom='EN DOCTOR Y DENTISTA',
            b_top='TE PODRÍAN REGRESAR', b_value=9000, b_at=at('$9000'), foot='*Ejemplo ilustrativo. Depende de tu ingreso.')
CTA = dict(l1='¿QUIERES SABER', l2='CUÁNTO TE TOCA?', pill='ESCRÍBENOS', tail='porque a lo mejor...',
           t1=at('cuánto'), t2=at('escríbenos'), t3=at('porque', 2))
LOGO_HIDE = at('quieres') - .15
CAPS_END = at('por', 2) - 0.15
MONEY = [at('regresar'), at('volver'), at('$9000')]
