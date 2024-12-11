import random
import tkinter as tk
from tkinter import ttk

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
        self.hands = [[]]  # Multiple hands for splits
        self.bets = [0]  # Corresponding bets for each hand
        self.standing = [False]  # Whether each hand is standing
        self.blackjack = [False]  # Track blackjack status for each hand

    def reset_hand(self):
        self.hands = [[]]
        self.bets = [0]
        self.standing = [False]
        self.blackjack = [False]

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.master.geometry("900x700")

        self.players = []
        self.dealer_hand = []
        self.deck = create_deck()
        self.current_player_index = 0
        self.phase = "setup"  # Player setup phase

        self.create_widgets()

    def create_widgets(self):
        """Set up initial GUI elements."""
        self.title_label = tk.Label(self.master, text="Welcome to Blackjack", font=("Helvetica", 24))
        self.title_label.pack(pady=10)

        self.player_selection_frame = tk.Frame(self.master)
        self.player_selection_frame.pack(pady=20)

        tk.Label(self.player_selection_frame, text="Select Number of Players:", font=("Helvetica", 18)).pack(side=tk.LEFT, padx=10)
        self.player_count = ttk.Combobox(self.player_selection_frame, values=list(range(1, 8)), font=("Helvetica", 18), width=5)
        self.player_count.pack(side=tk.LEFT, padx=10)
        self.player_count.set(1)

        self.start_button = tk.Button(self.master, text="Start Game", command=self.start_game, font=("Helvetica", 18))
        self.start_button.pack(pady=20)

        self.dealer_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.players_frame = tk.Frame(self.master)
        self.actions_frame = tk.Frame(self.master)
        self.bet_frame = tk.Frame(self.master)

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=20)

        self.hit_button = tk.Button(self.actions_frame, text="Hit", command=self.hit, font=("Helvetica", 16))
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.actions_frame, text="Stand", command=self.stand, font=("Helvetica", 16))
        self.stand_button.grid(row=0, column=1, padx=10)

        self.double_button = tk.Button(self.actions_frame, text="Double Down", command=self.double_down, font=("Helvetica", 16))
        self.double_button.grid(row=0, column=2, padx=10)

        self.split_button = tk.Button(self.actions_frame, text="Split", command=self.split, font=("Helvetica", 16))
        self.split_button.grid(row=0, column=3, padx=10)

        for amount in [25, 50, 100, 250, 500, 1000]:
            button = tk.Button(self.bet_frame, text=f"${amount}", command=lambda a=amount: self.place_bet(a), font=("Helvetica", 16))
            button.pack(side=tk.LEFT, padx=5)

        self.continue_button = tk.Button(self.master, text="Continue", command=self.reset_game, font=("Helvetica", 16), state=tk.DISABLED)
        self.continue_button.pack(pady=10)

    def start_game(self):
        """Start the game by creating players and initializing the game state."""
        num_players = int(self.player_count.get())
        self.setup_players(num_players)

        # Hide player selection and show game elements
        self.player_selection_frame.pack_forget()
        self.start_button.pack_forget()

        self.dealer_label.pack()
        self.players_frame.pack()
        self.bet_frame.pack(pady=20)
        self.actions_frame.pack(pady=20)

        self.reset_game()

    def setup_players(self, num_players):
        """Dynamically create the specified number of players."""
        self.players = [Player(f"Player {i + 1}") for i in range(num_players)]

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
            player.bets[0] = amount
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

    def deal_initial_cards(self):
        """Deal two cards to each player and the dealer."""
        for player in self.players:
            player.hands[0] = [deal_card(self.deck), deal_card(self.deck)]
        self.dealer_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.update_gui()
        self.check_blackjack()

    def check_blackjack(self):
        """Check for blackjack in all player hands and handle payouts."""
        dealer_blackjack = calculate_hand_value(self.dealer_hand) == 21
        messages = []  # Collect messages for the GUI

        if dealer_blackjack:
            messages.append("Dealer has Blackjack!")

    # Check each player's hands for blackjack
        for player in self.players:
            for i, hand in enumerate(player.hands):
            # Check for a valid blackjack
                if calculate_hand_value(hand) == 21 and len(hand) == 2:
                    player.blackjack[i] = True
                    if dealer_blackjack:
                        messages.append(f"{player.name}'s Hand {i + 1} ties with the dealer!")
                    else:
                        winnings = int(player.bets[i] * 1.5)
                        player.balance += winnings + player.bets[i]
                        messages.append(f"{player.name}'s Hand {i + 1} wins Blackjack payout of ${winnings}!")

    # Display collected messages
        if messages:
            self.result_label.config(text="\n".join(messages))
        self.update_gui()  # Update the GUI to reflect payouts and balances

    # Transition logic
        if dealer_blackjack:
            self.phase = "dealer"
            self.calculate_results()
            messages.append ("Dealer has Blackjack")
        else:
            self.master.after(2000, self.start_player_turn)  # Delay to let the player see messages


    def calculate_results(self):
        """Determine results for all players."""
        dealer_total = calculate_hand_value(self.dealer_hand)
        results = []
        to_remove = []
        for player in self.players:
            for i, hand in enumerate(player.hands):
                if player.blackjack[i]:  # Skip hands already processed for blackjack
                    results.append(f"{player.name} has Blackjack!")
                    break

                player_total = calculate_hand_value(hand)
                if player_total > 21:
                    results.append(f"{player.name}'s Hand {i + 1} busts and loses ${player.bets[i]}.")
                elif dealer_total > 21 or player_total > dealer_total:
                    winnings = player.bets[i]
                    player.balance += winnings + player.bets[i]
                    results.append(f"{player.name}'s Hand {i + 1} wins ${winnings}!")
                elif dealer_total == player_total:
                    player.balance += player.bets[i]
                    results.append(f"{player.name}'s Hand {i + 1} ties with the dealer.")
                else:
                    results.append(f"{player.name}'s Hand {i + 1} loses ${player.bets[i]}.")

            if player.balance == 0:
                to_remove.append(player)

        for player in to_remove:
            results.append(f"{player.name} has lost all their money. Thanks for playing!")
            self.players.remove(player)

        self.result_label.config(text="\n".join(results))
        self.continue_button.config(state=tk.NORMAL)

    def start_player_turn(self):
        """Handle turn for split hands if any."""
        if self.current_player_index >= len(self.players):
            self.start_dealer_turn()
            return
        player = self.players[self.current_player_index]
        for i, hand in enumerate(player.hands):
            if player.standing[i] or calculate_hand_value(hand) == 21:
                continue
            if len(player.hands) > 1:
                self.result_label.config(
                    text=f"{player.name}'s turn. Playing hand {i + 1}. Choose an action."
                )
            else:
                self.result_label.config(
                    text=f"{player.name}'s turn. Choose an action."
                )
            self.actions_frame.pack()
            self.bet_frame.pack_forget()
            return
        self.next_player_turn()

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

    def hit(self):
        """Player hits for the current hand."""
        player = self.players[self.current_player_index]
        for i, hand in enumerate(player.hands):
            if not player.standing[i]:
                hand.append(deal_card(self.deck))
                self.update_gui()
                if calculate_hand_value(hand) > 21:
                    self.result_label.config(text=f"{player.name} busts on hand {i + 1}!")
                    player.standing[i] = True
                break
        self.start_player_turn()

    def stand(self):
        """Player stands for the current hand."""
        player = self.players[self.current_player_index]
        for i, hand in enumerate(player.hands):
            if not player.standing[i]:
                player.standing[i] = True
                self.result_label.config(
                    text=f"{player.name} stands on hand {i + 1}."
                )
                break
        self.start_player_turn()

    def double_down(self):
        """Player doubles their bet and receives one more card."""
        player = self.players[self.current_player_index]
        for i, hand in enumerate(player.hands):
            if not player.standing[i] and player.balance >= player.bets[i]:
                player.balance -= player.bets[i]
                player.bets[i] *= 2
                hand.append(deal_card(self.deck))
                self.result_label.config(text=f"{player.name} doubles down on hand {i + 1}!")
                self.update_gui()
                if calculate_hand_value(hand) > 21:
                    self.result_label.config(text=f"{player.name} busts after doubling down!")
                player.standing[i] = True
                break
        self.start_player_turn()

    def split(self):
        """Player splits their hand into two if eligible."""
        player = self.players[self.current_player_index]
        if len(player.hands) >= 4:  # Limit the number of hands to 4
            self.result_label.config(text=f"{player.name} cannot split further (max 4 hands).")
            return
        for i, hand in enumerate(player.hands):
            if len(hand) == 2 and card_value(hand[0]) == card_value(hand[1]) and player.balance >= player.bets[i]:
                player.balance -= player.bets[i]
                new_hand = [hand.pop()]  # Remove one card to form a new hand
                player.hands.append(new_hand)
                player.bets.append(player.bets[i])  # Duplicate the bet for the new hand
                player.standing.append(False)  # Initialize standing status for the new hand
                player.blackjack.append(False)  # Initialize blackjack status for the new hand
                hand.append(deal_card(self.deck))
                new_hand.append(deal_card(self.deck))
                self.result_label.config(
                    text=f"{player.name} splits hand {i + 1} into two!"
                )
                self.update_gui()
                return  # Only allow one split per action
        self.result_label.config(text="You cannot split any hand.")

    def update_player_labels(self):
        """Update player labels with split hands."""
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        self.player_labels = []
        for player in self.players:
            display_text = []
            for i, hand in enumerate(player.hands):
                hand_display = ", ".join(hand) if hand else "No cards"
                display_text.append(
                    f"Hand {i + 1}: {hand_display} | Bet: ${player.bets[i]}"
                )
            label_text = f"{player.name}: {' | '.join(display_text)} | Balance: ${player.balance}"
            label = tk.Label(
                self.players_frame,
                text=label_text,
                font=("Helvetica", 16),
            )
            label.pack()
            self.player_labels.append(label)

    def update_gui(self):
        """Update GUI elements with current game state."""
        self.dealer_label.config(
            text=f"Dealer: {', '.join(self.dealer_hand[:1])}, ???" if self.phase != "dealer" else f"Dealer: {', '.join(self.dealer_hand)}"
        )
        self.update_player_labels()


if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()