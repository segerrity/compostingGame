import pygame
import sys
import random

# initialize Pygame
pygame.init()

# set up
screen_width, screen_height = 500, 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Composting Game")
pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

# text
grey = (105,105,105)
font = pygame.font.Font('freesansbold.ttf', 19)

# instruction texts
text1 = font.render('Help Sort Lunch Waste!', True, grey)
text2 = font.render('Click the Space Bar to Start', True, grey)
text1_rect = text1.get_rect(center=(150, 125))
text2_rect = text2.get_rect(center=(150, 150))
where_text = font.render('Where does it go?', True, grey)
where_rect = where_text.get_rect(center=(150, 100))
wrong_text = font.render('Try Again!', True, grey)
wrong_rect = wrong_text.get_rect(center=(150, 100))

# load extra images
background = pygame.image.load("Background.png").convert()
star = pygame.image.load("goldstar.png").convert_alpha()
correct_img = pygame.transform.scale(star, (300, 300))

# item starting position
item_loc = (150, 175)

# bins
trash_bin = pygame.Rect(32, 327, 63, 42)
compost_bin = pygame.Rect(144, 327, 63, 42)
recycle_bin = pygame.Rect(250, 327, 63, 42)
share_table = pygame.Rect(360, 292, 159, 65)

class LunchItem:
    def __init__(self, image_path, scale, correct_bin):
        # initialize food item with image, position, and correct bin
        image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(image, scale)
        self.original_pos = (150, 175)  # Store original position
        self.rect = self.image.get_rect(center=self.original_pos)
        self.correct_bin = correct_bin
        self.moving = False
        self.sorted = False  # Flag to track if item is placed correctly
        self.small_version = pygame.transform.scale(image, (60, 60))  # Small version for share table

    def draw(self):
        # draw the item on the screen if it's not sorted
        if not self.sorted:
            screen.blit(self.image, self.rect)

    def handle_movement(self, event):
        # handle drag-and-drop movement
        if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
            self.moving = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.moving = False
        elif event.type == pygame.MOUSEMOTION and self.moving:
            self.rect.move_ip(event.rel)

    def reset_position(self):
         # reset item to its original position
        self.rect.center = self.original_pos


# define items
items = [
    LunchItem("pizza.png", (100, 100), compost_bin),
    LunchItem("milk.png", (150, 150), share_table),
    LunchItem("carrots.png", (200, 200), compost_bin),
    LunchItem("plasticbag.png", (125, 125), trash_bin),
    LunchItem("napkin.png", (175,175), compost_bin),
    LunchItem("chips.png", (100, 100), share_table),
    LunchItem("plasticfork.png", (200, 200), recycle_bin),
    LunchItem("peeledclem.png", (100, 125), compost_bin),
]

# list to store small versions of share table items
share_table_items = []

# Game states
show_text = True
item_index = 0
feedback_timer = 0
correct, wrong = False, False
current_item = None  # initialize current_item as None
display_try_again = False  # control visibility

running = True
while running:
    screen.blit(background, (0, 0))

    if show_text:
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        pygame.display.flip()
    elif item_index < len(items):  # ensure items are left to sort
        current_item = items[item_index]  # get current item
        if not current_item.sorted:
            if not display_try_again:  # only show if we are not retrying
                screen.blit(where_text, where_rect)
            current_item.draw()

    # draw all small versions of items in the share table
    for item, pos in share_table_items:
        screen.blit(item, pos)

    # event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            show_text = False
        if current_item and not current_item.sorted:  # prevent interaction with sorted items
            current_item.handle_movement(event)

        # check if the item was dropped
        if event.type == pygame.MOUSEBUTTONUP and current_item and not current_item.sorted:
            if current_item.rect.colliderect(current_item.correct_bin):
                current_item.sorted = True  # mark item as sorted
                correct = True
                wrong = False
                display_try_again = False  
                feedback_timer = pygame.time.get_ticks()

                # If placed in the share table, add small version inside
                if current_item.correct_bin == share_table:
                    small_x = random.randint(share_table.left + 10, share_table.right - 50)
                    small_y = random.randint(share_table.top + 10, share_table.bottom - 50)
                    share_table_items.append((current_item.small_version, (small_x, small_y)))

            elif any(current_item.rect.colliderect(bin) for bin in [trash_bin, recycle_bin, share_table, compost_bin] if bin != current_item.correct_bin):
                correct = False
                wrong = True
                display_try_again = True  
                feedback_timer = pygame.time.get_ticks()
                current_item.reset_position()  # immediately reset position

    # feedback handling
    if correct or wrong:
        elapsed_time = pygame.time.get_ticks() - feedback_timer
        if correct:
            screen.blit(correct_img, (100, 100))
        elif wrong and display_try_again:
            screen.blit(wrong_text, wrong_rect)

        if elapsed_time > 1500:
            if correct and item_index < len(items) - 1:
                item_index += 1  # Move to the next item
                correct = False
            elif wrong:
                display_try_again = False  # hide after delay
                wrong = False  # Reset state

    pygame.display.flip()


# quit Pygame
pygame.quit()
sys.exit()
