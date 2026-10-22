# 🍕 The Packy BBS — Radio commands

Send these commands as **direct messages to your BBS radio**, not to a public channel.

| Command | Action |
| --- | --- |
| `/packy`, `/menu`, `/cancel` | Main menu |
| `/help`, `/apizza`, `/grinder` | Quick help |
| `/mail`, `/inbox` | Check mail |
| `/boards`, `/towngreen` | Bulletin boards (The Town Green) |
| `/fortune`, `/nutmeg` | Random Nutmeg Wisdom |
| `/tools`, `/utilities` | Utilities menu |

The existing one-letter menu options and existing quick commands remain available. These shortcuts are exact matches, case insensitive. In mail or bulletin text-entry steps, most shortcuts are ignored to avoid mangling content; `/cancel`, `/menu`, `/packy` and `/help` remain available.

## Design palette

`packy_desktop.py` implements the navy-and-gold Packy desktop with apizza-red buttons, shoreline lighthouse artwork, operator desks and log controls.

## Development

Run alias unit tests with:

```sh
python -m unittest discover -s tests -p 'test_packy_commands.py'
```

Radio integration and packaging still require hardware/runtime validation.


## Operator utilities

- `/node <ID or name>` — full radio node lookup.
- `/weather` — offline report or explicitly enabled internet weather.
- `/wire` — optional MQTT activity, separate from radio RX.
- `/announce <channel> <text>` — configured administrator nodes only.

See [configuration details](docs/CT_DESK.md).
