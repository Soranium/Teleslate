# teleslate.py
import tkinter as tk
import tkinter.font as tkFont
import keyboard
import pyperclip
import pyautogui
import queue
from pynput import mouse

from backend import DeepSeekTranslator


# ==============================
# APIKEY load
# ==============================
def load_api_key():
    with open("apikey.txt", "r", encoding="utf-8") as f:
        return f.read().strip()


translator = DeepSeekTranslator(load_api_key())
popup_queue = queue.Queue()


def choose_font(root):
    fonts = tkFont.families()

    noto_candidates = [
        "Noto Sans JP Light",
        "NotoSansJP-Light",
        "Noto Sans JP",
        "Noto Sans CJK JP",
        "Noto Sans",
    ]

    for name in noto_candidates:
        if name in fonts:
            return (name, 13)

    print("[FONT] Noto not found Yu Gothic UI used")
    return ("Yu Gothic UI", 13)


# ==============================
# Popup Window
# ==============================
class PopupWindow:
    def __init__(self, root, font_main):
        self.root = root
        self.font_main = font_main

        self.popup = None
        self.text_buffer = ""
        self.label = None
        self.frame = None

        self.width = 440
        self.height = 90
        self.opacity = 0.0

        self.following = True
        self.finished = False

        # 色
        self.color_neon = "#FFFFFF"
        self.color_bg = "#17191B"       
        self.border_color = "#170664"   

        # 追尾用
        self.cur_x = None
        self.cur_y = None
        self.ease = 0.25

    # ------------------------------------
    def open(self):
        if self.popup:
            return

        x, y = pyautogui.position()
        self.cur_x = x + 15
        self.cur_y = y + 25

        self.popup = tk.Toplevel(self.root)
        self.popup.overrideredirect(True)
        self.popup.attributes("-topmost", True)
        self.popup.attributes("-alpha", 0.0)

        # main frame
        self.frame = tk.Frame(
            self.popup,
            bg=self.color_bg,
            highlightthickness=2,
            highlightbackground=self.border_color,
        )
        self.frame.pack(fill="both", expand=True)

        # text label
        self.label = tk.Label(
            self.frame,
            text="",
            fg=self.color_neon,
            bg=self.color_bg,
            font=(self.font_main[0], 11),
            justify="left",
            wraplength=self.width - 40,
            padx=16,
            pady=14,
        )
        self.label.pack(anchor="nw")

        self.popup.geometry(f"{self.width}x{self.height}+{self.cur_x}+{self.cur_y}")

        self.popup.bind("<Button-1>", self.kill_and_close)

        self.fade_in()
        self.follow_cursor()

    # ------------------------------------
    def update_text(self, chunk):
        if not self.popup:
            self.open()

        self.text_buffer += chunk
        self.label.config(text=self.text_buffer)

        self.popup.update_idletasks()
        req_h = self.label.winfo_reqheight() + 28
        if req_h < 90:
            req_h = 90
        self.height = req_h

    # ------------------------------------
    def fade_in(self):
        if not self.popup:
            return
        if self.opacity < 0.92:
            self.opacity += 0.05
            self.popup.attributes("-alpha", self.opacity)
            self.popup.after(12, self.fade_in)

    def fade_out(self):
        if not self.popup:
            return
        if self.opacity > 0:
            self.opacity -= 0.06
            self.popup.attributes("-alpha", self.opacity)
            self.popup.after(18, self.fade_out)
        else:
            self.close()

    # ------------------------------------
    # cursor follow
    # ------------------------------------
    def follow_cursor(self):
        if not self.following or not self.popup:
            return

        mx, my = pyautogui.position()
        target_x = mx + 15
        target_y = my + 25

        if self.cur_x is None:
            self.cur_x = target_x
        if self.cur_y is None:
            self.cur_y = target_y

        self.cur_x += (target_x - self.cur_x) * self.ease
        self.cur_y += (target_y - self.cur_y) * self.ease

        self.popup.geometry(
            f"{self.width}x{self.height}+{int(self.cur_x)}+{int(self.cur_y)}"
        )

        self.popup.after(16, self.follow_cursor)

    # ------------------------------------
    def kill_and_close(self, event=None):
        translator.stop()
        self.following = False
        self.fade_out()

    def close(self):
        if self.popup:
            self.popup.destroy()
            self.popup = None
            self.text_buffer = ""

    def mark_finished(self):
        self.finished = True
        self.following = True
        self.popup.after(3000, self.fade_out)


# ==============================
# global click listener
# ==============================
popup_window: PopupWindow | None = None


def start_global_left_click_listener():
    def on_click(x, y, button, pressed):
        from pynput.mouse import Button
        if button == Button.left and pressed:
            if popup_window:
                popup_window.kill_and_close()

    listener = mouse.Listener(on_click=on_click)
    listener.daemon = True
    listener.start()


# ==============================
# DeepSeek callback
# ==============================
def on_start():
    popup_queue.put(("open", None))


def on_chunk(chunk):
    popup_queue.put(("chunk", chunk))


def on_finish():
    popup_queue.put(("finish", None))


# ==============================
# hotkey callback
# ==============================
def on_hotkey():
    text = pyperclip.paste().strip()
    if not text:
        return

    translator.translate_async(text, on_start, on_chunk, on_finish)


# ==============================
# Tk queue processor
# ==============================
def process_queue(root, font_main):
    global popup_window
    try:
        while True:
            msg, data = popup_queue.get_nowait()

            if msg == "open":
                popup_window = PopupWindow(root, font_main)
                popup_window.open()

            elif msg == "chunk":
                if popup_window:
                    popup_window.update_text(data)

            elif msg == "finish":
                if popup_window:
                    popup_window.mark_finished()

    except queue.Empty:
        pass

    root.after(30, lambda: process_queue(root, font_main))


# ==============================
# MAIN
# ==============================
def main():
    root = tk.Tk()
    root.update()

    font_main = choose_font(root)

    root.withdraw()

    print(">>> -Ctrl+X- to translate (from clipboard)")
    print(">>> left click popup to cancel streaming")

    start_global_left_click_listener()
    keyboard.add_hotkey("ctrl+x", lambda: on_hotkey())

    process_queue(root, font_main)
    root.mainloop()


if __name__ == "__main__":
    main()
