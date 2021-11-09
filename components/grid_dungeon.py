'''
Grid dungeon.
Allows the player to navigate a grid dungeon.
'''

from dataclasses import dataclass
from enum import IntEnum
from random import choice
from typing import Optional

from base_classes.dungeon import Direction, Dungeon, NavigationInfo, RoomContentFunction
from base_classes.scenario import Command, CommandFunction
from character_set import DungeonDrawingCharacterSet


class GridDirection(IntEnum):
    ''' Grid directions. '''
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


@dataclass
class GridDungeonsElements:
    ''' Elements of the dungeon. '''
    empty_room: str
    hidden_room: str
    vertical_door: str
    vertical_wall: str
    hidden_vertical_door_or_wall: str
    horizontal_door: str
    horizontal_wall: str
    hidden_horizontal_door_or_wall: str
    hidden_vertical_corner: str
    hidden_horizontal_corner: str
    all_hidden_corners: str
    southeast_corner: str
    northeast_corner: str
    northeast_and_southeast_corners: str
    southwest_corner: str
    southeast_and_southwest_corners: str
    northeast_and_southwest_corners: str
    northeast_southeast_and_southwest_corners: str
    northwest_corner: str
    northwest_and_southeast_corners: str
    northeast_and_northwest_corners: str
    northeast_northwest_and_southeast_corners: str
    northwest_and_southwest_corners: str
    northwest_southeast_and_southwest_corners: str
    northeast_northwest_and_southwest_corners: str
    all_corners: str


# Command player input strings for each direction.
COMMAND_INVOCATION_TEXT: dict[str, str] = {
    GridDirection.NORTH: 'N',
    GridDirection.SOUTH: 'S',
    GridDirection.EAST: 'E',
    GridDirection.WEST: 'W',
}

# Command names for each direction.
COMMAND_MENU_TEXT: dict[str, str] = {
    GridDirection.NORTH: '(N)orth',
    GridDirection.SOUTH: '(S)outh',
    GridDirection.EAST: '(E)ast',
    GridDirection.WEST: '(W)est',
}

# Direction names.
GRID_DIRECTION_NAME: dict[str, str] = {
    GridDirection.NORTH: 'North',
    GridDirection.SOUTH: 'South',
    GridDirection.EAST: 'East',
    GridDirection.WEST: 'West',
}

# Table of opposite directions.
GRID_DIRECTION_OPPOSITE: dict[str, str] = {
    GridDirection.NORTH: GridDirection.SOUTH,
    GridDirection.SOUTH: GridDirection.NORTH,
    GridDirection.EAST: GridDirection.WEST,
    GridDirection.WEST: GridDirection.EAST,
}


class GridDungeon(Dungeon):
    ''' Grid dungeon mixin. '''

    def __init__(
        self,
        character_set: DungeonDrawingCharacterSet,
        dungeon_width: int,
        dungeon_height: int,
        player_room: int,
    ):
        super().__init__(
            number_of_rooms = dungeon_width * dungeon_height,
            player_room = player_room
        )
        self.character_set: DungeonDrawingCharacterSet = character_set
        self.dungeon_width: int = dungeon_width
        self.dungeon_height: int = dungeon_height

        self.max_x: int = self.dungeon_width - 1
        self.max_y: int = self.dungeon_height - 1

        self.dungeon_elements: GridDungeonsElements = GridDungeonsElements(
            empty_room = 3 * ' ',
            hidden_room = 3 * ' ',
            vertical_door = ' ',
            vertical_wall = self.character_set.up_and_down,
            hidden_vertical_door_or_wall = ' ',
            horizontal_door = 3 * ' ',
            horizontal_wall = 3 * self.character_set.left_and_right,
            hidden_horizontal_door_or_wall = 3 * ' ',
            hidden_vertical_corner = self.character_set.up_and_down,
            hidden_horizontal_corner = self.character_set.left_and_right,
            all_hidden_corners = ' ',
            southeast_corner = self.character_set.up_and_left,
            northeast_corner = self.character_set.down_and_left,
            northeast_and_southeast_corners = self.character_set.up_down_and_left,
            southwest_corner = self.character_set.up_and_right,
            southeast_and_southwest_corners = self.character_set.up_left_and_right,
            northeast_and_southwest_corners = self.character_set.up_down_left_and_right,
            northeast_southeast_and_southwest_corners = self.character_set.up_down_left_and_right,
            northwest_corner = self.character_set.down_and_right,
            northwest_and_southeast_corners = self.character_set.up_down_left_and_right,
            northeast_and_northwest_corners = self.character_set.down_left_and_right,
            northeast_northwest_and_southeast_corners = self.character_set.up_down_left_and_right,
            northwest_and_southwest_corners = self.character_set.up_down_and_right,
            northwest_southeast_and_southwest_corners = self.character_set.up_down_left_and_right,
            northeast_northwest_and_southwest_corners = self.character_set.up_down_left_and_right,
            all_corners = self.character_set.up_down_left_and_right,
        )

        # Table of sungeon room internal Southeast corner characters.
        # The index to this table is composed as follows:
        # Bit 0 = The current room is visible.
        # Bit 1 = The room to the South is visible.
        # Bit 2 = The room to the East is visible.
        # Bit 3 = The room to the Southeast is visible.
        self.south_east_corners: list[str] = [
            self.dungeon_elements.all_hidden_corners,
            self.dungeon_elements.southeast_corner,
            self.dungeon_elements.northeast_corner,
            self.dungeon_elements.northeast_and_southeast_corners,
            self.dungeon_elements.southwest_corner,
            self.dungeon_elements.southeast_and_southwest_corners,
            self.dungeon_elements.northeast_and_southwest_corners,
            self.dungeon_elements.northeast_southeast_and_southwest_corners,
            self.dungeon_elements.northwest_corner,
            self.dungeon_elements.northwest_and_southeast_corners,
            self.dungeon_elements.northeast_and_northwest_corners,
            self.dungeon_elements.northeast_northwest_and_southeast_corners,
            self.dungeon_elements.northwest_and_southwest_corners,
            self.dungeon_elements.northwest_southeast_and_southwest_corners,
            self.dungeon_elements.northeast_northwest_and_southwest_corners,
            self.dungeon_elements.all_corners,
        ]

        self.room_contents_function: RoomContentFunction = self.room_contents
        self.rooms: list[int] = []
        self._create_dungeon()


    def description(self) -> None:
        ''' Describe the scenario. '''
        print('- You are in a dungeon.')


    def display(self) -> None:
        ''' Display the game. '''
        self._print_dungeon(self._rooms_visible_from_room(self.player_room))


    def commands(self) -> list[Command]:
        ''' Return a list of additional commands. '''
        commands: list[Command] = []
        directions: list[GridDirection] = self._directions_with_doors(self.player_room)
        if GridDirection.NORTH in directions:
            commands.append(self._create__command(GridDirection.NORTH, self._move_north_command))
        if GridDirection.SOUTH in directions:
            commands.append(self._create__command(GridDirection.SOUTH, self._move_south_command))
        if GridDirection.EAST in directions:
            commands.append(self._create__command(GridDirection.EAST, self._move_east_command))
        if GridDirection.WEST in directions:
            commands.append(self._create__command(GridDirection.WEST, self._move_west_command))
        return commands


    def game_over(self) -> None:
        '''
        The game is over.
        This function is called once at the end of the game.
        '''
        self._print_dungeon(range(self.number_of_rooms))


    def directions_with_doors(self, room: int) -> list[Direction]:
        ''' Returns a list of directions that contain doors in the given room. '''
        return [
            Direction(id = grid_direction, name = GRID_DIRECTION_NAME[grid_direction])
            for grid_direction in self._directions_with_doors(room)
        ]


    def navigation_info(self, direction: Direction, room: int) -> Optional[NavigationInfo]:
        ''' Returns navigation information from the given room. '''
        if not self._is_room_on_edge(direction.id, room):
            return NavigationInfo(
                direction = direction,
                name = GRID_DIRECTION_NAME[direction.id],
                room = self._room_in_direction(direction.id, room)
            )
        return None


    def navigate_towards_destination(
        self, start_room: int, destination_room: int
    ) -> Optional[NavigationInfo]:
        '''
        Given a start and destination room,
        if the destination room is visible from the start room,
        returns information on how to move from the start room towards the destination room.
        '''
        for door_direction in self._directions_with_doors(start_room):
            if destination_room in self._rooms_visible_in_direction(door_direction, start_room):
                return self.navigation_info(
                    Direction(id = door_direction, name = GRID_DIRECTION_NAME[door_direction]),
                    start_room
                )
        return None


    def room_in_direction(self, direction: Direction, room: int) -> Optional[int]:
        ''' Returns the adjacent room in the given direction from the given room. '''
        if not self._is_room_on_edge(direction.id, room):
            return self._room_in_direction(direction.id, room)
        return None


    def rooms_visible_from_room(self, room: int) -> list[int]:
        ''' Returns a list of all the rooms that are visible from the given room. '''
        return self._rooms_visible_from_room(room)


    def rooms_visible_in_direction(self, direction: Direction, room: int) -> list[int]:
        '''
        Returns a list of the rooms that are visible from the given room in the given direction.
        '''
        return self._rooms_visible_in_direction(direction.id, room)


    def set_room_contents_function(self, function: RoomContentFunction) -> None:
        ''' Sets the function to call to print a rooms contents. '''
        self.room_contents_function = function


    room_contents: RoomContentFunction
    def room_contents(self, room: int) -> Optional[str]:
        ''' Returns the given room's contents, as a single character string. '''
        return 'P' if room == self.player_room else None


    def _directions_with_doors(self, room: int) -> list[GridDirection]:
        ''' Returns a list of directions that contain doors in the given room. '''
        door_directions: list[GridDirection] = []
        for grid_direction in [
            GridDirection.NORTH, GridDirection.SOUTH, GridDirection.EAST, GridDirection.WEST,
        ]:
            if self.rooms[room]['doors'][grid_direction]:
                door_directions.append(grid_direction)
        return door_directions


    def _room_in_direction(self, grid_direction: GridDirection, room: int) -> int:
        '''
        Returns the adjacent room in the given direction from the given room.
        Note: No check is made if the returned room is valid. e.g. outside the dungeon edge.
        '''
        if grid_direction == GridDirection.NORTH:
            next_room = room - self.dungeon_width
        elif grid_direction == GridDirection.SOUTH:
            next_room = room + self.dungeon_width
        elif grid_direction == GridDirection.EAST:
            next_room = room + 1
        else:  # grid_direction == DIRECTION.WEST:
            next_room = room - 1
        return next_room


    def _rooms_visible_in_direction(self, grid_direction: GridDirection, room: int) -> list[int]:
        '''
        Returns a list of the rooms that are visible from the given room in the given direction.
        '''
        visible_rooms: list[int] = []
        while self.rooms[room]['doors'][grid_direction]:
            room = self._room_in_direction(grid_direction, room)
            visible_rooms.append(room)
        return visible_rooms


    def _rooms_visible_from_room(self, room: int) -> list[int]:
        ''' Returns a list of all the rooms that are visible from the given room. '''
        visible_rooms: list[int] = [room]
        for door_direction in self._directions_with_doors(room):
            visible_rooms.extend(self._rooms_visible_in_direction(door_direction, room))
        return visible_rooms


    def _create__command(self, grid_direction: GridDirection, function: CommandFunction) -> Command:
        ''' Create a Command. '''
        return Command(
            invocation_text = COMMAND_INVOCATION_TEXT[grid_direction],
            menu_text = COMMAND_MENU_TEXT[grid_direction],
            function = function,
        )


    def _move(self, grid_direction: GridDirection):
        ''' The player moves. '''
        print(f'You move {GRID_DIRECTION_NAME[grid_direction]}.')
        self.player_room = self._room_in_direction(grid_direction, self.player_room)
        return True


    _move_north_command: CommandFunction
    def _move_north_command(self) -> bool:
        ''' The player moves North. '''
        return self._move(GridDirection.NORTH)


    _move_south_command: CommandFunction
    def _move_south_command(self) -> bool:
        ''' The player moves South. '''
        return self._move(GridDirection.SOUTH)


    _move_east_command: CommandFunction
    def _move_east_command(self) -> bool:
        ''' The player moves East. '''
        return self._move(GridDirection.EAST)


    _move_west_command: CommandFunction
    def _move_west_command(self) -> bool:
        ''' The player moves West. '''
        return self._move(GridDirection.WEST)


    def _room_at_x_y(self, x: int, y: int) -> int:
        ''' Returns the room at the x, y coordinates. '''
        return x + y * self.dungeon_width


    def _room_x(self, room: int) -> int:
        ''' Returns the x-coordinate of the given room. '''
        return room % self.dungeon_width


    def _room_y(self, room: int) -> int:
        ''' Returns the y-coordinate of the given room.'''
        return room // self.dungeon_width


    def _is_room_on_edge(self, grid_direction: GridDirection, room: int) -> bool:
        ''' Returns True if the given room is on the given edge of the dungeon. '''
        return (
            (grid_direction == GridDirection.NORTH and self._room_y(room) == 0) or
            (grid_direction == GridDirection.SOUTH and self._room_y(room) == self.max_y) or
            (grid_direction == GridDirection.EAST and self._room_x(room) == self.max_x) or
            (grid_direction == GridDirection.WEST and self._room_x(room) == 0)
        )


    def _create_door_in_direction(self, grid_direction: GridDirection, room: int) -> None:
        '''
        Create a door in the given direction of the given room.
        This will not create a door through the edge of the dungeon.
        '''
        if not self._is_room_on_edge(grid_direction, room):
            self.rooms[room]['doors'][grid_direction] = True
            next_room: int = self._room_in_direction(grid_direction, room)
            self.rooms[next_room]['doors'][GRID_DIRECTION_OPPOSITE[grid_direction]] = True


    def _is_room_in_direction_mapped(self, grid_direction: GridDirection, room: int) -> bool:
        '''
        Returns True if the adjacent room in the given direction from the given room is mapped.
        Returns True if the given room is on the given edge of the dungeon.
        '''
        return (
            self._is_room_on_edge(grid_direction, room) or
            self.rooms[self._room_in_direction(grid_direction, room)]['mapped']
        )


    def _unmapped_directions(self, room: int) -> list[GridDirection]:
        ''' Returns a list of directions to unmapped rooms from the given room. '''
        unmapped_directions: list[GridDirection] = []
        for grid_direction in [
            GridDirection.NORTH, GridDirection.SOUTH, GridDirection.EAST, GridDirection.WEST
        ]:
            if not self._is_room_in_direction_mapped(grid_direction, room):
                unmapped_directions.append(grid_direction)
        return unmapped_directions


    def _carve_dungeon(self, room: int) -> None:
        ''' Carve out the internal passages of the dungeon. '''
        self.rooms[room]['mapped'] = True
        unmapped_directions: list[GridDirection] = self._unmapped_directions(room)
        while unmapped_directions:
            unmapped_direction: GridDirection = choice(unmapped_directions)
            self._create_door_in_direction(unmapped_direction, room)
            self._carve_dungeon(self._room_in_direction(unmapped_direction, room))
            unmapped_directions = self._unmapped_directions(room)


    def _default_room(self) -> dict[dict[GridDirection, bool], bool]:
        ''' Returns a default room for dungeon creation. '''
        # Upon creation, rooms have no doors and are unmapped.
        return {
            'doors': {
                GridDirection.NORTH: False,
                GridDirection.SOUTH: False,
                GridDirection.EAST: False,
                GridDirection.WEST: False,
            },
            'mapped': False,
        }


    def _create_dungeon(self) -> None:
        ''' Create the maze. '''
        # Initially, all rooms in the dungeon will have no doors.
        # _carve_dungeon() will create the doors.
        for _ in range(self.number_of_rooms):
            self.rooms.append(self._default_room())
        self._carve_dungeon(self.number_of_rooms // 2)  # Start in the center of the dungeon.


    def _print_dungeon_north_edge(self, visible_rooms: list[int]) -> None:
        '''
        Print the North edge of the dungeon.
        Hide the corner details of rooms that are not visible.
        '''
        # Print the North-West corner.
        print(self.dungeon_elements.northwest_corner, end='')

        # For all but the most Easterly room ...
        for x in range(self.max_x):

            # Print the North wall.
            print(self.dungeon_elements.horizontal_wall, end='')

            # Print the North-East corner.
            is_room_visible: bool = self._room_at_x_y(x, 0) in visible_rooms
            is_room_to_the_east_visible: bool = self._room_at_x_y(x + 1, 0) in visible_rooms
            if is_room_visible or is_room_to_the_east_visible:
                print(self.dungeon_elements.northeast_and_northwest_corners, end='')
            else:
                print(self.dungeon_elements.hidden_horizontal_corner, end='')

        # For the most Easterly room, print the North wall and the North-East corner.
        print(self.dungeon_elements.horizontal_wall, end='')
        print(self.dungeon_elements.northeast_corner)


    def _print_room_contents(self, room: int, is_room_visible: bool) -> None:
        '''
        Print the contents of the given room.
        Hide the contents of rooms that are not visible.
        '''
        if is_room_visible:
            contents = self.room_contents_function(room)
            print(f' {contents if contents else " "} ', end = '')
        else:
            print(self.dungeon_elements.hidden_room, end='')


    def _print_row_contents_and_vertical_walls(self, y: int, visible_rooms: list[int]) -> None:
        '''
        Print the contents and vertical walls of the rooms in a single row of the dungeon.
        Hide the room content and wall details of rooms that are not visible.
        '''
        # Print the West edge.
        print(self.dungeon_elements.vertical_wall, end='')

        # For all but the most Easterly room ...
        for x in range(self.max_x):

            # Print the room contents.
            room: int = self._room_at_x_y(x, y)
            is_room_visible: bool = room in visible_rooms
            self._print_room_contents(room, is_room_visible)

            # Print the East wall.
            is_room_to_the_east_visible: bool = self._room_at_x_y(x + 1, y) in visible_rooms
            if is_room_visible or is_room_to_the_east_visible:
                if self.rooms[room]['doors'][GridDirection.EAST]:
                    print(self.dungeon_elements.vertical_door, end='')
                else:
                    print(self.dungeon_elements.vertical_wall, end='')
            else:
                print(self.dungeon_elements.hidden_vertical_door_or_wall, end='')

        # For the most Easterly room, print the room contents and the East edge.
        room = self._room_at_x_y(self.max_x, y)
        is_room_visible = room in visible_rooms
        self._print_room_contents(room, is_room_visible)
        print(self.dungeon_elements.vertical_wall)


    def _print_room_south_wall(
        self, room, is_room_visible: bool, is_room_to_the_south_visible: bool
    ) -> None:
        '''
        Print the South wall of the given room.
        Hide the wall details of rooms that are not visible.
        '''
        if is_room_visible or is_room_to_the_south_visible:
            if self.rooms[room]['doors'][GridDirection.SOUTH]:
                print(self.dungeon_elements.horizontal_door, end='')
            else:
                print(self.dungeon_elements.horizontal_wall, end='')
        else:
            print(self.dungeon_elements.hidden_horizontal_door_or_wall, end='')


    def _print_row_horizontal_walls_and_corners(self, y: int, visible_rooms: list[int]) -> None:
        '''
        Print the horizontal walls and Southern corners of the rooms in a single row of the dungeon.
        Hide the wall and corner details of rooms that are not visible.
        '''
        # Print the South-West edge corner.
        is_room_visible: bool = self._room_at_x_y(0, y) in visible_rooms
        is_room_to_the_south_visible: bool = self._room_at_x_y(0, y + 1) in visible_rooms
        if is_room_visible or is_room_to_the_south_visible:
            print(self.dungeon_elements.northwest_and_southwest_corners, end='')
        else:
            print(self.dungeon_elements.hidden_vertical_corner, end='')

        # For all but the most Easterly room ...
        for x in range(self.max_x):

            # Determine the visibility of the room and its South and East neighbors.
            room: int = self._room_at_x_y(x, y)
            is_room_visible = room in visible_rooms
            is_room_to_the_south_visible = self._room_at_x_y(x, y + 1) in visible_rooms
            is_room_to_the_east_visible: bool = self._room_at_x_y(x + 1, y) in visible_rooms
            is_room_to_the_south_east_visible: bool = (
                self._room_at_x_y(x + 1, y + 1) in visible_rooms
            )

            # Print the South door or wall.
            self._print_room_south_wall(room, is_room_visible, is_room_to_the_south_visible)

            # Print the South-East corner.
            corner_index: int = (
                (1 if is_room_visible else 0) +
                (2 if is_room_to_the_south_visible else 0) +
                (4 if is_room_to_the_east_visible else 0) +
                (8 if is_room_to_the_south_east_visible else 0)
            )
            print(self.south_east_corners[corner_index], end='')

        # For the most Easterly room, print the South wall and the South-East corner.
        room = self._room_at_x_y(self.max_x, y)
        is_room_visible = room in visible_rooms
        is_room_to_the_south_visible = self._room_at_x_y(self.max_x, y + 1) in visible_rooms
        self._print_room_south_wall(room, is_room_visible, is_room_to_the_south_visible)
        if is_room_visible or is_room_to_the_south_visible:
            print(self.dungeon_elements.northeast_and_southeast_corners)
        else:
            print(self.dungeon_elements.hidden_vertical_corner)


    def _print_dungeon_south_edge(self, visible_rooms: list[int]) -> None:
        '''
        Print the South edge of the dungeon.
        Hide the corner details of rooms that are not visible.
        '''
        # Print the South-West corner.
        print(self.dungeon_elements.southwest_corner, end='')

        # For all but the most Easterly room ...
        for x in range(self.max_x):

            # Print the South wall.
            print(self.dungeon_elements.horizontal_wall, end='')

            # Print the South-East corner.
            is_room_visible: bool = self._room_at_x_y(x, self.max_y) in visible_rooms
            is_room_to_the_east_visible: bool = (
                self._room_at_x_y(x + 1, self.max_y) in visible_rooms
            )
            if is_room_visible or is_room_to_the_east_visible:
                print(self.dungeon_elements.southeast_and_southwest_corners, end='')
            else:
                print(self.dungeon_elements.hidden_horizontal_corner, end='')

        # For the most Easterly room, print the South wall and the South-East corner.
        print(self.dungeon_elements.horizontal_wall, end='')
        print(self.dungeon_elements.southeast_corner)


    def _print_dungeon(self, visible_rooms: list[int]) -> None:
        '''
        Print the dungeon.
        Hide the room details of rooms that are not visible.
        '''
        self._print_dungeon_north_edge(visible_rooms)
        for y in range(self.max_y):
            self._print_row_contents_and_vertical_walls(y, visible_rooms)
            self._print_row_horizontal_walls_and_corners(y, visible_rooms)
        self._print_row_contents_and_vertical_walls(self.max_y, visible_rooms)
        self._print_dungeon_south_edge(visible_rooms)
