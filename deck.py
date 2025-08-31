import pygame
import random
import os

class Deck:
    def __init__(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
                 "Jack", "Queen", "King", "Ace"]
        self.cards = [f"{rank} of {suit}" for suit in suits for rank in ranks]
        self.images = {}
        self.load_card_images()
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n=1):
        if n > len(self.cards):
            return []
        drawn = self.cards[:n]
        self.cards = self.cards[n:]
        return drawn

    def put_back(self, card):
        self.cards.append(card)

    def load_card_images(self, path="card_images/PNG/Cards (medium)"):
        self.images = {}
        for filename in os.listdir(path):
            if filename.endswith(".png"):
                key = filename.replace(".png", "")
                img = pygame.image.load(os.path.join(path, filename)).convert_alpha()
                img = pygame.transform.scale(img, (100, 145))  # scale to fit boxes
                self.images[key] = img

    def invert_card_colors(self, card_key):
        """Return a new surface with inverted colors"""
        card_img = self.images[card_key]
        inverted = pygame.Surface(card_img.get_size(), pygame.SRCALPHA)
        arr = pygame.surfarray.array3d(card_img)
        inv_arr = 255 - arr
        alpha = pygame.surfarray.array_alpha(card_img)
        pygame.surfarray.blit_array(inverted, inv_arr)
        pygame.surfarray.use_arraytype('numpy')  # ensure numpy is used
        pygame.surfarray.pixels_alpha(inverted)[:, :] = alpha  # restore alpha

        self.images[card_key] = inverted


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



# Example usage:
if __name__ == "__main__":
    deck = Deck()
    print(f"Deck has {len(deck)} cards.")
    hand = deck.draw(5)
    print("You drew:", hand)
    print(f"Deck now has {len(deck)} cards.")
