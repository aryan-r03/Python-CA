import random
import re
from datetime import datetime

RESPONSES = {
    r"hello|hi|hey|howdy|hiya": [
        "Hey there! How can I help you?",
        "Hello! What's on your mind?",
        "Hi! Great to see you.",
    ],
    r"good morning": [
        "Good morning! Hope your day is going great!",
        "Morning! Ready to conquer the day?",
    ],
    r"good night|goodbye|bye|see you|take care": [
        "Goodbye! Have a wonderful day!",
        "See you later! Take care.",
        "Bye! It was nice chatting with you.",
    ],
    r"how are you|how r u|how do you do|you ok": [
        "I'm doing great, thanks for asking! How about you?",
        "Running smoothly! What about you?",
        "All good on my end. How can I help?",
    ],
    r"what is your name|who are you|your name": [
        "I'm PyBot - your friendly terminal chatbot!",
        "Call me PyBot. Nice to meet you!",
    ],
    r"how old are you|your age": [
        "I was born the moment you ran this script!",
        "Age is just a number - I'm timeless.",
    ],
    r"what time is it|current time|tell me the time": [
        f"The current time is {datetime.now().strftime('%H:%M:%S')}.",
    ],
    r"what.*date|today.*date|what day": [
        f"Today is {datetime.now().strftime('%A, %d %B %Y')}.",
    ],
    r"weather|temperature|forecast": [
        "I wish I could check outside! I don't have internet access though.",
        "No idea - my weather sensor is broken. Try a weather app!",
    ],
    r"tell me a joke|joke|make me laugh|funny": [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "Why did the Python programmer wear glasses? Because he couldn't C#.",
        "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads.",
        "Why was the math book sad? It had too many problems.",
        "What do you call a fish without eyes? A fsh.",
    ],
    r"help|what can you do": [
        "I can chat, tell jokes, share the time/date, do math, and more!\n"
        "  Try: 'tell me a joke', 'what time is it', 'calculate 5 * 9'",
    ],
    r"you are (great|awesome|cool|amazing|smart|good)": [
        "Aw, thank you! You're pretty awesome yourself.",
        "That's very kind of you!",
        "You just made my circuits happy.",
    ],
    r"you (suck|are bad|are dumb|are stupid|are useless)": [
        "That's a bit harsh, but I'll try to do better!",
        "Ouch! I'm still learning. Let's move on.",
    ],
    r"python|programming|code|coding": [
        "Python is awesome! Clean syntax, great libraries.",
        "I'm literally made of Python code - so I'm a fan!",
        "Coding is fun. What are you building?",
    ],
    r"meaning of life|purpose of life|why are we here": [
        "42. - Douglas Adams",
        "To write great Python code, obviously.",
        "That's a big question. What do YOU think?",
    ],
    r"thank you|thanks|thx|ty": [
        "You're welcome!",
        "Happy to help!",
        "Anytime!",
    ],
}

FALLBACKS = [
    "Hmm, I'm not sure about that. Can you rephrase?",
    "Interesting! Tell me more.",
    "I don't have an answer for that one.",
    "That's beyond my knowledge. Try asking something else!",
    "Good question! I wish I knew.",
]

CYAN  = "\033[96m"
GREEN = "\033[92m"
RESET = "\033[0m"
BOLD  = "\033[1m"
DIM   = "\033[2m"


def try_math(text):
    expr = re.sub(r"[^0-9\+\-\*\/\(\)\.\s]", "", text).strip()
    if not expr or not any(c.isdigit() for c in expr):
        return None
    try:
        result = eval(expr, {"__builtins__": {}})
        return f"The answer is: {result}"
    except Exception:
        return None


def get_response(user_input):
    text = user_input.lower().strip()
    for pattern, replies in RESPONSES.items():
        if re.search(pattern, text):
            return random.choice(replies)
    math_result = try_math(text)
    if math_result:
        return math_result
    return random.choice(FALLBACKS)


def main():
    print(f"""
{CYAN}{BOLD}╔══════════════════════════════════════╗
║                PyBot                 ║
╚══════════════════════════════════════╝{RESET}
{DIM}Type a message and press Enter to chat.
Type 'quit' or 'bye' to exit.{RESET}
""")

    while True:
        try:
            user_input = input(f"{GREEN}{BOLD}You: {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{DIM}Goodbye!{RESET}")
            break

        if not user_input:
            continue

        if re.search(r"^(quit|exit|bye|q)$", user_input.lower()):
            print(f"{CYAN}{BOLD}Bot:{RESET} Goodbye! It was nice chatting with you.")
            break

        response = get_response(user_input)
        print(f"{CYAN}{BOLD}Bot:{RESET} {response}\n")


if __name__ == "__main__":
    main()