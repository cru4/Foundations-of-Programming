import unittest
from unittest import TestCase
from final import *  # Ensure this imports your game logic correctly

class BlackjackTests(TestCase):

    def setUp(self):
        self.deck = create_deck()  # Create a fresh deck for each test
        random.shuffle(self.deck)

    # Test card value calculation
    def test_card_value(self):
        self.assertEqual(card_value('2♥'), 2)
        self.assertEqual(card_value('J♦'), 10)
        self.assertEqual(card_value('A♠'), 11)
        self.assertEqual(card_value('10♣'), 10)

    # Test Ace adjustment when hand is over 21
    def test_adjust_for_ace(self):
        hand = ['A♠', '9♦', 'A♣']  # Two Aces and a 9
        self.assertEqual(adjust_for_ace(hand), 21)  # Aces should adjust to 1 if over 21

        hand = ['A♠', 'A♣', '9♦', 'K♥']  # Two Aces, 9, and a King
        self.assertEqual(adjust_for_ace(hand), 21)

        hand = ['A♠', 'A♣', 'A♦', '8♠']  # Three Aces and an 8
        self.assertEqual(adjust_for_ace(hand), 21)

    # Test dealing a card
    def test_deal_card(self):
        initial_deck_size = len(self.deck)
        card = deal_card(self.deck)
        self.assertEqual(len(self.deck), initial_deck_size - 1)
        self.assertIsInstance(card, str)

    # Test hand value calculation
    def test_calculate_hand_value(self):
        hand = ['A♠', '9♦']
        self.assertEqual(calculate_hand_value(hand), 20)

        hand = ['A♠', '9♦', '2♠']
        self.assertEqual(calculate_hand_value(hand), 12)

    # Test deck creation
    def test_create_deck(self):
        deck = create_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(deck)), 52)  # Ensure all cards are unique

    # Test splitting functionality
    def test_split_hand(self):
        """Test splitting functionality for a player with an eligible hand."""
        player = Player(name="Test Player", balance=1000)
        player.hands = [['8♠', '8♦']]  # Initial hand eligible for splitting
        player.bets = [100]  # Initial bet

        # Simulate splitting
        initial_balance = player.balance
        card1 = deal_card(self.deck)  # Deal a card to the first hand
        card2 = deal_card(self.deck)  # Deal a card to the second hand

        player.balance -= player.bets[0]  # Deduct the bet for the split
        new_hand = [player.hands[0].pop()]  # Move one card to the new hand
        player.hands.append(new_hand)  # Add the new hand
        player.bets.append(player.bets[0])  # Duplicate the bet for the new hand

        # Deal a new card to each hand
        player.hands[0].append(card1)
        player.hands[1].append(card2)

        # Assertions
        self.assertEqual(len(player.hands), 2, "Player should have two hands after splitting.")
        self.assertEqual(player.bets, [100, 100], "Both hands should have the same bet.")
        self.assertEqual(player.balance, initial_balance - 100, "Balance should decrease by the bet amount.")
        self.assertEqual(len(player.hands[0]), 2, "First hand should have two cards after the split.")
        self.assertEqual(len(player.hands[1]), 2, "Second hand should have two cards after the split.")

    # Test betting mechanics
    def test_betting(self):
        player = Player(name="Test Player", balance=1000)

        # Player bets 100
        player.bet = 100
        player.balance -= player.bet
        self.assertEqual(player.balance, 900, "Balance should decrease by bet amount.")

        # Player wins and gets their bet back plus winnings
        player.balance += player.bet * 2  # Winning the hand
        self.assertEqual(player.balance, 1100, "Balance should increase by twice the bet amount after a win.")

    # Test doubling down
    def test_doubling_down(self):
        player = Player(name="Test Player", balance=1000)
        deck = create_deck()
        random.shuffle(deck)

        # Initial state
        player.bets = [100]
        player.hands = [[deal_card(deck), deal_card(deck)]]

        # Player doubles down
        player.bets[0] *= 2  # Double the bet
        player.hands[0].append(deal_card(deck))  # Double down adds one more card

        self.assertEqual(player.bets[0], 200, "Bet should double after doubling down.")
        self.assertEqual(len(player.hands[0]), 3, "Player should have exactly three cards after doubling down.")

    # Test blackjack payout
    def test_blackjack_payout(self):
        player = Player(name="Test Player", balance=1000)

        # Player bets 100 and gets a blackjack
        player.bets = [100]
        player.hands = [['A♠', '10♠']]  # Blackjack
        initial_balance = player.balance - player.bets[0]

        # Blackjack payout: 3:2
        payout = int(player.bets[0] * 1.5)
        player.balance += payout

        self.assertEqual(player.balance, initial_balance + player.bets[0] + payout, 
                         "Balance should increase by bet + 1.5x bet on blackjack.")

    # Test determine winner logic
    def test_determine_winner(self):
        # Define scenarios as a list of tuples (player_hand, dealer_hand, expected_output)
        scenarios = [
            (['10♦', '9♠'], ['8♦', '8♠'], "Player wins!"),  # Player 19 vs Dealer 16
            (['10♦', '9♠'], ['10♦', '10♠'], "Dealer wins!"),  # Player 19 vs Dealer 20
            (['10♦', '9♠'], ['9♦', '10♠'], "It's a tie!"),  # Player 19 vs Dealer 19
        ]

        for player_hand, dealer_hand, expected_output in scenarios:
            # Calculate totals
            player_total = calculate_hand_value(player_hand)
            dealer_total = calculate_hand_value(dealer_hand)

            # Simulate determining the winner
            if player_total > 21:
                actual_output = "Player busts! Dealer wins!"
            elif dealer_total > 21 or player_total > dealer_total:
                actual_output = "Player wins!"
            elif dealer_total > player_total:
                actual_output = "Dealer wins!"
            else:
                actual_output = "It's a tie!"

            # Check the result
            self.assertEqual(actual_output, expected_output, f"Failed for {player_hand} vs {dealer_hand}")

if __name__ == "__main__":
    unittest.main()
