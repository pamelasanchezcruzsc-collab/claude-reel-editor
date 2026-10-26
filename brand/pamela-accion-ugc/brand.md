# Pamela · Acción UGC — marca de reels

## Account
Experiencia real como creadora UGC, Talent Manager y mentora: cómo empezar, trabajar con marcas y construir una profesión alrededor del contenido, sin falsas promesas · Mujeres que quieren crear contenido y colaborar con marcas, sobre todo madres que quieren crecer profesionalmente sin perder de vista su vida familiar.

Idioma de los reels: español (España).

## Reference reel
https://www.instagram.com/reel/Ddt_k_8TLVk/ - lo que le encanta: el ritmo, el dinamismo, los stickers, los zooms, los efectos de sonido y el texto que cambia de lugar.

## Colours
Tonos tierra y burdeos.
- Main: #964B53 (burdeos rosado: títulos, cabeceras de tarjetas)
- Pop: #961D1D (burdeos intenso: palabras clave, botones)
- Earth: #8F6656 (marrón cálido: bloques de color, detalles)
- Light: #E7E1DB (crema: fondos de tarjetas)
- Soft: #D0C8BF (beige: fondos secundarios)
- Never: amarillo chillón, colores fluorescentes/neón. (Amarillo pastel sí está permitido.)

## Fonts
- Headlines / hook: Montserrat ExtraBold
- Captions / body: Poppins SemiBold
- Accent (palabras destacadas, tarjetas): DM Serif Display
- CapCut stand-in: pendiente de elegir en CapCut

## Captions
Una palabra cada vez, grande y centrada, en minúsculas. Crema con sombra suave; palabra clave de cada frase en burdeos #961D1D. Sin contornos en los subtítulos (el contorno solo en el título del gancho).

## Graphics
Juguetón tipo scrapbook y dinámico: stickers, zooms (punch-ins) frecuentes, texto que cambia de posición. Muchos gráficos (busy: uno cada 2-4 s), siempre ilustrando lo que dice esa frase. Stickers propios en `stickers/` (copiar a `~/reels/assets/stickers/`): emojis con borde blanco tipo scrapbook, chapas burdeos/crema con washi tape amarillo pastel y círculos "paso 1/2/3". `stickers.html` + `shoot.js` (Playwright) generan más con el mismo estilo. Los tutoriales llevan sticker o gráfico en casi cada frase. Sin carrusel obligatorio por ahora.

## Sound
Lots: whoosh, pop, snap, ding.

## Pacing
Ritmo TikTok (elegido por Pamela, variante C): 1.25x y cortes al ras de la voz, sin pausas ni respiraciones entre frases (`jumpcut.py` con gap 0.12, air 0.06, thresh -27 tras `tighten.py`). Revisar a oído: ruidos sueltos entre tomas (mirar el guion, chasquidos) se cortan a mano. Solo se cortan muletillas puras: eh, em, mmm, ah. Nunca cortar "este", "bueno", "pues", "vale". Máximo 60 s.

## Call to action
Cambia en cada reel: preguntar a Pamela cuál quiere. Si no lo dice, usar la que diga en el vídeo. Siempre al final.

## Where she posts
Instagram y TikTok · 1080p · versión CapCut activada (vive en España).

## Rules
- Nunca texto claro (crema/beige) sin sombra o fondo encima de ropa blanca: siempre debe leerse.
- Nada de amarillo chillón ni colores fluorescentes; amarillo pastel sí.
- Nada de tipografías decorativas tipo "Halloween": algo básico y fácil de leer.
- Siempre dinámico, como el reel de referencia.
- Transcribir en español (nunca con el modelo solo inglés).
- Al elegir entre tomas repetidas: usar la que esté mirando a cámara (no la que lee el guion: párpados bajados) y comprobar que el volumen sea igual al resto (si una toma está ~10 dB más baja, el micro falló: descartarla).
- Palabra clave de los subtítulos (burdeos) siempre sobre un panel crema (`captions.accent_bg`): el burdeos sobre ropa azul u oscura no se lee.
- Subtítulos con sombra fuerte (`captions.shadow: "strong"`, sin contorno): el crema se perdía sobre atardeceres, arena y cielo claro.
