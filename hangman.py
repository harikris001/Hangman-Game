import os
import pygame
import random

pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("stranger.mp3")  # Replace "sound.wav" with the path to your sound file

winHeight = 480
winWidth = 700
win=pygame.display.set_mode((winWidth,winHeight))

# Colors
BLACK = (0,0, 0)
WHITE = (255,255,255)
RED = (255,0, 0)
GREEN = (0,255,0)
BLUE = (0,0,255)
LIGHT_BLUE = (102,255,255)

# Global Assets
btn_font = pygame.font.SysFont("inkfree", 20)
guess_font = pygame.font.SysFont("monospace", 24)
lost_font = pygame.font.SysFont('gabriola', 45)
splash_font = pygame.font.SysFont('gabriola', 60)  # Font for splash screen
loading_font = pygame.font.SysFont('comicsansms',30) # Font for loading screen
word = ''
buttons = []
guessed = []
hangmanPics = [pygame.image.load('step0.png'), pygame.image.load('step1.png'), pygame.image.load('step2.png'), pygame.image.load('step3.png'), pygame.image.load('step4.png'), pygame.image.load('step5.png'), pygame.image.load('step6.png')]

limbs = 0

# Function to load images from a folder
def load_images(folder):
    images = []
    for filename in os.listdir(folder):
        img = pygame.image.load(os.path.join(folder, filename))
        images.append(img)
    return images

# Load images for loading screen
loading_images = load_images("Loading")

# Game window setups
def redraw_game_window():
    global guessed
    global hangmanPics
    global limbs
    win.fill(WHITE)
    # Buttons
    for i in range(len(buttons)):
        if buttons[i][4]:
            pygame.draw.circle(win, BLACK, (buttons[i][1], buttons[i][2]), buttons[i][3])
            pygame.draw.circle(win, buttons[i][0], (buttons[i][1], buttons[i][2]), buttons[i][3] - 2
                               )
            label = btn_font.render(chr(buttons[i][5]), 1, BLACK)
            win.blit(label, (buttons[i][1] - (label.get_width() / 2), buttons[i][2] - (label.get_height() / 2)))

    spaced = spacedOut(word, guessed)
    label1 = guess_font.render(spaced, 1, BLACK)
    rect = label1.get_rect()
    length = rect[2]
    
    win.blit(label1,(winWidth/2 - length/2, 400))

    pic = hangmanPics[limbs]
    win.blit(pic, (winWidth/2 - pic.get_width()/2 + 20, 150))
    pygame.display.update()

# Select random word from text
def randomWord():
    file = open('words.txt')
    f = file.readlines()
    i = random.randrange(0, len(f) - 1)

    return f[i][:-1]

# Wrong Guess
def hang(guess):
    global word
    if guess.lower() not in word.lower():
        return True
    else:
        return False

# words space checker
def spacedOut(word, guessed=[]):
    spacedWord = ''
    guessedLetters = guessed
    for x in range(len(word)):
        if word[x] != ' ':
            spacedWord += '_ '
            for i in range(len(guessedLetters)):
                if word[x].upper() == guessedLetters[i]:
                    spacedWord = spacedWord[:-2]
                    spacedWord += word[x].upper() + ' '
        elif word[x] == ' ':
            spacedWord += ' '
    return spacedWord
            

def buttonHit(x, y):
    for i in range(len(buttons)):
        if x < buttons[i][1] + 20 and x > buttons[i][1] - 20:
            if y < buttons[i][2] + 20 and y > buttons[i][2] - 20:
                return buttons[i][5]
    return None

# End game checker
def end(winner=False):
    global limbs

    # Game lost
    lostTxt = 'OOPS! Lost, press any key to play again...'
    # Game win
    winTxt = 'WINNER!, press any key to play again...'
    redraw_game_window()
    pygame.time.delay(500)
    
    if winner == False:
        # Load game over image
        game_over_img = pygame.image.load('gameover.png')
        game_over_img = pygame.transform.scale(game_over_img, (640, 360))
        win.fill(RED)
        label = lost_font.render(lostTxt, 1, BLACK)
        wordTxt = lost_font.render(word.upper(), 1, BLACK)
        wordWas = lost_font.render('The phrase was: ', 1, BLACK)
        
        # Display game over image
        win.blit(game_over_img, (winWidth/2 - 320, winHeight/2 - 180))
        win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, winHeight/2 + 100))
        win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, winHeight/2 + 50))
        win.blit(label, (winWidth / 2 - label.get_width() / 2, winHeight/2 - 50))
    else:
        # Load you win image
        you_win_img = pygame.image.load('gamewin.png')
        you_win_img = pygame.transform.scale(you_win_img, (500, 500))
        win.fill(GREEN)
        label = lost_font.render(winTxt, 1, BLACK)
        wordTxt = lost_font.render(word.upper(), 1, BLACK)
        wordWas = lost_font.render('The phrase was: ', 1, BLACK)
        
        # Display you win image
        win.blit(you_win_img, (winWidth/2 - 250, winHeight/2 - 250))
        win.blit(wordTxt, (winWidth/2 - wordTxt.get_width()/2, winHeight/2 + 100))
        win.blit(wordWas, (winWidth/2 - wordWas.get_width()/2, winHeight/2 + 50))
        win.blit(label, (winWidth / 2 - label.get_width() / 2, winHeight/2 - 50))
    
    pygame.display.update()
    
    again = True
    while again:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                again = False
    reset()

# Sound
def play_sound():
    sound.play()


# game reset function
def reset():
    global limbs
    global guessed
    global buttons
    global word
    for i in range(len(buttons)):
        buttons[i][4] = True

    limbs = 0
    guessed = []
    word = randomWord()

# Function to display splash screen
def splash_screen():
    splash_text = "Hangman Game"
    instructions = "Click the letters to guess the word"
    splash_render = splash_font.render(splash_text, 1, BLACK)
    instructions_render = btn_font.render(instructions, 1, BLACK)
    
    play_sound()
    win.fill(WHITE)
    win.blit(splash_render, (winWidth/2 - splash_render.get_width()/2, 100))
    win.blit(instructions_render, (winWidth/2 - instructions_render.get_width()/2, 300))
    
    pygame.display.update()

    # Load images for the loop
    box_images = load_images("Box")
    
    # Display images in a loop
    start_time = pygame.time.get_ticks()
    current_time = start_time
    image_index = 0
    while current_time - start_time < 3000:  # Display images for 2 seconds
        win.fill(WHITE)
        win.blit(splash_render, (winWidth/2 - splash_render.get_width()/2, 100))
        win.blit(instructions_render, (winWidth/2 - instructions_render.get_width()/2, 200))
        
        # Display image between the texts
        box_img = pygame.transform.scale(box_images[image_index % len(box_images)], (259, 194))
        win.blit(box_img, (winWidth/2 - box_img.get_width()/2, 200))
        
        pygame.display.update()
        pygame.time.delay(17)
        
        current_time = pygame.time.get_ticks()
        image_index += 1


# Function to display loading screen
def loading_screen():
    start_time = pygame.time.get_ticks()
    current_time = start_time
    screen_index = 0
    
    while current_time - start_time < 5000:  # Display for 5 seconds
        win.fill(BLACK)
        win.blit(loading_images[screen_index % len(loading_images)], (winWidth/2 - loading_images[screen_index % len(loading_images)].get_width()/2, winHeight/2 - loading_images[screen_index % len(loading_images)].get_height()/2))
        loading_text = loading_font.render("Loading...", 1, WHITE)
        win.blit(loading_text, (winWidth/2 - loading_text.get_width()/2, 400))
        
        pygame.display.update()
        pygame.time.delay(17)
        
        current_time = pygame.time.get_ticks()
        screen_index += 1

# Main Thread
splash_screen()
loading_screen()

increase = round(winWidth / 13)
for i in range(26):
    if i < 13:
        y = 40
        x = 25 + (increase * i)
    else:
        x = 25 + (increase * (i - 13))
        y = 85
    buttons.append([LIGHT_BLUE, x, y, 20, True, 65 + i])
    # buttons.append([color, x_pos, y_pos, radius, visible, char])

word = randomWord()
inPlay = True

while inPlay:
    redraw_game_window()
    pygame.time.delay(10)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                inPlay = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            clickPos = pygame.mouse.get_pos()
            letter = buttonHit(clickPos[0], clickPos[1])
            if letter != None:
                guessed.append(chr(letter))
                buttons[letter - 65][4] = False
                if hang(chr(letter)):
                    if limbs != 5:
                        limbs += 1
                    else:
                        end()
                else:
                    print(spacedOut(word, guessed))
                    if spacedOut(word, guessed).count('_') == 0:
                        end(True)

pygame.quit()
