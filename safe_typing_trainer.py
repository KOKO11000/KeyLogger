#!/usr/bin/env python3
# -*- coding: utf-8 -*-
\"\"\"
CYBER LOGGER — SAFE TYPING TRAINER (LOCAL)
-----------------------------------------
אפליקציית פייתון מקומית לאימון הקלדה:
• מודדת ומציגה WPM, כמות מילים/תווים, וספירת Backspace.
• "רווח" מתחייב מילה (מוסיפה לרשימת מילים). "אנטר" מוריד שורה ומתחייב מילה אם יש.
• כל ההאזנה נעשית רק בתוך חלון האפליקציה (Tkinter). אין האזנה מערכתית ואין שליחה לרשת.

הרצה:
    python safe_typing_trainer.py

שימוש:
- לחצו Start כדי להתחיל למדוד, Stop לעצור. Clear לאיפוס.
- הקלידו בתוך תיבת הטקסט. אפשר לשמור קבצים:
  • Save TXT — שמירת המילים שהתחייבו (מופרדות ברווחים).
  • Save NDJSON — שמירת אירועים כ-NDJSON (שורה לכל אירוע).
\"\"\"
import json
import time
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class TypingTrainer:
    def __init__(self, root: tk.Tk):
        self.root = root
        root.title("Safe Typing Trainer — Local (לא זדוני)")
        root.geometry("900x600")
        root.configure(bg=\"#0b1220\")
        style = ttk.Style()
        style.theme_use(\"clam\")
        style.configure(\"TFrame\", background=\"#0b1220\")
        style.configure(\"TLabel\", background=\"#0b1220\", foreground=\"#e6f1ff\")
        style.configure(\"TButton\", background=\"#121a2e\", foreground=\"#dbe9ff\", borderwidth=0)
        style.map(\"TButton\", background=[(\"active\", \"#16223a\")])
        style.configure(\"Accent.TButton\", background=\"#35f0b2\", foreground=\"#061019\", font=(\"Segoe UI\", 10, \"bold\"))
        style.map(\"Accent.TButton\", background=[(\"active\", \"#2fd4a0\")])

        self.recording = False
        self.started_at = None
        self.chars = 0
        self.bksp = 0
        self.words = []
        self.current_word = \"\"
        self.events = []  # list of dicts

        self._build_ui()
        self._schedule_wpm_tick()

    def _build_ui(self):
        top = ttk.Frame(self.root)
        top.pack(fill=\"x\", padx=16, pady=12)

        title = ttk.Label(top, text=\"מצב אימון בטוח בתוך האפליקציה\", font=(\"Segoe UI\", 16, \"bold\"))
        title.pack(anchor=\"w\")
        sub = ttk.Label(top, text=\"אין האזנה מחוץ לחלון הזה • אין שליחה לרשת • רווח מתחייב מילה • אנטר יוריד שורה\", foreground=\"#8aa0b7\")
        sub.pack(anchor=\"w\", pady=(4,0))

        bar = ttk.Frame(self.root)
        bar.pack(fill=\"x\", padx=16, pady=(6,10))
        self.btn_start = ttk.Button(bar, text=\"Start\", style=\"Accent.TButton\", command=self.start)
        self.btn_stop  = ttk.Button(bar, text=\"Stop\", command=self.stop, state=\"disabled\")
        self.btn_clear = ttk.Button(bar, text=\"Clear\", command=self.clear, state=\"disabled\")
        self.btn_save_txt = ttk.Button(bar, text=\"Save TXT\", command=self.save_txt, state=\"disabled\")
        self.btn_save_json = ttk.Button(bar, text=\"Save NDJSON\", command=self.save_json, state=\"disabled\")

        for w in (self.btn_start, self.btn_stop, self.btn_clear, self.btn_save_txt, self.btn_save_json):
            w.pack(side=\"right\", padx=6)

        main = ttk.Frame(self.root)
        main.pack(fill=\"both\", expand=True, padx=16, pady=6)

        left = ttk.Frame(main)
        left.pack(side=\"right\", fill=\"both\", expand=True)
        right = ttk.Frame(main)
        right.pack(side=\"left\", fill=\"y\", padx=(0,10))

        # Metrics
        metrics = ttk.Frame(right)
        metrics.pack(fill=\"x\", pady=(0,10))
        self.lbl_wpm_v = ttk.Label(metrics, text=\"0\", font=(\"Segoe UI\", 18, \"bold\"))
        self._metric_block(metrics, \"WPM\", self.lbl_wpm_v).pack(fill=\"x\", pady=4)
        self.lbl_words_v = ttk.Label(metrics, text=\"0\", font=(\"Segoe UI\", 18, \"bold\"))
        self._metric_block(metrics, \"מילים\", self.lbl_words_v).pack(fill=\"x\", pady=4)
        self.lbl_chars_v = ttk.Label(metrics, text=\"0\", font=(\"Segoe UI\", 18, \"bold\"))
        self._metric_block(metrics, \"תווים\", self.lbl_chars_v).pack(fill=\"x\", pady=4)
        self.lbl_bksp_v = ttk.Label(metrics, text=\"0\", font=(\"Segoe UI\", 18, \"bold\"))
        self._metric_block(metrics, \"Backspace\", self.lbl_bksp_v).pack(fill=\"x\", pady=4)

        # Tokens list
        ttk.Label(right, text=\"מילים שהתחייבו\", foreground=\"#8aa0b7\").pack(anchor=\"w\", pady=(6,2))
        self.tokens = tk.Listbox(right, bg=\"#0a1020\", fg=\"#aef7e3\", bd=0, highlightthickness=0,
                                 selectbackground=\"#163b33\", selectforeground=\"#e1fff6\")
        self.tokens.pack(fill=\"both\", expand=True)

        # Text area
        ttk.Label(left, text=\"הקלד/י כאן (רק כאן נמדד):\", foreground=\"#8aa0b7\").pack(anchor=\"w\", pady=(0,4))
        self.text = tk.Text(left, bg=\"#0a1020\", fg=\"#e6f1ff\", insertbackground=\"#35f0b2\",
                            bd=0, highlightthickness=1, highlightbackground=\"#22314e\",
                            wrap=\"word\", font=(\"Segoe UI\", 11))
        self.text.pack(fill=\"both\", expand=True)
        self.text.bind(\"<Key>\", self.on_key)

        # Footer
        foot = ttk.Frame(self.root)
        foot.pack(fill=\"x\", padx=16, pady=8)
        ttk.Label(foot, text=\"© אימון מקומי ולא זדוני — הנתונים נשמרים לוקאלית אצלך\").pack(anchor=\"center\")

    def _metric_block(self, parent, label, value_widget):
        frame = ttk.Frame(parent)
        row1 = ttk.Frame(frame); row1.pack(fill=\"x\")
        ttk.Label(row1, text=label).pack(side=\"right\")
        value_widget.pack(side=\"left\")
        return frame

    # Controls
    def start(self):
        self.recording = True
        if self.started_at is None:
            self.started_at = time.perf_counter()
        self.btn_start.config(state=\"disabled\")
        self.btn_stop.config(state=\"normal\")
        self.btn_clear.config(state=\"normal\")
        self.text.focus_set()

    def stop(self):
        self.recording = False
        self.btn_start.config(state=\"normal\")
        self.btn_stop.config(state=\"disabled\")
        # still allow clear/save

    def clear(self):
        self.stop()
        self.started_at = None
        self.chars = 0
        self.bksp = 0
        self.words.clear()
        self.current_word = \"\"
        self.events.clear()
        self.tokens.delete(0, tk.END)
        self.text.delete(\"1.0\", tk.END)
        self._refresh_metrics()
        self.btn_clear.config(state=\"disabled\")
        self.btn_save_txt.config(state=\"disabled\")
        self.btn_save_json.config(state=\"disabled\")

    def _refresh_metrics(self):
        self.lbl_words_v.config(text=str(len(self.words)))
        self.lbl_chars_v.config(text=str(self.chars))
        self.lbl_bksp_v.config(text=str(self.bksp))
        # WPM updated in tick()

    def _schedule_wpm_tick(self):
        self._update_wpm()
        self.root.after(300, self._schedule_wpm_tick)

    def _update_wpm(self):
        if self.recording and self.started_at:
            minutes = max(1e-9, (time.perf_counter() - self.started_at) / 60.0)
            wpm = int(round(len(self.words) / minutes))
            self.lbl_wpm_v.config(text=str(wpm))

    # Logic
    def on_key(self, event: tk.Event):
        if not self.recording:
            return  # ignore all keys unless recording is on

        ts = int(time.time() * 1000)
        key = event.keysym

        if key == \"BackSpace\":
            self.bksp += 1
            if self.current_word:
                self.current_word = self.current_word[:-1]
            self.events.append({\"ts\": ts, \"type\": \"bksp\"})
            self._refresh_metrics()
            return  # let Text handle visual deletion

        if key == \"Return\":
            # commit last word, then let Text insert newline
            self._commit_word_if_any(ts)
            self.events.append({\"ts\": ts, \"type\": \"enter\"})
            self._refresh_metrics()
            return

        if key == \"space\":
            # commit word and allow a single space in Text
            self._commit_word_if_any(ts)
            self.events.append({\"ts\": ts, \"type\": \"space\"})
            self._refresh_metrics()
            return  # let Text add the space

        # Regular printable character
        ch = event.char
        if ch and len(ch) == 1 and ch.isprintable():
            self.current_word += ch
            self.chars += 1
            self.events.append({\"ts\": ts, \"type\": \"char\", \"ch\": ch})
            self._refresh_metrics()
            return
        # else: ignore control keys

    def _commit_word_if_any(self, ts: int):
        if self.current_word:
            self.words.append(self.current_word)
            self.tokens.insert(tk.END, self.current_word)
            self.current_word = \"\"
            self.btn_save_txt.config(state=\"normal\")
            self.btn_save_json.config(state=\"normal\")

    # Save files
    def save_txt(self):
        if not self.words:
            messagebox.showinfo(\"Nothing to save\", \"אין מילים לשמירה.\")
            return
        path = filedialog.asksaveasfilename(defaultextension=\".txt\", filetypes=[(\"Text\",\"*.txt\")], initialfile=\"trainer_words.txt\")
        if not path:
            return
        with open(path, \"w\", encoding=\"utf-8\") as f:
            f.write(\" \".join(self.words) + \"\\n\")
        messagebox.showinfo(\"Saved\", f\"נשמר בהצלחה:\\n{path}\")

    def save_json(self):
        if not self.events:
            messagebox.showinfo(\"Nothing to save\", \"אין אירועים לשמירה.\")
            return
        path = filedialog.asksaveasfilename(defaultextension=\".ndjson\", filetypes=[(\"NDJSON\",\"*.ndjson\"),(\"JSON\",\"*.json\"),(\"All\",\"*.*\")], initialfile=\"trainer_events.ndjson\")
        if not path:
            return
        with open(path, \"w\", encoding=\"utf-8\") as f:
            for ev in self.events:
                f.write(json.dumps(ev, ensure_ascii=False) + \"\\n\")
        messagebox.showinfo(\"Saved\", f\"נשמר בהצלחה:\\n{path}\")


if __name__ == \"__main__\":
    root = tk.Tk()
    app = TypingTrainer(root)
    root.mainloop()
