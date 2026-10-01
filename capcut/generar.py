from PIL import Image, ImageDraw, ImageFont, ImageFilter
W, H = 1920, 1080
CREMA = (244, 234, 216, 255)
ORO = (201, 160, 92, 255)
SERIF = "fuentes/CormorantGaramond-Italic.ttf"
CAPS = "fuentes/Cinzel.ttf"

def fuente(path, size, peso):
    f = ImageFont.truetype(path, size)
    try: f.set_variation_by_axes([peso])
    except Exception: pass
    return f

def texto_espaciado(d, xy, txt, f, fill, track):
    x, y = xy
    for ch in txt:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track

def ancho_espaciado(d, txt, f, track):
    return sum(d.textlength(c, font=f) for c in txt) + track * (len(txt) - 1)

def con_sombra(capa):
    a = capa.split()[3]
    sombra = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    sombra.putalpha(a.point(lambda v: int(v * 0.65)))
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    out = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    out.alpha_composite(sombra, (0, 4))
    out.alpha_composite(capa)
    return out

def frase(txt, nombre):
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    f = fuente(SERIF, 78, 500)
    w = d.textlength(txt, font=f)
    y = int(H * 0.76)
    d.text(((W - w) / 2, y), txt, font=f, fill=CREMA)
    # filete dorado corto bajo la frase
    d.line([(W / 2 - 40, y + 118), (W / 2 + 40, y + 118)], fill=ORO, width=2)
    con_sombra(capa).save(nombre)

def titulo(nombre):
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    ft = fuente(SERIF, 230, 400)
    t = "Ódiame"
    bb = d.textbbox((0, 0), t, font=ft)
    tw = bb[2] - bb[0]
    y = int(H * 0.36)
    d.text(((W - tw) / 2 - bb[0], y), t, font=ft, fill=CREMA)
    base = y + bb[3] + 34
    d.line([(W / 2 - 90, base), (W / 2 + 90, base)], fill=ORO, width=2)
    fc = fuente(CAPS, 40, 500)
    linea = "KIARA SOUL & DORIAN FERRER"
    track = 9
    cw = ancho_espaciado(d, linea, fc, track)
    texto_espaciado(d, ((W - cw) / 2, base + 30), linea, fc, CREMA, track)
    con_sombra(capa).save(nombre)

frase("Se prometieron no volver a verse", "01_se_prometieron.png")
frase("Pero ninguno quiso ser olvidado", "02_ninguno_quiso_ser_olvidado.png")
titulo("03_titulo_odiame.png")

# vista previa sobre fondo cálido oscuro, solo para revisar
for n in ["01_se_prometieron.png", "02_ninguno_quiso_ser_olvidado.png", "03_titulo_odiame.png"]:
    fondo = Image.new("RGBA", (W, H), (58, 36, 26, 255))
    g = Image.radial_gradient("L").resize((W, H))
    oscuro = Image.new("RGBA", (W, H), (14, 10, 10, 255)); oscuro.putalpha(g)
    fondo.alpha_composite(oscuro)
    fondo.alpha_composite(Image.open(n))
    fondo.convert("RGB").resize((960, 540)).save("vista_previa_" + n.replace(".png", ".jpg"), quality=88)
