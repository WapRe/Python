import random

class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.value} of {self.suit}"

class Deck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in ['Hearts', 'Diamonds', 'Clubs', 'Spades'] for value in range(2, 15)]

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

class Hand:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def calculate_value(self):
        value = 0
        aces = 0
        for card in self.cards:
            if card.value >= 10 and card.value <= 13:
                value += 10
            elif card.value == 14:
                aces += 1
                value += 11
            else:
                value += card.value

        while value > 21 and aces:
            value -= 10
            aces -= 1

        return value

class Game:
    def __init__(self):
        self.deck = Deck()
        self.player_hand = Hand()
        self.dealer_hand = Hand()
        self.max_account = 1000
        self.player_account = self.max_account

    def play_round(self):
        self.deck.shuffle()
        self.player_hand.cards = [self.deck.deal(), self.deck.deal()]
        self.dealer_hand.cards = [self.deck.deal(), self.deck.deal()]

        print("Player's cards:", ', '.join(str(card) for card in self.player_hand.cards))
        print("Player's hand value:", self.player_hand.calculate_value())
        print("Dealer's face-up card:", self.dealer_hand.cards[0])

        if self.player_account <= 0:
            print("You don't have enough balance to play.")
            return

        while True:
            try:
                bet = int(input(f"Place your bet (Current balance: {self.player_account}): "))
                if bet > self.player_account or bet <= 0:
                    raise ValueError("Invalid bet")
                break
            except ValueError as e:
                print(e, ". Please place a valid bet.")

        player_turn = True
        round_outcome = None
        while player_turn:
            action = input("Do you want to Hit or Stay? ").lower()
            if action == "hit":
                card = self.deck.deal()
                self.player_hand.add_card(card)
                print("You got:", card)
                print("Player's hand value:", self.player_hand.calculate_value())
                if self.player_hand.calculate_value() > 21:
                    print("Busted! You lose.")
                    self.player_account -= bet
                    round_outcome = "lose"
                    break
            else:
                player_turn = False

        if not round_outcome:
            while self.dealer_hand.calculate_value() < 17:
                self.dealer_hand.add_card(self.deck.deal())

            player_value = self.player_hand.calculate_value()
            dealer_value = self.dealer_hand.calculate_value()

            print("Player's hand value:", player_value)
            print("Dealer's hand value:", dealer_value)

            if dealer_value > 21 or player_value > dealer_value:
                print("You win!")
                self.player_account += bet
            elif player_value == dealer_value:
                print("It's a draw!")
            else:
                print("You lose!")
                self.player_account -= bet


    def play_game(self):
        while self.player_account > 0:
            self.play_round()
            print(f"Your balance is now {self.player_account}")
            if self.player_account > 0:
                play_again = input("Do you want to play again? (y/n) ").lower()
                if play_again != "y":
                    print("Thanks for playing!")
                    break
            else:
                print("You don't have enough balance to continue. Thanks for playing!")
                break

if __name__ == "__main__":
    game = Game()
    game.play_game()