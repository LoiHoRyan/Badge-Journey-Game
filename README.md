# 🏅 BADGE JOURNEY

> **Play to explore – Learn to reach further.**

**Badge Journey** is a 2D pixel-art platformer game with animated elements, built using Python. Players take on the role of a knight, exploring diverse lands, overcoming challenges, collecting badges, and reaching new milestones along the way.

The project aims to provide an entertaining experience that blends exploration with learning, featuring a vibrant, colorful game world suitable for children and teenagers.

---

## ✨ Key Features

- **Diverse Worlds:** The journey spans multiple lands, each with its own unique setting and challenges.
- **Exploration and Collection:** Players navigate through levels, collecting badges to expand their journey.
- **Challenges and Combat:** Face off against obstacles, enemies, and final bosses.
- **Skill System:** Utilize skills via the Q, E, R, and T keys; each skill consumes a specific amount of mana.
- **Visual Style:** Bright, pixel-art graphics that evoke a sense of fantasy adventure.
- **Level Data:** Game level information is structured as data, facilitating easy management and future development.

## 🌍 Game Worlds

The journey is planned to span 10 distinct worlds:

| No. | World |
|---:|---|
| 1 | Grasslands |
| 2 | Desert |
| 3 | Beach |
| 4 | Deep Forest |
| 5 | Snowy Region |
| 6 | Volcano |
| 7 | City in the Clouds |
| 8 | Mechanical Factory |
| 9 | Space |
| 10 | The Last Ancient Temple |

*The list above outlines the project's design direction; the content and progress of each world are subject to change during development.*

## 🕹️ Controls

| Key | Function |
|---|---|
| Q | Use Q skill (consumes 20 mana) |
| E | Use E skill (consumes 30 mana) |
| R | Use R skill (consumes 25 mana) |
| T | Use T skill (consumes 60 mana) |

> For movement, jumping, interaction, and other actions, please refer to the in-game tutorial or the control configuration for the current version.

## 🧰 Technologies and Tools

- **Python:** Primary programming language.
- **JSON:** Used for storing level data.
- **Tiled:** Map design tool (if utilized in the current version).
- **PyInstaller:** Used for packaging the desktop application via a `.spec` file.

Required Python libraries are listed in `requirements.txt`. ## 📁 Project Structure

```text
Badge-Journey-Game/
├── assets/                 # Game images and resources
├── data/                   # Game-related data
├── music/                  # Music and sound effects
├── saves/                  # Game save data (if applicable)
├── main.py                 # Program entry point
├── settings.py             # Game settings
├── levels.json             # Level data
├── game_icon.ico           # Game icon
├── requirements.txt        # List of Python dependencies
├── Badge Journey.spec      # PyInstaller build configuration
├── Badge Journey.md        # Project documentation
├── .gitignore              # Files/folders to exclude from Git
└── README.md               # Project introduction and instructions
```

*The structure may be subject to change based on the latest version of the source code.*

## 🚀 Installation and Running the Game

### 1. Requirements

- A Windows, macOS, or Linux computer with a version of Python compatible with the project's dependencies.
- Git (if cloning the source code via Git).
- All resources included in the repository.

### 2. Downloading the Source Code

```bash
git clone https://github.com/LoiHoRyan/Badge-Journey-Game.git
cd Badge-Journey-Game
```

Alternatively, download the repository as a ZIP file from GitHub and extract it. ### 3. Create a virtual environment (recommended)

```bash
python -m venv .venv
```

Activate the virtual environment:

**Windows (CMD):**
```bat
.venv\Scripts\activate
```

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
source .venv/bin/activate
```

### 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Run the project

```bash
python main.py
```

If the project requires additional configuration or resources, please check the relevant instructions provided in the project folders or documentation.

## 💾 Game Save Data

The `saves/` directory is intended for storing game progress, provided the current version utilizes this save mechanism. Please do not upload personal data or individual player save files to a public repository. You may include a sample save file if necessary.

## 🛠️ Project Development

You can contribute by:

1. Forking the repository.
2. Creating a new branch for your changes.
3. Implementing and testing your changes.
4. Submitting a Pull Request with a clear description.

When adding new resources, please place them in the appropriate directories and update the corresponding file paths within the source code or game data.

## 📌 Project Status

Badge Journey is currently under development. Features, levels, visuals, and content are subject to ongoing updates.

## 📄 Copyright and Resources

The resources within this project—including source code, images, audio, fonts, and data—may originate from various sources. Please verify the applicable permissions.
