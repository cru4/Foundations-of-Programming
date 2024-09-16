import random    
import unicodedata

# Define card values
def card_value(card):
    if card in ['J', 'Q', 'K']:
        return 10
    elif card == 'A':
        return 11  # Initially treat Ace as 11
    else:
        return int(card)

# Adjust Ace value if necessary
def adjust_for_ace(hand):
    total = sum([card_value(card) for card in hand])
    if total > 21 and 'A' in hand:
        total -= 10  # Change Ace value from 11 to 1
    return total

# Deal a card
def deal_card(deck):
    return deck.pop()

# Calculate the total value of a hand
def calculate_hand_value(hand):
    return adjust_for_ace(hand)

# Create and shuffle the deck
def create_deck():
    deck = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
    random.shuffle(deck)
    return deck

# Display hand
def display_hand(hand, owner="Player"):
    print(f"{owner}'s hand: {', '.join(hand)}")

# Player's turn
def player_turn(deck, player_hand):
    while True:
        display_hand(player_hand, "Player")
        total = calculate_hand_value(player_hand)
        print(f"Player's total: {total}")
        
        if total > 21:
            print("Player busts! You lose.")
            return False
        
        choice = input("Do you want to 'hit' or 'stand'? ").lower()
        if choice == 'hit':
            player_hand.append(deal_card(deck))
        elif choice == 'stand':
            break
        else:
            print("Invalid choice. Please choose 'hit' or 'stand'.")
    
    return True

# Dealer's turn
def dealer_turn(deck, dealer_hand):
    print("\nDealer reveals their hidden card.")
    display_hand(dealer_hand, "Dealer")
    
    while calculate_hand_value(dealer_hand) < 17:
        dealer_hand.append(deal_card(deck))
        display_hand(dealer_hand, "Dealer")
    
    total = calculate_hand_value(dealer_hand)
    print(f"Dealer's total: {total}")
    
    if total > 21:
        print("Dealer busts! You win.")
        return False
    
    return True

# Determine the winner
def determine_winner(player_hand, dealer_hand):
    player_total = calculate_hand_value(player_hand)
    dealer_total = calculate_hand_value(dealer_hand)
    
    if player_total > dealer_total:
        print("Player wins!")
    elif player_total < dealer_total:
        print("Dealer wins!")
    else:
        print("It's a tie!")

# Main game function
def play_blackjack():
    print("Welcome to Blackjack!")
    
    # Create and shuffle the deck
    deck = create_deck()
    
    # Deal initial cards
    player_hand = [deal_card(deck), deal_card(deck)]
    dealer_hand = [deal_card(deck), deal_card(deck)]
    
    # Show player's hand and dealer's visible card
    display_hand(player_hand, "Player")
    print(f"Dealer's visible card: {dealer_hand[0]}")
    
    # Player's turn
    if player_turn(deck, player_hand):
        # Dealer's turn
        if dealer_turn(deck, dealer_hand):
            # Determine the winner
            determine_winner(player_hand, dealer_hand)

# Play the game
play_blackjack()

def play_again():
    while True:
        play_blackjack()
        play_again = input("Play again? ('Yes' or 'no') ").lower()
        if play_again != 'yes':
            print("Thanks for playing!")
            break
    
play_again()

