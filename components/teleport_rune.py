'''
Teleportaion rune scenario.
You can place the rune in a room and teleport to it at any time.
'''

from typing import Optional
from base_classes.dungeon import Dungeon

from base_classes.scenario import Command, CommandFunction


class TeleportRune:
    ''' Teleportation rune scenario. '''


    def __init__(self, dungeon: Dungeon):
        self.dungeon = dungeon
        self.teleport_room: Optional[int] = None


    def description(self) -> None:
        ''' Describe the scenario. '''
        print('- You have one teleportation rune.')
        print('  You can place the rune in a room, and then teleport back to it later.')
        print('  When you teleport to the rune, you automatically pick it up for later use.')


    def commands(self) -> list[Command]:
        ''' Returns a list of additional commands. '''
        name: str = 'Place (t)eleport rune' if self.teleport_room is None else '(T)eleport to rune'
        function: CommandFunction = (
            self._place_rune_command if self.teleport_room is None else self._teleport_command
        )
        commands = [Command(
            invocation_text = 'T',
            menu_text = name,
            function = function,
        )]
        return commands


    def room_contents(self, room: int) -> Optional[str]:
        ''' Returns the given room's contents, as a single character string. '''
        return 'T' if room == self.teleport_room else None


    _place_rune_command: CommandFunction
    def _place_rune_command(self) -> bool:
        ''' Function to place a teleport rune. '''
        print('You place the teleport rune.')
        self.teleport_room = self.dungeon.player_room
        return True


    _teleport_command: CommandFunction
    def _teleport_command(self) -> bool:
        ''' Function to teleport to the rune. '''
        print('You teleport to the rune.')
        self.dungeon.player_room = self.teleport_room
        self.teleport_room = None
        return True
