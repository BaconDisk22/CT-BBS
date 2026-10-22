# Connecticut artwork

Both images are drawn in code by `scripts/draw_ct_artwork.py` (Pillow, macOS system
fonts: Impact, Futura, American Typewriter). They are embedded in the app and
packaged for offline use. They are not UI mockups.

- `ct-banner.png` (2172x724): night shoreline on Long Island Sound with stars, a full
  moon and its reflection, a Charter Oak silhouette and a red-and-white striped
  lighthouse with a beam. Left panel: THE / gold PACKY / red BBS, "NUTMEG STATE •
  COMMUNICATIONS DIVISION" and "Take a left where the old Ames used to be."
- `ct-icon.png` (1254x1254): rounded navy Dock tile with a gold rim, the striped
  lighthouse over the water, gold PACKY lettering and "BBS • CT". Transparent corners.

Regenerate with `python scripts/draw_ct_artwork.py`, then run `scripts/make_icon.py`,
which resizes the icon for the Mac packaging pipeline and `docs/images/app-icon.png`.
