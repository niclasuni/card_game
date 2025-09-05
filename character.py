from deck import Deck


class Character:
    def __init__(self):
        self.deck = Deck()
        self.drawn_cards = []
        self.drawn_cards.extend(self.deck.draw(3))
        self.hand = []

        self.selected_card = None
        self.selected_card_position = None
        self.deckbuilder_selected_card_key = None
        self.life = 100
        self.poison = 0
        self.shield = 0

        self.mana = 1

        self.enemy_card_start_time = 0
        self.ENEMY_DISPLAY_TIME = 750


    def calc_damage(self, card_str, enemy):
        rank_str, suit = card_str.split(" of ")

        rank_map = {
            "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7,
            "8": 8, "9": 9, "10": 10,
            "Jack": 11, "Queen": 12, "King": 13, "Ace": 14
        }
        value = rank_map.get(rank_str, None)

        self.mana -= value
        if suit == 'Clubs':
            enemy.poison += value
        elif suit == 'Spades':
            enemy.life -= value - enemy.shield if value > enemy.shield else 0
        elif suit == 'Diamonds':
            self.shield += value
        elif suit == 'Hearts':
            self.life += value

        enemy.life -= enemy.poison

        enemy.shield -= 2 if enemy.shield > 0 else 0
        self.poison -= 2 if self.poison > 0 else 0

        if self.mana < 0:
            enemy.mana = abs(self.mana)