import random
import math
import tkinter as tk

# ── Word list ─────────────────────────────────────────────────────────────────
WORDS = [
    "python", "hangman", "computer", "keyboard", "monitor",
    "elephant", "umbrella", "mountain", "internet", "developer",
    "algorithm", "database", "variable", "function", "library"
]

# ── Colour palette ────────────────────────────────────────────────────────────
BG = "#0d1117"
PANEL = "#161b22"
BORDER = "#30363d"
ACCENT = "#f85149"
CORRECT = "#56d364"
WRONG = "#f85149"
HINT = "#8b949e"
TITLEFG = "#e6edf3"

BTN_BG = "#ff8c00"
BTN_HOV = "#ffa833"
BTN_PRS = "#cc7000"
BTN_FG = "#000000"
BTN_OK = "#1f4a2e"
BTN_BAD = "#3d1a1a"

MAX_WRONG = 6


# ── Round button ──────────────────────────────────────────────────────────────
class RoundButton(object):
    W = 38
    H = 34
    R = 10

    def __init__(self, parent, text, command):
        self._command = command
        self._enabled = True
        self._bg = BTN_BG
        self._fg = BTN_FG
        self._text = text

        self.cv = tk.Canvas(parent,
                            width = self.W, height = self.H,
                            bg = parent.cget("bg"),
                            highlightthickness = 0)
        self._draw(self._bg, self._fg)

        self.cv.bind("<Enter>", self._enter)
        self.cv.bind("<Leave>", self._leave)
        self.cv.bind("<ButtonPress-1>", self._press)
        self.cv.bind("<ButtonRelease-1>", self._release)

    def pack(self, **kw):
        self.cv.pack(**kw)

    def _rounded_rect_points(self, x1, y1, x2, y2, r, steps=12):
        pts = []
        corners = [
            (x1 + r, y1 + r, 180), 
            (x2 - r, y1 + r,  90),  
            (x2 - r, y2 - r,   0), 
            (x1 + r, y2 - r, 270), 
        ]
        for cx, cy, start_deg in corners:
            for i in range(steps + 1):
                angle = math.radians(start_deg - i * 90.0 / steps)
                pts.append(cx + r * math.cos(angle))
                pts.append(cy - r * math.sin(angle))
        return pts

    def _draw(self, bg, fg):
        c = self.cv
        c.delete("all")
        pts = self._rounded_rect_points(2, 2, self.W - 2, self.H - 2, self.R)
        c.create_polygon(pts, fill = bg, outline = bg, smooth = False)
        c.create_text(self.W // 2, self.H // 2,
                      text=self._text, fill=fg,
                      font=("Courier", 10, "bold"))

    def _enter(self, _=None):
        if self._enabled:
            self._draw(BTN_HOV, self._fg)

    def _leave(self, _=None):
        if self._enabled:
            self._draw(self._bg, self._fg)

    def _press(self, _=None):
        if self._enabled:
            self._draw(BTN_PRS, self._fg)

    def _release(self, _=None):
        if self._enabled:
            self._draw(self._bg, self._fg)
            self._command()

    def disable(self, bg, fg):
        self._enabled = False
        self._bg = bg
        self._fg = fg
        self.cv.configure(cursor = "")
        self._draw(bg, fg)

    def reset(self):
        self._enabled = True
        self._bg = BTN_BG
        self._fg = BTN_FG
        self.cv.configure(cursor = "arrow")
        self._draw(self._bg, self._fg)


# ── App ───────────────────────────────────────────────────────────────────────
class HangmanApp(object):
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.root.configure(bg = BG)
        self.root.resizable(True, True)
        self.root.minsize(560, 580)
        self.wins = 0
        self.losses  = 0
        self.word = ""
        self.guessed = set()
        self.wrong = 0
        self.buttons = {}
        self._build_ui()
        self._new_game()

    def _build_ui(self):
        # Title
        bar = tk.Frame(self.root, bg = BG)
        bar.pack(fill = "x", padx = 22, pady = (20, 4))
        tk.Label(bar, text = "HANGMAN", font = ("Courier", 20, "bold"),
                 bg = BG, fg = TITLEFG).pack(side = "left")
        self.score_var = tk.StringVar(value = "Wins: 0   Losses: 0")
        tk.Label(bar, textvariable = self.score_var,
                 font = ("Courier", 10), bg = BG, fg = HINT).pack(side = "right")

        sep(self.root)

        # Middle row
        mid = tk.Frame(self.root, bg = BG)
        mid.pack(padx = 22, pady = 10, fill = "x", expand = True)

        gal = tk.Frame(mid, bg = PANEL, padx = 6, pady = 6)
        gal.pack(side = "left", anchor = "n", padx = (0, 14))
        self.canvas = tk.Canvas(gal, width = 220, height = 240,
                                bg = PANEL, highlightthickness = 0)
        self.canvas.pack()

        info = tk.Frame(mid, bg = BG)
        info.pack(side = "left", anchor = "n", fill = "x", expand = True)

        wc = card(info)
        wc.pack(fill = "x", pady = (0, 8))
        tk.Label(wc, text = "WORD", font = ("Courier", 9, "bold"),
                 bg = PANEL, fg = HINT).pack(anchor = "w")
        self.word_var = tk.StringVar()
        tk.Label(wc, textvariable = self.word_var,
                 font = ("Courier", 22, "bold"), bg = PANEL, fg = CORRECT,
                 anchor = "w", wraplength = 320).pack(anchor = "w", fill = "x")

        lc = card(info)
        lc.pack(fill = "x", pady = (0, 8))
        tk.Label(lc, text = "LIVES", font = ("Courier", 9, "bold"),
                 bg = PANEL, fg = HINT).pack(anchor = "w")
        self.lives_var = tk.StringVar()
        tk.Label(lc, textvariable = self.lives_var,
                 font = ("Courier", 15), bg = PANEL, fg = CORRECT).pack(anchor = "w")

        mc = card(info)
        mc.pack(fill = "x")
        tk.Label(mc, text = "WRONG GUESSES", font = ("Courier", 9, "bold"),
                 bg = PANEL, fg = HINT).pack(anchor = "w")
        self.missed_var = tk.StringVar()
        tk.Label(mc, textvariable = self.missed_var,
                 font = ("Courier", 12), bg = PANEL, fg = WRONG,
                 width = 14, wraplength = 158, anchor = "w").pack(anchor = "w")

        sep(self.root)

        # Keyboard
        kb = tk.Frame(self.root, bg = BG)
        kb.pack(pady = 8)
        for row_str in ("QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"):
            row = tk.Frame(kb, bg = BG)
            row.pack(pady = 3)
            for ch in row_str:
                btn = RoundButton(row, ch, command = lambda c = ch: self._guess(c))
                btn.pack(side = "left", padx = 3)
                self.buttons[ch] = btn

        sep(self.root)

        tk.Button(self.root, text = "NEW GAME",
                  font = ("Courier", 11, "bold"),
                  bg = BTN_BG, fg = BTN_FG,
                  activebackground = BTN_HOV, activeforeground = BTN_FG,
                  relief = "flat", cursor = "arrow", padx = 20, pady = 8,
                  command = self._new_game).pack(pady = (6, 18))

    def _new_game(self):
        self.word = random.choice(WORDS)
        self.guessed = set()
        self.wrong   = 0
        self.score_var.set("Wins: {}   Losses: {}".format(self.wins, self.losses))
        self._refresh()
        for btn in self.buttons.values():
            btn.reset()

    def _guess(self, letter):
        letter = letter.lower()
        if letter in self.guessed:
            return
        self.guessed.add(letter)
        btn = self.buttons[letter.upper()]
        if letter in self.word:
            btn.disable(bg = BTN_OK, fg = CORRECT)
        else:
            self.wrong += 1
            btn.disable(bg = BTN_BAD, fg = WRONG)
        self._refresh()
        self._check_end()

    def _refresh(self):
        display = "  ".join(c if c in self.guessed else "_" for c in self.word)
        self.word_var.set(display)
        rem = MAX_WRONG - self.wrong
        self.lives_var.set("♥ " * rem + "♡ " * self.wrong)
        missed = sorted(c.upper() for c in self.guessed if c not in self.word)
        self.missed_var.set("  ".join(missed) if missed else "—")
        self._draw_gallows(self.wrong)

    def _check_end(self):
        if all(c in self.guessed for c in self.word):
            self.wins += 1
            self._popup("win")
        elif self.wrong >= MAX_WRONG:
            self.losses += 1
            self._popup("loss")

    def _draw_gallows(self, stage):
        c = self.canvas
        c.delete("all")
        c.create_line(15, 225, 205, 225, fill = BORDER, width = 3, capstyle = "round")
        c.create_line(55, 225, 55, 18, fill = BORDER, width = 4, capstyle = "round")
        c.create_line(55, 18, 148, 18, fill = BORDER, width = 4, capstyle = "round")
        c.create_line(148, 18, 148, 50, fill = BORDER, width = 4, capstyle = "round")
        c.create_line(55, 55, 88, 18, fill = BORDER, width = 3)
        if stage >= 1:
            c.create_oval(130, 50, 166, 86, outline = ACCENT, fill = "#2d1515", width = 3)
        if stage >= 2:
            c.create_line(148, 86,  148, 150, fill = ACCENT, width = 3, capstyle = "round")
        if stage >= 3:
            c.create_line(148, 103, 118, 133, fill = ACCENT, width = 3, capstyle = "round")
        if stage >= 4:
            c.create_line(148, 103, 178, 133, fill = ACCENT, width = 3, capstyle = "round")
        if stage >= 5:
            c.create_line(148, 150, 118, 188, fill = ACCENT, width = 3, capstyle = "round")
        if stage >= 6:
            c.create_line(148, 150, 178, 188, fill = ACCENT, width = 3, capstyle = "round")
            c.create_text(141, 63, text = "X", fill = ACCENT, font = ("Courier", 9, "bold"))
            c.create_text(157, 63, text = "X", fill = ACCENT, font = ("Courier", 9, "bold"))
            c.create_arc(136, 72, 160, 86, start = 200, extent = 140,
                         outline = ACCENT, width = 2, style = "arc")

    def _popup(self, outcome):
        ov = tk.Toplevel(self.root)
        ov.overrideredirect(True)
        ov.configure(bg = PANEL)
        self.root.update_idletasks()
        rx = self.root.winfo_x()
        ry = self.root.winfo_y()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        ov.geometry("300x185+{}+{}".format(rx + rw // 2 - 150, ry + rh // 2 - 92))
        color = CORRECT if outcome == "win" else ACCENT
        msg = "YOU WIN!" if outcome == "win" else "GAME OVER"
        face = "^__^" if outcome == "win" else "x__x"
        tk.Frame(ov, height = 3, bg = color).pack(fill = "x")
        body = tk.Frame(ov, bg = PANEL)
        body.pack(fill = "both", expand = True, padx = 2, pady = (0, 2))
        tk.Label(body, text = face, font = ("Courier", 20, "bold"),
                 bg = PANEL, fg = color).pack(pady = (14, 2))
        tk.Label(body, text = msg, font = ("Courier", 15, "bold"),
                 bg = PANEL, fg = color).pack()
        tk.Label(body, text = "The word was:  " + self.word.upper(),
                 font = ("Courier", 11), bg = PANEL, fg = HINT).pack(pady = 5)
        def play_again():
            ov.destroy()
            self._new_game()
        tk.Button(body, text = "PLAY AGAIN",
                  font = ("Courier", 10, "bold"),
                  bg = BTN_BG, fg = BTN_FG,
                  activebackground = BTN_HOV, activeforeground = BTN_FG,
                  relief = "flat", cursor = "arrow", padx = 16, pady = 6,
                  command = play_again).pack(pady = (2, 14))


# ── helpers ───────────────────────────────────────────────────────────────────
def sep(parent):
    tk.Frame(parent, height = 1, bg = BORDER).pack(fill = "x", padx = 22, pady = 4)

def card(parent):
    return tk.Frame(parent, bg = PANEL, padx = 12, pady = 10)


# ── run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    HangmanApp(root)
    root.mainloop()
