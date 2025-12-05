from RoseKing import *

game = RoseKing()

while not game.done:
    game.print()
    print(
        f"It is {colored('red','red') if game.player == Color.RED else colored('blue','blue')}'s turn!"
    )
    move = input("Move (number or 'draw'):")
    try:
        assert (
            move == "draw" or move.isdigit()
        ), "Move must be either 'draw' or a number"
        if move == "draw":
            game.draw_card()
        else:
            game.play_card(int(move))
    except AssertionError as err:
        print(colored(f"Error: {err}", "yellow"))
