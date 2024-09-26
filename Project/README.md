# Blackjack Game
This is a simple Blackjack game implemented in Python. It allows you to play one hand of Blackjack at a time against a computer dealer. All basic rules of Blackjack apply, including Ace adjustments, however features such as betting, splitting, and doubling down have not yet been implemented.

# Features
Blackjack game (Player vs. Dealer).
Ace adjustments from value 11 to 1 if hand value > 21, function works regardless of number of Aces in hand.
Game follows basic rules (see rules section).
Player chooses whether to hit or stand.
If player has a hand value of 21, their turn automatically ends.
Player chooses whether to continue playing after each hand.

# Rules
1. Basic Rules:
At the beginning of the hand, the player and dealer are both dealt two cards, with the dealer's second card being hidden.
If player hand value > dealer hand value, player wins, and vice versa.
If player hand value = dealer hand value, it is a tie.
If hand value > 21, player or dealer busts, that hand loses.
Dealer stands at hand value 17 or higher.
2. Card Values:
Number cards are worth their numerical value.
Face cards (J,Q,K) are worth 10.
Aces are worth 11, but adjusted to be worth 1 if hand value > 21.
3. Player Actions:
Player chooses to hit (be dealt another card) or stand (keep the value of their current hand, end their turn).
Player chooses to play again (yes or no) after each hand.
4. Dealer actions:
Dealer reveals their hidden card once it is their turn, continues hitting their hand until the value = 17 or more, or they bust.

# Running the Code
1. Copy or download the code
2. Run the code from the python terminal
3. Play the game
4. Continue playing, or stop playing the game via user input (will be prompted to choose "yes" or "no").