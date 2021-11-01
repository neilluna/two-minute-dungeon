'''
Hold position.
Allows the player to hold position.
'''

from base_classes.scenario import Command, CommandFunction


class HoldPosition:
    '''
    Hold position.
    Allows the player to hold position.
    '''


    def commands(self) -> list[Command]:
        ''' Returns a list of commands available to the player. '''
        return [Command(
            invocation_text = 'H',
            menu_text = '(H)old position',
            function = self._hold_position_command,
        )]


    _hold_position_command: CommandFunction
    def _hold_position_command(self) -> bool:
        ''' The player holds position. '''
        print('You hold position.')
        return True
