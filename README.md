# Teleslate

A small, clipboard-based translation utility for Windows.

Teleslate reads text from the clipboard and sends it to an external streaming translation API (for example, DeepSeek). The translated text is shown in a small popup window near the mouse cursor as the API streams the result.

This tool is useful when other translation services become paid or restricted and you want to use your own API key.

## Table of contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [Security](#security)
- [License](#license)

## Features

- Clipboard-to-translation workflow: copy text with `Ctrl+C`, then press `Ctrl+X` to display the translation popup
- Streaming translation output updated in real time as the API responds
- Left-click the popup to cancel an ongoing stream
- Editable translation prompt in `backend.py` for custom tone, language, and formatting
- Automatic font selection for better Japanese rendering

## Requirements

- Windows with Python 3.10 or newer
- See `requirements.txt` for Python package dependencies

## Installation

1. Clone the repository:

```powershell
git clone https://github.com/Soranium/Teleslate.git
cd Teleslate
```

2. Create `apikey.txt` in the repository root and paste your API bearer token as a single line:

```
sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

3. Install Python dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the app:

```powershell
python teleslate.py
```

## Usage

1. Copy the text you want to translate (select and press `Ctrl+C`).
2. Press `Ctrl+X` to start the translation. A popup near the mouse cursor will appear and fill incrementally as the API streams the translated text.
3. Left-click the popup to cancel streaming and close the window.

**Workflow:** `Ctrl+C` to copy, then `Ctrl+X` to show translation.

## Configuration

### API key

Store your bearer token in `apikey.txt` (a single line).

### Prompt and API endpoint

Open `backend.py` and edit:

- `DeepSeekTranslator.API_URL` — change if using a different API service
- `DeepSeekTranslator.PROMPT` — customize translation instructions (tone, formatting, target language, etc.)

### Fonts

`teleslate.py` contains `choose_font()` which tries several fonts (Noto Sans JP variants, falls back to `Yu Gothic UI`). Add or reorder font names in the `noto_candidates` list to match your system fonts.

### Hotkey

Change the hotkey by editing the `keyboard.add_hotkey("ctrl+x", ...)` call in `teleslate.py`. Ensure the hotkey doesn't conflict with system shortcuts.

## Development

### Repository structure

- `teleslate.py` — main application (Tkinter GUI, global hotkey listener, clipboard reading, popup window management)
- `backend.py` — streaming API client (implements `DeepSeekTranslator` class with `translate_async` and `stop` methods)
- `apikey.txt` — stores your API bearer token (not version controlled)
- `requirements.txt` — Python package dependencies
- `font/` — directory for custom fonts (optional)

### API client

The `DeepSeekTranslator` class uses `requests` with `stream=True` to fetch translation tokens incrementally. Callbacks (`on_start`, `on_chunk`, `on_finish`) are used to update the GUI.

## Troubleshooting

- **Hotkey does not respond:** Try running the script as Administrator. Some global hotkey libraries require elevated privileges on Windows.
- **No translation appears:** Ensure you copied text to the clipboard first and that `apikey.txt` contains a valid API token.
- **API connection errors:** Verify `DeepSeekTranslator.API_URL` is correct and check your network/proxy settings. Confirm your API token is valid.
- **Popup not showing:** Check that text was actually copied to the clipboard and is not empty.

## Security

- `apikey.txt` contains a secret bearer token. Do not commit it to a public repository or share it.
- Add `apikey.txt` to `.gitignore` to prevent accidental commits.

## License

This project follows the terms in the repository `LICENSE` file.
