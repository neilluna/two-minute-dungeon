''' Game settings. '''

from base_classes.scenario import Scenario
from scenarios.bow_and_blink import BowAndBlink


scenario_list: list[Scenario] = [
    BowAndBlink,
]
