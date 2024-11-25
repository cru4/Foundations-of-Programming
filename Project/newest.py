import random
import tkinter as tk

# Define card values
def card_value(card):
    rank = card[:-1]
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def adjust_for_ace(hand):
    total = sum(card_value(card) for card in hand)
    ace_count = sum(1 for card in hand if card.startswith('A'))
    while total > 21 and ace_count:
        total -= 10
        ace_count -= 1
    return total

def deal_card(deck):
    return deck.pop()

def calculate_hand_value(hand):
    return adjust_for_ace(hand)

def create_deck():
    suits = ['♥', '♦', '♣', '♠']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f'{rank}{suit}' for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

class Player:
    def __init__(self, name, balance=1000):
        self.name = name
        self.balance = balance
        self.hand = []
        self.bet = 0
        self.standing = False
        self.blackjack = False

    def reset_hand(self):
        self.hand = []
        self.bet = 0
        self.standing = False
        self.blackjack = False

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.master.geometry("800x600")

        self.players = []
        self.dealer_hand = []
        self.deck = create_deck()
        self.current_player_index = 0
        self.phase = "betting"  # Current phase: "betting", "gameplay", or "dealer"

        self.setup_players()
        self.create_widgets()
        self.reset_game()

    def setup_players(self):
        """Initialize players."""
        self.players.append(Player("Player 1"))
        self.players.append(Player("Player 2"))
        self.players.append(Player("Player 3"))

    def create_widgets(self):
        """Set up GUI elements."""
        self.title_label = tk.Label(self.master, text="Welcome to Blackjack", font=("Helvetica", 24))
        self.title_label.pack(pady=10)

        self.dealer_label = tk.Label(self.master, text="Dealer: ???", font=("Helvetica", 18))
        self.dealer_label.pack()

        self.players_frame = tk.Frame(self.master)
        self.players_frame.pack(pady=10)
        self.player_labels = []
        for player in self.players:
            label = tk.Label(self.players_frame, text=f"{player.name}: Balance: ${player.balance}", font=("Helvetica", 16))
            label.pack()
            self.player_labels.append(label)

        self.actions_frame = tk.Frame(self.master)
        self.actions_frame.pack(pady=20)

        self.hit_button = tk.Button(self.actions_frame, text="Hit", command=self.hit, font=("Helvetica", 16))
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.actions_frame, text="Stand", command=self.stand, font=("Helvetica", 16))
        self.stand_button.grid(row=0, column=1, padx=10)

        self.double_button = tk.Button(self.actions_frame, text="Double Down", command=self.double_down, font=("Helvetica", 16))
        self.double_button.grid(row=0, column=2, padx=10)

        self.bet_frame = tk.Frame(self.master)
        self.bet_frame.pack(pady=20)
        self.bet_buttons = []
        for amount in [25, 50, 100, 250, 500, 1000]:
            button = tk.Button(self.bet_frame, text=f"${amount}", command=lambda a=amount: self.place_bet(a), font=("Helvetica", 16))
            button.pack(side=tk.LEFT, padx=5)
            self.bet_buttons.append(button)

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=20)

        self.continue_button = tk.Button(self.master, text="Continue", command=self.reset_game, font=("Helvetica", 16), state=tk.DISABLED)
        self.continue_button.pack(pady=10)

    def reset_game(self):
        """Reset the game state for a new round."""
        self.deck = create_deck()
        self.dealer_hand = []
        for player in self.players:
            player.reset_hand()
        self.current_player_index = 0
        self.phase = "betting"
        self.update_gui()
        self.result_label.config(text="Place your bets!")
        self.bet_frame.pack()
        self.actions_frame.pack_forget()
        self.continue_button.config(state=tk.DISABLED)

    def place_bet(self, amount):
        """Handle a player's bet."""
        if self.phase != "betting":
            return
        player = self.players[self.current_player_index]
        if player.balance >= amount:
            player.bet = amount
            player.balance -= amount
            self.result_label.config(text=f"{player.name} bet ${amount}.")
            self.update_gui()
            self.current_player_index += 1
            if self.current_player_index >= len(self.players):
                self.phase = "gameplay"
                self.current_player_index = 0
                self.deal_initial_cards()
            else:
                self.result_label.config(text=f"{self.players[self.current_player_index].name}, place your bet.")
        else:
            self.result_label.config(text=f"{player.name} doesn't have enough balance!")

    def remove_broke_players(self):
        """Remove players with zero balance."""
        self.players = [player for player in self.players if player.balance > 0]
        if not self.players:
            self.result_label.config(text="All players are out of money! Game over.")
            self.bet_frame.pack_forget()
            self.actions_frame.pack_forget()
            self.continue_button.config(state=tk.DISABLED)
            return False
        return True

    def deal_initial_cards(self):
        """Deal two cards to each player and the dealer."""
        if not self.remove_broke_players():
            return
        for player in self.players:
            player.hand = [deal_card(self.deck), deal_card(self.deck)]
        self.dealer_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.update_gui()
        self.check_blackjack()

    def check_blackjack(self):
        """Check for blackjack and handle payouts."""
        for player in self.players:
            if calculate_hand_value(player.hand) == 21:
                player.blackjack = True
                winnings = int(player.bet * 1.5)
                player.balance += winnings
                self.result_label.config(text=f"{player.name} has Blackjack and wins ${winnings}!")
        self.start_player_turn()

    def start_player_turn(self):
        """Start the turn for the current player."""
        if not self.remove_broke_players():
            return
        self.phase = "gameplay"
        if self.current_player_index >= len(self.players):
            self.start_dealer_turn()
            return
        player = self.players[self.current_player_index]
        if player.blackjack or calculate_hand_value(player.hand) == 21:
            self.result_label.config(text=f"{player.name} has a natural 21. Moving on.")
            self.current_player_index += 1
            self.start_player_turn()
            return
        self.result_label.config(text=f"{player.name}'s turn. Choose an action.")
        self.actions_frame.pack()
        self.bet_frame.pack_forget()

    def hit(self):
        """Player hits and receives another card."""
        player = self.players[self.current_player_index]
        player.hand.append(deal_card(self.deck))
        self.update_gui()
        if calculate_hand_value(player.hand) > 21:
            self.result_label.config(text=f"{player.name} busts!")
            self.next_player_turn()

    def stand(self):
        """Player stands and ends their turn."""
        self.result_label.config(text=f"{self.players[self.current_player_index].name} stands.")
        self.next_player_turn()

    def double_down(self):
        """Player doubles their bet and receives one more card."""
        player = self.players[self.current_player_index]
        if player.balance >= player.bet:
            player.balance -= player.bet
            player.bet *= 2
            player.hand.append(deal_card(self.deck))
            self.result_label.config(text=f"{player.name} doubles down!")
            self.update_gui()
            if calculate_hand_value(player.hand) > 21:
                self.result_label.config(text=f"{player.name} busts after doubling down!")
            self.next_player_turn()
        else:
            self.result_label.config(text=f"{player.name} doesn't have enough balance to double down!")

    def next_player_turn(self):
        """Transition to the next player's turn."""
        self.current_player_index += 1
        if self.current_player_index >= len(self.players):
            self.start_dealer_turn()
        else:
            self.start_player_turn()

    def start_dealer_turn(self):
        """Dealer plays after all players finish."""
        self.phase = "dealer"
        self.result_label.config(text="Dealer's turn.")
        while calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card(self.deck))
        self.update_gui()
        self.calculate_results()

    def calculate_results(self):
        """Determine results for all players."""
        dealer_total = calculate_hand_value(self.dealer_hand)
        results = []
        for player in self.players:
            player_total = calculate_hand_value(player.hand)
            if player_total > 21:
                results.append(f"{player.name} busts and loses ${player.bet}.")
            elif dealer_total > 21 or player_total > dealer_total:
                winnings = player.bet * 2
                player.balance += winnings
                results.append(f"{player.name} wins ${winnings}!")
            elif player_total == dealer_total:
                player.balance += player.bet
                results.append(f"{player.name} ties and gets their bet back.")
            else:
                results.append(f"{player.name} loses ${player.bet}.")
        self.result_label.config(text="\n".join(results))
        self.continue_button.config(state=tk.NORMAL)

    def update_gui(self):
        """Update GUI elements with current game state."""
        self.dealer_label.config(text=f"Dealer: {', '.join(self.dealer_hand[:1])}, ???" if self.phase != "dealer" else f"Dealer: {', '.join(self.dealer_hand)}")
        for i, player in enumerate(self.players):
            hand_display = ", ".join(player.hand) if player.hand else "No cards"
            self.player_labels[i].config(text=f"{player.name}: {hand_display} | Balance: ${player.balance} | Bet: ${player.bet}")

    def quit_fullscreen(self, event=None):
        """Exit fullscreen."""
        self.master.attributes('-fullscreen', False)
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
