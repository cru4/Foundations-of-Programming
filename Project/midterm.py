import random  # Random numbers for dealing 
import unicodedata  # For suits 

# Define card values
def card_value(card):
    rank = card[:-1]  # Allow hand values to be calculated since the suit was getting in the way of that function
    if rank in ['J', 'Q', 'K']:
        return 10
    elif rank == 'A':
        return 11  # Initially treat Ace as 11
    else:
        return int(rank)

# Adjust Ace value if necessary
def adjust_for_ace(hand):
    total = sum([card_value(card) for card in hand])
    ace_count = sum(1 for card in hand if card.startswith('A'))  # Count the number of Aces

    # Adjust Ace value from 11 to 1 as long as total is over 21 and there are Aces to adjust
    while total > 21 and ace_count:
        total -= 10
        ace_count -= 1  # Reduce the number of Aces that can be adjusted

    return total

# Deal a card
def deal_card(deck):
    return deck.pop()

# Calculate the total value of a hand
def calculate_hand_value(hand):
    return adjust_for_ace(hand)

# Create and shuffle the deck
def create_deck():
    suits = ['♥', '♦', '♣', '♠']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck = [f'{rank}{suit}' for suit in suits for rank in ranks]
    random.shuffle(deck)
    return deck

# Display hand
def display_hand(hand, owner="Player"):
    print(f"{owner}'s hand: {', '.join(hand)}")

# Betting
def player_turn(deck, player_hand, player_balance, bet):
    while True:
        display_hand(player_hand, "Player")
        total = calculate_hand_value(player_hand)
        print(f"Player's total: {total}")

        if total == 21:
            break

        if total > 21:
            player_balance -= bet
            print(f"Player busts! You lose. Your new balance is: ${player_balance}")
            return False, player_balance
        
        choice = input("Do you want to 'hit' or 'stand'? ").lower()
        if choice == 'hit':
            player_hand.append(deal_card(deck))
        elif choice == 'stand':
            break
        else:
            print("Invalid choice. Please choose 'hit' or 'stand'.")

    return True, player_balance

# Dealer's turn
def dealer_turn(deck, dealer_hand, player_balance, bet):
    print("\nDealer reveals their hidden card.")
    display_hand(dealer_hand, "Dealer")

    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        display_hand(dealer_hand, "Dealer")

    total = calculate_hand_value(dealer_hand)
    print(f"Dealer's total: {total}")

    if total > 21:
        player_balance += bet
        print(f"Dealer busts! You win. Your new balance is: ${player_balance}")
        return False, player_balance

    return True, player_balance

# Determine the winner
def determine_winner(player_hand, dealer_hand, player_balance, bet):
    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)

    if player_total > dealer_total:
        player_balance += bet
        print(f"Player wins! Your new balance is: ${player_balance}")
    elif player_total < dealer_total:
        player_balance -= bet
        print(f"Dealer wins! Your new balance is: ${player_balance}")
    else:
        print(f"It's a tie! Your balance remains: ${player_balance}")

    return player_balance

# Main game function
def play_blackjack():
    print("Welcome to Blackjack!")
    
    player_balance = 1000  # Starting balance

    while True:
        if player_balance <= 0:
            print("You are out of money! Game over.")
            play_again = input("Would you like to play again? ('Yes' or 'No') ").lower()
            if play_again == 'yes':
                print("New game!")
                player_balance = 1000  # Reset balance for new game
                continue  # Restart the game loop
            else:
                print("Thanks for playing!")
                break
        
        try:
            bet = int(input(f"Your balance is ${player_balance}. Place your bet: $"))
            if bet > player_balance or bet <= 0:
                print(f"Invalid bet amount. Your balance is ${player_balance}.")
                continue
        except ValueError:
            print("Please enter a valid number.")
            continue

        # Create and shuffle the deck
        deck = create_deck()

        # Deal initial cards
        player_hand = [deal_card(deck), deal_card(deck)]  # Player's hand
        dealer_hand = [deal_card(deck), deal_card(deck)]  # Dealer's hand

        # Show player's hand and dealer's visible card
        display_hand(player_hand, "Player")
        print(f"Dealer's visible card: {dealer_hand[0]}")
        
        # Player's turn
        player_still_in_game, player_balance = player_turn(deck, player_hand, player_balance, bet)
        
        # Dealer's turn and winner determination
        if player_still_in_game:
            dealer_still_in_game, player_balance = dealer_turn(deck, dealer_hand, player_balance, bet)
            if dealer_still_in_game:
                player_balance = determine_winner(player_hand, dealer_hand, player_balance, bet)
        
        # Ask to continue playing
        if player_balance > 0:
            continue_playing = input("Continue playing? ('Yes' or 'No') ").lower()
            if continue_playing != 'yes':
                print(f"Thanks for playing! Your final balance is ${player_balance}.")
                break

# Play the game
if __name__ == "__main__":
    play_blackjack()
