'''
Dungeon interface.
All dungeons use this, directly or indirectly, as a base class.
'''

from dataclasses import dataclass
from typing import Callable, Optional


@dataclass
class Direction:
    ''' A direction in the dungeon. '''
    id: int    # Dungeon implementation specific direction id.
    name: str  # Dungeon implementation specific direction name.


@dataclass
class NavigationInfo:
    ''' Navigation information. '''
    direction: Direction  # Direction of interest.
    name: str             # Name of the direction of interest.
    room: int             # Room in the direction of interest.


# Scenario member funtion to call when printing a rooms contents.
# Called like so:
#
# def function(self, room: int) -> Optional[str]:
#
# If the scenario has content in the given room, then return the content as a single character string.
# If the scenario has no content in the given room, then return None.
RoomContentFunction = Callable[[int], Optional[str]]


class Dungeon:
    ''' Dungeon interface. '''


    def __init__(self, number_of_rooms: int, player_room: int):
        self.number_of_rooms: int = number_of_rooms
        self.player_room: int = player_room


    def directions_with_doors(self, room: int) -> list[Direction]:
        ''' Returns a list of directions that contain doors in the given room. '''


    def navigation_info(self, direction: Direction, room: int) -> Optional[NavigationInfo]:
        '''
        Returns navigation information from the given room.
        Returns None if the navigation information room would be invalid.
        '''


    def navigate_towards_destination(
        self, start_room: int, destination_room: int
    ) -> Optional[NavigationInfo]:
        '''
        Given a start and destination room,
        if the destination room is visible from the start room,
        returns information on how to move from the start room towards the destination room.
        Returns None if no direction can be determined.
        '''


    def room_in_direction(self, direction: Direction, room: int) -> Optional[int]:
        '''
        Returns the adjacent room in the given direction from the given room.
        Returns None if not room exists in that direction.
        '''


    def rooms_visible_from_room(self, room: int) -> list[int]:
        ''' Returns a list of all the rooms that are visible from the given room. '''


    def rooms_visible_in_direction(self, direction: Direction, room: int) -> list[int]:
        '''
        Returns a list of the rooms that are visible from the given room in the given direction.
        '''

    def set_room_contents_function(self, function: RoomContentFunction) -> None:
        ''' Sets the function to call to print a rooms contents. '''
