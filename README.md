# Dino Run Game  🦖

This is a Python implementation of the classic "Dino Run" game using the `pygame` library. Below is a breakdown of the code, section by section.

---

## 1. **Imports and Initialization**
```python
import os
import sys
import pygame
import random
from pygame import *

pygame.init()
```

### What’s Happening Here?
- **`import os`**: Helps manage file paths (e.g., loading images from the `resources` folder).
- **`import sys`**: Provides system-specific functions (e.g., exiting the game).
- **`import pygame`**: The main library for creating games (handles graphics, sound, and input).
- **`import random`**: Used to generate random numbers (e.g., for obstacle placement).
- **`pygame.init()`**: Initializes all pygame modules to get the game ready.

---

## 2. **Game Setup**
```python
screenDisplay = (width_screen, height_screen) = (600, 400)
FPS = 60
gravity = 0.6

black_color = (0, 0, 0)
white_color = (255, 255, 255)
backgroundColor = (235, 235, 235)

highest_scores = 0

screenDisplay = pygame.display.set_mode(screenDisplay)
timerClock = pygame.time.Clock()
pygame.display.set_caption("Dino Run")
```

### What’s Happening Here?
- **Screen Setup**:
  - Screen size: `600x400` pixels.
  - FPS (Frames Per Second): `60` (controls how fast the game runs).
  - Gravity: `0.6` (controls how the dino falls after jumping).
- **Colors**:
  - `black_color`, `white_color`, `backgroundColor`: Define colors for the game.
- **Game Window**:
  - `pygame.display.set_mode()`: Creates the game window.
  - `pygame.time.Clock()`: Helps control the game speed.
  - `pygame.display.set_caption()`: Sets the window title to "Dino Run".

---

## 3. **Loading Sounds**
```python
soundOnJump = pygame.mixer.Sound('resources/jump.wav')
soundOnDie = pygame.mixer.Sound('resources/die.wav')
soundOnCheckpoint = pygame.mixer.Sound('resources/checkPoint.wav')
```

### What’s Happening Here?
- **Sound Effects**:
  - `soundOnJump`: Plays when the dino jumps.
  - `soundOnDie`: Plays when the dino hits an obstacle.
  - `soundOnCheckpoint`: Plays every 100 points scored.

---

## 4. **Loading Images**
```python
def load_image(name, sx=-1, sy=-1, colorkey=None):
    fullname = os.path.join('resources', name)
    img = pygame.image.load(fullname)
    img = img.convert()
    
    if colorkey is not None:
        if colorkey == -1:
            colorkey = img.get_at((0, 0))
        img.set_colorkey(colorkey, RLEACCEL)

    if sx != -1 or sy != -1:
        img = pygame.transform.scale(img, (sx, sy))

    return (img, img.get_rect())
```

### What’s Happening Here?
- **`load_image()`**:
  - Loads an image from the `resources` folder.
  - Optionally scales the image to a specific size (`sx`, `sy`).
  - Handles transparency (removes background color).

---

## 5. **Loading Sprite Sheets**
```python
def load_sprite_sheet(s_name, namex, namey, scx=-1, scy=-1, c_key=None):
    fullname = os.path.join('resources', s_name)
    sh = pygame.image.load(fullname)
    sh = sh.convert()

    sh_rect = sh.get_rect()

    sprites = []

    sx = sh_rect.width / namex
    sy = sh_rect.height / namey

    for i in range(0, namey):
        for j in range(0, namex):
            rect = pygame.Rect((j*sx, i*sy, sx, sy))
            img = pygame.Surface(rect.size)
            img = img.convert()
            img.blit(sh, (0, 0), rect)

            if c_key is not None:
                if c_key == -1:
                    c_key = img.get_at((0, 0))
                img.set_colorkey(c_key, RLEACCEL)

            if scx != -1 or scy != -1:
                img = pygame.transform.scale(img, (scx, scy))

            sprites.append(img)

    sprite_rect = sprites[0].get_rect()

    return sprites, sprite_rect
```

### What’s Happening Here?
- **`load_sprite_sheet()`**:
  - Loads a sprite sheet (a single image containing multiple frames).
  - Splits the sheet into individual frames for animation.
  - Handles transparency and scaling.

---

## 6. **Game Objects**

### 6.1 **Dino Class**
```python
class Dino():
    def __init__(self, sx=-1, sy=-1):
        self.imgs, self.rect = load_sprite_sheet('dino.png', 5, 1, sx, sy, -1)
        self.imgs1, self.rect1 = load_sprite_sheet('dino_ducking.png', 2, 1, 59, sy, -1)
        self.rect.bottom = int(0.98 * height_screen)
        self.rect.left = width_screen / 15
        self.image = self.imgs[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.jumping = False
        self.dead = False
        self.ducking = False
        self.blinking = False
        self.movement = [0,0]
        self.jumpSpeed = 11.5

        self.stand_position_width = self.rect.width
        self.duck_position_width = self.rect1.width
```

### What’s Happening Here?
- **Dino Attributes**:
  - `imgs`: Running animation frames.
  - `imgs1`: Ducking animation frames.
  - `rect`: Position and size of the dino.
  - `jumping`, `ducking`, `dead`: States of the dino.
  - `score`: Tracks the player’s score.
- **Methods**:
  - `draw()`: Draws the dino on the screen.
  - `update()`: Handles movement, gravity, and animation.

---

### 6.2 **Ground Class**
```python
class Ground():
    def __init__(self,speed=-5):
        self.image,self.rect = load_image('ground.png',-1,-1,-1)
        self.image1,self.rect1 = load_image('ground.png',-1,-1,-1)
        self.rect.bottom = height_screen
        self.rect1.bottom = height_screen
        self.rect1.left = self.rect.right
        self.speed = speed
```

### What’s Happening Here?
- **Ground Attributes**:
  - `image`: Ground texture.
  - `rect`: Position and size of the ground.
  - `speed`: Controls how fast the ground scrolls.
- **Methods**:
  - `draw()`: Draws the ground.
  - `update()`: Moves the ground to create a scrolling effect.

---

### 6.3 **Obstacles (Cactus and Birds)**
```python
class Cactus(pygame.sprite.Sprite):
    def __init__(self,speed=5,sx=-1,sy=-1):
        self.imgs, self.rect = load_sprite_sheet('cactus-small.png', 3, 1, sx, sy, -1)
        self.rect.bottom = int(0.98 * height_screen)
        self.rect.left = width_screen + self.rect.width
        self.image = self.imgs[random.randrange(0, 3)]
        self.movement = [-1*speed,0]
```

### What’s Happening Here?
- **Cactus**:
  - Randomly spawns cacti of varying sizes.
  - Moves left towards the dino.
- **Birds**:
  - Flies at random heights to challenge the player.

---

## 7. **Game Logic**

### 7.1 **Introduction Screen**
```python
def introduction_screen():
    ado_dino = Dino(44,47)
    ado_dino.blinking = True
    starting_game = False

    while not starting_game:
        # Handle events and draw the intro screen
```

### What’s Happening Here?
- Displays the game logo and a blinking dino.
- Starts the game when the player presses the spacebar or up arrow.

---

### 7.2 **Gameplay Loop**
```python
def gameplay():
    global highest_scores
    gp = 4
    g_Over = False
    g_exit = False
    gamer_Dino = Dino(44,47)
    new_grnd = Ground(-1*gp)
    score_boards = Scoreboard()
    highScore = Scoreboard(width_screen * 0.78)
    counter = 0

    while not g_exit:
        # Handle events, update objects, and draw the game
```

### What’s Happening Here?
- **Main Game Loop**:
  - Handles player input (jump, duck).
  - Updates game objects (dino, ground, obstacles).
  - Checks for collisions.
  - Increases difficulty over time.

---

### 7.3 **Game Over Screen**
```python
def gameover_display_message(rbtn_image, gmo_image):
    rbtn_rect = rbtn_image.get_rect()
    rbtn_rect.centerx = width_screen / 2
    rbtn_rect.top = height_screen * 0.52

    gmo_rect = gmo_image.get_rect()
    gmo_rect.centerx = width_screen / 2
    gmo_rect.centery = height_screen * 0.35

    screenDisplay.blit(rbtn_image, rbtn_rect)
    screenDisplay.blit(gmo_image, gmo_rect)
```

### What’s Happening Here?
- Displays the "Game Over" message and a replay button.
- Allows the player to restart or exit the game.

---

## 8. **Main Function**
```python
def main():
    isGameQuit = introduction_screen()
    if not isGameQuit:
        gameplay()

main()
```

### What’s Happening Here?
- **Game Flow**:
  1. Displays the introduction screen.
  2. Starts the gameplay loop.
  3. Handles game over and restart logic.

---

## 9. **Key Features**
- Infinite runner mechanics.
- Progressive difficulty scaling.
- Pixel-perfect collision detection.
- Sound effects for actions (jump, die, checkpoint).
- Persistent high score tracking.

---

## 10. **How to Play**
- **Space/Up Arrow**: Jump.
- **Down Arrow**: Duck.
- **Escape**: Exit the game.
- **Enter/Space**: Restart after game over.

---

This breakdown explains the entire code in **README.md syntax**. Let me know if you need further clarification! 😊