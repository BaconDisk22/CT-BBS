<div align="center">

# 🤌 THE SITDOWN BBS
### 🇮🇹 North Jersey Communications Division 🇮🇹

**“Ayyy, pull up a chair. We gotta talk.”**

🖤 **Jersey Black** · ❤️ **Italian Red** · 💚 **Italian Green** · 🟡 **Diner Gold**

*A neighborhood social club for Meshtastic radio communications. Everybody's got connections.*

</div>

---

## 🥩 Welcome to the family

Around here, we don't just send messages. **We have sitdowns.**

**The Sitdown BBS** is a New Jersey–themed fork of the TC²-BBS Meshtastic bulletin board server. Send direct messages over Meshtastic to access community bulletins, mail, channel information, and utilities—no internet required for the radio link.

Think old-school bulletin boards with a North Jersey attitude: diner coffee, Sunday gravy, and the eternal **pork roll vs. Taylor ham** debate. Whatever exit you're from, there's a seat at the table.

> **Important:** This is an independent community project with a fictional Italian-American social-club theme. It is not affiliated with any television show.

## 📻 What's in the family business?

| Jersey name | What it does |
| --- | --- |
| 🥩 **The Social Club** | Bulletin boards and community posts |
| ✉️ **A Word With You** | BBS mail |
| 🗺️ **What Exit?** | Channel directory |
| 📊 **Who's Connected?** | Server utilities and statistics |
| 🔮 **Jersey Wisdom** | Random fortunes |
| 🖥️ **The Sitdown Desktop** | Experimental GUI launcher for macOS and other Tkinter platforms |
| 🧪 **Demo Mode** | Explore the desktop controls without a connected radio |
| 📦 **The Books** | Create a ZIP backup of available local settings and database files |

**Development note:** The desktop interface is an early implementation. Live radio diagnostics, restore, packaged Mac releases, and automated screenshots are not yet finished or validated.

## 🤌 The Playbook — radio commands

Send these as **direct messages to the Meshtastic BBS node**.

| Command | Meaning |
| --- | --- |
| `/sitdown` or `/menu` | Back to the main menu |
| `/help` or `/ayyy` | Quick help |
| `/mail` or `/inbox` | Check your mail |
| `/boards` or `/socialclub` | Open the bulletin board |
| `/fortune` | Get a random fortune |
| `/tools` | Utilities |
| `/cancel` | Return to the main menu |

The original TC²-BBS one-letter menus and quick commands remain available. The new aliases are currently on the feature branch until merged. More details: [SITDOWN_COMMANDS.md](SITDOWN_COMMANDS.md).

## 🖥️ Run the desktop preview

Requires **Python 3 with Tkinter** and the dependencies listed in `requirements.txt`. For a live radio, configure your Meshtastic node and create `config.ini` first.

```bash
git clone https://github.com/BaconDisk22/The-Sitdown-BBS.git
cd The-Sitdown-BBS
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp example_config.ini config.ini
# Edit config.ini for your device.
python3 sitdown_desktop.py
```

Select **Demo mode** if you don't have a radio connected. For the original headless server:

```bash
python3 server.py
```

**Intel Mac users:** A packaged click-to-open `.app`/`.dmg` is planned, but not yet available. Until then, use the Python desktop preview. See [SITDOWN_DESKTOP.md](SITDOWN_DESKTOP.md) for current limitations.

## 🎨 Jersey colors, not Joker colors

| Role | Color |
| --- | --- |
| Background | `#121212` Jersey Black |
| Panels | `#242424` Charcoal |
| Primary actions | `#C62828` Italian Red |
| Connected / start | `#008C45` Italian Green |
| Text | `#F5F5F0` Mozzarella White |
| Highlights | `#F4B942` Diner Gold |

No purple, no Joker branding. Just Jersey.

## 🧪 Development and testing

```bash
python3 -m unittest discover -s tests -p 'test_sitdown_commands.py'
```

GitHub Actions also checks syntax and the command alias tests. Hardware validation is still required before calling a radio release production-ready.

## 🙏 Respect to the original crew

**The Sitdown BBS** is based on **TC²-BBS Meshtastic** by **TheCommsChannel (TC²)**. The original project provided the BBS architecture and Meshtastic integration; this fork adds its own Jersey theme, shortcuts, and desktop preview.

- [Original TC²-BBS-mesh project](https://github.com/TheCommsChannel/TC2-BBS-mesh)
- [Meshtastic](https://meshtastic.org/)
- [Python Meshtastic examples](https://github.com/meshtastic/python)
- [pdxlocations Meshtastic examples](https://github.com/pdxlocations/Meshtastic-Python-Examples)

**License:** GNU General Public License v3.0, consistent with the original project. Keep original copyright notices and license terms.

---

<div align="center">

### 🤌 “Fuggedaboutit. You're family now.”

**THE SITDOWN BBS** · *North Jersey Communications Division*

*Built for the mesh. Raised in Jersey.*

</div>
