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

        # Load and scale icons
        path = get_asset_path('board_game_icons/PNG/Default (64px)/skull.png')
        self.ui_poison = pygame.image.load(path)
        path = get_asset_path('board_game_icons/PNG/Default (64px)/shield.png')
        self.ui_shield = pygame.image.load(path)
        self.ui_poison = pygame.transform.scale(self.ui_poison, (20, 20))
        self.ui_shield = pygame.transform.scale(self.ui_shield, (20, 20))

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

        start_color = self.BUTTON_HOVER_COLOR if self.button_hover(300, 200, 200, 50) else self.BUTTON_COLOR
        deck_color = self.BUTTON_HOVER_COLOR if self.button_hover(300, 300, 200, 50) else self.BUTTON_COLOR
        options_color = self.BUTTON_HOVER_COLOR if self.button_hover(300, 400, 200, 50) else self.BUTTON_COLOR
        quit_color = self.BUTTON_HOVER_COLOR if self.button_hover(300, 500, 200, 50) else self.BUTTON_COLOR

        self.draw_button("Start Game", 300, 200, 200, 50, start_color)
        self.draw_button("Load Deck", 300, 300, 200, 50, deck_color)
        self.draw_button("Options", 300, 400, 200, 50, options_color)
        self.draw_button("Quit", 300, 500, 200, 50, quit_color)

    def draw_game(self, player, enemy):
        screen = self.screen
        font = self.font
        WIDTH = self.WIDTH
        HEIGHT = self.HEIGHT

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

    def draw_win_screen(self):
        win_text = self.font.render("YOU WIN!", True, self.WHITE)
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