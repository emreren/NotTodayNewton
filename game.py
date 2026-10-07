# ==================================================
#  NOT TODAY, NEWTON
#  Newton is sitting under an apple tree. If an apple lands
#  on his head, he will discover gravity. Not today!
#  Move your basket left and right with the arrow keys and catch the apples.
#  Miss 3 apples and Newton discovers gravity: game over.
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
WIDTH = 600                  # width of the window
HEIGHT = 500                 # height of the window
SPEED = 6                    # how many dots the basket moves each step
FALL_SPEED = 3               # how fast the apples fall at the start


# ---------- THINGS IN THE GAME ----------
# An Actor is a thing in the game that has a picture. It finds its picture
# in the "images" folder by its name: Actor("basket") → images/basket.png
# An Actor's x and y are the CENTER of its picture. It also has edges: left, right, top, bottom.
# Careful: numbers get BIGGER as you go DOWN the screen. The top is 0, the bottom is 500.

basket = Actor("basket", midbottom=(WIDTH / 2, HEIGHT))  # at the bottom, in the middle
apples = []          # a list of all the apples on the screen (empty at the start)
score = 0            # how many apples you caught
lives = 3            # how many more apples you can miss
best_score = 0       # your best score so far
game_over = False    # is the game over? "No" (False) at the start


# ---------- NEW APPLE ----------

def new_apple():
    # Make a new apple just above the window, in a random place
    x = random.randint(20, WIDTH - 20)  # stay 20 dots away from the edges
    apple = Actor("apple", (x, -20))    # -20: the apple starts a little above the screen
    apples.append(apple)                # add the new apple to the list


# ---------- NEW GAME ----------

def new_game():
    # Put everything back the way it was at the start
    global score, lives, game_over  # we are going to change these variables from above
    score = 0
    lives = 3
    game_over = False
    apples.clear()           # remove all apples from the list
    basket.x = WIDTH / 2     # put the basket back in the middle


# ---------- DRAW THE SCREEN ----------
# Pygame Zero calls this function by itself 60 times every second.
# Colors are a mix of (red, green, blue); each one goes from 0 to 255.

def draw():
    screen.fill((135, 206, 235))  # paint everything sky blue
    basket.draw()                 # draw the basket's picture

    for apple in apples:  # for every apple in the list...
        apple.draw()      # ...draw the apple's picture

    # Write the score at the top left and the lives at the top right
    screen.draw.text(f"Score: {score}", topleft=(10, 10), fontsize=32, color="white")
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


# ---------- MOVE EVERYTHING ----------
# Pygame Zero calls this function 60 times every second too, just before drawing the screen.

def update():
    global score, lives, best_score, game_over  # we are going to change these variables from above

    # If the game is over, stop here and don't move anything
    if game_over:
        return

    # Left arrow moves the basket left, right arrow moves it right
    if keyboard.left:
        basket.x -= SPEED  # smaller x means the basket goes left
    if keyboard.right:
        basket.x += SPEED  # bigger x means the basket goes right

    # Don't let the basket leave the window
    if basket.left < 0:
        basket.left = 0
    if basket.right > WIDTH:
        basket.right = WIDTH

    # Every 5 points, the apples fall a little faster
    # (// keeps only the whole part of a division: 12 // 5 = 2)
    fall_speed = FALL_SPEED + score // 5

    # Look at every apple in the list, one by one.
    # apples[:] is a copy of the list. We remove apples inside the loop,
    # so we walk through the copy; otherwise some apples would be skipped.
    for apple in apples[:]:
        apple.y += fall_speed  # move the apple down a little

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
    # If the game is over and you pressed SPACE, start a new game
    if game_over and key == keys.SPACE:
        new_game()


# Run the new_apple function once every second (like setting an alarm)
clock.schedule_interval(new_apple, 1.0)
