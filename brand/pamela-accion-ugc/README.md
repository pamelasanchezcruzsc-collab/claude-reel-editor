# Marca de Pamela · Acción UGC

Archivo de marca del editor de reels, guardado aquí para no repetir la entrevista en cada sesión nueva.

Para restaurarlo en una máquina nueva (después de instalar el editor):

```bash
mkdir -p ~/reels/fonts
cp brand/pamela-accion-ugc/brand.md brand/pamela-accion-ugc/brand.json ~/reels/
cp brand/pamela-accion-ugc/fonts/*.ttf ~/reels/fonts/
```

Tipografías (licencia SIL Open Font License): Montserrat ExtraBold, Poppins SemiBold, DM Serif Display.

Notas para Claude:
- Los reels son en español: transcribir con un modelo multilingüe y `--language es`, nunca `small.en` (el `transcribe.py` del editor lo tiene fijo en inglés).
- En la nube, Whisper necesita `huggingface.co` permitido en la red del entorno.
