# Jersey artwork

Production raster artwork generated with the built-in image-generation tool from
the user's supplied Jersey desktop/icon reference on 2026-10-18. These assets are
embedded in the actual app and packaged offline; they are not UI mockups.

- `jersey-banner.png`: Nighttime North Jersey waterfront and illuminated bridge,
  distressed green SIT / white DOWN / red brush BBS lettering, division subtitle,
  and a tricolor New Jersey silhouette. No rendered controls or window chrome.
- `jersey-icon.png`: Rounded dark tile, fine silver rim, nighttime waterfront,
  large distressed tricolor New Jersey silhouette, stacked white THE SITDOWN and
  vivid red brush BBS. Transparent outer corners.

Prompt set: create production artwork closely matching the screenshot's cinematic
nighttime waterfront, distressed lettering and green/white/red Jersey identity.
Banner prompt requested exact text “THE SITDOWN BBS” and “NORTH JERSEY •
COMMUNICATIONS DIVISION”, edge-to-edge landscape artwork without controls.
Icon prompt requested a single rounded-square Dock icon with the same imagery,
exact title, silver rim and transparent exterior; no UI or extra captions.

`scripts/make_icon.py` resizes this approved icon for the Mac packaging pipeline.
It must not replace the artwork with the earlier simple skyline drawing.
