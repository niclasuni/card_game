import pygame
import random
import sys

from drawing import draw_arrow
from character import Character
from deck import card_name_to_filename


def select_card(mouse_pos, last_cards, start_x, y_pos, box_width=100, box_height=145, spacing=10):
    """
    Check if the mouse clicked on one of the displayed card boxes.

    Parameters:
        mouse_pos: tuple (x, y) of mouse click
        last_cards: list of currently displayed cards (up to 5)
        start_x, y_pos: top-left position of the first card box
        box_width, box_height: size of each card box
        spacing: space between boxes

    Returns:
        The card name if a box was clicked, otherwise None
    """
    for i in range(len(last_cards)):
        rect = pygame.Rect(start_x + i * (box_width + spacing), y_pos, box_width, box_height)
        if rect.collidepoint(mouse_pos):
            return last_cards[i]  # return the card clicked
    return None


# -------------------------------
# Pygame setup
# -------------------------------
pygame.init()
WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Card Draw Game")

font = pygame.font.SysFont(None, 32)
clock = pygame.time.Clock()


### MAIN MENU

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (0, 128, 255)
BUTTON_HOVER_COLOR = (0, 255, 255)

def draw_button(text, x, y, width, height, color):
    pygame.draw.rect(screen, color, (x, y, width, height))
    label = font.render(text, True, BLACK)
    screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

# Check if mouse is over a button
def button_hover(x, y, width, height):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return x <= mouse_x <= x + width and y <= mouse_y <= y + height

running = True
while running:
    screen.fill(WHITE)

    # Draw buttons
    start_color = BUTTON_HOVER_COLOR if button_hover(300, 200, 200, 50) else BUTTON_COLOR
    options_color = BUTTON_HOVER_COLOR if button_hover(300, 300, 200, 50) else BUTTON_COLOR
    quit_color = BUTTON_HOVER_COLOR if button_hover(300, 400, 200, 50) else BUTTON_COLOR

    draw_button("Start Game", 300, 200, 200, 50, start_color)
    draw_button("Options", 300, 300, 200, 50, options_color)
    draw_button("Quit", 300, 400, 200, 50, quit_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse click events
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if button_hover(300, 200, 200, 50):  # Start Game
                print("Start Game clicked")
                running = False
                # Call the function to start the game (you can transition here)
            elif button_hover(300, 300, 200, 50):  # Options
                print("Options clicked")
                # You can create an options menu here
            elif button_hover(300, 400, 200, 50):  # Quit
                running = False

    pygame.display.flip()

### MAIN GAME
# Button setup
button_rect = pygame.Rect(0, 0, 150, 50)  # will set to top-right later
button_color = (70, 130, 180)
button_hover = (100, 160, 210)

reverse_button_rect = pygame.Rect(0, 0, 150, 50)  # size of the button
reverse_button_color = (70, 130, 180)
reverse_button_hover = (100, 160, 210)

play_button_rect = pygame.Rect(0, 0, 150, 50)

ui_poison = pygame.image.load("board_game_icons/PNG/Default (64px)/skull.png")
ui_shield = pygame.image.load("board_game_icons/PNG/Default (64px)/shield.png")
ui_poison = pygame.transform.scale(ui_poison, (20, 20))
ui_shield = pygame.transform.scale(ui_shield, (20, 20))

# Deck and drawn cards

player = Character()
enemy = Character()


enemy_turn_step = None

played_card = None
player_turn = True

# -------------------------------
# Main loop
# -------------------------------
running = True
while running:
    screen.fill((34, 139, 34))  # green table background

    lifebar_player = pygame.Rect(0, 0, 30, player.life)
    lifebar_player.bottomleft = (20, 695)
    lifebar_enemy = pygame.Rect(0, 0, 30, enemy.life)
    lifebar_enemy.topleft = (20, 25)
    screen.blit(ui_poison, (70, 695))
    screen.blit(ui_shield, (120, 695))
    screen.blit(ui_poison, (70, 2))
    screen.blit(ui_shield, (120, 2))


    pygame.draw.rect(screen, (255, 255, 255), lifebar_player, border_radius=10)
    pygame.draw.rect(screen, (255, 255, 255), lifebar_enemy, border_radius=10)

    value_text = font.render(str(player.life), True, (255, 255, 255))
    text_rect = value_text.get_rect(center=(lifebar_player.centerx, lifebar_player.bottom + 12))
    screen.blit(value_text, text_rect)
    value_text = font.render(str(player.poison), True, (0, 0, 0))
    text_rect = value_text.get_rect(center=(lifebar_player.right + 50, lifebar_player.bottom + 12))
    screen.blit(value_text, text_rect)
    value_text = font.render(str(player.shield), True, (0, 0, 0))
    text_rect = value_text.get_rect(center=(lifebar_player.right + 100, lifebar_player.bottom + 12))
    screen.blit(value_text, text_rect)

    value_text = font.render(str(enemy.life), True, (255, 255, 255))
    text_rect = value_text.get_rect(center=(lifebar_enemy.centerx, lifebar_enemy.top - 12))
    screen.blit(value_text, text_rect)
    value_text = font.render(str(enemy.poison), True, (0, 0, 0))
    text_rect = value_text.get_rect(center=(lifebar_enemy.right + 50, lifebar_enemy.top - 12))
    screen.blit(value_text, text_rect)
    value_text = font.render(str(enemy.shield), True, (0, 0, 0))
    text_rect = value_text.get_rect(center=(lifebar_enemy.right + 100, lifebar_enemy.top - 12))
    screen.blit(value_text, text_rect)

    # --- Draw button at top-right
    button_rect.topright = (WIDTH - 20, HEIGHT - 70)
    mouse_pos = pygame.mouse.get_pos()
    color = button_hover if button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, button_rect, border_radius=10)

    text = font.render("Draw Card", True, (255, 255, 255))
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)

    reverse_button_rect.topright = (WIDTH - 20, HEIGHT - 140)
    color = button_hover if reverse_button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, reverse_button_rect, border_radius=10)
    text = font.render("Reverse", True, (255, 255, 255))
    text_rect = text.get_rect(center=reverse_button_rect.center)
    screen.blit(text, text_rect)

    play_button_rect.topright = (WIDTH - 200, HEIGHT - 140)
    color = button_hover if play_button_rect.collidepoint(mouse_pos) else button_color
    pygame.draw.rect(screen, color, play_button_rect, border_radius=10)
    text = font.render("Play", True, (255, 255, 255))
    text_rect = text.get_rect(center=play_button_rect.center)
    screen.blit(text, text_rect)

    center = pygame.Vector2(WIDTH / 2 - 350, 95 if not player_turn else 630)
    end = pygame.Vector2(WIDTH / 2 - 300, 95 if not player_turn else 630)
    # draw_arrow(screen, center, end, pygame.Color("dodgerblue"), 10, 20, 12)
    draw_arrow(screen, center, end, pygame.Color(0, 0, 0), 10, 20, 12)

    # --- Draw 5 card boxes at the bottom
    box_width = 100
    box_height = 145
    spacing = 10
    start_x = (WIDTH - (5 * box_width + 4 * spacing)) // 2
    y_pos = HEIGHT - box_height - 20

    last_cards = player.drawn_cards[-5:]
    enemy_last_cards = enemy.drawn_cards[-5:]

    for i in range(5):
        card_slot_rect = pygame.Rect(start_x + i * (box_width + spacing), y_pos, box_width, box_height)
        enemy_card_slot_rect = pygame.Rect(start_x + i * (box_width + spacing), 20, box_width, box_height)

        # Draw empty box
        pygame.draw.rect(screen, (200, 200, 200), card_slot_rect, border_radius=5)
        pygame.draw.rect(screen, (200, 200, 200), enemy_card_slot_rect, border_radius=5)

        # Decide border color
        if i < len(last_cards) and last_cards[i] == player.selected_card:
            border_color = (255, 215, 0)  # highlight
        else:
            border_color = (0, 0, 0)
        pygame.draw.rect(screen, border_color, card_slot_rect, 3, border_radius=5)

        if i < len(enemy_last_cards) and enemy_last_cards[i] == enemy.selected_card:
            border_color = (255, 215, 0)  # highlight
        else:
            border_color = (0, 0, 0)
        pygame.draw.rect(screen, border_color, enemy_card_slot_rect, 3, border_radius=5)

        # Draw card image if it exists
        if i < len(last_cards):
            card_key = card_name_to_filename(last_cards[i])
            card_img = player.deck.images.get(card_key)
            if card_img:
                img_rect = card_img.get_rect(center=card_slot_rect.center)
                screen.blit(card_img, img_rect)

        if i < len(enemy_last_cards):
            card_key = card_name_to_filename(enemy_last_cards[i])
            card_img = enemy.deck.images.get(card_key)
            if card_img:
                img_rect = card_img.get_rect(center=enemy_card_slot_rect.center)
                screen.blit(card_img, img_rect)

        if played_card:
            card_key = card_name_to_filename(played_card)
            card_img = player.deck.images.get(card_key) if not player_turn else enemy.deck.images.get(card_key)
            if card_img:
                # Scale to fit nicely in the center
                center_img = pygame.transform.scale(card_img, (200, 290))  # adjust size
                center_rect = center_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                screen.blit(center_img, center_rect)

    ###
    if player_turn:

        # --- Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    player.deck.put_back('Jack of Spades')

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(event.pos):
                    # Draw a new card
                    new_cards = player.deck.draw(1)
                    player.drawn_cards.extend(new_cards)
                    if len(player.drawn_cards) >= 6:
                        player.drawn_cards = player.drawn_cards[1:]
                    # Deselect if selected card is no longer in hand
                    if player.selected_card not in player.drawn_cards:
                        selected_card = None
                        selected = None

                elif reverse_button_rect.collidepoint(event.pos):
                    # Reverse colors of selected card
                    if player.selected_card:
                        card_key = card_name_to_filename(player.selected_card)
                        if card_key in player.deck.images:
                            player.deck.invert_card_colors(card_key)

                elif play_button_rect.collidepoint(event.pos):
                    # Play the selected card
                    if player.selected_card in player.drawn_cards:
                        played_card = player.selected_card

                        if player.selected_card in player.drawn_cards:
                            player.calc_damage(played_card, enemy)
                            player.drawn_cards.remove(player.selected_card)
                            player.selected_card = None  # deselect immediately
                            selected = None
                            player_turn = not player_turn

                    enemy_card = enemy.deck.draw(1)
                    enemy.drawn_cards.extend(enemy_card)
                    enemy_turn_step = 1
                    if enemy_turn_step:
                        enemy_card = enemy_card[0]  # get the card name
                        enemy.enemy_card_start_time = pygame.time.get_ticks()

                else:
                    # Check if a card box was clicked
                    selected = select_card(event.pos, player.drawn_cards[-5:], start_x, y_pos)
                    if selected and selected in player.drawn_cards:
                        player.selected_card = selected
                        print("You selected:", player.selected_card)

    # Enemy turn
    else:
        for event in pygame.event.get():
            pass

        if enemy_turn_step == 1:
            elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
            if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                card_key = card_name_to_filename(enemy_card)
                card_img = enemy.deck.images.get(card_key)
                if card_img:
                    # Draw on the left side
                    enemy_img = pygame.transform.scale(card_img, (100, 145))  # adjust size
                    enemy_rect = enemy_img.get_rect(midleft=(20, HEIGHT // 2))
                    screen.blit(enemy_img, enemy_rect)
            else:
                enemy_turn_step += 1
                enemy.enemy_card_start_time = pygame.time.get_ticks()

        elif enemy_turn_step == 2:
            elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
            if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                if not enemy.selected_card:
                    enemy.selected_card = random.choice(enemy.drawn_cards)
            else:
                enemy_turn_step = 3
                enemy.enemy_card_start_time = pygame.time.get_ticks()

        elif enemy_turn_step == 3:
            elapsed = pygame.time.get_ticks() - enemy.enemy_card_start_time
            if elapsed <= enemy.ENEMY_DISPLAY_TIME:
                if enemy.selected_card in enemy.drawn_cards:
                    played_card = enemy.selected_card
                    enemy.calc_damage(played_card, player)
                    enemy.drawn_cards.remove(enemy.selected_card)
                    enemy.selected_card = None  # deselect immediately
                    selected = None
            else:
                enemy_turn_step = 4

        if enemy_turn_step == 4:
            player_turn = not player_turn

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
