# backend.py
import requests
import json
import threading


class DeepSeekTranslator:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.stop_flag = False
        self.thread = None

        self.API_URL = "https://api.deepseek.com/chat/completions"
        #↓  You can freely customize the prompt.The default prompt is automatically converted into Japanese.
        self.PROMPT = """
                        あなたは高精度忠実でな翻訳システムです。
                        文脈も日本語にのネイティブの会話に沿って翻訳してください。
                        様々な言語にから日本語に翻訳してください。」
                        以下の文書をネイティブで読みやすい日本語に翻訳してください。
                        元の文書の改行や強調などはできるだけ見やすくしてください
                        翻訳結果だけを書いてください。（説明禁止）

                        翻訳対象：

                    """

    def stop(self):
        """Streamingを中断"""
        self.stop_flag = True

    def translate_stream(self, text, on_start, on_chunk, on_finish):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "system", "content": self.PROMPT},
                {"role": "user", "content": text},
            ],
            "stream": True,
        }

        self.stop_flag = False

        if on_start:
            on_start()

        try:
            with requests.post(self.API_URL, json=payload, headers=headers, stream=True) as r:
                for line in r.iter_lines(decode_unicode=True):
                    if self.stop_flag:
                        break

                    if not line or not line.startswith("data: "):
                        continue
                    if line.strip() == "data: [DONE]":
                        break

                    try:
                        data = json.loads(line.replace("data: ", ""))
                        delta = data["choices"][0]["delta"]
                        if "content" in delta:
                            on_chunk(delta["content"])
                    except:
                        pass

        finally:
            if on_finish:
                on_finish()

    def translate_async(self, text, on_start, on_chunk, on_finish):
        self.thread = threading.Thread(
            target=self.translate_stream,
            args=(text, on_start, on_chunk, on_finish),
            daemon=True,
        )
        self.thread.start()
