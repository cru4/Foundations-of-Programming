import unittest
from unittest import mock
from unittest import TestCase
from midterm import *  # Ensure this imports your game logic correctly

class CreateTests(TestCase):
   
    def setUp(self):
        self.deck = create_deck()  # Create a fresh deck for each test
        random.shuffle(self.deck)
        self.player_hand = []
        self.dealer_hand = []

    # Test for card value calculation
    def test_card_value(self):
        print ("test is running")
        self.assertEqual(card_value('2♥'), 2)
        self.assertEqual(card_value('J♦'), 10)
        self.assertEqual(card_value('A♠'), 11)
        self.assertEqual(card_value('10♣'), 10)
        print ("test passed")

    # Test for Ace adjustment when hand is over 21
    def test_adjust_for_ace(self):
        print ("test is running")
        hand = ['A♠', '9♦', 'A♣']  # Two Aces and a 9
        self.assertEqual(adjust_for_ace(hand), 21)  # Aces should adjust to 1 if over 21

        hand = ['A♠', 'A♣', '9♦', 'K♥']  # Two Aces, 9, and a King
        self.assertEqual(adjust_for_ace(hand), 21)

        hand = ['A♠', 'A♣', 'A♦', '8♠']  # Three Aces and an 8
        self.assertEqual(adjust_for_ace(hand), 21)
        print ("test passed")

    # Test dealing card
    def test_deal_card(self):
        print ("test is running")
        initial_deck_size = len(self.deck)
        card = deal_card(self.deck)
        self.assertEqual(len(self.deck), initial_deck_size - 1)
        self.assertIsInstance(card, str)
        print ("test passed")

    # Test hand calculation
    def test_calculate_hand_value(self):
        print ("test is running")
        hand = ['A♠', '9♦']
        self.assertEqual(calculate_hand_value(hand), 20)
        hand = ['A♠', '9♦', '2♠']
        self.assertEqual(calculate_hand_value(hand), 12)
        print ("test passed")

    # Test winner determination
    def test_determine_winner(self):
        print ("test is running")
        player_hand = ['10♦', '9♠']  # Total 19
        dealer_hand = ['8♦', '8♠']   # Total 16
        with mock.patch('builtins.print') as mocked_print:
            determine_winner(player_hand, dealer_hand)
            mocked_print.assert_called_with("Player wins!")

        player_hand = ['10♦', '9♠']  # Total 19
        dealer_hand = ['10♦', '10♠']   # Total 20
        with mock.patch('builtins.print') as mocked_print:
            determine_winner(player_hand, dealer_hand)
            mocked_print.assert_called_with("Dealer wins!")

        player_hand = ['10♦', '9♠']  # Total 19
        dealer_hand = ['9♦', '10♠']   # Total 19
        with mock.patch('builtins.print') as mocked_print:
            determine_winner(player_hand, dealer_hand)
            mocked_print.assert_called_with("It's a tie!")
        print ("test passed")

    # Test deck creation (52 unique cards)
    def test_create_deck(self):
        print ("test is running")
        deck = create_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(deck)), 52)  # Ensure all cards are unique
        print ("test passed")


if __name__ == "__main__":
    unittest.main()
    CreateTests