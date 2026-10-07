# ==================================================
#  NOT TODAY, NEWTON
#  Newton is sitting under an apple tree. If an apple lands
#  on his head, he will discover gravity. Not today!
#  Each time you press an arrow key, your basket moves one square left or right.
#  Catch the apples! Miss 3 apples and Newton discovers gravity: game over.
#
#  To play, run this command in the same folder:  pgzrun game.py
#
#  We never call draw, update or on_key_down ourselves.
#  Pygame Zero looks for these names and calls them for us.
#  That is why they must be spelled exactly like this.
# ==================================================

import random  # a ready-made tool for picking random numbers


# ---------- SETTINGS ----------
# Change these numbers to make the game easier or harder.

TITLE = "Not Today, Newton"  # the name at the top of the window
WIDTH = 600                  # width of the window: 12 squares
HEIGHT = 500                 # height of the window: 10 squares
CELL = 50                    # dots per square (apples and the basket move square by square)
WAIT = 30                    # steps between two apple moves (60 steps = 1 second)
APPLE_EVERY = 3              # a new apple falls every this many seconds
GRID = True                  # show the numbered grid (set to False to hide it)


# ---------- THINGS IN THE GAME ----------
# An Actor is a thing in the game that has a picture. It finds its picture
# in the "images" folder by its name: Actor("basket") → images/basket.png
# An Actor's x and y are the CENTER of its picture. It also has edges: left, right, top, bottom.
# Careful: numbers get BIGGER as you go DOWN the screen. The top is 0, the bottom is 500.

basket = Actor("basket", midbottom=(275, HEIGHT))  # at the bottom, in the middle of column 6
apples = []          # a list of all the apples on the screen (empty at the start)
score = 0            # how many apples you caught
lives = 3            # how many more apples you can miss
best_score = 0       # your best score so far
game_over = False    # is the game over? "No" (False) at the start
counter = 0          # counts the steps we wait before the apples fall


# ---------- NEW APPLE ----------

def new_apple():
    # Pick a random column and put the apple in its middle, just above the screen
    column = random.randint(0, WIDTH // CELL - 1)  # a column from 0 to 11
    x = column * CELL + CELL / 2                    # the middle of that column
    apple = Actor("apple", (x, -CELL / 2))          # start one square above the screen
    apples.append(apple)                            # add the new apple to the list


# ---------- NEW GAME ----------

def new_game():
    # Put everything back the way it was at the start
    global score, lives, game_over  # we are going to change these variables from above
    score = 0
    lives = 3
    game_over = False
    apples.clear()    # remove all apples from the list
    basket.x = 275    # put the basket back in column 6


# ---------- NUMBERED GRID ----------
# Draws a map in the background so you can see where an apple is on the screen.
# Each square is 50 dots: column 3 is x from 100 to 150, row 5 is y from 200 to 250.
# Row numbers are on the left, column numbers at the bottom (like a chessboard).

def draw_grid():
    line_color = (205, 235, 250)  # a light blue, a little brighter than the sky

    for column in range(WIDTH // CELL):  # 600 // 50 = 12 columns: 0, 1, 2, ... 11
        x = column * CELL                # the left edge of this column
        screen.draw.line((x, 0), (x, HEIGHT), line_color)  # a line going down
        # We started counting at 0, but we write the numbers starting at 1
        screen.draw.text(str(column + 1), center=(x + CELL / 2, HEIGHT - 12),
                         fontsize=20, color="white")

    for row in range(HEIGHT // CELL):  # 500 // 50 = 10 rows: 0, 1, 2, ... 9
        y = row * CELL                 # the top edge of this row
        screen.draw.line((0, y), (WIDTH, y), line_color)   # a line going across
        screen.draw.text(str(row + 1), center=(12, y + 12),
                         fontsize=20, color="white")


# ---------- DRAW THE SCREEN ----------
# Pygame Zero calls this function by itself 60 times every second.
# Colors are a mix of (red, green, blue); each one goes from 0 to 255.

def draw():
    screen.fill((135, 206, 235))  # paint everything sky blue
    if GRID and not game_over:
        draw_grid()               # while playing, draw the numbered grid in the background
    basket.draw()                 # draw the basket's picture

    for apple in apples:  # for every apple in the list...
        apple.draw()      # ...draw the apple's picture

    # Write the score at the top left (a little to the right of the row numbers)
    # and the lives at the top right
    screen.draw.text(f"Score: {score}", topleft=(35, 10), fontsize=32, color="white")
    screen.draw.text(f"Lives: {lives}", topright=(WIDTH - 10, 10), fontsize=32, color="white")

    # If the game is over, show Newton and write big letters in the middle
    if game_over:
        middle = WIDTH / 2
        screen.blit("newton", (middle - 60, 45))  # images/newton.png, 120 dots wide
        screen.draw.text("GAME OVER", center=(middle, 205), fontsize=72, color="white")
        screen.draw.text("BONK! Newton discovered gravity.",
                         center=(middle, 255), fontsize=30, color="white")
        screen.draw.text(f"Score: {score}    Best: {best_score}",
                         center=(middle, 300), fontsize=36, color="white")
        screen.draw.text("Press SPACE to play again",
                         center=(middle, 345), fontsize=28, color="white")


# ---------- MAKE THE APPLES FALL ----------
# Pygame Zero calls this function 60 times every second too, just before drawing the screen.
# Let's call each time it runs a "step".

def update():
    global score, lives, best_score, game_over, counter  # we are going to change these

    # If the game is over, stop here and don't move anything
    if game_over:
        return

    # We don't move the apples every step, only every few steps, so they fall square by square.
    # Every 5 points the wait gets shorter and the apples fall more often.
    # (// keeps only the whole part of a division: 12 // 5 = 2)
    wait = max(15, WAIT - (score // 5) * 5)
    counter += 1
    if counter < wait:
        return      # not time yet
    counter = 0     # it's time: reset the counter and move the apples

    # Look at every apple in the list, one by one.
    # apples[:] is a copy of the list. We remove apples inside the loop,
    # so we walk through the copy; otherwise some apples would be skipped.
    for apple in apples[:]:
        apple.y += CELL  # move the apple one square down

        if basket.colliderect(apple):
            # IF the apple touched the basket: you caught it! Get 1 point.
            score += 1
            apples.remove(apple)
        elif apple.top > HEIGHT:
            # OTHERWISE, IF the apple hit the ground: you missed it! Lose 1 life.
            lives -= 1
            apples.remove(apple)

    # No lives left: the game is over
    if lives <= 0:
        game_over = True
        best_score = max(best_score, score)  # keep the bigger of the two as the best score


# ---------- WHEN A KEY IS PRESSED ----------
# Pygame Zero calls this function by itself whenever you press a key.

def on_key_down(key):
    # If the game is over: SPACE starts a new game, other keys do nothing
    if game_over:
        if key == keys.SPACE:
            new_game()
        return

    # Each arrow key press moves the basket one square (without leaving the window)
    if key == keys.LEFT and basket.left > 0:
        basket.x -= CELL  # smaller x means the basket goes left
    if key == keys.RIGHT and basket.right < WIDTH:
        basket.x += CELL  # bigger x means the basket goes right


# Run the new_apple function every APPLE_EVERY seconds (like setting an alarm)
clock.schedule_interval(new_apple, APPLE_EVERY)
