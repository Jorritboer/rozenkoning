from RoseKing import *

import arcade

# Set how many rows and columns we will have
ROW_COUNT = 9
COLUMN_COUNT = 9

# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 30
HEIGHT = 30

# This sets the margin between each cell
# and on the edges of the screen.
MARGIN_CELL = 5
MARGIN_GRID = 200

# Do the math to figure out our screen dimensions
SCREEN_WIDTH = (WIDTH + MARGIN_CELL) * COLUMN_COUNT + 2 * MARGIN_GRID
SCREEN_HEIGHT = (HEIGHT + MARGIN_CELL) * ROW_COUNT + 2 * MARGIN_GRID
SCREEN_TITLE = "Array Backed Grid Example"


class MyGame(arcade.Window):

    def __init__(self, width, height, title):
        super().__init__(width, height, title)

        self.game = RoseKing()

        self.red_card_sprites = []
        for i in range(5):
            self.red_card_sprites.append(
                arcade.SpriteSolidColor(
                    50,
                    150,
                    MARGIN_GRID + 20 + i * (50 + 2 * MARGIN_CELL) + 25,
                    115,
                    arcade.color.RED,
                )
            )
        self.blue_card_sprites = []
        for i in range(5):
            self.blue_card_sprites.append(
                arcade.SpriteSolidColor(
                    50,
                    150,
                    MARGIN_GRID + 20 + i * (50 + 2 * MARGIN_CELL) + 25,
                    625,
                    arcade.color.BLUE,
                )
            )

        self.draw_pile = arcade.SpriteSolidColor(
            100,
            150,
            80,
            400,
            arcade.color.DARK_GREEN,
        )

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        # This command has to happen before we start drawing
        self.clear()

        for row in range(ROW_COUNT):
            for column in range(COLUMN_COUNT):

                # Do the math to figure out where the box is
                x = (MARGIN_CELL + WIDTH) * column + MARGIN_GRID + WIDTH // 2
                y = (MARGIN_CELL + HEIGHT) * row + MARGIN_GRID + HEIGHT // 2

                # Draw the box
                arcade.draw_lbwh_rectangle_filled(
                    x, y, WIDTH, HEIGHT, arcade.color.WHITE
                )

                if self.game.board[column][8 - row] == Color.BLUE:
                    arcade.draw_circle_filled(
                        x + WIDTH / 2, y + WIDTH / 2, WIDTH / 2, arcade.color.BLUE
                    )
                elif self.game.board[column][8 - row] == Color.RED:
                    arcade.draw_circle_filled(
                        x + WIDTH / 2, y + WIDTH / 2, WIDTH / 2, arcade.color.RED
                    )

                if self.game.cur_pos_x == column and self.game.cur_pos_y == 8 - row:
                    arcade.draw_circle_filled(
                        x + WIDTH / 2, y + WIDTH / 2, WIDTH / 3, arcade.color.YELLOW
                    )

        for card in self.red_card_sprites:
            if self.game.player == Color.RED:
                arcade.draw_sprite(card, alpha=255)
            else:
                arcade.draw_sprite(card, alpha=50)
        for card in self.blue_card_sprites:
            if self.game.player == Color.BLUE:
                arcade.draw_sprite(card, alpha=255)
            else:
                arcade.draw_sprite(card, alpha=50)

        # drawing card text
        for i, card in enumerate(self.game.red_cards):
            arcade.Text(
                f"{card.direction} {'I' * card.n}",
                MARGIN_GRID + 20 + i * (50 + 2 * MARGIN_CELL) + 5,
                115,
            ).draw()
        for i, card in enumerate(self.game.blue_cards):
            arcade.Text(
                f"{card.direction} {'I' * card.n}",
                MARGIN_GRID + 20 + i * (50 + 2 * MARGIN_CELL) + 5,
                625,
            ).draw()

        if self.game.player == Color.RED:
            arcade.Text(f"Red's turn!", 20, 500, arcade.color.RED).draw()
        else:
            arcade.Text(f"Blue's turn!", 20, 500, arcade.color.BLUE).draw()

        arcade.Text(
            f"Knights: {self.game.blue_knights}", 525, 625, arcade.color.BLUE
        ).draw()
        arcade.Text(
            f"Knights: {self.game.red_knights}", 525, 115, arcade.color.RED
        ).draw()

        arcade.Text(
            f"Score: {self.game.blue_score}", 525, 575, arcade.color.BLUE
        ).draw()
        arcade.Text(f"Score: {self.game.red_score}", 525, 165, arcade.color.RED).draw()

        arcade.draw_sprite(self.draw_pile)
        arcade.Text(f"Draw:\n {len(self.game.draw_cards)} cards left", 20, 450).draw()

    print()

    def on_mouse_press(self, x, y, button, modifiers):
        try:
            if self.game.player == Color.RED:
                for i in range(len(self.red_card_sprites)):
                    card = self.red_card_sprites[i]
                    if card.collides_with_point((x, y)):
                        self.game.play_card(i + 1)
                        break
            else:
                for i in range(len(self.blue_card_sprites)):
                    card = self.blue_card_sprites[i]
                    if card.collides_with_point((x, y)):
                        self.game.play_card(i + 1)
                        break

            if self.draw_pile.collides_with_point((x, y)):
                self.game.draw_card()
        except AssertionError as err:
            print(colored(f"Error: {err}", "yellow"))


if __name__ == "__main__":
    MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()
