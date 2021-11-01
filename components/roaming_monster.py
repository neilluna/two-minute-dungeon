'''
Roaming monster scenario.
A roaming monster wanders through the grid maze.
'''

from random import choice
from typing import Optional

from base_classes.dungeon import Direction, Dungeon, NavigationInfo


class RoamingMonster:
    ''' Roaming monster. '''


    def __init__(self, dungeon: Dungeon, monster_room: int, monster_health: int = 1):
        self.dungeon: Dungeon = dungeon
        self.monster_room: int = monster_room
        self.monster_health: int = monster_health

        self.monster_last_saw_player_in_room: Optional[int] = None

        # Record how many times the monster has visited each room.
        self.visits_per_room: list[int] = []
        for _ in range(self.dungeon.number_of_rooms):
            self.visits_per_room.append(0)
        self.visits_per_room[self.monster_room] = 1


    def description(self) -> None:
        ''' Describe the scenario. '''
        print('- A monster roams this dungeon. If it catches you, you will lose.')


    def room_contents(self, room: int) -> Optional[str]:
        ''' Returns the given room's contents. Single character string. '''
        return 'M' if room == self.monster_room else None


    def post_player_turn(self) -> bool:
        '''
        Runs after the command function is run.
        Handles the monsters turn.
        '''
        # If the monster is in the same room as the player ...
        if self.monster_room == self.dungeon.player_room:
            print('The monster does not move.')

        # The monster is in a different room as the player ...
        else:
            # Can the monster see the player?
            visible_rooms: list[int] = self.dungeon.rooms_visible_from_room(self.monster_room)
            is_player_visible: bool = self.dungeon.player_room in visible_rooms

            # If the monster sees the player ...
            if is_player_visible:
                move_information: NavigationInfo = self.dungeon.navigate_towards_destination(
                    self.monster_room, self.dungeon.player_room
                )
                print(f'The monster sees you. The monster moves {move_information.name}.')

                # The monster remembers where he last saw the player.
                self.monster_last_saw_player_in_room = self.dungeon.player_room

            # The monster does not see the player, but remembers where it saw the player last ...
            elif self.monster_last_saw_player_in_room:
                move_information: NavigationInfo = self.dungeon.navigate_towards_destination(
                    self.monster_room, self.monster_last_saw_player_in_room
                )

            # The monster does not see the player, nor remembers where it saw the player last ...
            else:
                # Which directions can the monster move?
                directions: list[Direction] = self.dungeon.directions_with_doors(self.monster_room)
                navigation_info_list: list[NavigationInfo] = [
                    self.dungeon.navigation_info(direction, self.monster_room)
                    for direction in directions
                ]

                # Sort the direction list by monster visits, ascending.
                # The monster prefers the roads less traveled.
                navigation_info_list.sort(
                    key = lambda navigation_info: self.visits_per_room[navigation_info.room]
                )
                lowest_number_of_visits: int = self.visits_per_room[navigation_info_list[0].room]
                move_information_list: list[NavigationInfo] = [
                    navigation_info
                    for navigation_info in navigation_info_list
                    if self.visits_per_room[navigation_info.room] == lowest_number_of_visits
                ]
                move_information: NavigationInfo = choice(move_information_list)

            # Move the monster.
            self.monster_room = move_information.room

            # If the monster is in the room where he remembers last seeing the player,
            # then the monster forgets where he last saw the player.
            if self.monster_room == self.monster_last_saw_player_in_room:
                self.monster_last_saw_player_in_room = None

            # Update the number of times that the monster has visited this room.
            self.visits_per_room[self.monster_room] = self.visits_per_room[self.monster_room] + 1

        # If the monster is in the same room as the player ...
        if self.monster_room == self.dungeon.player_room:
            print('The monster catches you. You lose.')
            return False

        return True
