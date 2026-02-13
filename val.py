import turtle
import math
import random
import time
import threading
from playsound import playsound

# ------------------------
# Screen setup
# ------------------------
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("For You 💖")
screen.tracer(0)

t = turtle.Turtle()
t.hideturtle()
t.speed(0)

star_t = turtle.Turtle()
star_t.hideturtle()
star_t.speed(0)
star_t.color("white")

# ------------------------
# Music & sound
# ------------------------
def play_music():
    try:
        playsound(r"C:\Users\marja\CODE\val\music.mp3", block=True)
    except Exception as e:
        print("Music error:", e)

def play_click():
    try:
        playsound(r"C:\Users\marja\CODE\val\click.mp3", block=False)
    except Exception as e:
        print("Click sound error:", e)
        
music_thread = threading.Thread(target=play_music, daemon=True)
music_thread.start()

# ------------------------
# Messages (cycle on click)
# ------------------------
messages = [
    ("Te extraño. 💗", "Always here for you"),
    ("Te quiero mucho, amigo.", "You matter to me"),
    ("Siempre estoy aquí para ti.", "No matter what"),
    ("Gracias por existir.", "✨")
]

message_index = 0
show_message = False
fade_alpha = 0.0

# ------------------------
# Stars
# ------------------------
stars = []
for _ in range(120):
    stars.append((random.randint(-380, 380), random.randint(-280, 280), random.randint(1, 3)))

def draw_stars():
    star_t.clear()
    for x, y, size in stars:
        star_t.penup()
        star_t.goto(x, y)
        star_t.pendown()
        star_t.dot(size)

# ------------------------
# Heart math
# ------------------------
def heart_point(angle, scale):
    x = scale * 16 * math.sin(angle) ** 3
    y = scale * (
        13 * math.cos(angle)
        - 5 * math.cos(2 * angle)
        - 2 * math.cos(3 * angle)
        - math.cos(4 * angle)
    )
    return x, y

def draw_heart(scale, color, pen_size=2):
    t.color(color)
    t.width(pen_size)
    t.begin_fill()
    for i in range(361):
        a = math.radians(i)
        x, y = heart_point(a, scale)
        t.goto(x, y)
    t.end_fill()

# ------------------------
# Mini hearts
# ------------------------
mini_hearts = []
for _ in range(10):
    mini_hearts.append({
        "x": random.randint(-300, 300),
        "y": random.randint(-300, -150),
        "speed": random.uniform(0.6, 1.5),
        "size": random.uniform(0.4, 0.7)
    })

def draw_mini_heart(x, y, scale, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for i in range(361):
        a = math.radians(i)
        hx, hy = heart_point(a, scale)
        t.goto(x + hx, y + hy)
    t.end_fill()

# ------------------------
# Click detection (inside heart)
# ------------------------
def is_inside_heart(x, y, scale):
    nx = x / scale
    ny = (y + 10) / scale
    return (nx**2 + (ny - abs(nx)**(2/3))**2) <= 1

def on_click(x, y):
    global show_message, message_index, fade_alpha
    if is_inside_heart(x, y, current_scale):
        show_message = True
        fade_alpha = 0.0
        message_index = (message_index + 1) % len(messages)
        play_click()

screen.onclick(on_click)

# ------------------------
# Text (fade in)
# ------------------------
def draw_text():
    global fade_alpha
    if not show_message:
        return

    fade_alpha = min(fade_alpha + 0.05, 1)

    r = int(255 * fade_alpha)
    g = int(179 * fade_alpha)
    b = int(198 * fade_alpha)
    color = (r/255, g/255, b/255)

    t.penup()
    t.goto(0, 0)
    t.color(color)
    t.write(messages[message_index][0], align="center", font=("Arial", 26, "bold"))

    t.goto(0, -35)
    t.color(color)
    t.write(messages[message_index][1], align="center", font=("Arial", 14, "normal"))

# ------------------------
# Animation loop
# ------------------------
pulse = 0
direction = 1
current_scale = 14

while True:
    t.clear()
    draw_stars()

    pulse += 0.08 * direction
    if pulse > 1.2:
        direction = -1
    if pulse < -1.2:
        direction = 1

    current_scale = 14 + pulse

    # Glow
    for s in range(20, 15, -1):
        t.penup()
        t.goto(0, -10)
        t.pendown()
        draw_heart(s, "#2b0000", 2)

    # Main heart
    t.penup()
    t.goto(0, -10)
    t.pendown()
    draw_heart(current_scale, "#ff1a1a", 3)

    # Mini hearts
    for h in mini_hearts:
        h["y"] += h["speed"]
        if h["y"] > 300:
            h["y"] = random.randint(-300, -150)
            h["x"] = random.randint(-300, 300)
        draw_mini_heart(h["x"], h["y"], h["size"], "#ff4d6d")

    draw_text()

    screen.update()
    time.sleep(0.01)