from typing import List

import nextcord
from nextcord import Interaction, Member


class TicTacToeButton(nextcord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int, user1: Member, user2: Member):
        super().__init__(style=nextcord.ButtonStyle.secondary, label='\u200b', row=y)
        self.x = x
        self.y = y
        self.user1 = user1
        self.user2 = user2

    async def callback(self, interaction: Interaction):
        assert self.view is not None
        view: TicTacToe = self.view
        if view.current_player.id != interaction.user.id:
            return
        state = view.board[self.y][self.x]
        if state in (view.user1, view.user2):
            return

        if view.current_player == view.user1:
            self.style = nextcord.ButtonStyle.danger
            self.label = 'X'
            self.disabled = True
            view.board[self.y][self.x] = view.user1
            view.current_player = view.user2
            content = f"**{view.user1.name} vs {view.user2.name}**\n\nTurn: {view.current_player.mention} (**X**)"
        else:
            self.style = nextcord.ButtonStyle.success
            self.label = 'O'
            self.disabled = True
            view.board[self.y][self.x] = view.user2
            view.current_player = view.user1
            content = f"**{view.user1.name} vs {view.user2.name}**\n\nTurn: {view.current_player.mention} (**O**)"
        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.user1:
                content = f'**{view.user1.name} vs {view.user2.name}**\n\n{view.user1.mention} won!!! :sunglasses:'
            elif winner == view.user2:
                content = f'**{view.user1.name} vs {view.user2.name}**\n\n{view.user2.mention} won!!! :sunglasses:'
            else:
                content = f'**{view.user1.name} vs {view.user2.name}**\n\nIt is a tie!!'
            for child in view.children:
                child.disabled = True
            view.stop()
        await interaction.response.edit_message(content=content, view=view)


class TicTacToe(nextcord.ui.View):
    children: List[TicTacToeButton]
    Tie = 2

    def __init__(self, user1: Member, user2: Member):
        super().__init__()
        self.user1 = user1
        self.user2 = user2
        self.current_player = self.user1
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y, self.user1, self.user2))

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
