import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 500
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Composting Game")

# mouse set up
system = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND)
pygame.mouse.set_cursor(system)

# background
background = pygame.image.load("Background.png").convert()
#start text
grey = (105,105,105)
font = pygame.font.Font('freesansbold.ttf', 19)
text1 = font.render('Help Sort Lunch Waste!', True, grey)
text2 = font.render('Click the Space Bar to Start', True, grey)
text1Rect = text1.get_rect(center = (300//2,250//2))
text2Rect = text2.get_rect(center = (300//2,300//2))
whereText = font.render('Where does it go?', True, grey)
whereRect = whereText.get_rect(center = (300//2,200//2))

# cans & share table detect collision set up
trash = pygame.Rect(32, 327, 63, 42)
compost = pygame.Rect(144, 327, 63, 42)
recycle = pygame.Rect(250, 327, 63, 42)
share = pygame.Rect(341, 292, 159, 65)

#correct screen
correctImg = pygame.image.load("thumbsup.jpeg").convert()

itemLoc = (300//2, 350//2)
#food items
p = pygame.image.load("pizza.png").convert_alpha()
# scale pizza
pizza = pygame.transform.scale(p, (100, 100))
pRect = pizza.get_rect(center = itemLoc)
milk = pygame.image.load("milk.png").convert_alpha()
milkCart = pygame.transform.scale(milk, (150, 150))
milkRect = milkCart.get_rect(center = itemLoc)
carr = pygame.image.load("carrots.png").convert_alpha()
carrot = pygame.transform.scale(carr, (200, 200))
carrRect = milkCart.get_rect(center = itemLoc)

# displaying background
screen.blit(background, (0, 0))
pygame.display.flip()

# Main game loop
running = True
showText = True
wheretextOn = False
moving = False
pizzaOn = False
milkOn = False
carrotOn = False
forkOn = False
napkinOn = False
correct = False
wrong = False
tryAgain = False
feedbackTimer = 0
itemCount = 1

while running:
    screen.blit(background, (0,0))
    if showText == True:
        screen.blit(text1, text1Rect)
        screen.blit(text2, text2Rect)
        pygame.display.flip()
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            showText = False
            #show first item
            pizzaOn = True
            wheretextOn = True
        if pizzaOn:
            # moving the pizza
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pRect.collidepoint(event.pos):
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = False
            elif event.type == pygame.MOUSEMOTION and moving:
                pRect.move_ip(event.rel)
        if milkOn:
            # moving the milk
            if event.type == pygame.MOUSEBUTTONDOWN:
                if milkRect.collidepoint(event.pos):
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = False
            elif event.type == pygame.MOUSEMOTION and moving:
                milkRect.move_ip(event.rel)
        if carrotOn:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if carrRect.collidepoint(event.pos):
                    moving = True
            elif event.type == pygame.MOUSEBUTTONUP:
                moving = False
            elif event.type == pygame.MOUSEMOTION and moving:
                carrRect.move_ip(event.rel)
    # pizza logic
    if pizzaOn:
        if wheretextOn:
            screen.blit(whereText, whereRect)
        screen.blit(pizza, pRect)
        # check if they put it in the right bin
        if pRect.colliderect(compost):
            itemCount = 2
            wrong = False
            correct = True
            pizzaOn = False
            wheretextOn = True
            feedback_timer = pygame.time.get_ticks()
        elif pRect.colliderect(trash) or pRect.colliderect(recycle) or pRect.colliderect(share):
            correct = False
            wrong = True
            pizzaOn = True
            wheretextOn = False
            tryAgain = True
            pRect.center = (itemLoc)
            feedback_timer = pygame.time.get_ticks()
    if milkOn:
        screen.blit(milkCart, milkRect)
        if wheretextOn:
            screen.blit(whereText, whereRect)
        # correct case
        if milkRect.colliderect(share):
            itemCount = 3
            wrong = False
            correct = True
            milkOn = False
            wheretextOn = True
            feedback_timer = pygame.time.get_ticks()
        elif milkRect.colliderect(trash) or milkRect.colliderect(recycle) or milkRect.colliderect(compost):
            correct = False
            wrong = True
            milkOn = True
            wheretextOn = False
            tryAgain = True
            milkRect.center = (itemLoc)
            feedback_timer = pygame.time.get_ticks()
    if carrotOn:
        screen.blit(carrot, carrRect)
        if wheretextOn:
            screen.blit(whereText, whereRect)
        # correct case
        if carrRect.colliderect(compost):
            itemCount = 4
            wrong = False
            correct = True
            carrotOn = False
            wheretextOn = True
            feedback_timer = pygame.time.get_ticks()
        elif carrRect.colliderect(trash) or carrRect.colliderect(recycle) or carrRect.colliderect(share):
            correct = False
            wrong = True
            carrotOn = True
            wheretextOn = False
            tryAgain = True
            carrRect.center = (itemLoc)
            feedback_timer = pygame.time.get_ticks()
    if correct or wrong:
        elapsed_time = pygame.time.get_ticks() - feedback_timer
        if correct:
            screen.blit(correctImg, (100, 100))
        if wrong:
            wrong_text = font.render('Try Again!', True, grey)
            wrongRect = wrong_text.get_rect(center=(300//2,200//2))
            screen.blit(wrong_text, wrongRect)
        if elapsed_time > 2000:
            if correct and itemCount == 2:
                milkOn = True
                correct = False
                wheretextOn = True
            if correct and itemCount == 3:
                carrotOn = True
                correct = False
                wheretextOn = True
    pygame.display.flip()


# Quit Pygame
pygame.quit()
sys.exit()