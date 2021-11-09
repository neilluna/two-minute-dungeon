'''
Quit the game.
Allows the player to quit the game.
'''

from base_classes.scenario import Command, CommandFunction


class Quit:
    '''
    Quit the game.
    Allows the player to quit the game.
    '''


    def commands(self) -> list[Command]:
        ''' Returns a list of commands available to the player. '''
        return [Command(
            invocation_text = 'Q',
            menu_text = '(Q)uit the game',
            function = self._quit_game_command,
        )]


    _quit_game_command: CommandFunction
    def _quit_game_command(self) -> bool:
        ''' The player quits the game. '''
        print('You quit the game.')
        return False
