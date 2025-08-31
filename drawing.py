import pygame

class UI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(None, 32)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.BUTTON_COLOR = (0, 128, 255)
        self.BUTTON_HOVER_COLOR = (0, 255, 255)

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
        options_color = self.BUTTON_HOVER_COLOR if self.button_hover(300, 300, 200, 50) else self.BUTTON_COLOR
        quit_color = self.BUTTON_HOVER_COLOR if self.button_hover(300, 400, 200, 50) else self.BUTTON_COLOR

        self.draw_button("Start Game", 300, 200, 200, 50, start_color)
        self.draw_button("Options", 300, 300, 200, 50, options_color)
        self.draw_button("Quit", 300, 400, 200, 50, quit_color)


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