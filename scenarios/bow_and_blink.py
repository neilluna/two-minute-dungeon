'''
Simple bow scenario.
You can shoot the monster with your bow.
'''

from random import randint
from typing import Optional

from base_classes.scenario import Command, CommandFunction, Scenario
from character_set import UNICODE_DUNGEON_DRAWING_CHARACTER_SET
from components.grid_dungeon import GridDungeon
from components.hold_position import HoldPosition
from components.quit import Quit
from components.roaming_monster import RoamingMonster
from components.teleport_rune import TeleportRune


class BowAndBlink(Scenario):
    ''' Simple bow scenario.'''

    def __init__(self) -> None:
        self.dungeon: GridDungeon = GridDungeon(UNICODE_DUNGEON_DRAWING_CHARACTER_SET, 7, 5, 0)
        self.dungeon.set_room_contents_function(self.room_contents)
        self.monster: RoamingMonster = RoamingMonster(
            self.dungeon, self.dungeon.number_of_rooms - 1, randint(3, 5)
        )
        self.teleport: TeleportRune = TeleportRune(self.dungeon)
        self.hold_position: HoldPosition = HoldPosition()
        self.quit: Quit = Quit()


    def description(self) -> None:
        ''' Describe the scenario. '''
        self.dungeon.description()
        self.monster.description()
        print('- You have a bow. You can shoot the monster if you can see it.')
        print('  If you shoot the monster enough times, you will win.')
        self.teleport.description()


    def display(self) -> None:
        ''' Describe the scenario. '''
        self.dungeon.display()


    def commands(self) -> list[Command]:
        ''' Returns a list of additional commands. '''
        commands = self.dungeon.commands()
        commands.extend(self.hold_position.commands())

        # Can the player see the monster?
        visible_rooms: list[int] = self.dungeon.rooms_visible_from_room(self.dungeon.player_room)
        if self.monster.monster_room in visible_rooms:
            commands.extend([Command(
                invocation_text = 'F',
                menu_text = '(F)ire bow',
                function = self._fire_bow_command,
            )])

        commands.extend(self.teleport.commands())
        commands.extend(self.quit.commands())
        return commands


    def post_player_turn(self) -> bool:
        ''' Runs after the command function is run. '''
        return self.monster.post_player_turn()


    def game_over(self) -> None:
        ''' The game is over. '''
        self.dungeon.game_over()


    def room_contents(self, room: int) -> Optional[str]:
        ''' Returns the given room's contents. Single character string. '''
        contents = self.monster.room_contents(room)
        if not contents:
            contents = self.dungeon.room_contents(room)
        if not contents:
            contents = self.teleport.room_contents(room)
        return contents


    _fire_bow_command: CommandFunction
    def _fire_bow_command(self) -> bool:
        ''' Function for the "Fire Bow" command. '''
        print('You fire your bow.')
        self.monster.monster_health = self.monster.monster_health - 1
        if self.monster.monster_health:
            print('You shot the monster, but it is not enough.')
            return True
        print('You shot and defeated the monster. You win.')
        return False
