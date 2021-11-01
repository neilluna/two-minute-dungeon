''' Two minute dungeon. '''

from random import choice

from base_classes.scenario import Command, Scenario

from settings import scenario_list


def main() -> None:
    ''' Main game program. '''
    print('Welcome to two-minute dungeon.')

    scenario: Scenario = choice(scenario_list)()
    scenario.description()

    while True:
        scenario.display()
        commands: list[Command] = scenario.commands()
        if not commands:
            break
        command_menu: str = ', '.join([command.menu_text for command in commands])
        print(f'Commands: {command_menu}')
        user_choice: str = input('Command? ').lower()
        if user_choice not in [command.invocation_text.lower() for command in commands]:
            print('Invalid command.')
            continue
        command: Command = [
            command
            for command in commands
            if command.invocation_text.lower() == user_choice
        ][0]
        if not command.function() or not scenario.post_player_turn():
            break

    scenario.game_over()
    print('Thank you for playing.')


if __name__== "__main__":
    main()
