# Upstream audit — 2026-10-18

Baseline: BaconDisk22/The-Sitdown-BBS `e71eefe`. Read upstream main and closed
TheCommsChannel/TC2-BBS-mesh PRs [160](https://github.com/TheCommsChannel/TC2-BBS-mesh/pull/160)
and [162](https://github.com/TheCommsChannel/TC2-BBS-mesh/pull/162) before implementation.

The fork already has the skyline dashboard, eight navigation controls, process/RX
status, searchable/exportable logs, restart controls, personality model, icon
pipeline, and Intel packaging. Retain and extend those components.

Upstream main has basic statistics and mail-recipient lookup, but lacks the
requested utilities. PR 162 supersedes 160's utilities and adds node persistence.
Its announcement handlers do not enforce an administrator allowlist; the MQTT
script defaults to a public broker and shared credentials. Wholesale adoption
would violate this fork's administrator-only and opt-in requirements.

Implement narrow shared services around the existing Meshtastic interface:
explicit administrator IDs, enabled-channel validation, UTF-8 byte limits,
one startup broadcast attempt, full in-memory radio node lookup, then optional
weather/MQTT and desktop controls. Keep the TCP constructor and BBS sync routing.
Do not import unrelated database refactors or replace the radio receive path.
