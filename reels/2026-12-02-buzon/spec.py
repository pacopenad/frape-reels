# Reel: Buzón tributario: actívalo antes del 31 de diciembre (Lo básico · tema hot)
# Fuente: SAT minisitio Buzón Tributario (transitorio Cuarto RMF 2026; CFF 86-C y 86-D). Validar con FPM.
S = [
    (0.0, 'v', 'carta_sat', 0.0, 'punch'),
    (at('tienes') - .1, 'v', 'tiendita', 0.0, 'whip'),
    (at('pagas') - .1, 'v', 'banco', 0.0, 'whip'),
    (at('sientes') - .1, 'v', 'confiado', 0.0, 'whip'),
    (at('nadie', 1, 2) - .1, 'v', 'pensando', 0.0, 'blur'),
    (at('buzón', 2, 1) - .1, 'v', 'portal', 0.0, 'whip'),
    (at('pero') - .1, 'v', 'ojo', 0.0, 'zoom'),
    (at('$3850', 1, 1) - .1, 'v', 'cuenta_efectivo', 0.0, 'whip'),
    (at('quién') - .1, 'v', 'no_se', 0.0, 'blur'),
    (at('casi') - .1, 'v', 'sala_juntas', 0.0, 'whip'),
    (at('necesitas', 1, 2) - .1, 'v', 'pensando', 1.5, 'blur'),
    (at('efirma', 1, 1) - .1, 'v', 'efirma_usb', 0.0, 'whip'),
    (at('correo', 1, 1) - .1, 'v', 'telefono', 0.0, 'whip'),
    (at('secreto', 1, 1) - .1, 'v', 'lupa', 0.0, 'blur'),
    (at('link', 1, 2) - .1, 'v', 'portal', 1.0, 'whip'),
    (at('hasta', 1, 1) - .1, 'v', 'fecha_limite', 0.0, 'zoom'),
    (at('quieres') - .1, 'g', 'cta', 0, 'zoom'),
]
key = [
    (0.0, at('tienes') - .15, [('¿EL SAT TE VA A', 0.05, '#fff', 90), ('MULTAR', at('multar'), YEL, 160), ('EN ENERO?', at('enero'), '#fff', 110)], 'top'),
    (at('pero'), at('$3850', 1, 1) - .15, [('PERO OJO:', at('pero'), YEL, 120), ('MULTAS', at('multar', 2), '#fff', 120), ('DESDE 2027', at('2027'), YEL, 110)], 'top'),
    (at('secreto', 1, 1), at('link', 1, 2) - .15, [('EL SECRETO', at('secreto', 1, 1), YEL, 100), ('CONFÍRMALOS', at('confirmarlos'), '#fff', 104)], 'top'),
    (at('hasta', 1, 1), at('quieres') - .15, [('TIENES HASTA EL', at('hasta', 1, 1), '#fff', 84), ('31 DE', at('31'), YEL, 150), ('DICIEMBRE', at('diciembre'), YEL, 120)], 'top'),
]
extra = [
    (at('nadie', 1, 2), at('buzón', 2, 1) - .15, [('LO QUE NADIE', at('nadie', 1, 2), '#fff', 110), ('TE DICE...', at('dice'), YEL, 110)], 'mid'),
    (at('buzón', 2, 1), at('pero') - .15, [('BUZÓN', at('buzón', 2), YEL, 150), ('TRIBUTARIO', at('tributario'), '#fff', 110)], 'low'),
    (at('$3850', 1, 1), at('quién') - .15, [('DE $3,850', at('$3850'), '#fff', 110), ('A $11,540', at('$11540'), RD, 130)], 'low'),
    (at('quién'), at('casi') - .15, [('¿QUIÉN LO', at('quién'), '#fff', 120), ('ACTIVA?', at('activar'), YEL, 140)], 'low'),
    (at('casi'), at('necesitas', 1, 2) - .15, [('PERSONAS FÍSICAS', at('personas'), '#fff', 90), ('Y EMPRESAS', at('empresas'), YEL, 110)], 'low'),
    (at('efirma', 1, 1), at('secreto', 1, 1) - .15, [('E.FIRMA O CONTRASEÑA', at('efirma'), '#fff', 76), ('CORREO', at('correo'), YEL, 110), ('Y CELULAR', at('celular'), YEL, 110)], 'low'),
    (at('link', 1, 2), at('hasta', 1, 1) - .15, [('LINK DEL CORREO', at('link'), '#fff', 90), ('CÓDIGO AL CELULAR', at('código'), YEL, 84)], 'low'),
]
CTA = dict(l1='¿QUIERES SABER', l2='SI YA ESTÁ ACTIVO?', pill='ESCRÍBENOS', tail='a lo mejor el SAT ya te escribió...',
           t1=at('saber'), t2=at('escríbenos'), t3=at('porque'))
LOGO_HIDE = at('quieres') - .15
CAPS_END = at('quieres') - 0.15
MONEY = []
