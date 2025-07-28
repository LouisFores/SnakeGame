from tkinter import *
import random

# ===== Constants =====
GAME_WIDTH = 800
GAME_HEIGHT = 500
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BONUS_COLOR = "#FFD700"
OBSTACLE_COLORS = ["#5c4033", "#228B22", "#808080"]
BACKGROUND_COLOR = "#1e1e1e"

# ===== Game Variables =====
direction = 'down'
score = 0
history = []
bonus_fruit = None
bonus_active = False
obstacles = []
SPEED = 100


# ===== Classes =====
class Snake:
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = [[0, 0] for _ in range(BODY_PARTS)]
        self.squares = []
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                             fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


class Food:
    def __init__(self):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if [x, y] not in snake.coordinates and (x, y) not in obstacles:
                break
        self.coordinates = [x, y]
        self.shape = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                        fill=FOOD_COLOR, tag="food")


# ===== Game Logic =====
def next_turn(snake, food):
    global bonus_fruit, bonus_active, score

    x, y = snake.coordinates[0]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    new_head = [x, y]
    snake.coordinates.insert(0, new_head)

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE,
                                     fill=SNAKE_COLOR)
    snake.squares.insert(0, square)

    if new_head == food.coordinates:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete("food")
        food = Food()

        if score % 5 == 0 and score != 0 and not bonus_active:
            spawn_bonus_fruit()

    elif bonus_active and bonus_fruit and new_head == bonus_fruit:
        score += 3
        label.config(text=f"Score: {score}")
        canvas.delete("bonus")
        bonus_fruit = None
        bonus_active = False

    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        save_history()
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)


def change_direction(new_dir):
    global direction
    opposites = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}
    if direction != opposites.get(new_dir):
        direction = new_dir


def check_collision(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    if [x, y] in snake.coordinates[1:]:
        return True

    if (x, y) in obstacles:
        return True

    return False


def game_over():
    canvas.create_text(GAME_WIDTH // 2, GAME_HEIGHT // 2,
                       font=('consolas', 50), text="GAME OVER", fill="red")
    restart_btn.pack(pady=10)
    show_history()


def save_history():
    history.append({
        'score': score,
        'difficulty': difficulty_var.get()
    })


def show_history():
    text = "\n".join([f"Score: {h['score']} | Speed: {h['difficulty']}" for h in history[-5:]])
    history_label.config(text=f"Lịch sử gần nhất:\n{text}")


def start_game():
    global direction, score, SPEED, snake, food, bonus_fruit, bonus_active, obstacles

    canvas.delete(ALL)
    restart_btn.pack_forget()
    direction = 'down'
    score = 0
    label.config(text="Score: 0")
    SPEED = int(difficulty_var.get())
    bonus_fruit = None
    bonus_active = False
    obstacles = []

    generate_obstacles()

    snake = Snake()
    food = Food()

    next_turn(snake, food)


def generate_obstacles(count=10):
    for _ in range(count):
        while True:
            x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
            if (x, y) not in obstacles:
                break
        color = random.choice(OBSTACLE_COLORS)
        obstacles.append((x, y))
        canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=color, tag="obstacle")


def spawn_bonus_fruit():
    global bonus_fruit, bonus_active
    while True:
        x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE
        if [x, y] not in snake.coordinates and (x, y) not in obstacles:
            break
    bonus_fruit = [x, y]
    bonus_active = True
    canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=BONUS_COLOR, tag="bonus")
    window.after(3000, remove_bonus_fruit)


def remove_bonus_fruit():
    global bonus_fruit, bonus_active
    if bonus_active:
        canvas.delete("bonus")
        bonus_fruit = None
        bonus_active = False


# ===== GUI Setup =====
window = Tk()
window.title("🐍 Snake Game Pixie Edition")
window.resizable(False, False)

top_frame = Frame(window, bg="#222")
top_frame.pack(pady=10)

label = Label(top_frame, text="Score: 0", font=('consolas', 24), bg="#222", fg="white")
label.grid(row=0, column=0, padx=20)

difficulty_var = StringVar(value="100")
difficulty_menu = OptionMenu(top_frame, difficulty_var, "100", "50", "20")
difficulty_menu.config(font=('consolas', 14))
difficulty_menu.grid(row=0, column=1)

start_btn = Button(top_frame, text="Start", font=('consolas', 14), bg="#28a745", fg="white", command=start_game)
start_btn.grid(row=0, column=2, padx=10)

restart_btn = Button(top_frame, text="Chơi lại", font=('consolas', 14), bg="#007bff", fg="white", command=start_game)

history_label = Label(window, text="", font=('consolas', 12), justify=LEFT)
history_label.pack(pady=10)

canvas = Canvas(window, bg=BACKGROUND_COLOR, width=GAME_WIDTH, height=GAME_HEIGHT)
canvas.pack()

window.update()
win_width = window.winfo_width()
win_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width - win_width) / 2)
y = int((screen_height - win_height) / 2)
window.geometry(f"{win_width}x{win_height}+{x}+{y}")

# Key bindings: WASD
window.bind('<w>', lambda e: change_direction("up"))
window.bind('<a>', lambda e: change_direction("left"))
window.bind('<s>', lambda e: change_direction("down"))
window.bind('<d>', lambda e: change_direction("right"))

# Run app
window.mainloop()
