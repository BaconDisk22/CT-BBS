<div align="center">

<img src="assets/ct-banner.png" alt="The Packy BBS banner: shoreline lighthouse at night" width="900">

# 🍕 THE PACKY BBS
### ⚓ Nutmeg State Communications Division ⚓

**“Come on in. Take a left where the old Ames used to be.”**

🌊 **Long Island Sound Navy** · 🟡 **Nutmeg Gold** · 🍅 **Apizza Red** · 🦪 **White Clam White**

*A Meshtastic bulletin board for the whole state: the Valley, the Shoreline, the Quiet Corner and, fine, even Fairfield County.*

</div>

---

## 🏛️ Welcome to the Nutmeg State

Around here we don't just send messages. **We stop by the packy.**

**The Packy BBS** is a Connecticut-themed Meshtastic bulletin board server based on the open-source TC²-BBS project (by way of The Sitdown BBS). Send direct messages over Meshtastic to read the town bulletins, check your mail, browse channels and run utilities. The radio link needs no internet.

Think old-school bulletin boards with a Connecticut attitude: apizza arguments, grinders, the Merritt, Brass Bonanza, and directions based on stores that closed in 1999. Whichever town you're from (and it's better than the next town over), there's a stool at the counter.

> **Important:** This is an independent community project and a loving homage to Connecticut. It is not affiliated with, or endorsed by, any business, team, utility or town mentioned in its jokes.

## 📻 What's on the menu?

| Connecticut name | What it does |
| --- | --- |
| 🌳 **The Town Green** | Bulletin boards and community posts |
| ✉️ **Note on the Windshield** | BBS mail |
| 🗺️ **Where the Old Ames Was** | Channel directory |
| ⚡ **Is Eversource Up?** | Server utilities and statistics |
| 🔮 **Nutmeg Wisdom** | 100 random Connecticut fortunes |
| 🌦️ **Wait-Five-Minutes Weather Desk** | Offline report or opt-in internet weather |
| 🏛️ **The First Selectman Has Spoken** | Admin-only announcements |
| 🖥️ **The Packy Desktop** | Tabbed desktop with server status, searchable logs, operator desks and full node lookup |
| 🧪 **Demo Mode** | Explore the desktop without connecting or transmitting over radio |
| 🔋 **The Generator** | ZIP backup of local settings and databases (you already know what's coming) |

**Development note:** This repository starts from The Sitdown BBS as of its v0.1.0-rc.6 feature set. Desktop features, MQTT monitoring and Intel Mac packaging carry over unchanged; only names, copy, art and defaults are Connecticut. Radio and broker behavior still needs fresh testing with real hardware.

## 🏛️ Town Hall: dashboard tools

| Control | What it does |
| --- | --- |
| **Find in Log / Find Next** | Search the visible server activity log |
| **Save Log** | Export the visible log as UTF-8 text |
| **Clear Log** | Clear the visible log without stopping the BBS |
| **Nodes / Who's Who** | Search the whole radio node database by ID or name |
| **Refresh USB Ports** | List serial devices; fills in the port when exactly one is found |
| **Restart on crash** | Optionally restart the server after an unexpected exit, with capped backoff |
| **Radio activity** | Reports incoming messages seen in BBS logs, without claiming a permanent link |

### Nutmeg Mouth Control

The Home page offers **Clean**, **Valley** and **Route 8** greeting styles. Settings configures the startup broadcast greeting, with a separate opt-in for public profanity. Custom announcements, mail and technical notices are always sent verbatim.

## 🥪 The Grinder Menu: radio commands

Send these as **direct messages to the Meshtastic BBS node**.

| Command | Meaning |
| --- | --- |
| `/packy` or `/menu` | Back to the main menu |
| `/help`, `/apizza` or `/grinder` | Quick help |
| `/mail` or `/inbox` | Check your mail |
| `/boards` or `/towngreen` | The Town Green bulletin boards |
| `/fortune` or `/nutmeg` | Nutmeg Wisdom |
| `/tools` | Utilities |
| `/cancel` | Return to the main menu |
| `/node <ID or name>` | Full radio node lookup |
| `/weather` | Wait-Five-Minutes Weather Desk |
| `/wire` | Optional MQTT topic counts |
| `/announce <channel> <text>` | Administrator-only broadcast |

The original TC²-BBS one-letter menus and quick commands still work alongside the Connecticut shortcuts. More details: [PACKY_COMMANDS.md](PACKY_COMMANDS.md).

## 📡 MQTT network: CTMesh

The desktop can watch one MQTT network, **CTMesh**, receive-only by default. It defaults to the public `mqtt.meshtastic.org` broker and stays off until you turn it on in Settings; point it at your channel's topic. Networks are listed in one place (`NETWORK_LABELS` in `packy_mqtt_feed.py`), so adding a real second Connecticut network later is a small change.

## 🖥️ Desktop

<img src="docs/images/app-icon.png" alt="The Packy BBS Dock icon: striped lighthouse with PACKY lettering" width="180">

The dashboard uses navy and gold panels, apizza-red buttons, and a night shoreline banner with a lighthouse and the Charter Oak. Controls include **Open the Packy**, **Closed for the Blizzard**, **The Grinder Menu**, **The Board of Selectmen**, **The Generator** and **Ask a Valley Guy**. All artwork is drawn by [scripts/draw_ct_artwork.py](scripts/draw_ct_artwork.py) and bundled for offline use.

Demo screenshots in `docs/images/*-preview-demo.png` come from the **README desktop screenshot** workflow. Re-run it after a UI change so they show the current look.

[Desktop screenshot automation](https://github.com/BaconDisk22/CT-BBS/actions/workflows/readme-desktop-screenshot.yml) · [Intel Mac releases](https://github.com/BaconDisk22/CT-BBS/releases)

### 📦 Download the latest Intel Mac build

[![Intel Mac test build](https://github.com/BaconDisk22/CT-BBS/actions/workflows/intel-mac-test-build.yml/badge.svg)](https://github.com/BaconDisk22/CT-BBS/actions/workflows/intel-mac-test-build.yml)

- **GitHub Releases:** look for the latest `CT-BBS-Intel-Mac-*.dmg` attached to a successful release.
- **GitHub Actions:** open a successful **Intel Mac test build** run and download the **CT-BBS-Intel-Mac-Test** artifact. Artifacts expire after 14 days.
- **Intel Mac:** builds target x86-64 macOS and are **unsigned and unnotarized**. Approve trusted builds in macOS Privacy & Security if prompted.
- **Live radio:** configure your Meshtastic device before starting the real BBS server. A running process alone does not confirm a connected radio.

For packaging details see [INTEL_MAC_TEST_BUILDS.md](INTEL_MAC_TEST_BUILDS.md), and for releases see [RELEASE_PROCESS.md](RELEASE_PROCESS.md).

### 🛠️ Run from source

Requires **Python 3 with Tkinter** and the dependencies in `requirements.txt`.

```bash
git clone https://github.com/BaconDisk22/CT-BBS.git
cd CT-BBS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp example_config.ini config.ini
# Review config.ini before connecting a radio.
python3 packy_desktop.py
```

Turn on **Demo mode** to explore without a radio. For the headless server, run `python3 server.py`. The default weather location is Meriden, near the middle of the state.

## 🎨 Nutmeg colors

| Role | Color |
| --- | --- |
| Background | `#06101F` Long Island Sound Navy |
| Panels | `#0B1A30` Merritt Midnight |
| Primary actions | `#B3261E` Apizza Char Red |
| Connected / start | `#2FBF71` Town Green |
| Text | `#F4F1EA` White Clam White |
| Highlights | `#E8B931` Nutmeg Gold |

## 🧪 Development and testing

```bash
python3 -m unittest discover -s tests
```

GitHub Actions runs syntax checks and the full unit test suite, and the Intel Mac workflow runs the real-window desktop tests. You still need to test with real hardware before calling a radio release production-ready.

## 🙏 Respect to the original crew

**Upstream credit:** The Packy BBS is based on **TC²-BBS Meshtastic** by **TheCommsChannel (TC²)**, through the New Jersey-themed **The Sitdown BBS**. The original project provided the BBS architecture and Meshtastic integration; this fork adds its own Connecticut theme, shortcuts, fortunes and artwork.

- [Original TC²-BBS-mesh project](https://github.com/TheCommsChannel/TC2-BBS-mesh)
- [Meshtastic](https://meshtastic.org/)
- [Python Meshtastic examples](https://github.com/meshtastic/python)
- [pdxlocations Meshtastic examples](https://github.com/pdxlocations/Meshtastic-Python-Examples)

**License:** GNU General Public License v3.0, consistent with the original project. Keep original copyright notices and license terms.

---

<div align="center">

### 🍕 “Wait five minutes. You're from here now.”

**THE PACKY BBS** · *Nutmeg State Communications Division*

*Built for the mesh. Raised on apizza.*

</div>
