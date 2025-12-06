# Teleslate

A small, clipboard-based translation utility for Windows.

Teleslate reads text from the clipboard and sends it to an external streaming translation API (e.g. DeepSeek).
The translated text is shown in a small popup window near the mouse cursor as the API streams the result.
This tool is useful when other translation services become paid or restricted and you want to use your own API key.

Features

- Clipboard -> translation hotkey (default: `Ctrl+C` then `Ctrl+X` to start showing the translation)
- Streaming translation output shown in a popup; left-click the popup to cancel the stream
- Prompt for translation is editable in `backend.py` for custom style/behavior
- Automatic font selection for Japanese-friendly rendering

Repository structure (important files)

- `teleslate.py` — main application (Tkinter GUI, global hotkey registration, clipboard reading)
- `backend.py` — streaming client that connects to a translation API (DeepSeek-compatible)
- `apikey.txt` — put your API bearer token here (single line, read by the program)

Requirements

- Python 3.10 or newer (Windows)
- See `requirements.txt` for Python package dependencies

Installation

1. Clone this repository or copy the files to a folder.
2. Create `apikey.txt` in the repository root and paste your API bearer token as a single line. Example:

```
sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

3. Install dependencies using `requirements.txt`:

```powershell
python -m pip install -r requirements.txt
```

Usage

1. Run the app (PowerShell recommended):

```powershell
python teleslate.py
```

2. Copy any text you want to translate (for example, select text and press `Ctrl+C`).
3. Press `Ctrl+X` (default hotkey) to start translation. The popup will appear near the mouse cursor and will be filled incrementally as the API streams the translation.
   - Note: the workflow is copy with `Ctrl+C`, then press `Ctrl+X` to display the translation.
4. Left-click the popup to cancel an ongoing stream and close the popup.

Configuration & Customization

- Prompt: open `backend.py` and edit `DeepSeekTranslator.PROMPT` to change translation instructions (tone, formatting, rules, etc.).
- API endpoint: if you use a different service, update `DeepSeekTranslator.API_URL` accordingly.
- Fonts: `teleslate.py` contains `choose_font()` that tries several fonts; add or change names to match your system fonts.
- Hotkey: change the hotkey in `teleslate.py` where `keyboard.add_hotkey("ctrl+x", ...)` is called if you prefer a different shortcut.

Troubleshooting

- Hotkey not responding: try running the script as Administrator (the `keyboard` package may require elevated privileges for global hooks).
- Nothing is pasted/translated: make sure you copied text to the clipboard before pressing `Ctrl+X`.
- API errors or no response: verify the token in `apikey.txt`, and check the `API_URL` in `backend.py` for the correct endpoint and expected request format.

Security note

- `apikey.txt` contains a secret bearer token. Keep it private and do not commit it to public repositories.

License
This project follows the terms in the repository `LICENSE` file.

Contributing

- Bug reports and small improvements are welcome. For larger changes (new features, refactor), please open an issue first so we can discuss the design.
