''' Dungeon drawing character sets. '''

from dataclasses import dataclass


@dataclass
class DungeonDrawingCharacterSet:
    ''' Character set used to draw the dungeon. '''
    up_and_down: str
    up_down_and_left: str
    up_down_left_and_right: str
    up_down_and_right: str
    up_and_left: str
    up_left_and_right: str
    up_and_right: str
    left_and_right: str
    down_and_left: str
    down_left_and_right: str
    down_and_right: str


ASCII_DUNGEON_DRAWING_CHARACTER_SET: DungeonDrawingCharacterSet = DungeonDrawingCharacterSet(
    up_and_down = '|',
    up_down_and_left = '+',
    up_down_left_and_right = '+',
    up_down_and_right = '+',
    up_and_left = '+',
    up_left_and_right = '+',
    up_and_right = '+',
    left_and_right = '-',
    down_and_left = '+',
    down_left_and_right = '+',
    down_and_right = '+',
)

UNICODE_DUNGEON_DRAWING_CHARACTER_SET: DungeonDrawingCharacterSet = DungeonDrawingCharacterSet(
    up_and_down = '\u2502',
    up_down_and_left = '\u2524',
    up_down_left_and_right = '\u253c',
    up_down_and_right = '\u251c',
    up_and_left = '\u2518',
    up_left_and_right = '\u2534',
    up_and_right = '\u2514',
    left_and_right = '\u2500',
    down_and_left = '\u2510',
    down_left_and_right = '\u252c',
    down_and_right = '\u250c',
)
