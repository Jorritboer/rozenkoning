from enum import Enum
from termcolor import colored
from random import shuffle


class Color(Enum):
    RED = 1
    BLUE = 2


class Direction(Enum):
    NORTH = 1
    NORTH_EAST = 2
    EAST = 3
    SOUTH_EAST = 4
    SOUTH = 5
    SOUTH_WEST = 6
    WEST = 7
    NORTH_WEST = 8

    def __str__(self):
        match self.name:
            case "NORTH":
                return "↑"
            case "NORTH_EAST":
                return "↗"
            case "EAST":
                return "→"
            case "SOUTH_EAST":
                return "↘"
            case "SOUTH":
                return "↓"
            case "SOUTH_WEST":
                return "↙"
            case "WEST":
                return "←"
            case "NORTH_WEST":
                return "↖"


class Card:

    def __init__(self, direction: Direction, n: int):
        self.direction = direction
        self.n = n


class RoseKing:

    # size of the board
    N = 9

    def __init__(self):
        self.board: list[list[Color]] = [([None] * self.N) for _ in range(self.N)]
        self.cur_pos_x: int = 4
        self.cur_pos_y: int = 4
        self.player: Color = Color.RED
        self.done = False
        self.stones = 52
        self.red_knights = 4
        self.blue_knights = 4
        self.draw_cards: list[Card] = []
        for dir in Direction:
            for n in range(1, 4):
                self.draw_cards.append(Card(dir, n))
        shuffle(self.draw_cards)
        self.discard_cards: list[Card] = []
        self.red_cards: list[Card] = []
        self.blue_cards: list[Card] = []
        for _ in range(5):
            # draw card for red
            self.draw_card()
            # draw card for blue
            self.draw_card()

    def draw_card(self):
        if self.player == Color.RED:
            assert (
                len(self.red_cards) < 5
            ), "Red already has 5 cards so cannot draw another"
            if len(self.draw_cards) == 0:
                self.draw_cards = self.discard_cards
                shuffle(self.draw_cards)
                self.discard_cards = []
            self.red_cards.append(self.draw_cards.pop())
            self.player = Color.BLUE
        else:
            assert (
                len(self.blue_cards) < 5
            ), "Red already has 5 cards so cannot draw another"
            if len(self.draw_cards) == 0:
                self.draw_cards = self.discard_cards
                shuffle(self.draw_cards)
                self.discard_cards = []
            self.blue_cards.append(self.draw_cards.pop())
            self.player = Color.RED

    def print(self):
        def print_cards(cards: list[Card], knights: int):
            for i in range(len(cards)):
                card = cards[i]
                print(f"{i+1}: {card.direction} {'I' * card.n}")
            print(f"Knights: {knights}")

        print("Red cards:")
        print_cards(self.red_cards, self.red_knights)
        # print board
        for y in range(self.N):
            for x in range(self.N):
                if x == self.cur_pos_x and y == self.cur_pos_y:
                    if self.board[x][y] == None:
                        print(colored("*", "yellow"), end="")
                    elif self.board[x][y] == Color.RED:
                        print(colored("*", "red"), end="")
                    elif self.board[x][y] == Color.BLUE:
                        print(colored("*", "blue"), end="")
                elif self.board[x][y] == Color.RED:
                    print(colored("o", "red"), end="")
                elif self.board[x][y] == Color.BLUE:
                    print(colored("o", "blue"), end="")
                else:
                    print("o", end="")
            print()

        # print blue cards
        print("Blue cards:")
        print_cards(self.blue_cards, self.blue_knights)

        print(
            f"Draw pile: {len(self.draw_cards)}, discard pile: {len(self.discard_cards)}, stones: {self.stones}"
        )

    def move(self, col, row, color: Color):
        self.board[col][row] = color

    def play_card(self, card_nr: int):
        if self.player == Color.RED:
            assert card_nr >= 1 and card_nr <= len(
                self.red_cards
            ), f"You can play cards {[i + 1 for i in range(len(self.red_cards))]}, not {card_nr}"

            card = self.red_cards.pop(card_nr - 1)
        else:
            assert card_nr >= 1 and card_nr <= len(
                self.blue_cards
            ), f"You can play cards {[i + 1 for i in range(len(self.blue_cards))]}, not {card_nr}"

            card = self.blue_cards.pop(card_nr - 1)

        new_x = self.cur_pos_x
        new_y = self.cur_pos_y
        match card.direction:
            case Direction.NORTH:
                new_y -= card.n
            case Direction.NORTH_EAST:
                new_x += card.n
                new_y -= card.n
            case Direction.EAST:
                new_x += card.n
            case Direction.SOUTH_EAST:
                new_x += card.n
                new_y += card.n
            case Direction.SOUTH:
                new_y += card.n
            case Direction.SOUTH_WEST:
                new_y += card.n
                new_x -= card.n
            case Direction.WEST:
                new_x -= card.n
            case Direction.NORTH_WEST:
                new_y -= card.n
                new_x -= card.n

        assert (
            new_x >= 0 and new_x < self.N and new_y >= 0 and new_y < self.N
        ), "You cannot play this card because it would place the crown outside of the board"
        self.cur_pos_x = new_x
        self.cur_pos_y = new_y
        if self.board[self.cur_pos_x][self.cur_pos_y] != None:
            assert (
                self.board[self.cur_pos_x][self.cur_pos_y] != self.player
            ), "The player's stone itself is there"
            # if not its own color, it is the others, so the player needs a knight
            if self.player == Color.RED:
                assert (
                    self.red_knights > 0
                ), "Red has no knights so cannot play this move"
                self.red_knights -= 1
            else:
                assert (
                    self.blue_knights > 0
                ), "Blue has no knights so cannot play this move"
                self.blue_knights -= 1

        self.board[self.cur_pos_x][self.cur_pos_y] = self.player

        self.discard_cards.append(card)
        self.stones -= 1
        if self.stones == 0:
            self.done = True

        if self.player == Color.RED:
            self.player = Color.BLUE
        else:
            self.player = Color.RED


game = RoseKing()

while not game.done:
    game.print()
    print(f"It is {'red' if game.player == Color.RED else 'blue'}'s turn!")
    move = input("Move (number or 'draw'):")
    assert move == "draw" or move.isdigit(), "Move must be either 'draw' or a number"
    if move == "draw":
        game.draw_card()
    else:
        game.play_card(int(move))
