# Estudio de Reels

Review page (Claude artifact): https://claude.ai/artifact/Key2dp6vJptMtVi8n1igzX

- `estudio.html` — the page. Declares `db` (rules: `reel` and `review` write=admin), `assets`, `user`.
- `reel/current` (seeded by Claude): versions (asset ids of 540p proxies, `timeScale` maps edit.json times to that version), cards (id `c<i>` = index in edit.json), captions (flattened words), stickers, sounds.
- `review/decisions` (written by the page): `version`, `removedCards`, `cardText`, `captionEdits{wordIndex:{text,accent}}`,
  `added[{kind:sticker|emoji|sound, ref, t (seconds in that version's video), dur, x, y (1080x1920 centre), size (px width), db}]`, `notes[{t,text}]`, `status` (`ready` = apply).
- `estudio_ids.json` — asset ids of the uploaded sticker PNGs and sound mp4s. `estudio_seed.py` builds `reel/current` for a reel.
