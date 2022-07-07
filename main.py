# RULES
# each player has $1000
# player takes the other's money if he wins the round
# player can hit or stand
# *** hit - player gets a new card each time he calls hit
# *** stand - player doesn't get a new card
# winner and loser are declared when one loses all his money but his hand is not over 21
# "BLACKJACK" is announced when player gets 21
# player is declared as bust when his hand is over 21 while the other player is declared as winner
# when game is a tie, bet is redistributed among both players
# human player can start a new game when the current game is over
# deck: A, 2, 3, 4, 5, 6, 7, 8, 9, 10, J, Q, K -- each * 4 (13 cards * 4 = 52)
# *** A - 1 or 11 points
# *** 2 - 2 points, 3 - 3 points, and so on...
# *** J, Q, or K - 10 points

import time
import random

is_winner_declared = False


class Player:
    def __init__(self, name, current_hand, money=1000):
        self.name = name
        self.current_hand = current_hand
        self.money = money

    def bet(self, player_bet):
        self.money -= player_bet

        if player_bet == human_bet:
            print('Dealer:', self.name, 'bet', player_bet)
            print('Your money remaining:', self.money)
        else:
            print('Dealer: Bot bet', player_bet)

    def hit(self, player_turn):
        card_received = player_turn.pass_out()
        player_turn.update_deck(card_received)

    def collect_prize(self, prize):
        self.money += prize
        return self.money


class Deck:
    def __init__(self, deck, player):
        self.deck = deck
        self.player = player

    # update the deck after a card selected
    def update_deck(self, selected_card):
        for key, card in enumerate(self.deck):
            if card.keys() == selected_card.keys():
                # remove card from the deck
                card.update({str(list(card.keys())[0]): card[str(list(card.keys())[0])] - 1})  # {key: value}

            # if all 4 cards of the same number passed out, remove from deck
            if card[str(list(card.keys())[0])] == 0:
                self.deck.pop(key)

    def pass_out(self):
        card_selected = random.choice(self.deck)  # randomly select card from the deck

        if self.player == human_player:
            human_hand.append(list(card_selected.keys())[0])
            print('Your current hand:', human_hand)
        elif self.player == bot_player:
            bot_hand.append(list(card_selected.keys())[0])

            if len(bot_hand) >= 2:
                print("Bot's current hand:", bot_hand[1])

        return card_selected


def calculate_card_num(player_hand):
    current_hand = []

    for card in player_hand:
        if card == 'A':
            current_hand.append(1)
            current_hand.append(11)
        elif card == 'J' or card == 'Q' or card == "K":
            current_hand.append(10)
        else:
            current_hand.append(int(card))

    current_hand.sort()

    if current_hand[0] == 1 and current_hand[len(current_hand)-1] == 11:
        sum_after_exclude_11 = sum(current_hand[:len(current_hand) - 1])
        sum_after_exclude_1 = sum(current_hand[1:len(current_hand)])

        if sum_after_exclude_11 < 21 and sum_after_exclude_1 < 21:
            return max(sum_after_exclude_11, sum_after_exclude_1)
        elif sum_after_exclude_11 < 21 < sum_after_exclude_1:
            return sum_after_exclude_11
        elif sum_after_exclude_1 < 21 < sum_after_exclude_11:
            return sum_after_exclude_1
        elif sum_after_exclude_11 == 21:
            return sum_after_exclude_11
        elif sum_after_exclude_1 == 21:
            return sum_after_exclude_1
        else:
            # else if sum_after_exclude_11 > 21 and sum_after_exclude_1 > 21
            return min(sum_after_exclude_11, sum_after_exclude_1)
    else:
        return sum(current_hand)


def start_game():
    while new_game:
        human_player_name = input('Please provide your player name: ').strip()

        if len(human_player_name) > 1:
            return human_player_name
        else:
            continue


def set_new_round():
    card_counter_reset = 1
    initial_betting_reset = True
    enable_human_get_card_reset = True
    enable_bot_get_card_reset = False
    human_hand_reset = []
    bot_hand_reset = []
    default_deck_reset = [{'A': 4},
                          {'2': 4},
                          {'3': 4},
                          {'4': 4},
                          {'5': 4},
                          {'6': 4},
                          {'7': 4},
                          {'8': 4},
                          {'9': 4},
                          {'10': 4},
                          {'J': 4},
                          {'Q': 4},
                          {'K': 4}]
    total_human_bet_reset = 0
    total_bot_bet_reset = 0

    return card_counter_reset, initial_betting_reset, enable_human_get_card_reset, enable_bot_get_card_reset, \
           human_hand_reset, bot_hand_reset, default_deck_reset, total_human_bet_reset, total_bot_bet_reset


if __name__ == '__main__':
    new_game = True
    player_name = start_game()
    card_limit = 8

    if new_game:
        card_counter, initial_betting, enable_human_get_card, enable_bot_get_card, human_hand, bot_hand, default_deck, \
        total_human_bet, total_bot_bet = set_new_round()

        human_player = Player(player_name, human_hand)
        bot_player = Player('Bot', bot_hand)

        print('Your bank:', human_player.money)

        while not is_winner_declared:
            print('Dealer: Shuffling deck...')
            time.sleep(4)

            while card_counter < card_limit:
                card_passed_out = {}
                human_turn = Deck(default_deck, player=human_player)
                bot_turn = Deck(default_deck, player=bot_player)

                # each player take $50 out of pocket as initial bet
                if initial_betting:
                    if human_player.money >= 50 and bot_player.money >= 50:
                        human_player.money -= 50
                        bot_player.money -= 50

                        total_human_bet += 50
                        total_bot_bet += 50
                    elif human_player.money >= 50 > bot_player.money:
                        human_player.money -= 50
                        total_human_bet += 50

                        total_bot_bet += bot_player.money
                        bot_player.money -= bot_player.money
                    elif bot_player.money >= 50 > human_player.money:
                        bot_player.money -= 50
                        total_bot_bet += 50

                        total_human_bet += human_player.money
                        human_player.money -= human_player.money
                    else:
                        total_human_bet += human_player.money
                        human_player.money -= human_player.money

                        total_bot_bet += bot_player.money
                        bot_player.money -= bot_player.money

                    initial_betting = False

                # start passing out cards
                if card_counter < 5:
                    if enable_human_get_card and not enable_bot_get_card:
                        card_passed_out = human_turn.pass_out()
                        human_turn.update_deck(card_passed_out)
                        card_counter += 1
                    elif not enable_human_get_card and enable_bot_get_card:
                        card_passed_out = bot_turn.pass_out()
                        bot_turn.update_deck(card_passed_out)
                        card_counter += 1
                elif card_counter == 5 or card_counter == 6:
                    # see if first 2 cards = blackjack
                    if len(human_hand) == 2 and len(bot_hand) == 2:
                        human_blackjack = calculate_card_num(human_hand)
                        bot_blackjack = calculate_card_num(bot_hand)

                        if human_blackjack == 21 or bot_blackjack == 21 or human_blackjack > 21 or bot_blackjack > 21:
                            # go determine winner
                            card_counter = 9
                            break
                        else:
                            card_counter = card_counter  # continue the current round

                    human_hit_counter = 1
                    human_hit_or_stand_flag = True
                    human_bet_flag = True

                    while human_hit_or_stand_flag:
                        try:
                            human_hit_or_stand = input('Dealer: Hit or Stand? ').strip().lower()

                            if human_hit_or_stand == 'hit':
                                human_player.hit(human_turn)

                                # if current hand is over 21, immediately announce winner/loser
                                current_human_result = calculate_card_num(human_hand)
                                if current_human_result > 21:
                                    card_counter = 9
                                    human_bet_flag = False
                                    break

                                human_hit_or_stand_flag = False
                            elif human_hit_or_stand == 'stand':
                                print('Your current hand: ', human_hand)
                                human_hit_or_stand_flag = False
                            else:
                                print('Dealer: Invalid input. Enter Hit or Stand.')
                                continue
                        except:
                            print('Dealer: Invalid input. Try again.')
                            continue

                    while human_bet_flag:
                        try:
                            if human_player.money > 0:
                                human_bet = int(input('Dealer: Enter an amount (0, 1, 5, 25, 50, 100, 500) to '
                                                          'increase your bet: ').strip())

                                if human_bet in (0, 1, 5, 25, 50, 100, 500):
                                    if human_bet > human_player.money:
                                        print("Dealer: You don't have that much. Try again.")
                                    else:
                                        human_player.bet(human_bet)
                                        total_human_bet += human_bet
                                        print('Total in the pot:', total_human_bet + total_bot_bet)
                                        human_bet_flag = False
                                else:
                                    print('Dealer: Invalid amount. Enter 0, 1, 5, 25, 50, 100, or 500.')
                                    continue
                            else:
                                human_bet_flag = False
                        except:
                            print('Dealer: Invalid amount. Try again.')
                            continue

                    if human_hit_or_stand == 'hit':
                        card_counter += 1
                        continue
                    elif human_hit_or_stand == 'stand':
                        if card_counter == 6:
                            card_counter += 1
                        else:
                            card_counter += 2

                        continue
                elif card_counter == 7:
                    bot_hit_counter = 1

                    while True:
                        bot_hit_or_stand = random.choice(['hit', 'stand'])

                        if bot_player.money > 0:
                            bot_bet = random.choice([0, 1, 5, 25, 50, 100, 500])
                            bot_player.bet(bot_bet)
                            total_bot_bet += bot_bet
                            print('Total in the pot:', total_human_bet + total_bot_bet)
                        else:
                            pass

                        if bot_hit_or_stand == 'hit':
                            bot_player.hit(bot_turn)

                            # if current hand is over 21, immediately announce winner/loser
                            current_bot_result = calculate_card_num(human_hand)
                            if current_bot_result > 21:
                                card_counter = 9
                                break

                            bot_hit_counter += 1

                            if bot_hit_counter < 3:
                                card_counter += 1
                                continue
                            else:
                                card_counter += 1
                                break
                        elif bot_hit_or_stand == 'stand':
                            if card_counter == 7:
                                card_counter += 2
                            elif card_counter == 8:
                                card_counter += 1

                            break

                # see if first 2 cards = blackjack
                #if len(human_hand) == 2 and len(bot_hand) == 2:
                 #   human_blackjack = calculate_card_num(human_hand)
                  #  bot_blackjack = calculate_card_num(bot_hand)

                   # if human_blackjack == 21 or bot_blackjack == 21 or human_blackjack > 21 or bot_blackjack > 21:
                        # go determine winner
                    #    card_counter = 9
                    #else:
                     #   card_counter = card_counter  # continue the current round

                # next player's turn
                if enable_human_get_card and not enable_bot_get_card:
                    enable_human_get_card = False
                    enable_bot_get_card = True
                elif not enable_human_get_card and enable_bot_get_card:
                    enable_human_get_card = True
                    enable_bot_get_card = False
            else:
                print('Total in the Pot (Sealed):', total_human_bet + total_bot_bet)

                # determine game result
                human_result = calculate_card_num(human_hand)
                bot_result = calculate_card_num(bot_hand)
                human_bank = 0
                bot_bank = 0

                if human_result < 21 and bot_result < 21:
                    if human_result > bot_result:
                        print('Dealer: You win!')
                        human_bank = human_player.collect_prize(total_human_bet + total_bot_bet)
                        bot_bank = bot_player.collect_prize(0)
                    elif bot_result > human_result:
                        print('Dealer: Bot wins!')
                        bot_bank = bot_player.collect_prize(total_human_bet + total_bot_bet)
                        human_bank = human_player.collect_prize(0)
                    else:
                        print('Dealer: Split')
                        #  get back what they distributed
                        human_bank = human_player.collect_prize(total_human_bet)
                        bot_bank = bot_player.collect_prize(total_bot_bet)
                elif bot_result > 21 > human_result:
                    print('Dealer: You win!')
                    human_bank = human_player.collect_prize(total_human_bet + total_bot_bet)
                    bot_bank = bot_player.collect_prize(0)
                elif human_result > 21 > bot_result:
                    print('Dealer: BUST! Bot wins!')
                    bot_bank = bot_player.collect_prize(total_human_bet + total_bot_bet)
                    human_bank = human_player.collect_prize(0)
                elif human_result == 21:
                    print('Dealer: BLACKJACK!')
                    human_bank = human_player.collect_prize(total_human_bet + total_bot_bet)
                    bot_bank = bot_player.collect_prize(0)
                elif bot_result == 21:
                    print('Dealer: Bot BLACKJACK!')
                    bot_bank = bot_player.collect_prize(total_human_bet + total_bot_bet)
                    human_bank = human_player.collect_prize(0)
                elif (human_result == 21 and bot_result == 21) or (human_result > 21 and bot_result > 21):
                    print('Dealer: Split')
                    #  return the bet what they distributed
                    human_bank = human_player.collect_prize(total_human_bet)
                    bot_bank = bot_player.collect_prize(total_bot_bet)

                print("Dealer: Human's hand:", human_hand)
                print("Dealer: Bot's hand:", bot_hand)
                print('Your money remaining:', human_bank)

                if human_bank == 0:
                    print("Dealer: You're the winner!")
                    is_winner_declared = True
                elif bot_bank == 0:
                    print("Dealer: Bot is the winner!")
                    is_winner_declared = True
                elif human_bank > 0 and bot_bank > 0:
                    card_counter, initial_betting, enable_human_get_card, enable_bot_get_card, human_hand, bot_hand, \
                    default_deck, total_human_bet, total_bot_bet = set_new_round()
                    continue
        else:
            time.sleep(2)

            while True:
                try:
                    rematch = input("Dealer: Enter 'R' for re-match or 'Q' to quit: ").upper()

                    if rematch != 'R' or rematch != 'Q':
                        continue
                    elif rematch == 'R':
                        new_game = True
                        break
                    else:
                        new_game = False
                        break
                except:
                    continue
    else:
        print('Dealer: Better luck next time!')


