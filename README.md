<div align="center">
  <img width="327" height="447" alt="Mascot Bot" src="https://github.com/user-attachments/assets/e6aa0648-a217-454e-b746-741c11aebaac" />
  <h1>🐶 Mascot — Ultimate Frisbee Discord Bot</h1>
  <p><i>A simple Discord bot that keeps your ultimate team updated on games, standings, and field status</i></p>
</div>

---

### 🥏 About Mascot

Mascot was created to make it easier for my ultimate frisbee team to stay informed about our **weekly games and standings**.

Every week, I used to manually post:
- Who we're playing against  
- The jersey colour to wear  
- The field number and location
- Our current standings in the league

Now, Mascot automates that! It fetches info directly from the league website and field status updates so I can just type a quick command in Discord. 

---

### 🌐 Data Sources

Mascot currently scrapes data using **BeautifulSoup** from:
- 🗓️ [Perpetual Motion League Schedules & Standings](https://perpetualmotion.org/ultimate-schedules-and-standings/)  
  → for weekly games and standings  
- 🌱 [City of Guelph Sports Field Status](https://guelph.ca/seasonal/sports-field-status/)  
  → for up-to-date field closures and conditions  

---

### 💬 Commands

#### 🏟️ Game & Attendance
| Command | Description | Example |
|----------|--------------|----------|
| `!game <division> <date>` | Get upcoming game info | `!game b2 1026` |
| `!st <division>` | Show current standings | `!st b2` |
| `!field` | Check field status | `!field` |
| `!at` | Dynamic attendance check with ✅ / ❌ reactions | `!at` |

---

#### ⚙️ Config & Admin
| Command | Description | Example |
|----------|--------------|----------|
| `!set_div <division> <id>` | Set team ID for schedule | `!set_div b2 16259` |
| `!list_div` | List all divisions | `!list_div` |
| `!set_st <division> <id>` | Set standings ID | `!set_st b2 2394` |
| `!list_st` | List standings divisions | `!list_st` |
| `!add_playoff <Day, Mon DD>` | Add playoff date | `!add_playoff Sun, Jan 11` |
| `!list_playoffs` | List playoff dates | `!list_playoffs` |
| `!add_holiday <Day, Mon DD>` | Add holiday date | `!add_holiday Sun, Dec 28` |
| `!list_holidays` | List holidays | `!list_holidays` |
| `!clear` | Clear all configs | `!clear` |

---
<div align="center">

🗓️ **Game Information Embed with Attendance Tracking**  
<img width="417" height="341" alt="Mascot announcement example" src="https://github.com/user-attachments/assets/21c1e81f-fd67-41ce-aea1-5630d431f20f" />

---

🐶 **List of Commands**  
<img width="620" height="531" alt="Weekly schedule example" src="https://github.com/user-attachments/assets/cc7792fa-126a-4965-a890-5f9ef5794785" />

---

📊 **Standings Overview**  
<img width="722" height="275" alt="Standings example" src="https://github.com/user-attachments/assets/222daec4-c921-47fb-afb5-35486dedb1a9" />

</div>

---
### 🧩 Tech Stack
- **Python 3.11+**
- **Discord.py**
- **BeautifulSoup4**
- **Requests**
- **JSON for config storage**

---

### 🧠 Future Ideas
- Automatically post weekly game reminders
---

### ✨ Most recent updates
- Improved file structure (cogs, services, and utils)
- Revamped message structure and format to make it easier to read
- Integrated config commands for admins to add/delete team IDs per season and new teams (no more manually adding it!)
- Live attendance tracking that lists attendees directly in the announcement message 

---
<div align="center">
  <sub>Built with 🥏 + 💻 by An Pham</sub>
</div>
