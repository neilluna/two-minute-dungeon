'''
Scenario interface.
All scenarios use this, directly or indirectly, as a base class.
'''

from dataclasses import dataclass
from typing import Callable, Optional


# Scenario member funtion to call when the command is invoked.
# Called like so:
#
# function(self) -> bool
#
# If the member function returns a True, game play continues.
# If the member function returns a False, game play ends.
CommandFunction = Callable[[], bool]


@dataclass
class Command:
    '''
    Command information.
    The scenario commands() member function returns a list of these dictionaries.
    '''
    invocation_text: str       # What input text invokes this command?
    menu_text: str             # Text of the command to be used in the menu of commands.
    function: CommandFunction  # Scenario member funtion to call when the command is invoked.
    # If the command is invoked, the member function is called like so: function(self)
    # See 'CommandFunction' type alias above.


class Scenario:
    '''
    Scenario base class.
    All scenarios use this, directly or indirectly, as a base class.
    '''


    def description(self) -> None:
        '''
        Describe the scenario.
        This function is called once at the beginning of the game.
        '''


    def display(self) -> None:
        '''
        Display the game.
        This function is called once every turn.
        '''


    def commands(self) -> list[Command]:
        '''
        Add commands to the given commands.
        This function is called once every turn.
        '''


    def post_player_turn(self) -> bool:
        '''
        This function is called once every turn, after the player's turn.
        Returns a True to continue playing the game.
        Returns a False to end the game.
        '''


    def game_over(self) -> None:
        '''
        The game is over.
        This function is called once at the end of the game.
        '''
