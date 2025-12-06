![Image](https://github.com/user-attachments/assets/f5bf53da-01a5-46be-8b5e-3b8e1df836e9)
# Teleslate
Teleslate is a lightweight Windows/Linux tool that uses a DeepSeek API key
to translate text copied to the clipboard.

(Copy text with Ctrl+C → Translate with Ctrl+X)

The translation result appears in real time as a small popup near the mouse cursor.

It can be used as a simple and convenient alternative when Telegram’s translation feature or other free services become paid.

----日本語----

Teleslate は DeepSeek の API Key を使用し、

クリップボードにコピーしたテキストを翻訳する Windows/Linux向けの軽量ツールです。
（Ctrl+C でコピー → Ctrl+X で翻訳）

翻訳結果はマウスカーソル付近に小さなポップアップとしてリアルタイム表示されます。

テレグラムの翻訳や無料サービスが有料化された場合の、 シンプルで手軽な代替手段として利用できます。
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

- Windows/Linux with Python 3.10 or newer
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

- **Hotkey does not respond:** Try running the script as Administrator. Some global hotkey libraries require elevated privileges on Windows/Linux.
- **No translation appears:** Ensure you copied text to the clipboard first and that `apikey.txt` contains a valid API token.
- **API connection errors:** Verify `DeepSeekTranslator.API_URL` is correct and check your network/proxy settings. Confirm your API token is valid.
- **Popup not showing:** Check that text was actually copied to the clipboard and is not empty.

## Security

- `apikey.txt` contains a secret bearer token. Do not commit it to a public repository or share it.
- Add `apikey.txt` to `.gitignore` to prevent accidental commits.

## License

This project follows the terms in the repository `LICENSE` file.
