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
        self.assertEqual(card_value('2♥'), 2)
        self.assertEqual(card_value('J♦'), 10)
        self.assertEqual(card_value('A♠'), 11)
        self.assertEqual(card_value('10♣'), 10)

    # Test for Ace adjustment when hand is over 21
    def test_adjust_for_ace(self):
        hand = ['A♠', '9♦', 'A♣']  # Two Aces and a 9
        self.assertEqual(adjust_for_ace(hand), 21)  # Aces should adjust to 1 if over 21

        hand = ['A♠', 'A♣', '9♦', 'K♥']  # Two Aces, 9, and a King
        self.assertEqual(adjust_for_ace(hand), 21)

        hand = ['A♠', 'A♣', 'A♦', '8♠']  # Three Aces and an 8
        self.assertEqual(adjust_for_ace(hand), 21)

    # Test dealing card
    def test_deal_card(self):
        initial_deck_size = len(self.deck)
        card = deal_card(self.deck)
        self.assertEqual(len(self.deck), initial_deck_size - 1)
        self.assertIsInstance(card, str)

    # Test hand calculation
    def test_calculate_hand_value(self):
        hand = ['A♠', '9♦']
        self.assertEqual(calculate_hand_value(hand), 20)
        hand = ['A♠', '9♦', '2♠']
        self.assertEqual(calculate_hand_value(hand), 12)

    # Test player's bust scenario
    @mock.patch('builtins.input', side_effect=['hit', 'hit', 'stand'])
    def test_player_bust(self, mock_input):
        self.player_hand = ['10♦', '8♠']
        self.deck = ['5♣'] + self.deck  # Add card to make player bust
        result = player_turn(self.deck, self.player_hand)
        self.assertFalse(result)  # Player should bust and return False

    # Test dealer turn, ensuring dealer stands at 17 or higher
    def test_dealer_turn(self):
        self.dealer_hand = ['10♦', '6♠']
        self.deck = ['5♣', '9♦', '2♠'] + self.deck
        result = dealer_turn(self.deck, self.dealer_hand)
        self.assertTrue(result)  # Dealer should stand when reaching 17 or more

    # Test winner determination
    def test_determine_winner(self):
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

    # Test deck creation (52 unique cards)
    def test_create_deck(self):
        deck = create_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(len(set(deck)), 52)  # Ensure all cards are unique

