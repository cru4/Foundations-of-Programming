import random
import tkinter as tk
from tkinter import messagebox

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

class BlackjackGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Blackjack")
        self.master.attributes('-fullscreen', True)
        self.master.bind("<Escape>", self.quit_fullscreen)
        
        self.player_balance = 1000
        self.bet = 0
        self.deck = create_deck()
        
        self.create_widgets()
        self.reset_game()  # Reset the game on start

    def create_widgets(self):
        self.title_label = tk.Label(self.master, text="Welcome to Blackjack", font=("Helvetica", 24))
        self.title_label.pack(pady=10)
        
        self.balance_label = tk.Label(self.master, text=f"Balance: ${self.player_balance}", font=("Helvetica", 18))
        self.balance_label.pack(pady=10)
        
        self.bet_label = tk.Label(self.master, text="Place your bet: ", font=("Helvetica", 18))
        self.bet_label.pack(pady=10)

        # Bet buttons
        self.bet_button_frame = tk.Frame(self.master)
        self.bet_button_frame.pack(pady=10)
        
        self.bet_25_button = tk.Button(self.bet_button_frame, text="$25", command=lambda: self.set_bet(25), font=("Helvetica", 18))
        self.bet_25_button.grid(row=0, column=0, padx=5)
        
        self.bet_50_button = tk.Button(self.bet_button_frame, text="$50", command=lambda: self.set_bet(50), font=("Helvetica", 18))
        self.bet_50_button.grid(row=0, column=1, padx=5)
        
        self.bet_100_button = tk.Button(self.bet_button_frame, text="$100", command=lambda: self.set_bet(100), font=("Helvetica", 18))
        self.bet_100_button.grid(row=0, column=2, padx=5)

        # New betting buttons
        self.bet_250_button = tk.Button(self.bet_button_frame, text="$250", command=lambda: self.set_bet(250), font=("Helvetica", 18))
        self.bet_250_button.grid(row=0, column=3, padx=5)

        self.bet_500_button = tk.Button(self.bet_button_frame, text="$500", command=lambda: self.set_bet(500), font=("Helvetica", 18))
        self.bet_500_button.grid(row=0, column=4, padx=5)

        self.bet_1000_button = tk.Button(self.bet_button_frame, text="$1000", command=lambda: self.set_bet(1000), font=("Helvetica", 18))
        self.bet_1000_button.grid(row=0, column=5, padx=5)

        self.player_hand_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.player_hand_label.pack(pady=10)

        self.dealer_hand_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.dealer_hand_label.pack(pady=10)

        self.action_frame = tk.Frame(self.master)
        self.action_frame.pack(pady=20)

        self.hit_button = tk.Button(self.action_frame, text="Hit", command=self.hit, font=("Helvetica", 18))
        self.hit_button.grid(row=0, column=0, padx=10)

        self.stand_button = tk.Button(self.action_frame, text="Stand", command=self.stand, font=("Helvetica", 18))
        self.stand_button.grid(row=0, column=1, padx=10)

        self.double_button = tk.Button(self.action_frame, text="Double Down", command=self.double_down, font=("Helvetica", 18))
        self.double_button.grid(row=0, column=2, padx=10)

        self.result_label = tk.Label(self.master, text="", font=("Helvetica", 18))
        self.result_label.pack(pady=20)

        self.continue_button = tk.Button(self.master, text="Continue Playing", command=self.continue_playing, font=("Helvetica", 18), state=tk.DISABLED)
        self.continue_button.pack(pady=10)

    def reset_game(self):
        self.player_hand = []
        self.dealer_hand = []
        self.bet = 0
        self.deck = create_deck()  # Reset the deck
        self.update_display()  # Clear displayed hands
        self.result_label.config(text="")  # Clear the result message
        self.continue_button.config(state=tk.DISABLED)  # Disable continue button
        self.action_frame.pack_forget()  # Hide action buttons
        self.enable_double_down()  # Enable or disable double down based on hand
        self.bet_button_frame.pack(pady=10)  # Show betting buttons again

    def enable_double_down(self):
        self.double_button.config(state=tk.NORMAL if len(self.player_hand) == 2 else tk.DISABLED)

    def update_display(self):
        player_total = calculate_hand_value(self.player_hand)
        self.player_hand_label.config(text=f"Your Hand: {', '.join(self.player_hand)} (Total: {player_total})")
        
        # Show only one dealer card until the player's turn is complete
        if self.dealer_hand:
            self.dealer_hand_label.config(text=f"Dealer's Hand: {self.dealer_hand[0]}, ???")
        else:
            self.dealer_hand_label.config(text="")

    def set_bet(self, amount):
        if self.player_balance >= amount and self.bet == 0:  # Allow betting only if no bet is placed
            self.bet = amount
            self.player_balance -= self.bet
            self.balance_label.config(text=f"Balance: ${self.player_balance}")
            self.start_new_game()  # Start the game after placing the bet
        else:
            # If the bet is already placed or insufficient balance, do nothing
            pass

    def start_new_game(self):
        self.player_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.dealer_hand = [deal_card(self.deck), deal_card(self.deck)]
        self.update_display()
        self.enable_double_down()  # Enable or disable double down based on hand

        player_total = calculate_hand_value(self.player_hand)
        if player_total == 21:  # Check for Blackjack
            self.result_label.config(text="Blackjack! You win!")
            self.player_balance += int(self.bet * 2.5)  # Blackjack payout
            self.balance_label.config(text=f"Balance: ${self.player_balance}")
            self.action_frame.pack_forget()  # Hide action buttons
            self.continue_button.config(state=tk.NORMAL)  # Enable continue button
            return

        self.action_frame.pack(pady=20)  # Show action buttons

    def hit(self):
        self.player_hand.append(deal_card(self.deck))
        total = calculate_hand_value(self.player_hand)
        if total > 21:
            self.result_label.config(text=f"Bust! You lost ${self.bet}.")
            self.action_frame.pack_forget()  # Hide action buttons
            self.continue_button.config(state=tk.NORMAL)  # Enable continue button
        else:
            self.update_display()
            self.enable_double_down()  # Update double down availability

    def stand(self):
        self.result_label.config(text="You chose to stand.")
        self.reveal_dealer_hand()  # Reveal dealer's hand and determine winner

    def double_down(self):
        if self.player_balance >= self.bet:  # Check if player can double down
            self.player_balance -= self.bet  # Deduct the original bet
            self.bet *= 2  # Double the bet
            self.balance_label.config(text=f"Balance: ${self.player_balance}")
            self.player_hand.append(deal_card(self.deck))  # Deal one card
            total = calculate_hand_value(self.player_hand)
            if total > 21:
                self.result_label.config(text=f"Bust! You lost ${self.bet}.")
                self.action_frame.pack_forget()  # Hide action buttons
                self.continue_button.config(state=tk.NORMAL)  # Enable continue button
            else:
                self.update_display()
                self.reveal_dealer_hand()  # Reveal dealer's hand and determine winner
        else:
            # If not enough balance, do nothing
            pass

    def reveal_dealer_hand(self):
        self.dealer_hand_label.config(text=f"Dealer's Hand: {', '.join(self.dealer_hand)} (Total: {calculate_hand_value(self.dealer_hand)})")

        # Dealer's turn to play
        while calculate_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(deal_card(self.deck))
            self.dealer_hand_label.config(text=f"Dealer's Hand: {', '.join(self.dealer_hand)} (Total: {calculate_hand_value(self.dealer_hand)})")

        self.determine_winner()  # Determine the winner

    def determine_winner(self):
        player_total = calculate_hand_value(self.player_hand)
        dealer_total = calculate_hand_value(self.dealer_hand)

        if player_total > 21:
            self.result_label.config(text=f"Bust! You lost ${self.bet}.")
        elif dealer_total > 21 or player_total > dealer_total:
            self.result_label.config(text=f"You win! You gain ${self.bet}.")
            self.player_balance += self.bet * 2  # Regular win payout
            self.balance_label.config(text=f"Balance: ${self.player_balance}")
        elif player_total == dealer_total:
            self.result_label.config(text="It's a tie! Your bet is returned.")
            self.player_balance += self.bet  # Return bet
            self.balance_label.config(text=f"Balance: ${self.player_balance}")
        else:
            self.result_label.config(text=f"You lost! You lost ${self.bet}.")

        self.action_frame.pack_forget()  # Hide action buttons
        self.continue_button.config(state=tk.NORMAL)  # Enable continue button

    def continue_playing(self):
        self.reset_game()  # Reset game for a new round

    def quit_fullscreen(self, event):
        self.master.attributes('-fullscreen', False)
        self.master.quit()

if __name__ == "__main__":
    root = tk.Tk()
    game = BlackjackGame(root)
    root.mainloop()
