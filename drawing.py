import pygame
import sys
import os

def get_asset_path(relative_path):
    """ Get the absolute path to an asset, works for dev and for PyInstaller bundled exe """
    if hasattr(sys, '_MEIPASS'):
        # Running as a bundled executable
        base_path = sys._MEIPASS
    else:
        # Running in normal Python environment
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def card_name_to_filename(card_name):
    """Convert 'Ace of Spades' -> 'card_spades_A'"""
    rank_map = {
        "2": "02", "3": "03", "4": "04", "5": "05", "6": "06", "7": "07",
        "8": "08", "9": "09", "10": "10",
        "Jack": "J",  # ← map face cards
        "Queen": "Q",
        "King": "K",
        "Ace": "A"
    }
    suit_map = {
        "Hearts": "hearts",
        "Diamonds": "diamonds",
        "Clubs": "clubs",
        "Spades": "spades"
    }
    rank, _, suit = card_name.partition(" of ")
    return f"card_{suit_map[suit]}_{rank_map[rank]}"

class UI:
    def __init__(self, screen, width=1280, height=720):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 32)

        self.WIDTH = width
        self.HEIGHT = height

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_COLOR = (0, 128, 255)
        self.BUTTON_HOVER_COLOR = (0, 255, 255)

        # Button setup
        self.button_rect = pygame.Rect(0, 0, 150, 50)
        self.reverse_button_rect = pygame.Rect(0, 0, 150, 50)
        self.play_button_rect = pygame.Rect(0, 0, 150, 50)

        self.button_color = (70, 130, 180)
        self.button_hover_color = (100, 160, 210)

        self.new_card_deck = None
        self.new_card_index = 0
        self.deckbuilder_index = None

        # Load and scale icons
        path = get_asset_path('board_game_icons/PNG/Default (64px)/skull.png')
        self.ui_poison = pygame.image.load(path)
        path = get_asset_path('board_game_icons/PNG/Default (64px)/shield.png')
        self.ui_shield = pygame.image.load(path)
        self.ui_poison = pygame.transform.scale(self.ui_poison, (20, 20))
        self.ui_shield = pygame.transform.scale(self.ui_shield, (20, 20))

        self.clock = pygame.time.Clock()

    def display_fps(self):
        # Get the current FPS
        fps = self.clock.get_fps()

        # Render the FPS as text
        fps_text = self.font.render(f"FPS: {fps:.4f}", True, (0, 0, 0))  # White color

        # Draw the FPS text in the top-right corner
        self.screen.blit(fps_text, (self.screen.get_width() - 120, 10))

    def draw_button(self, text, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, (x, y, width, height))
        label = self.font.render(text, True, self.BLACK)
        self.screen.blit(label, (x + (width - label.get_width()) // 2, y + (height - label.get_height()) // 2))

    # Check if mouse is over a button
    def button_hover(self, x, y, width, height):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        return x <= mouse_x <= x + width and y <= mouse_y <= y + height

    def draw_main(self):
        self.screen.fill(self.WHITE)
        self.display_fps()

        start_color = self.BUTTON_HOVER_COLOR if self.button_hover(150, 200, 200, 50) else self.BUTTON_COLOR
        deck_color = self.BUTTON_HOVER_COLOR if self.button_hover(150, 300, 200, 50) else self.BUTTON_COLOR
        loader_color = self.BUTTON_HOVER_COLOR if self.button_hover(150, 400, 200, 50) else self.BUTTON_COLOR
        options_color = self.BUTTON_HOVER_COLOR if self.button_hover(150, 500, 200, 50) else self.BUTTON_COLOR
        quit_color = self.BUTTON_HOVER_COLOR if self.button_hover(150, 600, 200, 50) else self.BUTTON_COLOR

        self.draw_button("Start Game", 150, 200, 200, 50, start_color)
        self.draw_button("Deckbuilder", 150, 300, 200, 50, deck_color)
        self.draw_button("Load Deck", 150, 400, 200, 50, loader_color)
        self.draw_button("Options", 150, 500, 200, 50, options_color)
        self.draw_button("Quit", 150, 600, 200, 50, quit_color)

    def draw_deck_builder(self, player):
        CARD_WIDTH = 50
        CARD_HEIGHT = 70
        CARD_MARGIN = 10

        # Loop over the card slots and display images
        for i, image in enumerate(player.deck.cards):
            # Calculate the grid position
            row = i // 13  # 4 rows, each with 13 cards
            col = i % 13  # 13 columns
            x_pos = col * (CARD_WIDTH + CARD_MARGIN) + CARD_MARGIN + 400
            y_pos = row * (CARD_HEIGHT + CARD_MARGIN) + CARD_MARGIN

            card_key = card_name_to_filename(image)
            card_img = player.deck.images.get(card_key)
            self.screen.blit(card_img, (x_pos, y_pos))
            if self.deckbuilder_index == i:
                card_rect = card_img.get_rect(topleft=(x_pos+1, y_pos+3))
                card_rect = card_rect.inflate(-27, -4)
                pygame.draw.rect(self.screen, (255, 215, 0), card_rect, 5)

            if pygame.mouse.get_pressed()[0]:  # Left mouse click
                mouse_pos = pygame.mouse.get_pos()
                card_rect = pygame.Rect(x_pos, y_pos, CARD_WIDTH, CARD_HEIGHT)

                if card_rect.collidepoint(mouse_pos):
                    player.deckbuilder_selected_card_key = card_key
                    self.deckbuilder_index = row * 13 + col

        if player.deckbuilder_selected_card_key:
            self.card_modifier(player)
            self.draw_swap_menu(player)

    def card_modifier(self, player):

        if self.new_card_deck is None:
            self.new_card_deck = player.deck.create_new_deck()

        enlarged_x_pos = self.screen.get_width() // 2 - 150 // 2  # Center horizontally
        enlarged_y_pos = self.screen.get_height() - 250  # Position a little above the bottom
        card_img = player.deck.images.get(player.deckbuilder_selected_card_key)
        self.screen.blit(pygame.transform.scale(card_img, (150, 150)), (enlarged_x_pos, enlarged_y_pos))

        level_color = self.BUTTON_HOVER_COLOR if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos, 200, 50) else self.BUTTON_COLOR
        swap_color = self.BUTTON_HOVER_COLOR if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos+50, 200, 50) else self.BUTTON_COLOR
        reverse_color = self.BUTTON_HOVER_COLOR if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos+100, 200, 50) else self.BUTTON_COLOR
        save_color = self.BUTTON_HOVER_COLOR if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos+150, 200, 50) else self.BUTTON_COLOR

        self.draw_button("Level Up", enlarged_x_pos + 200, enlarged_y_pos, 200, 50, level_color)
        self.draw_button("Swap", enlarged_x_pos + 200, enlarged_y_pos+50, 200, 50, swap_color)
        self.draw_button("Reverse", enlarged_x_pos + 200, enlarged_y_pos+100, 200, 50, reverse_color)
        self.draw_button("Save", enlarged_x_pos + 200, enlarged_y_pos+150, 200, 50, save_color)

        for event in pygame.event.get():  # Left mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                # LEVEL UP
                if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos, 200, 50):
                    print('LEVEL UP')
                # SWAP
                if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos + 50, 200, 50):
                    print('SWAP')
                    swapped_in = player.deck.swap_card(player.deckbuilder_selected_card_key, self.deckbuilder_index, self.new_card_deck[self.new_card_index])
                    print(swapped_in)
                    player.deckbuilder_selected_card_key = card_name_to_filename(swapped_in)
                # REVERSE
                if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos + 100, 200, 50):
                    # card_key = card_name_to_filename(player.deckbuilder_selected_card_image)
                    if player.deckbuilder_selected_card_key in player.deck.images:
                        player.deck.invert_card_colors(player.deckbuilder_selected_card_key)

                # SAVE
                if self.button_hover(enlarged_x_pos + 200, enlarged_y_pos + 150, 200, 50):
                    player.deckbuilder_selected_card_key = None

                # ARROW LEFT
                if self.button_hover(1039, 535, 50, 50):
                    self.new_card_index -= 1
                    if self.new_card_index < 0:
                        self.new_card_index = len(player.deck.cards) - self.new_card_index
                if self.button_hover(1165, 535, 50, 50):
                    self.new_card_index += 1
                    if self.new_card_index > len(player.deck.cards) - 1:
                        self.new_card_index = 0


    def draw_swap_menu(self, player):
        enlarged_x_pos = self.screen.get_width() // 2 + 450 // 2  # Center horizontally
        enlarged_y_pos = self.screen.get_height() - 250  # Position a little above the bottom
        swap_card = self.new_card_deck[self.new_card_index]
        card_key = card_name_to_filename(swap_card)
        card_img = player.deck.images.get(card_key)
        self.screen.blit(pygame.transform.scale(card_img, (150, 150)), (enlarged_x_pos + 174, enlarged_y_pos))

        # Arrows
        center_back = pygame.Vector2(enlarged_x_pos + 199, enlarged_y_pos + 65)
        end_back = pygame.Vector2(enlarged_x_pos + 174, enlarged_y_pos + 65)
        center_forward = pygame.Vector2(enlarged_x_pos + 300, enlarged_y_pos + 65)
        end_forward = pygame.Vector2(enlarged_x_pos + 325, enlarged_y_pos + 65)
        draw_arrow(self.screen, center_back, end_back, pygame.Color(0, 0, 0), 10, 20, 12)
        draw_arrow(self.screen, center_forward, end_forward, pygame.Color(0, 0, 0), 10, 20, 12)

    def draw_game(self, player, enemy):
        screen = self.screen
        font = self.font
        WIDTH = self.WIDTH
        HEIGHT = self.HEIGHT

        self.display_fps()

        # --- Mana ---
        circle_radius = 10
        circle_spacing = 25
        num_circles_player = player.mana
        num_circles_enemy = enemy.mana

        # Draw the line of circles
        y = HEIGHT / 2 - circle_radius / 2 + 15
        for i in range(num_circles_player):
            x = 50 + i * circle_spacing
            pygame.draw.circle(screen, (0, 0, 0), (x, y), circle_radius)
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(50, y, 15 * circle_spacing + circle_radius * 2, circle_radius * 2), 2)

        y = HEIGHT / 2 - circle_radius / 2 - 15
        for i in range(num_circles_enemy):
            x = 50 + i * circle_spacing
            pygame.draw.circle(screen, (0, 0, 0), (x, y), circle_radius)
        pygame.draw.rect(screen, (0, 0, 0),
                         pygame.Rect(50, y, 15 * circle_spacing + circle_radius * 2, circle_radius * 2), 2)

        # --- Lifebars ---
        lifebar_player = pygame.Rect(0, 0, 30, player.life)
        lifebar_player.bottomleft = (20, HEIGHT - 25)

        lifebar_enemy = pygame.Rect(0, 0, 30, enemy.life)
        lifebar_enemy.topleft = (20, 25)

        screen.blit(self.ui_poison, (70, HEIGHT - 5 - 20))
        screen.blit(self.ui_shield, (120, HEIGHT - 5 - 20))
        screen.blit(self.ui_poison, (70, 2))
        screen.blit(self.ui_shield, (120, 2))

        pygame.draw.rect(screen, (255, 255, 255), lifebar_player, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), lifebar_enemy, border_radius=10)

        # --- Player Text ---
        self.draw_value_text(font, str(player.life), lifebar_player.centerx, lifebar_player.bottom + 12, (255, 255, 255))
        self.draw_value_text(font, str(player.poison), lifebar_player.right + 50, lifebar_player.bottom + 12, (0, 0, 0))
        self.draw_value_text(font, str(player.shield), lifebar_player.right + 100, lifebar_player.bottom + 12, (0, 0, 0))

        # --- Enemy Text ---
        self.draw_value_text(font, str(enemy.life), lifebar_enemy.centerx, lifebar_enemy.top - 12, (255, 255, 255))
        self.draw_value_text(font, str(enemy.poison), lifebar_enemy.right + 50, lifebar_enemy.top - 12, (0, 0, 0))
        self.draw_value_text(font, str(enemy.shield), lifebar_enemy.right + 100, lifebar_enemy.top - 12, (0, 0, 0))

        # --- Buttons ---
        mouse_pos = pygame.mouse.get_pos()

        # Draw Card Button
        self.button_rect.topright = (WIDTH - 20, HEIGHT - 70)
        color = self.button_hover_color if self.button_rect.collidepoint(mouse_pos) else self.button_color
        self.draw_button("Draw Card", self.button_rect.x, self.button_rect.y, self.button_rect.width, self.button_rect.height, color)

        # Reverse Button
        self.reverse_button_rect.topright = (WIDTH - 20, HEIGHT - 140)
        color = self.button_hover_color if self.reverse_button_rect.collidepoint(mouse_pos) else self.button_color
        self.draw_button("Reverse", self.reverse_button_rect.x, self.reverse_button_rect.y, self.reverse_button_rect.width, self.reverse_button_rect.height, color)

        # Play Button
        self.play_button_rect.topright = (WIDTH - 200, HEIGHT - 140)
        color = self.button_hover_color if self.play_button_rect.collidepoint(mouse_pos) else self.button_color
        self.draw_button("Play", self.play_button_rect.x, self.play_button_rect.y, self.play_button_rect.width, self.play_button_rect.height, color)


    def draw_value_text(self, font, text, x, y, color):
        value_text = font.render(text, True, color)
        text_rect = value_text.get_rect(center=(x, y))
        self.screen.blit(value_text, text_rect)

    def draw_end_screen(self, player_won):
        win_text = self.font.render(f"YOU {'WIN' if player_won else 'LOSE'}!", True, self.WHITE)
        sub_text = self.font.render("Press any key to exit...", True, self.WHITE)
        self.screen.fill(self.BLACK)
        self.screen.blit(win_text, (self.WIDTH // 2 - win_text.get_width() // 2, self.HEIGHT // 3))
        self.screen.blit(sub_text, (self.WIDTH // 2 - sub_text.get_width() // 2, self.HEIGHT // 2))


def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 2,
        head_width: int = 4,
        head_height: int = 2,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)