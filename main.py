import random, re, tkinter as tk
from datetime import datetime

RESPONSES = {
    r"hello|hi|hey": ["Hey there!", "Hello! How can I help?"],
    r"how are you": ["I'm great, thanks!", "Running smoothly!"],
    r"your name|who are you": ["I'm PyBot!", "Call me PyBot."],
    r"joke|funny": [
        "Why do programmers prefer dark mode? Light attracts bugs!",
        "Why did the Python dev wear glasses? He couldn't C#.",
    ],
    r"time": [lambda: f"It's {datetime.now().strftime('%H:%M:%S')}."],
    r"date|day": [lambda: f"Today is {datetime.now().strftime('%A, %d %B %Y')}."],
    r"bye|goodbye": ["Goodbye! Take care.", "See you later!"],
    r"thank": ["You're welcome!", "Happy to help!"],
    r"help": ["I can chat, tell jokes, do math, and share time/date!"],
    r"python": ["Python is awesome!", "I'm literally made of Python!"],
}

FALLBACKS = ["Hmm, not sure about that.", "Interesting! Tell me more.", "Try asking something else!"]

def get_response(text):
    t = text.lower()
    for pattern, replies in RESPONSES.items():
        if re.search(pattern, t):
            r = random.choice(replies)
            return r() if callable(r) else r
    try:
        expr = re.sub(r"[^0-9+\-*/().\s]", "", t).strip()
        if expr and any(c.isdigit() for c in expr):
            result = eval(expr, {'__builtins__': {}})
            return f"Answer: {result}"
    except (SyntaxError, ValueError, ZeroDivisionError, NameError, TypeError):
        return "Invalid math expression. Try something like: 2+2 or 10/5"
    return random.choice(FALLBACKS)

# GUI -- using tkinter
root = tk.Tk()
root.title("PyBot")
root.geometry("500x520")
root.configure(bg="#0e0f14")

chat = tk.Text(root, bg="#161720", fg="#e8e6ff", font=("Segoe UI", 11),
               relief="flat", state="disabled", wrap="word", padx=10, pady=10)
chat.pack(fill="both", expand=True, padx=10, pady=(10, 4))
chat.tag_config("bot",  foreground="#7c6dfa")
chat.tag_config("user", foreground="#a89aff")

def post(who, msg):
    chat.config(state="normal")
    tag = "bot" if who == "PyBot" else "user"
    chat.insert("end", f"{who}: ", tag)
    chat.insert("end", msg + "\n")
    chat.config(state="disabled")
    chat.see("end")

def send(event=None):
    text = entry.get().strip()
    if not text: return
    entry.delete(0, "end")
    post("You", text)
    root.after(300, lambda: post("PyBot", get_response(text)))

frame = tk.Frame(root, bg="#0e0f14")
frame.pack(fill="x", padx=10, pady=(0, 10))

entry = tk.Entry(frame, bg="#1e1f2e", fg="#e8e6ff", insertbackground="white",
                 font=("Segoe UI", 11), relief="flat")
entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 8))
entry.bind("<Return>", send)
entry.focus()

tk.Button(frame, text="Send", bg="#7c6dfa", fg="white", relief="flat",
          font=("Segoe UI", 10, "bold"), padx=12, command=send).pack(side="right")

post("PyBot", "Hi! I'm PyBot. Ask me anything or type a math expression!")
root.mainloop()
