import nextcord
from typing import List
from nextcord import slash_command, Client, Interaction, SlashOption, Member, InteractionMessage, Embed
from nextcord.ext import commands
from utils import Configuration

GUILD_IDS = [825894722324922438]


class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int, user1: Member, user2: Member):
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.user1 = user1
        self.user2 = user2

    async def callback(self, interaction: nextcord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        if view.current_player.id != interaction.user.id:
            return
        state = view.board[self.y][self.x]
        if state in (view.X, view.O):
            return

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.X
            view.current_player = view.O
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
        content = f"It is now {view.current_player.display_name}'s turn"

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f'**** {view.X}'
            elif winner == view.O:
                content = f'{view.O}'
            else:
                content = "It's a tie!"

            for child in view.children:
                child.disabled = True

            view.stop()

        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(nextcord.ui.View):
    children: List[TicTacToeButton]
    Tie = 2

    def __init__(self, user1: Member, user2: Member):
        super().__init__()
        self.X = user1
        self.O = user2
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, self.X, self.O))

    def check_board_winner(self):
        # Check horizontal
        for line in range(3):
            if self.board[line][0] == self.board[line][1] == self.board[line][2] != 0:
                return self.board[line][0]

        # Check vertical
        for line in range(3):
            if self.board[0][line] == self.board[1][line] == self.board[2][line] != 0:
                return self.board[0][line]

        # Check diagonal
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != 0:
            return self.board[0][2]
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != 0:
            return self.board[0][0]

        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None


class Games(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @slash_command(name="tictactoe", description="Play tictactoe", guild_ids=GUILD_IDS)
    async def tictactoe(self, interaction: Interaction,
                        user: Member = SlashOption(name="user", description="Challenge someone!", required=True)):
        await interaction.response.send_message('Tic Tac Toe: X goes first', view=TicTacToe(interaction.user, user))


def setup(client: Client):
    client.add_cog(Games(client))
