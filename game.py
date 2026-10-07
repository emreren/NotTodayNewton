# NOT TODAY, NEWTON
# Newton is sitting under an apple tree. If an apple lands on his head, he will discover gravity!
# Move the basket one square left or right with the arrow keys and catch the apples.
# Miss 3 apples and the game is over.
# To play:  pgzrun game.py  or  python3 game.py

import pgzrun  # Pygame Zero: ready-made names like Actor and screen come from here
import random  # for picking random numbers

# ---------- SETTINGS ----------
TITLE = "Not Today, Newton"
WIDTH = 600          # width of the window: 12 squares
HEIGHT = 500         # height of the window: 10 squares
CELL = 50            # the size of one square
WAIT = 30            # every how many steps the apples fall one square (60 steps a second)
APPLE_EVERY = 180    # every how many steps a new apple comes (180 steps = 3 seconds)

# ---------- THINGS IN THE GAME ----------
# An Actor is a thing with a picture; it takes its picture from the images folder.
# Careful: y gets bigger as you go down the screen. The top is 0, the bottom is 500.
basket = Actor("basket", midbottom=(275, HEIGHT))  # in the bottom row, column 6
apples = []        # all the apples on the screen
score = 0
lives = 3
game_over = False
counter = 0        # step counter for making the apples fall
apple_counter = 0  # step counter for new apples


def new_apple():
    # Pick a random column and put the apple in its middle, just above the screen
    column = random.randint(0, 11)
    apple = Actor("apple", (column * CELL + 25, -25))
    apples.append(apple)


def draw_grid():
    # Draw numbered squares in the background. Row numbers grow downward, just like y.
    for column in range(12):
        x = column * CELL
        screen.draw.line((x, 0), (x, HEIGHT), (205, 235, 250))
        screen.draw.text(str(column + 1), center=(x + 25, HEIGHT - 12), fontsize=20)
    for row in range(10):
        y = row * CELL
        screen.draw.line((0, y), (WIDTH, y), (205, 235, 250))
        screen.draw.text(str(row + 1), center=(12, y + 12), fontsize=20)


def draw():
    # Pygame Zero calls this 60 times a second by itself and draws the screen again
    screen.fill((135, 206, 235))  # sky blue

    if game_over:
        screen.blit("newton", (240, 45))
        screen.draw.text("GAME OVER", center=(300, 205), fontsize=72)
        screen.draw.text("BONK! Newton discovered gravity.", center=(300, 255), fontsize=30)
        screen.draw.text(f"Score: {score}", center=(300, 300), fontsize=36)
        return

    draw_grid()
    basket.draw()
    for apple in apples:
        apple.draw()
    screen.draw.text(f"Score: {score}", topleft=(35, 10), fontsize=32)
    screen.draw.text(f"Lives: {lives}", topright=(590, 10), fontsize=32)


def update():
    # Pygame Zero calls this 60 times a second too. Let's call each call a "step".
    global score, lives, game_over, counter, apple_counter
    if game_over:
        return

    # Make a new apple every APPLE_EVERY steps
    apple_counter += 1
    if apple_counter == APPLE_EVERY:
        apple_counter = 0
        new_apple()

    # The apples don't fall every step, only every few steps.
    # Every 5 points we wait 5 steps less, so the apples get faster (but at least 15 steps).
    wait = WAIT - (score // 5) * 5
    if wait < 15:
        wait = 15
    counter += 1
    if counter < wait:
        return
    counter = 0

    # Move every apple one square down. apples[:] is a copy, because we remove apples in the loop.
    for apple in apples[:]:
        apple.y += CELL

        if basket.colliderect(apple):
            # IF the apple touched the basket: get 1 point
            score += 1
            apples.remove(apple)
        elif apple.top > HEIGHT:
            # OTHERWISE, IF the apple hit the ground: lose 1 life
            lives -= 1
            apples.remove(apple)

    if lives == 0:
        game_over = True


def on_key_down(key):
    # Each arrow key press moves the basket one square (without leaving the screen)
    if key == keys.LEFT and basket.left > 0:
        basket.x -= CELL
    if key == keys.RIGHT and basket.right < WIDTH:
        basket.x += CELL


pgzrun.go()  # start the game
